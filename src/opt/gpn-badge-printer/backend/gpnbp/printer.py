import cups
from pathlib import Path
import logging


class PrinterNotFound(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class Printer:
    def __init__(self, printer_name: str):
        logging.info(f'Initializing Printer {printer_name}')
        self.printer_name = printer_name
        self.cups = cups.Connection()
        if printer_name not in self.cups.getPrinters():
            raise PrinterNotFound(f'Printer {printer_name} not found!')

    def status(self):
        return self.cups.getPrinters()[self.printer_name]

    def printFile(self, filename: Path) -> int:
        jobid = self.cups.printFile(printer=self.printer_name,
                                    filename=filename.as_posix(),
                                    title=filename.name,
                                    options={})
        logging.info(f'Printing \'{filename}\' on {self.printer_name}: ID={jobid}')
        return jobid

    def getJobDetails(self, jobid: int) -> dict:
        return self.cups.getJobAttributes(jobid)

    def cancelJob(self, jobid: int, purge: bool = False):
        logging.info(f'Cancel {jobid}')
        self.cups.cancelJob(jobid, purge)

    def printTestPage(self):
        logging.info(f'Printing TestPage on {self.printer_name}')
        self.cups.printTestPage(self.printer_name)


class PrinterMockup:
    def __init__(self, printer_name: str):
        self.printer_name = 'MOCK'
        logging.info(f'Initializing MOCK Printer {printer_name}')

    def status(self):
        return {'printer-is-shared': False,
                'printer-state': -1,
                'printer-state-message': 'Mocked printer',
                'printer-state-reasons': ['paused'],
                'printer-type': -1,
                'printer-uri-supported': '',
                'printer-location': '',
                'printer-info': 'Mocked printer',
                'device-uri': '',
                'printer-make-and-model': 'MOCKUP'}

    def printFile(self, filename: Path) -> int:
        logging.info(f'Printing \'{filename}\' on {self.printer_name}: ID=---')
        return -1

    def getJobDetails(self, jobid: int) -> dict:
        return {'attributes-charset': 'utf-8',
                'attributes-natural-language': 'en-gb',
                'number-of-documents': 1,
                'job-media-progress': 0,
                'job-more-info': 'http://localhost/jobs/314',
                'job-printer-up-time': 1652019936,
                'job-printer-uri': 'ipp://localhost/printers/Nadeldrucker',
                'job-uri': 'ipp://localhost/jobs/314',
                'printer-uri': 'ipp://localhost/printers/Nadeldrucker',
                'document-format-detected': 'application/vnd.cups-pdf-banner',
                'document-format': 'application/vnd.cups-pdf-banner',
                'job-priority': 50,
                'job-uuid': 'urn:uuid:6bf5df3a-638b-3269-4f7b-b5a4bcd098ee',
                'date-time-at-completed': None,
                'date-time-at-creation': '(IPP_TAG_DATE)',
                'date-time-at-processing': None,
                'time-at-completed': None,
                'time-at-creation': 1652019894,
                'time-at-processing': None,
                'job-id': 314,
                'job-state': 3,
                'job-state-reasons': 'none',
                'job-impressions-completed': 0,
                'job-media-sheets-completed': 0,
                'job-k-octets': 1,
                'job-hold-until': 'no-hold',
                'job-sheets': ['none', 'none']}


    def cancelJob(self, jobid: int, purge: bool = False):
        logging.info(f'Cancel {jobid}')
        pass

    def printTestPage(self):
        logging.info(f'Printing TestPage on {self.printer_name}')
        pass
