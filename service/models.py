"""
Account Model

The Account model persists Customer Account records and provides the
CRUD operations used by the REST API in service/routes.py.
"""
import logging
from datetime import date
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""


class Account(db.Model):
    """
    Class that represents an Account
    """

    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256))
    phone_number = db.Column(db.String(32), nullable=True)
    date_joined = db.Column(db.Date(), nullable=False, default=date.today)

    def __repr__(self):
        return f"<Account {self.name} id=[{self.id}]>"

    def create(self):
        """Creates an Account in the database"""
        logger.info("Creating %s", self.name)
        self.id = None
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates an Account in the database"""
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """Removes an Account from the database"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes an Account into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "date_joined": self.date_joined.isoformat(),
        }

    def deserialize(self, data):
        """
        Deserializes an Account from a dictionary

        Args:
            data (dict): A dictionary containing the Account data
        """
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.address = data["address"]
            self.phone_number = data.get("phone_number")
            if "date_joined" in data:
                self.date_joined = date.fromisoformat(data["date_joined"])
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError("Invalid Account: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Account: body of request contained bad or no data " + str(error)
            ) from error
        return self

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        if "sqlalchemy" not in app.extensions:
            db.init_app(app)
            app.app_context().push()
        db.create_all()

    @classmethod
    def all(cls):
        """Returns all of the Accounts in the database"""
        logger.info("Processing all Accounts")
        return cls.query.all()

    @classmethod
    def find(cls, account_id):
        """Finds an Account by its ID"""
        logger.info("Processing lookup for id %s ...", account_id)
        return cls.query.get(account_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Accounts with the given name"""
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
