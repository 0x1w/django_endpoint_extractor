from pathlib import Path

from view import exit_error
from model import network
from requests.exceptions import InvalidURL, InvalidSchema, MissingSchema, ConnectionError


class RunningConfig:
    outfile: Path
    url = None
    delay = 0.0
    _args = None

    def __init__(self, args):
        self.url = args.url
        self.outfile = args.out
        self.delay = args.delay
        self._args = args

    def _validate_url(self):
        url = self.url
        resp = None
        try:
            resp = network.session.get(url)
        except MissingSchema:
            exit_error("No schema supplied!")
        except InvalidSchema:
            exit_error(f"Invalid schema supplied '{url.split('://')[0]}' ")
        except InvalidURL:
            exit_error(f"Invalid URL: {url}")
        except ConnectionError:
            exit_error("Can't connect to the target!")

        if resp.status_code != 404:
            exit_error(f"{url} - Invalid status code!")

    def _validate_outfile(self):
        if self.outfile.is_dir():
            exit_error("Excepted output file path but directory path specified!")
        self.outfile.write_text("")  # create if not exists/clear if exists

    def validate_args(self):
        self._validate_url()
        if self.outfile:
            self._validate_outfile()


running: RunningConfig
