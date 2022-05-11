from gpnbp.configuration import GPNBPConfig, ConfigurationError
from gpnbp.badge.badge import BadgeGenerator
from gpnbp.printer import Printer, PrinterMockup

from typing import Union
import sys
import logging
import json
from pathlib import Path

logging.basicConfig(level=logging.CRITICAL)


class GPNBPCli:
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
        try:
            self.config = GPNBPConfig(config_file)
        except (OSError, KeyError, json.JSONDecodeError):
            raise ConfigurationError("Couldn't load configuration file")

        self.badge_generator = BadgeGenerator(self.config.badge)

        if self.config.cups.enabled:
            self.printer = Printer(self.config.cups.printer_name)
        else:
            self.printer = PrinterMockup(self.config.cups.printer_name)

    def main(self):
        while True:
            pretix_token = input('Scan your ticket or press ENTER: ')
            if pretix_token != '':
                pass
            fields = dict()
            for field in self.config.badge.fields:
                fields[field] = input(self.config.badge.fields[field].description + ': ')

            file = Path('/tmp/badge')

            self.badge_generator.getBadge(strings=fields).save(file.as_posix(), format='png')
            print('Printing the FRONT of your Badge')
            self.printer.printFile(file)
            input('Turn you badge around and put it back in the printer, then press ENTER')
            print('Printing the BACK of your Badge')
            self.printer.printFile(file)
            file.unlink()


if __name__ == "__main__":
    cli = GPNBPCli()
    cli.main()
