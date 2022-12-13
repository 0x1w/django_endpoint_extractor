#!/bin/python3

from pathlib import Path

import requests
from requests.exceptions import MissingSchema, ConnectionError, InvalidSchema, InvalidURL

from model.target import Target
from view import display_error, display_results

import argparse


def exit_error(msg):
    display_error(msg)
    exit(-1)


def check_url(url):
    resp = None
    try:
        resp = requests.get(url)
    except MissingSchema:
        exit_error("No schema supplied!")
    except InvalidSchema:
        exit_error(f"Invalid schema supplied '{url.split('://')[0]}' ")
    except InvalidURL:
        exit_error(f"Invalid URL: {url}")
    except ConnectionError:
        exit_error("Can't connect to the target!")

    if resp.status_code != 404:
        exit_error(f"{url} - It's not a 404 page URL")


def main():
    parser = argparse.ArgumentParser(
        description='Recursive extract all endpoints from Django 404-page debug information')
    parser.add_argument("url", type=str, help="url of the 404 page with debug information")
    parser.add_argument("-o", "--out", type=Path, metavar="PATH", help="path to the output file", default=None)
    parser.add_argument("-d", "--delay", type=float, help="delay per request", default=0.3)
    args = parser.parse_args()

    url = args.url
    outfile = args.out

    check_url(url)
    if outfile:  # clear if passed
        outfile.write_text("")

    target = Target(url, outfile, args.delay)
    if not target.is_valid():
        exit_error("Target invalid: check if target's debug mode is turned on")

    target.parse_endpoints()
    display_results(target.endpoint_counters, target.start_time)

    


if __name__ == "__main__":
    main()
