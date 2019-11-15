from processing.transform import *
import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal


class AnalysisTests(unittest.TestCase):

    def setUp(self):
        try:
            Data = {'trip_distance': [0.2, 2, 3.5],
                    'tpep_pickup_datetime': ['2019-06-01 00:55:13', '2019-06-01 00:55:13', '2019-06-01 00:55:13']
                    }

            df = pd.DataFrame(Data, columns=['tpep_pickup_datetime', 'trip_distance'])
            self.testdata = df
        except Exception as e:
            print('cannot create dataframe: {}'.format(e))

    def test_avg_trip_distance(self):
        Data = {'avg_trip_distance': [1.9],
                'pickup_month': [6]
                }

        df = pd.DataFrame(Data, columns=['pickup_month', 'avg_trip_distance'])
        df = df[['pickup_month', 'avg_trip_distance']]

        attributes = {
            'month': '1',
            'year': '2019',
            'taxi_color': 'yellow',
            'verbose': True
        }
        transform = Transform(**attributes)
        assert_frame_equal(transform.avg_trip_distance_local(self.testdata), df)
