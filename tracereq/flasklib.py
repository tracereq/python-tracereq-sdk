from flask import Flask, request
from flask.signals import request_started, request_finished
from . import Integration
from .hub import Hub
from .tracing import generate_trace_req_packet, Trace


class FlaskLibIntegration(Integration):
    identifier = "flasklib"

    def install(self):
        request_started.connect(_request_started)

        def tracereq_wsgi_app(self, environ, start_response):
            hub = Hub.current

            trace_id = Trace.get_trace_from_headers(environ)
            hub.set_trace(trace_id)
            return self.wsgi_app(environ, start_response)

        Flask.__call__ = tracereq_wsgi_app

    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app


def _request_started(app, **kwargs):
    hub = Hub.current
    current_trace = hub.get_trace()
    current_req_packet = generate_trace_req_packet(current_trace, request)
    hub.client.transport.send(current_req_packet)
