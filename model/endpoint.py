import re


class Endpoint:
    _path = None
    _has_pattern = None
    _url = None  # need for displaying and logging url cos its more useful for user than path
    _allowed_methods = "unknown"

    status_code = 0
    node_depth = 0

    def __init__(self, path, url, depth):
        self._path = path
        self._url = url
        self.node_depth = depth

    @property
    def has_pattern(self):  # more about patterns https://docs.djangoproject.com/en/4.1/topics/http/urls/
        if not isinstance(self._has_pattern, bool):
            self._has_pattern = bool(re.search("[<[=:]", self._path))
        return self._has_pattern

    @property
    def path(self):
        return self._path

    def set_allowed_methods(self, methods):
        self._allowed_methods = methods

    def set_status_code(self, scode):
        self.status_code = scode

    def __eq__(self, other):
        return self.path == other.path

    def __str__(self):
        need_test = ""
        if self.has_pattern:
            need_test = "(NEED TESTING)"
        return f"{self._url} ({self._allowed_methods}) => {self.status_code} {need_test}"

    def save(self, results_pt):
        if self.status_code == 404:
            return  # don't save endpoints node
        with open(results_pt, 'a') as results:
            results.write(str(self) + "\n")
            results.close()
