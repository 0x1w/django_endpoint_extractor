#!/bin/python3

import time
from os.path import basename

import requests
from sys import argv

from requests.exceptions import MissingSchema, ConnectionError, InvalidSchema, InvalidURL

from model.target import Target
from view import error

DELAY = 0.3


def exit_error(msg):
    error(msg)
    exit(-1)


def main():
    global DELAY
    argc = len(argv)
    if argc < 2:
        example = "https://example.com/404_page"
        pname = basename(argv[0])
        exit_error(
            f'''Please, provide 404 page URL
Usage: python3 {pname} {example} 
       python3 {pname} {example} results.txt       
        ''')

    url = argv[1]
    save_pt = None
    resp = None

    if argc > 2:
        save_pt = argv[2]

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

    if save_pt:  # clear results file
        f = open(save_pt, 'w')
        f.close()

    delay_msg = "Enter delay (Leave blank to use 0.3): "
    delay = input(delay_msg)
    while delay:
        try:
            if delay:
                DELAY = float(delay)
            break
        except ValueError:
            error("Invalid delay value, try again...")
            delay = input(delay_msg)

    target = Target(url, save_pt, DELAY)
    target.parse_endpoints()

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
