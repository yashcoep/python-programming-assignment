import pandas as pd
from step import Step


class LoadDataset(Step):
    def __init__(self, context):
        """
       constructor for the LoadDataset class
       :param context: workflow context containing necessary details to process steps
       :return: LoadDataset object
       """
        print(self.__class__)
        self.context = context

    def process(self):
        """
        Process loads training data from csv to TRAINING_DATA table
        loads ideal functions from csv to IDEAL_FUNC table
        :return: "FindIdealFunction" string to go to the FindIdealFunction step
        """
        try:
            try:
                df_ideal = pd.read_csv('datasets/ideal.csv')
            except FileNotFoundError:
                print("Ideal dataset not found")
                return 'ErrorStep'

            try:
                df_train = pd.read_csv('datasets/train.csv')
            except FileNotFoundError:
                print("Train dataset not found")
                return 'ErrorStep'
            df_ideal.to_sql('IDEAL_FUNC', self.context.connection, if_exists='replace', index=False)
            df_train.to_sql('TRAINING_DATA', self.context.connection, if_exists='replace', index=False)
            return 'FindIdealFunction'
        except ValueError as e:
            print(e)
            return 'ErrorStep'
        except Exception as e:
            print("Error occurred  " + e)
            return 'ErrorStep'
