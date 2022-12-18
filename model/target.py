import time
from urllib.parse import urlparse

from model import network
from bs4 import BeautifulSoup

from model.endpoint import Endpoint
from view import display_endpoint, display_endpoint_node


class Target:
    _host = None
    _start_path = None
    _outfile = None

    start_time = None  # analytics
    endpoint_counters = {}  # analytics
    delay = 0

    def __init__(self, url, outfile, delay):
        urlp = urlparse(url)
        self._host = f"{urlp[0]}://{urlp[1]}"
        self._start_path = urlp.path
        self._outfile = outfile
        self.delay = delay

    def get_full_url(self, path):
        return f"{self._host}{path}"

    def get_soup(self, path):
        return BeautifulSoup(network.session.get(self.get_full_url(path)).content, "html.parser")

    def get_endpoints(self, path, depth):
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
                endpoints.append(Endpoint(path, self.get_full_url(path), depth))
        return endpoints

    def is_valid(self):
        # faster than call get_endpoints
        soup = self.get_soup(self._start_path)
        info_div = soup.find(id="info")
        return bool(info_div)

    def _parse_endpoints_recursive(self, path, found, node_depth):
        endpoints = self.get_endpoints(path, node_depth)
        if not len(endpoints):
            return
        for ep in endpoints:
            if ep not in found:
                # found - already found endpoints, we need it to filter new endpoints from 'endpoints node' listing
                if not ep.has_pattern:
                    resp = network.session.get(self.get_full_url(ep.path))
                    time.sleep(self.delay)  # waf prevention
                    status_code = resp.status_code
                    if status_code == 404:  # there is more endpoints in this path, so we need to parse it directly
                        display_endpoint_node(ep)
                        self._parse_endpoints_recursive(ep.path, endpoints, node_depth + 1)
                    if "Allow" in resp.headers:
                        ep.set_allowed_methods(resp.headers["Allow"])  # allowed methods will be displayed to user
                    ep.set_status_code(status_code)  # will be displayed to user
                if self._outfile:
                    ep.save(self._outfile)  # saving endpoint to outfile
                display_endpoint(ep)
                if ep.status_code not in self.endpoint_counters:
                    self.endpoint_counters[ep.status_code] = 0
                self.endpoint_counters[ep.status_code] += 1

    def parse_endpoints(self):
        self.start_time = time.time()
        return self._parse_endpoints_recursive(self._start_path, [], 0)
