from pathlib import Path
import csv

from gpnbp.ticket.TicketDataSource import TicketDataSource


class CSV(TicketDataSource):
    def __init__(self,
                 path: str,
                 delimiter: str = ',',
                 ticket_code_field: str = 'ticket_code',
                 case_sensitive: bool = True):
        Path(path)
        raw_data = list()
        self.data = dict()
        self.case_sensitive = case_sensitive
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
                index = parsed_row[ticket_code_field] if self.case_sensitive else parsed_row[ticket_code_field].lower()
                self.data[index] = parsed_row

    def getTicket(self, ticket_code: str) -> dict[str, str]:
        index = ticket_code if self.case_sensitive else ticket_code.lower()
        return self.data[index]

