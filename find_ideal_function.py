import sys

import pandas as pd

from empty_table import EmptyTableException
from step import Step


class FindIdealFunction(Step):
    def __init__(self, context):
        """
        constructor for the FindIdealFunction class
        :param context: workflow context containing necessary details to process steps
        :return: FindIdealFunction object
        """
        print(self.__class__)
        self.step_name = "FindIdealFunctionStep"
        self.context = context

    def process(self):
        """
        Process loads training data from TRAINING_DATA table
        loads ideal functions from IDEAL_FUNC table
        and map training data to ideal functions
        :return: "MapTestDataToIdealFunction" string to go to the MapTestDataToIdealFunction step
        """
        try:

            # load training data from database and if empty then throw EmptyTableException
            self.context.train_df = pd.read_sql_table('TRAINING_DATA', self.context.connection)
            if self.context.train_df.empty:
                raise (EmptyTableException())

            # load ideal function data from database and if empty then throw EmptyTableException
            self.context.ideal_df = pd.read_sql_table('IDEAL_FUNC', self.context.connection)
            if self.context.ideal_df.empty:
                raise (EmptyTableException())

            # first loop over each training function to find its ideal value
            for trainLoop in range(1, 5):
                minDeviation = sys.float_info.max

                #  loop over each ideal function to find  map to the train functions
                for idealLopp in range(1, 51):

                    # calculate deviation y_train - y_test using dataframe subtract column to column
                    deviation = self.context.train_df["y" + str(trainLoop)].sub(
                        self.context.ideal_df["y" + str(idealLopp)])

                    # square each deviation and sum to get final squared deviation
                    sqDeviation = deviation.pow(2).sum()

                    # check for the minimum deviation
                    if sqDeviation < minDeviation:
                        minDeviation = sqDeviation
                        mappedIdealLoop = idealLopp

                print("Map train " + str(trainLoop) + " to Ideal function " + str(mappedIdealLoop))
                self.context.mapping_train_to_ideal[trainLoop] = mappedIdealLoop

            # return next step of mapping test data to ideal function
            return "MapTestDataToIdealFunction"

        except Exception as e:
            print("Error occurred  " + e)

            # return next step as error step if error occurs
            return 'ErrorStep'
