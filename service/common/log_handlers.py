"""
Log Handlers

This module sets up a consistent log formatter so that log statements
look the same whether running locally, in a container, or in Kubernetes.
"""
import logging


def init_logging(app, log_level=logging.INFO):
    """Sets up a Gunicorn-style formatter for the Flask app logger"""
    app.logger.setLevel(log_level)
    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )
    handler.setFormatter(formatter)
    for old_handler in app.logger.handlers:
        app.logger.removeHandler(old_handler)
    app.logger.addHandler(handler)
    app.logger.propagate = False
    app.logger.info("Logging handler established")
