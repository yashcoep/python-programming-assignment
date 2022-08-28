import sqlite3
import sqlalchemy as db


class Step:
    def __init__(self, context):
        print(self.__class__)
        self.step_name = "Step"

        # Init Processing creating database
        conn = sqlite3.connect('test_database')
        c = conn.cursor()
        conn.commit()

        engine = db.create_engine('sqlite:///test_database')
        context.connection = engine.connect()
        self.context = context

    def process(self):
        print("Processing ")
        return "LoadDataset"
