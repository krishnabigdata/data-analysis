#!/usr/bin/env python3

import argparse
import sys

import colorama
from processing.transform import *
from exitstatus import ExitStatus


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Taxi Data Analysis',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--year',
                        type=int,
                        default=2019,
                        required=True,
                        dest='year',
                        help='year of data to load')

    parser.add_argument('--month',
                        type=int,
                        default=1,
                        choices=[1,2,3,4,5,6],
                        required=True,
                        dest='month',
                        help='month of data to load')

    parser.add_argument('--color',
                        type=str,
                        default='yellow',
                        choices=['yellow'],
                        required=True,
                        dest='color',
                        help='color of data to load')

    parser.add_argument('--action',
                        type=str,
                        choices=['all','download','load','avg_trip','avg_trip_local','rolling_avg_trip'],
                        default='all',
                        required=True,
                        dest='action',
                        help='action to be performed')

    parser.add_argument('--verbose',
                        type=bool,
                        default=True,
                        required=False,
                        dest='verbose',
                        help='logging action to be performed')

    return parser.parse_args()


def main() -> ExitStatus:
    """Main function, calls the method based on input

    :return:
    """
    colorama.init(autoreset=True, strip=False)
    args = parse_args()
    transform = Transform(color=args.color, year=args.year,month=args.month,verbose=args.verbose)
    if args.action == 'load':
        transform.load_data()
    elif args.action == 'download':
        transform.download_data()
    elif args.action == 'avg_trip':
        transform.avg_trip_distance()
    elif args.action == 'avg_trip_local':
        print(transform.calc_avg_trip_distance_local())
    elif args.action == 'rolling_avg_trip':
        transform.rolling_avg_trip_distance()
    elif args.action == 'all':
        transform.download_data()
        transform.load_data()
        transform.avg_trip_distance()
        transform.rolling_avg_trip_distance()

    return ExitStatus.success


if __name__ == '__main__':
    sys.exit(main())
