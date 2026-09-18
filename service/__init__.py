"""
Package: service

This module creates and configures the Flask application, including the
Talisman security headers and CORS policy used by the Accounts REST API.
"""
import sys
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS
from service import config
from service.common import log_handlers

app = Flask(__name__)
app.config.from_object(config)

# Configure Talisman security headers (X-Frame-Options, X-Content-Type-Options,
# Content-Security-Policy, Referrer-Policy, Strict-Transport-Security, ...).
# force_https is disabled so the service also works behind the plain-HTTP
# ingress used by the test client, Docker and Kubernetes in this project.
csp = {
    "default-src": "'self'",
    "object-src": "'none'",
}
talisman = Talisman(app, force_https=False, content_security_policy=csp)

# Configure Cross-Origin Resource Sharing (CORS) so the API can be called
# from browser-based clients hosted on a different origin.
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# pylint: disable=wrong-import-position, cyclic-import
from service import models, routes  # noqa: E402, F401
from service.common import error_handlers, cli_commands  # noqa: E402, F401

try:
    models.Account.init_db(app)
except Exception as error:  # pylint: disable=broad-except
    app.logger.critical("%s: Cannot continue", error)
    sys.exit(4)

log_handlers.init_logging(app, "INFO")

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")
app.logger.info("Service initialized!")
