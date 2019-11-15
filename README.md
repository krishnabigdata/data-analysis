## Yellow Taxi Data Processing and Analysis

Analyzing Yellow Taxi Data. This project can executed using Docker Container for loading data to ``DB`` as a scheduler Job using ``Chronos`` in `Mesos` Platform or ``Kubernetes Scheduler``

Requirements
------------

Python 3.7+.



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


Usage
---------

Commands to use the `processing` cli

    .. code-block:: bash 

    usage: processing [-h] --year YEAR --month {1,2,3,4,5,6} --color {yellow}
                  --action
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
      

- `all`: Performs all steps ``Downloading``, ``LoadingToDB``

Scaling Up
---------

We can use the below options for distributed processing in order to process huge volume of data.

- ``pyspark`` - For distributed processing
- ``DB``: Parallel loading of files to DB and analysis using SQL queries.