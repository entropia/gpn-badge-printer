from flask import Flask, send_from_directory
from flask.scaffold import Scaffold
from gpnbp.configuration import GPNBPConfig
from gpnbp.badge.badge import BadgeGenerator
from gpnbp.printer import Printer, PrinterMockup
from typing import Union

frontend_dir = '../../frontend'


class WebAPI(Flask):
    def __init__(self,
                 config: GPNBPConfig.App,
                 badge_generator: BadgeGenerator,
                 printer: Union[Printer, PrinterMockup],
                 import_name: str):
        super().__init__(import_name)
        self.config = config
        self.badge_generator = badge_generator
        self.printer = printer

    @route('/')
    @route('/<path:path>')
    def serve_frontend(path="index.html"):
        return send_from_directory(directory=frontend_dir, path=path)

    @route('/api/badge/preview', methods=['POST'])
    def badge_preveiw():
        badge_generator
