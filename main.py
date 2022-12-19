#!/bin/python3

from pathlib import Path
from model.target import Target
from view import display_results, exit_error
from model import config
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Recursive extract all endpoints from Django 404-page debug information')
    parser.add_argument("url", type=str, help="url of the 404 page with debug information")
    parser.add_argument("-o", "--out", type=Path, metavar="PATH", help="path to the output file", default=None)
    parser.add_argument("-d", "--delay", type=float, help="delay per request", default=0.3)
    args = parser.parse_args()

    config.running = config.RunningConfig(args)

    config.running.validate_args()

    target = Target()
    if not target.is_valid():
        exit_error("Target invalid: check if target's debug mode is turned on")

    target.parse_endpoints()
    display_results(target.endpoint_counters, target.start_time)


if __name__ == "__main__":
    main()
