from pathlib import Path
import csv

from gpnbp.ticket.TicketDataSource import TicketDataSource


class CSV(TicketDataSource):
    def __init__(self,
                 path: str,
                 delimiter: str = ',',
                 ticket_code_field: str = 'ticket_code'):
        Path(path)
        raw_data = list()
        self.data = dict()
        with open(path) as f:
            reader = csv.reader(f, delimiter=delimiter)
            for row in reader:
                raw_data.append(row)
            header = raw_data[0]
            raw_data = raw_data[1:]
            for row in raw_data:
                parsed_row = dict()
                for item in header:
                    parsed_row[item] = row[header.index(item)]
                self.data[parsed_row[ticket_code_field]] = parsed_row

    def getTicket(self, ticket_code: str) -> dict[str, str]:
        return self.data[ticket_code]

