from step import Step
from matplotlib import pyplot as plt

import pandas as pd


class DisplayData(Step):
    def __init__(self, context):
        print(self.__class__)
        self.step_name = "DisplayDataStep"
        self.context = context

    def process(self):
        df1, df2, df3, df4 = self.mapTestDataToIdeal()

        plt.subplot(2, 2, 1)  # row 1, col 2 index 1
        plt.plot(self.context.ideal_df['x'], self.context.ideal_df['y' + str(self.context.mapping_train_to_ideal[1])],
                 color='red', label ='ideal')
        plt.xlabel('X-axis ')
        plt.ylabel('Y-axis ')
        plt.plot(self.context.train_df['x'], self.context.train_df['y1'], label="train")
        plt.scatter(df1['x'], df1['y'],c='green', label="test")

        plt.subplot(2, 2, 2)  # index 2
        plt.plot(self.context.ideal_df['x'], self.context.ideal_df['y' + str(self.context.mapping_train_to_ideal[2])],
                 color='red', label ='ideal')
        plt.xlabel('X-axis ')
        plt.ylabel('Y-axis ')
        plt.plot(self.context.train_df['x'], self.context.train_df['y2'], label="train")
        plt.scatter(df2['x'], df2['y'],c='green', label="test")

        plt.subplot(2, 2, 3)  # index 2
        plt.plot(self.context.ideal_df['x'], self.context.ideal_df['y' + str(self.context.mapping_train_to_ideal[3])],
                 color='red', label ='ideal')
        plt.xlabel('X-axis ')
        plt.ylabel('Y-axis ')
        plt.plot(self.context.train_df['x'], self.context.train_df['y3'], label="train")
        plt.scatter(df3['x'], df3['y'],c='green', label="test")

        plt.subplot(2, 2, 4)  # index 2
        plt.plot(self.context.ideal_df['x'], self.context.ideal_df['y' + str(self.context.mapping_train_to_ideal[4])],
                 color='red', label ='ideal')
        plt.xlabel('X-axis ')
        plt.ylabel('Y-axis ')
        plt.plot(self.context.train_df['x'], self.context.train_df['y4'], label="train")
        plt.scatter(df4['x'], df4['y'],c='green', label="test")

        plt.show()

    def mapTestDataToIdeal(self):

        inv_map = {v: k for k, v in self.context.mapping_train_to_ideal.items()}
        df1 = pd.DataFrame()
        df2 = pd.DataFrame()
        df3 = pd.DataFrame()
        df4 = pd.DataFrame()

        for j in self.context.mapping_test_to_ideal:
            ideal_func = self.context.mapping_test_to_ideal.get(j)
            train_func = inv_map.get(ideal_func)
            if train_func == 1:
                df1 = df1.append(self.context.test_df.iloc[[j - 1]])
            elif train_func == 2:
                df2 = df2.append(self.context.test_df.iloc[[j - 1]])
            elif train_func == 3:
                df3 = df3.append(self.context.test_df.iloc[[j - 1]])
            elif train_func == 4:
                df4 = df4.append(self.context.test_df.iloc[[j - 1]])

        return df1, df2, df3, df4
