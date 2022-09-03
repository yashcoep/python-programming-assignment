import math
from turtle import pd

"""
TaskContext contains all the data needed for each step to execute the current step
"""


class TaskContext:

    def __init__(self):
        self.mapping_test_to_ideal = {}
        self.count_test_to_ideal = {}
        self.base_MSE = {}
        self.factor_to_MSE = {}
        self.ideal_df = None
        self.train_df = None
        self.mapping_train_to_ideal = {}
        self.connection = None
        self.test_df = None
        self.factor = math.sqrt(2)
        self.display = True

    def get_connection(self):
        return self.connection

    def set_connection(self, connection):
        self.connection = connection

    def get_mapping_train_to_ideal(self):
        return self.mapping_train_to_ideal

    def set_mapping_train_to_ideal(self, mapping_train_to_ideal):
        self.mapping_train_to_ideal = mapping_train_to_ideal

    def get_train_df(self):
        return self.train_df

    def set_train_df(self, train_df):
        self.train_df = train_df

    def get_ideal_df(self):
        return self.ideal_df

    def set_ideal_df(self, ideal_df):
        self.ideal_df = ideal_df

    def get_mapping_test_to_deal(self):
        return self.mapping_test_to_ideal

    def set_mapping_test_to_deal(self, mapping_test_to_ideal):
        self.mapping_test_to_ideal = mapping_test_to_ideal
