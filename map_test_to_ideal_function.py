import math
import sys
import pandas as pd

from step import Step


class MapTestDataToIdealFunction(Step):
    def __init__(self, context):
        """
       constructor for the MapTestDataToIdealFunction class
       :param context: workflow context containing necessary details to process steps
       :return: MapTestDataToIdealFunction object
       """
        print(self.__class__)
        self.step_name = "MapTestDataToIdealFunctionStep"
        self.context = context

    def process(self):
        """
        Process loads test data from csv
        Maps each test point to ideal function
        :return: "DisplayDataBokeh" string to go to the DisplayDataBokeh step
        """
        try:
            mappingMaxDeviation = {}
            # find max deviation
            for k in self.context.mapping_train_to_ideal.keys():
                output = self.context.ideal_df["y" + str(self.context.mapping_train_to_ideal[k])] - \
                         self.context.train_df["y" + str(k)]
                mappingMaxDeviation["y" + str(k)] = output.max()
            try:
                df_test = pd.read_csv('datasets/test.csv')
            except FileNotFoundError as f1:
                print("Test Dataset not found " + f1)
                return "ErrorStep"

            self.context.test_df = df_test
            index = 1
            for row in df_test.iterrows():
                minCurDeviationTestVsIdeal = sys.float_info.max
                count = 0;
                for k in self.context.mapping_train_to_ideal.keys():
                    indexX = self.context.ideal_df.index[self.context.ideal_df['x'] == row[1].get(key="x")].tolist()
                    idealValueSeries = self.context.ideal_df["y" + str(self.context.mapping_train_to_ideal[k])].iloc[
                        indexX]
                    idealValue = idealValueSeries.tolist()[0]
                    curDeviationTestvsIdeal = abs(idealValue - row[1].get(key="y"))
                    if curDeviationTestvsIdeal < (mappingMaxDeviation["y" + str(k)] * self.context.factor):
                        count = count + 1
                        if minCurDeviationTestVsIdeal > curDeviationTestvsIdeal:
                            minCurDeviationTestVsIdeal = curDeviationTestvsIdeal
                            print("Mapping " + str(row[1].get(key="x")) + " to " + str(
                                self.context.mapping_train_to_ideal[k]))
                            self.context.mapping_test_to_ideal[index] = self.context.mapping_train_to_ideal[k]
                    else:
                        print("Not Mapping " + str(row[1].get(key="x")))
                if str(count) in self.context.count_test_to_ideal.keys():
                    self.context.count_test_to_ideal[str(count)] = self.context.count_test_to_ideal[str(count)] + 1
                else:
                    self.context.count_test_to_ideal[str(count)] = 1
                index = index + 1

            self.persistTestToDb()
            sorted_dt = {key: value for key, value in
                         sorted(self.context.mapping_test_to_ideal.items(), key=lambda item: item[1])}
            self.context.mapping_test_to_ideal = sorted_dt
            self.reconstruct_complete_mapping()
            return "DisplayDataBokeh"
        except Exception as e:
            print("Error occurred  " + e)
            return "ErrorStep"

    def persistTestToDb(self):
        """
        persistTestToDb test data to db
        """
        testToIdealMap = pd.DataFrame(
            columns=['X (test func)', 'Y (test func)', 'Delta Y (test func)', 'No. of ideal func'])
        df_test = pd.read_csv('datasets/test.csv')
        index = 1
        for row in df_test.iterrows():
            y = row[1].get(key="y")
            x = row[1].get(key="x")
            idealFuncNo = self.context.mapping_test_to_ideal.get(index)
            if idealFuncNo is None:
                idealFunc = None
                deviation = -1
            else:
                idealFunc = "y" + str(idealFuncNo)
                idealRow = self.context.ideal_df.loc[self.context.ideal_df['x'] == x]
                yIdealValue = idealRow["y" + str(idealFuncNo)]
                deviation = abs(yIdealValue.get(yIdealValue.index[0]) - y)
            testToIdealMap = testToIdealMap.append(
                {'X (test func)': x, 'Y (test func)': y, 'Delta Y (test func)': deviation,
                 'No. of ideal func': idealFunc}, ignore_index=True)
            index = index + 1
        testToIdealMap.to_sql('TEST_DATA_IDEAL_FUNC_DEVIATION', self.context.connection, if_exists='replace',
                              index=False)
        print(testToIdealMap)

    def reconstruct_complete_mapping(self):
        train_data_frames = list()
        for i in range(1, 5):
            train_data_frames.append(self.context.train_df[['x', 'y' + str(i)]])

        for train_fn, ideal_fn in self.context.mapping_train_to_ideal.items():
            temp_df = self.context.ideal_df['y' + str(ideal_fn)]
            train_data_frames[train_fn - 1] = train_data_frames[train_fn - 1].join(temp_df, how='right', rsuffix = '_')

        for train_fn, ideal_fn in self.context.mapping_train_to_ideal.items():
            self.context.base_MSE['y' + str(ideal_fn)] = (train_data_frames[train_fn - 1].iloc[:,1] - train_data_frames[train_fn - 1].iloc[:,2]).pow(2).sum()

        print()
