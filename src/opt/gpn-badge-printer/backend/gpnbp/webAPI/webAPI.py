import base64
from io import BytesIO

import cups

from gpnbp.server import GPNBPServer
from gpnbp.webAPI.Response import Response
from gpnbp.webAPI.Request import Request

import flask
import werkzeug.exceptions
from typing import Any
from pathlib import Path
import json
from uuid import uuid4

frontend_dir = '../../../frontend'
temp_dir = '/tmp/'


class WebAPI:
    app = flask.Flask('gpnbp.webAPI.webAPI')
    server: GPNBPServer

    def __init__(self, server_object: GPNBPServer):
        global server
        server = server_object
        self.app.run(host=server.config.app.host,
                     port=server.config.app.port,
                     debug=server.config.app.debug)

    @staticmethod
    def json_response(obj: Any):
        return flask.Response(json.dumps(obj, default=lambda o: getattr(o, '__dict__', str(o))),
                              content_type='application/json')

    @staticmethod
    def json_error_response(error: Response.Error):
        return flask.Response(json.dumps(error, default=lambda o: getattr(o, '__dict__', str(o))),
                              content_type='application/json',
                              status=error.code)

    @staticmethod
    @app.route('/')
    @app.route('/<path:path>')
    def serve_frontend(path="index.html"):
        try:
            if int(flask.__version__[0]) > 1:
                return flask.send_from_directory(directory=frontend_dir, path=path)
            else:
                return flask.send_from_directory(directory=frontend_dir, filename=path)
        except werkzeug.exceptions.NotFound:
            path = path + 'index.html'
            if int(flask.__version__[0]) > 1:
                return flask.send_from_directory(directory=frontend_dir, path=path)
            else:
                return flask.send_from_directory(directory=frontend_dir, filename=path)

    @staticmethod
    @app.route('/api/badge/info', methods=['GET'])
    def badgeInfo():
        try:
            response = Response.Badge.DefinitionResponse()
            response.width = server.config.badge.size.width
            response.height = server.config.badge.size.height
            response.fields = list()
            for field in server.config.badge.fields:
                field_response = Response.Badge.DefinitionResponse.Field()
                field_response.name = field
                field_response.description = server.config.badge.fields[field].description
                field_response.max_length = server.config.badge.fields[field].max_length
                response.fields.append(field_response)
            return WebAPI.json_response(response)
        except:
            response = Response.Error()
            response.code = 500
            response.message = f'Server Error'
            return WebAPI.json_error_response(response)

    @staticmethod
    @app.route('/api/badge/preview', methods=['POST'])
    def badge_preview():
        try:
            try:
                # Parse request
                http_request = flask.request.json
                request = Request.Badge.Request()
                request.show_margins = http_request['show_margins']
                request.show_background = http_request['show_background']
                request.fields = list()
                for field in http_request['fields']:
                    field_request = Request.Badge.Request.Field()
                    field_request.name = field['name']
                    field_request.value = field['value']
                    request.fields.append(field_request)

                # Generate response
                response = Response.Badge.PreviewResponse()

                strings = dict()
                for field in request.fields:
                    strings[field.name] = field.value

                badge = server.badge_generator.getBadge(strings=strings,
                                                        show_margins=request.show_margins,
                                                        show_background=request.show_background)
            except KeyError:
                response = Response.Error()
                response.code = 400
                response.message = f'Bad request'
                return WebAPI.json_error_response(response)

            data = BytesIO()
            badge.save(data, "PNG")
            data64 = base64.b64encode(data.getvalue())
            response.image = u'data:img/png;base64,' + data64.decode('utf-8')
            response.fields = request.fields
            return WebAPI.json_response(response)
        except None:
            response = Response.Error()
            response.code = 500
            response.message = f'Server Error'
            return WebAPI.json_error_response(response)

    @staticmethod
    @app.route('/api/badge/print', methods=['POST'])
    def badge_print():
        try:
            try:
                # Parse request
                http_request = flask.request.json
                request = Request.Badge.Request()
                request.show_margins = http_request['show_margins']
                request.show_background = http_request['show_background']
                request.fields = list()
                for field in http_request['fields']:
                    field_request = Request.Badge.Request.Field()
                    field_request.name = field['name']
                    field_request.value = field['value']
                    request.fields.append(field_request)

                # Generate response
                response = Response.Printer.Job()
                strings = dict()
                for field in request.fields:
                    strings[field.name] = field.value
                badge = server.badge_generator.getBadge(strings=strings,
                                                        show_margins=request.show_margins,
                                                        show_background=request.show_background)
            except KeyError:
                response = Response.Error()
                response.code = 400
                response.message = f'Bad request'
                return WebAPI.json_error_response(response)
            try:
                # Temporary file
                file = Path(temp_dir + uuid4().hex)
                badge.save(file.as_posix(), "PNG")
                response.jobid = server.printer.printFile(file)
                file.unlink()
                return WebAPI.json_response(response)
            except cups.IPPError as e:
                response = Response.Error()
                response.code = 530
                response.message = f'Cups Error: {e}'
                return WebAPI.json_error_response(response)
        except:
            response = Response.Error()
            response.code = 500
            response.message = f'Server Error'
            return WebAPI.json_error_response(response)

    @staticmethod
    @app.route('/api/printer/status', methods=['GET'])
    def printer_status():
        try:
            try:
                response = Response.Printer.Status()
                cups_status = server.printer.status()
                response.printer_state = cups_status['printer-state']
                response.printer_state_message = cups_status['printer-state-message']
                response.printer_state_reasons = cups_status['printer-state-reasons']
                response.printer_name = server.printer.printer_name
                return WebAPI.json_response(response)
            except cups.IPPError as e:
                response = Response.Error()
                response.code = 530
                response.message = f'Cups Error: {e}'
                return WebAPI.json_error_response(response)
        except KeyError:
            response = Response.Error()
            response.code = 500
            response.message = f'Server Error'
            return WebAPI.json_error_response(response)

    @staticmethod
    @app.route('/api/printer/job/<int:jobid>', methods=['GET'])
    def printer_job_status(jobid: int):
        #try:
            try:
                response = Response.Printer.JobStatus()
                job_status = server.printer.getJobDetails(jobid)
                response.jobid = job_status['job-id']
                response.number_of_documents = job_status['number-of-documents']
                response.time_at_completed = job_status['time-at-completed']
                response.time_at_creation = job_status['time-at-creation']
                response.time_at_processing = job_status['time-at-processing']
                response.job_state = job_status['job-state']
                response.job_state_reason = job_status['job-state-reasons']
                response.job_printer_state_message = job_status.get('job-printer-state-message', '')
                response.job_printer_state_reasons = job_status.get('job-printer-state-reasons', [])
                return WebAPI.json_response(response)
            except cups.IPPError as e:
                response = Response.Error()
                response.code = 530
                response.message = f'Cups Error: {e}'
                return WebAPI.json_error_response(response)
        #except:
        #    response = Response.Error()
        #    response.code = 500
        #    response.message = f'Server Error'
       #     return WebAPI.json_error_response(response)

    @staticmethod
    @app.route('/api/ticket/<ticket_code>', methods=['GET'])
    def ticket_get(ticket_code: str):
        try:
            try:
                # Parse request
                request = Request.Ticket.Request()
                request.ticket_code = ticket_code
            except KeyError:
                response = Response.Error()
                response.code = 400
                response.message = f'Bad request'
                return WebAPI.json_error_response(response)

            # Generate response
            try:
                response = Response.Ticket.Response()
                response.fields = server.ticket.getTicket(ticket_code)
                return WebAPI.json_response(response)
            except KeyError:
                response = Response.Error()
                response.code = 404
                response.message = f'Ticket {ticket_code} not found!'
            return WebAPI.json_error_response(response)
        except:
            response = Response.Error()
            response.code = 500
            response.message = f'Server Error'
            return WebAPI.json_error_response(response)
