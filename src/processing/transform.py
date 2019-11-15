import pandas as pd
import urllib.request
from sqlalchemy import create_engine
import os
from os.path import abspath, exists
from processing import constant
from processing.util import data_logger
import logging


class Transform(object):

    def _find_project_path(self):
        """Finds the current project directory

        :return:
        """
        current_path = os.getcwd().split(os.sep)
        for i in range(len(current_path), 0, -1):
            path = os.sep.join(current_path[0:i])
            if os.path.exists(os.path.join(path, 'setup.cfg')):
                return path

        raise RuntimeError(
            "Could not find the project directory, please re-run this command in that directory."
            "CWD: " + os.getcwd()
        )

    def __init__(self, **kwargs):
        """Initialize the current class

        :param kwargs:
        """
        self.__dict__.update(kwargs)

        if self.verbose :
            data_logger.setLevel(logging.INFO)

        self.path=self._find_project_path()

        self.engine = create_engine(
            'postgresql://' + os.environ.get('POSTGRESQL_USER','test') + ':' + os.environ.get('POSTGRESQL_PASSWORD','test') + '@' +
            os.environ.get('POSTGRESQL_HOST','localhost') + ':' + os.environ.get('POSTGRESQL_PORT','5432') + '/' + os.environ.get(
                'POSTGRESQL_DATABASE','test'), echo=False,isolation_level="AUTOCOMMIT")

    def download_data(self):
        """Downloads data from s3 based on Year,Month and color

        :return:
        """
        filename = "{0}_tripdata_{1}-{2:0=2d}.csv".format(self.color, self.year, self.month)
        try:
            if not self.db_exists(filename, 'DOWNLOADED'):
                data_logger.info('File downloading for %s, is %s' % (filename, 'STARTED'))
                urllib.request.urlretrieve("https://s3.amazonaws.com/nyc-tlc/trip+data/" + filename,
                                           os.path.join(self.path, "dataset/{}".format(filename)))
                self.db_exec(self._get_sql_status(filename, 'DOWNLOADED'))
                data_logger.info('File downloading for %s, is %s' % (filename, 'COMPLETED'))
            else:
                data_logger.info('File downloading for %s, is %s' % (filename, 'SKIPPED'))
        except Exception as e:
            data_logger.exception("Error while downloading file '%s': %s" % (filename, e))
            return None

    def db_exec(self, sql):
        """Executes SQL commands

        :param sql: statement to execute in the DB
        :return:
        """
        self.engine.execute(sql)

    def db_exists(self, filename, status):
        """Checks the status of the file based on it, decides the next step

        :param filename: filename for which the status to be checked
        :param status: to check for which status
        :return:
        """
        sql = f"select * from {constant.TBL_STATUS} where filename='{filename}' and status='{status}';"
        data_logger.info("Executing sql '%s'" % (sql))
        result = self.engine.execute(sql)
        res = result.fetchone()
        data_logger.info("Result for status for file '%s': %s" % (filename, res))
        return res is not None

    def _get_sql_status(self, filename, status):
        """Frames sql statement to load the status of pipeline to status tbl

        :param filename:
        :param status:
        :return:
        """
        sql = f"INSERT INTO {constant.TBL_STATUS} (id, filename, updated_datetime, status) " \
            f"VALUES(nextval('reporting.tbl_status_id_seq'::regclass),'{filename}' , current_timestamp,'{status}');"
        return sql

    def _createTable(self):
        """Creates schema and all necessary tbl in PostgreSQL

        :return:
        """
        f_path =  os.path.join (self.path,"sql","V1.0_CREATE_TABLE.sql")
        if exists(f_path):
            with open(f_path) as f:
                self.engine.execute(f.read())

    def load_data(self):
        """Loads the CSV file to the DB table.

        :return:
        """
        self._createTable()
        i, chunksize = 1, 10000
        filename = "{0}_tripdata_{1}-{2:0=2d}.csv".format(self.color, self.year, self.month)
        try:
            if self.db_exists(filename, 'DOWNLOADED'):
                fp = os.path.join(self.path, "dataset/{}".format(filename))
                self.db_exec(self._get_sql_status(filename, 'IN_PROGRESS'))
                if exists(fp):
                    filename = os.path.basename(fp)
                    data_logger.info('Loading file: %s to table, is %s' % (filename, 'STARTED'))
                    for ds in pd.read_csv(fp, chunksize=chunksize, iterator=True):
                        ds = ds.rename(columns={'VendorID': 'vendor_id', 'RatecodeID': 'ratecode_id'
                            , 'PULocationID': 'pu_location_id', 'DOLocationID': 'do_location_id'})
                        ds['pickup_year'] = pd.DatetimeIndex(ds['tpep_pickup_datetime']).year
                        ds['pickup_month'] = pd.DatetimeIndex(ds['tpep_pickup_datetime']).month
                        ds['pickup_day'] = pd.DatetimeIndex(ds['tpep_pickup_datetime']).day
                        ds['pickup_hour'] = pd.DatetimeIndex(ds['tpep_pickup_datetime']).hour
                        ds['dropoff_hour'] = pd.DatetimeIndex(ds['tpep_dropoff_datetime']).hour
                        ds['taxi_color'] = self.color
                        ds['filename'] = filename
                        ds.index += i
                        ds.to_sql(constant.TBL_TAXI, self.engine, if_exists='append', schema="reporting")
                        i = ds.index[-1] + 1
                    self.db_exec(self._get_sql_status(filename, 'COMPLETED'))
                    data_logger.info('Loading file: %s to table, is %s' % (filename, 'COMPLETED'))
                    del ds
            else:
                data_logger.info('Loading file: %s to table, is %s' % (filename, 'SKIPPED'))
        except Exception as e:
            data_logger.exception("Error while loading file '%s' to table: %s" % (filename, e))
            return None

    def calc_avg_trip_distance_local(self):
        filename = "{0}_tripdata_{1}-{2:0=2d}.csv".format(self.color, self.year, self.month)
        fp = os.path.join(self.path, "dataset/{}".format(filename))
        if exists(fp):
           filename = os.path.basename(fp)
           data_logger.info('Processing file: %s ' % (filename))
           df = pd.read_csv(fp)
           return self.avg_trip_distance_local(df)

    def avg_trip_distance_local(self,df):
        df['pickup_month'] = pd.DatetimeIndex(df['tpep_pickup_datetime']).month
        df = df[['pickup_month', 'trip_distance']]
        result = df.groupby(['pickup_month'],as_index=False).mean().rename(columns={'trip_distance': 'avg_trip_distance'})
        return result

    def avg_trip_distance(self):
        """Calculates avg trip distance for every month

        :return:
        """
        df = pd.read_sql_query("select pickup_month,avg( trip_distance ) as avg_trip_distance,"
                               "count(*) as total_records from " + constant.TBL_TAXI + ""
                                                                                       "group by pickup_month",
                               con=self.engine)
        print(df)

    def rolling_avg_trip_distance(self):
        """Rolling avg trip distance for every 45 days

        :return:
        """
        df = pd.read_sql_query("with cte_tbl as ( select AVG(trip_distance) as trip_distance ,tpep_pickup_datetime::DATE "
                               "as pickup_date  from reporting.tbl_taxi group by tpep_pickup_datetime::DATE) "
                               "SELECT pickup_date,AVG(trip_distance) OVER (ORDER BY pickup_date  rows"
                               " BETWEEN 45 PRECEDING AND current row) AS rolling_average FROM cte_tbl ORDER BY pickup_date;",
                               con=self.engine)
        print(df)