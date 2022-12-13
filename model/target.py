import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from model.endpoint import Endpoint
from view import info


class Target:
    _host = None
    _start_path = None
    _save_pt = None

    start_time = None  # analytics
    endpoints_total = {}  # analytics
    delay = 0

    def __init__(self, url, save_pt, delay):
        urlp = urlparse(url)
        self._host = f"{urlp[0]}://{urlp[1]}"
        self._start_path = urlp.path
        self._save_pt = save_pt
        self.delay = delay

    def get_full_url(self, path):
        return f"{self._host}{path}"

    def get_soup(self, path):
        return BeautifulSoup(requests.get(self.get_full_url(path)).content, "html.parser")

    def get_endpoints(self, path):
        endpoints = []
        soup = self.get_soup(path)
        info_div = soup.find(id="info")
        if not info_div:
            return False
        lis = info_div.find_all("li")
        for li in lis:
            path = li.get_text()
            if path:
                path = '/' + path.replace('\n', '').replace(' ', '')
                endpoints.append(Endpoint(path, self.get_full_url(path)))
        return endpoints

    def is_valid(self):
        # faster than call get_endpoints
        soup = self.get_soup(self._start_path)
        info_div = soup.find(id="info")
        return bool(info_div)

    def _parse_endpoints_recursive(self, path, found, prefix):
        endpoints = self.get_endpoints(path)
        if not len(endpoints):
            return
        for ep in endpoints:
            if ep not in found:
                # found - already found endpoints, we need it to filter new endpoints from 'endpoints directory' listing
                if not ep.has_pattern:
                    resp = requests.get(self.get_full_url(ep.path))
                    time.sleep(self.delay)  # waf prevention
                    status_code = resp.status_code
                    if status_code == 404:  # there is more endpoints in this path, so we need to parse it directly
                        info(f"Found endpoint directory {prefix}{ep}")
                        self._parse_endpoints_recursive(ep.path, endpoints, prefix + "  ")
                    if "Allow" in resp.headers:
                        ep.set_allowed_methods(resp.headers["Allow"])  # allowed methods will be displayed to user
                    ep.set_status_code(status_code)  # will be displayed to user
                if self._save_pt:
                    ep.save(self._save_pt)  # saving endpoint to results file
                info(f"Found endpoint: {prefix}{ep}")
                if ep.status_code not in self.endpoints_total:
                    self.endpoints_total[ep.status_code] = 0
                self.endpoints_total[ep.status_code] += 1

    def parse_endpoints(self):
        self.start_time = time.time()
        return self._parse_endpoints_recursive(self._start_path, [], "")
