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
            self.context.train_df = pd.read_sql_table('TRAINING_DATA', self.context.connection)
            if self.context.train_df.empty:
                raise (EmptyTableException())
            self.context.ideal_df = pd.read_sql_table('IDEAL_FUNC', self.context.connection)
            if self.context.ideal_df.empty:
                raise (EmptyTableException())

            for trainLoop in range(1, 5):
                maxDeviation = sys.float_info.max
                for idealLopp in range(1, 51):
                    deviation = self.context.train_df["y" + str(trainLoop)].sub(
                        self.context.ideal_df["y" + str(idealLopp)])
                    sqDeviation = deviation.pow(2).sum()
                    if sqDeviation < maxDeviation:
                        maxDeviation = sqDeviation
                        mappedIdealLoop = idealLopp
                print("Map train " + str(trainLoop) + " to Ideal function " + str(mappedIdealLoop))
                self.context.mapping_train_to_ideal[trainLoop] = mappedIdealLoop
            return "MapTestDataToIdealFunction"
        except Exception as e:
            print("Error occurred  " + e)
            return 'ErrorStep'
