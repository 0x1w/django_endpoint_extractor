#!/bin/python3

import time
from pathlib import Path

import requests
from requests.exceptions import MissingSchema, ConnectionError, InvalidSchema, InvalidURL

from model.target import Target
from view import error

import argparse


def exit_error(msg):
    error(msg)
    exit(-1)


def main():
    parser = argparse.ArgumentParser(
        description='Recursive extract all endpoints from Django 404-page debug information')
    parser.add_argument("url", type=str, help="an url of the 404 page with debug information")
    parser.add_argument("-o", "--out", type=Path, metavar="PATH", help="an path to the output file", default=None)
    parser.add_argument("-d", "--delay", type=float, help="delay per request", default=0.3)
    args = parser.parse_args()

    url = args.url
    save_pt = args.out
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

    if save_pt:  # clear results file if exists
        save_pt.write_text("")

    target = Target(url, save_pt, args.delay)
    if target.is_valid():
        target.parse_endpoints()
    else:
        exit_error("Target invalid")
        
    print(f"{'=' * 20}\nTime of work: {int(time.time() - target.start_time)} sec\n")
    total = 0
    ep_total = target.endpoints_total
    for scode in ep_total:
        if not scode:
            continue
        value = ep_total[scode]
        total += value
        print(f"{scode} Endpoints: {value}")
    if 0 in ep_total:
        print(f"Endpoints that need test: {ep_total[0]}")
    print(f"\nTotal number of endpoints: {total}")


if __name__ == "__main__":
    main()
