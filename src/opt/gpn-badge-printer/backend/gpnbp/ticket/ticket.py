from gpnbp.ticket.TicketDataSource import TicketDataSource
from gpnbp.ticket.pretix import Pretix
from gpnbp.ticket.csv import CSV
from gpnbp.configuration import GPNBPConfig


class TicketManager:
    datasource: TicketDataSource

    def __init__(self, config: GPNBPConfig.Ticket):
        self.config = config
        if self.config.enabled:
            self.init_datasource()

    def init_datasource(self) -> bool:
        if self.config.datasource.name == "csv":
            self.datasource = CSV(**self.config.datasource.config)
            return True
        if self.config.datasource.name == "pretix":
            self.datasource = Pretix(**self.config.datasource.config)
            return True
        return False

    def getTicket(self, ticket_code):
        return self.datasource.getTicket(ticket_code)
