import logging
from flask import request


class RequestFilter(logging.Filter):
    def filter(self, record):
        try:
            record.remote_addr = request.remote_addr
            record.method = request.method
            record.path = request.path
        except RuntimeError:
            record.remote_addr = '-'
            record.method = '-'
            record.path = '-'
        return True


class RequestFormatter(logging.Formatter):
    def format(self, record):
        return super().format(record)
