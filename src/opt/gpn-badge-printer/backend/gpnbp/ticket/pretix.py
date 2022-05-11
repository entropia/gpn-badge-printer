import requests
from gpnbp.ticket.TicketDataSource import TicketDataSource


class Pretix(TicketDataSource):
    def __init__(self,
                 url: str,
                 event: str,
                 token: str):
        self.baseURL = url
        self.event = event
        self.authToken = token

    def getTicket(self, ticket_code: str) -> dict[str, str]:
        pass
