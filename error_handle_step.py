import sqlalchemy as db
import pandas as pd

from find_ideal_function import FindIdealFunction
from step import Step


class ErrorStep(Step):
    def __init__(self, context):
        """
        constructor for the ErrorStep class
        :param context: workflow context containing necessary details to process steps
        :return: ErrorStep object
        """
        print(self.__class__)
        self.context = context

    def process(self):
        """
        Error handling for the workflow
        :return: done string to finish the process
        """
        print("Error occurred in processing Shutting down")
        return "Done"
