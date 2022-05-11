from gpnbp.configuration import GPNBPConfig, ConfigurationError
from gpnbp.badge.badge import BadgeGenerator
from gpnbp.printer import Printer, PrinterMockup
from gpnbp.ticket.ticket import TicketManager

from typing import Union
import sys
import logging

class GPNBPServer:
    config: GPNBPConfig
    badge_generator: BadgeGenerator
    printer: Union[Printer, PrinterMockup]

    def __init__(self):
        # Load config file
        if len(sys.argv) >= 2:
            config_file = sys.argv[1]
        else:
            config_file = 'files/conf.json'
        logging.info(f'Loading configfile {config_file}')
        self.config = GPNBPConfig(config_file)

        self.badge_generator = BadgeGenerator(self.config.badge)

        if self.config.cups.enabled:
            self.printer = Printer(self.config.cups.printer_name)
        else:
            self.printer = PrinterMockup(self.config.cups.printer_name)

        self.ticket = TicketManager(self.config.ticket)
