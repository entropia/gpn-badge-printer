import abc


class TicketDataSource(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def getTicket(self, ticket_code: str) -> dict[str, str]:
        pass
