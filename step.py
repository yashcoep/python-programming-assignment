import sqlite3
import sqlalchemy as db

"""
Parent class of all steps
Takes care of initialization of database connection and setup the initial context
"""


class Step:
    def __init__(self, context):
        print(self.__class__)
        self.step_name = "Step"

        # Init Processing creating database
        conn = sqlite3.connect('test_database')
        c = conn.cursor()
        conn.commit()

        # setup connection
        engine = db.create_engine('sqlite:///test_database')
        context.connection = engine.connect()
        self.context = context

    def process(self):
        print("Processing ")
        return "LoadDataset"
