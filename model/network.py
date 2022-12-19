from requests import Session
import urllib3
from urllib3.exceptions import InsecureRequestWarning


class CustomSession(Session):
    def __init__(self):
        super().__init__()
        self.verify = False


urllib3.disable_warnings(InsecureRequestWarning)
session = CustomSession()
