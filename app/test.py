import unittest
from flask_sqlalchemy import SQLAlchemy
from init import create_app
from models import db

class AppTest(unittest.TestCase):
    """this class represents the app's test case"""

    def set_up(self):
        """ 
        initialize the app with
        - test DB
        - setting up a web client
        """
        
        self.app = create_app("test")
        
        # context for SQLAlchemy to be aware of the Flask app' we're using
        # https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
        self.app.app_context().push()
        
        # bootstrap database, here we conveniently dont use db migrations
        db.init_app(self.app)
        db.create_all()
        
        # defining the web client
        self.client = self.app.test_client

    # tearing down logic helps guarantee that code runs in isolation
    # although, keep in mind that sometimes
    # it's better to put tear down logic in the setup
    # because an error may crash your whole test suite without your intended
    # teardown logic being executed
    def tear_down(self):
        """
        reset logic:
        - reset DB after each test is run
        """
        engine = SQLAlchemy.create_engine("postgresql://usr:pwd@pgsql-test:5433/crypto")
        connection = engine.raw_connection()
        cursor = connection.cursor()
        command = "DROP TABLE crypto, crypto_lists;"
        cursor.execute(command)
        connection.commit()
        cursor.close()

    def test_1(self):
        pass

    def test_2(self):
        pass


# make tests executable
if __name__ == "__main__":
    unittest.main()
