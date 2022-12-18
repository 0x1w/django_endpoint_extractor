from requests import Session
import urllib3


class CustomSession(Session):
    def __init__(self):
        super().__init__()
        self.verify = False


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = CustomSession()
