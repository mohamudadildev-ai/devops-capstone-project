"""
Test cases for the Account Model
"""
import os
import logging
import unittest
from service.models import Account, DataValidationError, db
from service import app
from tests.factories import AccountFactory

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///test.db")


class TestAccountModel(unittest.TestCase):
    """Test Cases for the Account Model"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Account.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Run before each test"""
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """Run after each test"""
        db.session.remove()

    def test_create_an_account(self):
        """It should create an Account and assign it an id"""
        account = AccountFactory()
        account.create()
        self.assertIsNotNone(account.id)
        accounts = Account.all()
        self.assertEqual(len(accounts), 1)

    def test_read_an_account(self):
        """It should read an Account by id"""
        account = AccountFactory()
        account.create()
        found_account = Account.find(account.id)
        self.assertEqual(found_account.id, account.id)
        self.assertEqual(found_account.name, account.name)
        self.assertEqual(found_account.email, account.email)

    def test_list_all_accounts(self):
        """It should list all Accounts in the database"""
        for _ in range(3):
            AccountFactory().create()
        accounts = Account.all()
        self.assertEqual(len(accounts), 3)

    def test_update_an_account(self):
        """It should update an existing Account"""
        account = AccountFactory()
        account.create()
        account.name = "Updated Name"
        account.update()
        found_account = Account.find(account.id)
        self.assertEqual(found_account.name, "Updated Name")

    def test_update_with_no_id(self):
        """It should raise an error when updating without an id"""
        account = AccountFactory()
        account.id = None
        self.assertRaises(DataValidationError, account.update)

    def test_delete_an_account(self):
        """It should delete an Account from the database"""
        account = AccountFactory()
        account.create()
        self.assertEqual(len(Account.all()), 1)
        account.delete()
        self.assertEqual(len(Account.all()), 0)

    def test_serialize_an_account(self):
        """It should serialize an Account into a dictionary"""
        account = AccountFactory()
        data = account.serialize()
        self.assertIn("id", data)
        self.assertEqual(data["name"], account.name)
        self.assertEqual(data["email"], account.email)
        self.assertEqual(data["address"], account.address)
        self.assertEqual(data["phone_number"], account.phone_number)

    def test_deserialize_an_account(self):
        """It should deserialize an Account from a dictionary"""
        data = AccountFactory().serialize()
        account = Account()
        account.deserialize(data)
        self.assertEqual(account.name, data["name"])
        self.assertEqual(account.email, data["email"])

    def test_deserialize_with_key_error(self):
        """It should raise DataValidationError for missing data"""
        account = Account()
        self.assertRaises(DataValidationError, account.deserialize, {})

    def test_deserialize_with_type_error(self):
        """It should raise DataValidationError for bad data"""
        account = Account()
        self.assertRaises(DataValidationError, account.deserialize, [])
