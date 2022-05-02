import requests


class PretixAPI:
    def __init__(self,
                 url: str,
                 event: str,
                 token: str):
        self.baseURL = url
        self.event = event
        self.authToken = token
