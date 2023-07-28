from flask import Flask, _request_ctx_stack
from flask.signals import request_started, request_finished
from . import Integration
from tracereq_sdk.engine import Engine
from tracereq_sdk.tracing import generate_trace_event, Trace, generalize_request


class FlasklibIntegration(Integration):
    integration_key = "flasklib"

    def install(self):
        request_started.connect(_request_started)
        request_finished.connect(_request_finished)

        def tracereq_wsgi_app(self, environ, start_response):
            engine = Engine.current

            trace = Trace.get_trace_from_environ(environ, span_type='http.server')
            engine.set_trace(trace)
            return self.wsgi_app(environ, start_response)

        Flask.__call__ = tracereq_wsgi_app

    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app


def _request_started(app, **kwargs):
    engine = Engine.current
    current_request_data = generalize_request(_request_ctx_stack.top.request)

    engine.set_request_data(current_request_data)


def _request_finished(app, response, **kwargs):
    engine = Engine.current
    current_trace = engine.get_trace()
    Trace.mark_finish(current_trace)

    current_request_data = engine.get_request_data()
    current_trace_event = generate_trace_event(current_trace, current_request_data, response)

    engine.client.transport.send(current_trace_event)
