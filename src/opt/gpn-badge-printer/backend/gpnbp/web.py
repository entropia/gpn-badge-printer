from flask import Flask, send_from_directory, Response
import json


class App(Flask):
    def __init__(self):
        super().__init__(__name__)

    def json_response(self, json_data):
        return Response(json.dumps(json_data, indent="\t"),
                        mimetype='application/json')

    @route('/')
    @route('/<path:path>')
    def serve_frontend(self, path="index.html"):
        return send_from_directory('frontend', path)

    @route('/api/status')
    def printer_status(self):
        return self.json_response()
