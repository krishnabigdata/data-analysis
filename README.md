## Yellow Taxi Data Processing and Analysis

Analyzing Yellow Taxi Data. This project can be executed using Docker as Container for loading data to ``DB`` as a scheduler Job using ``Chronos`` in `Mesos` Platform or ``Kubernetes Scheduler``

Data Downloading and Loading Process are tracked and managed using table ``tbl_status`` 


Requirements
------------

Python 3.7+ and PostgresSql



Project Structure
-----------------

    .. code-block::
    .
    |-- Dockerfile
    |-- MANIFEST.in
    |-- Makefile
    |-- README.md
    |-- dataset
    |   |-- 
    |-- docker-compose.yml
    |-- requirements.txt
    |-- setup.cfg
    |-- setup.py
    |-- sql
    |   `-- V1.0_CREATE_TABLE.sql
    |-- src
    |   `-- processing
    |       |-- __init__.py
    |       |-- cli.py
    |       |-- constant.py
    |       |-- transform.py
    |       `-- util.py
    |-- tests
    |   |-- __init__.py
    |   `-- test_analysis.py
    `-- yellow_taxi_analysis.ipynb


Output
--------

``yellow_taxi_analysis.ipynb`` : Has all the analysis outputs.

Installing
---------

Steps:

- ``git clone https://github.com/krishnabigdata/taxi-data-analysis.git``

- ``pip install -r taxi-data-analysis/requirements.txt``

- ``pip install --upgrade taxi-data-analysis``

- ``docker-compose up -d``


Docker
------

Building Docker and using docker

- ``make build -e VERSION=latest``
- ``make push -e VERSION=latest``
- ``docker run -t -i --network host docker.io/krishnabigdata/taxi_data_analysis -v ${PWD}:/taxi_data_analysis/dataset --action download --year 2019 --month 1 --color yellow``

Usage
---------

Commands to use the `processing` cli

    .. code-block:: bash 

    usage: processing [-h] [--year YEAR] [--month {1,2,3,4,5,6}]
                  [--color {yellow}] --action
                  {all,download,load,avg_trip,avg_trip_local,rolling_avg_trip}
                  [--verbose VERBOSE]

    Taxi Data Analysis
    
    optional arguments:
      -h, --help            show this help message and exit
      --year YEAR           year of data to load (default: 2019)
      --month {1,2,3,4,5,6}
                            month of data to load (default: 1)
      --color {yellow}      color of data to load (default: yellow)
      --action {all,download,load,avg_trip,avg_trip_local,rolling_avg_trip}
                            action to be performed (default: all)
      --verbose VERBOSE     logging action to be performed (default: True)
      

- `all`: Performs all steps 
    - ``Downloading``, ``LoadingToDB``, ``Queries DB for AVG and Rolling AVG``
- ``avg_trip_local``
    - Calculates Trip Distance Average by Month by Querying the Locally downloaded file.
- ``avg_trip``
    - Calculates Trip Distance Average by Month by Querying the DB.
- ``rolling_avg_trip``
    - Calculates 45 Day Rolling Trip Distance Average by Querying the DB.


Scaling Up
---------

We can use the below options for distributed processing in order to process huge volume of data which cannot be processed by
single instance.

- ``pyspark`` - For distributed processing
- ``DB``: Parallel loading of files to DB and analysis using SQL queries.
- ``Streaming``: Data produced as events to ``Kafka`` and Processing using `Kafa-Connect connectors` or ``Spark Structured Streaming`` or ``Consume from Kafka`` and load to ``DB`` ``->`` SQL Query