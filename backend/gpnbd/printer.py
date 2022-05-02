import cups
from pathlib import Path


class Printer:
    def __init__(self, name: str):
        self.name = name
        self.cups = cups.Connection()

    def status(self):
        return self.cups.getPrinters()[self.name]

    def printFile(self, filename: Path):
        self.cups.printFile(printer=self.name,
                            filename=filename.as_posix(),
                            title=filename.name,
                            options={})
