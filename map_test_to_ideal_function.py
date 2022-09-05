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
            # find max deviation of ideal to train mapping for each of the 4 mappings
            for k in self.context.mapping_train_to_ideal.keys():
                output = self.context.ideal_df["y" + str(self.context.mapping_train_to_ideal[k])] - \
                         self.context.train_df["y" + str(k)]
                mappingMaxDeviation["y" + str(k)] = output.max()

            # load test cases to data frame
            try:
                df_test = pd.read_csv('datasets/test.csv')
            except FileNotFoundError as f1:
                print("Test Dataset not found " + f1)
                return "ErrorStep"

            self.context.test_df = df_test
            index = 1

            # iterate over each of the test case
            for row in df_test.iterrows():

                minCurDeviationTestVsIdeal = sys.float_info.max

                # count will be used for research part of assignment to identify number of ideal functions test can
                # be mapped
                count = 0;

                # we try to map test case to each of the mapping
                for k in self.context.mapping_train_to_ideal.keys():

                    # get ideal function y value for the x value of the test case
                    indexX = self.context.ideal_df.index[self.context.ideal_df['x'] == row[1].get(key="x")].tolist()
                    idealValueSeries = self.context.ideal_df["y" + str(self.context.mapping_train_to_ideal[k])].iloc[
                        indexX]
                    idealValue = idealValueSeries.tolist()[0]

                    # calculate the deviation of the test y value with the ideal y value
                    curDeviationTestVsIdeal = abs(idealValue - row[1].get(key="y"))

                    # if current test deviation is less than maximum ideal deviation by factor ( in assignment case
                    # factor is sqrt(2))
                    if curDeviationTestVsIdeal < (mappingMaxDeviation["y" + str(k)] * self.context.factor):

                        # increment count as this test case can be mapped to current ideal function
                        count = count + 1

                        # if multiple ideal functions mapping satisfies above case choose one with minimum test to
                        # ideal deviation
                        if minCurDeviationTestVsIdeal > curDeviationTestVsIdeal:
                            minCurDeviationTestVsIdeal = curDeviationTestVsIdeal
                            print("Mapping " + str(row[1].get(key="x")) + " to " + str(
                                self.context.mapping_train_to_ideal[k]))
                            self.context.mapping_test_to_ideal[index] = self.context.mapping_train_to_ideal[k]

                # this is for research part we will store how many test cases were mapped to 0,1,2,3 ideal functions
                if str(count) in self.context.count_test_to_ideal.keys():
                    self.context.count_test_to_ideal[str(count)] = self.context.count_test_to_ideal[str(count)] + 1
                else:
                    self.context.count_test_to_ideal[str(count)] = 1
                index = index + 1

            # test db call to store the test case mapping to ideal function with deviation
            self.persistTestToDb()

            # this is for research part of written assignment
            sorted_dt = {key: value for key, value in
                         sorted(self.context.mapping_test_to_ideal.items(), key=lambda item: item[1])}
            self.context.mapping_test_to_ideal = sorted_dt
            self.reconstruct_complete_mapping()

            # return display data step as next step
            return "DisplayDataBokeh"
        except Exception as e:
            print("Error occurred  " + e)
            return "ErrorStep"

    def persistTestToDb(self):
        """
        persistTestToDb test data to db
        """

        # database table structure
        testToIdealMap = pd.DataFrame(
            columns=['X (test func)', 'Y (test func)', 'Delta Y (test func)', 'No. of ideal func'])

        df_test = pd.read_csv('datasets/test.csv')
        index = 1
        for row in df_test.iterrows():

            # get x,y values to add to database
            y = row[1].get(key="y")
            x = row[1].get(key="x")

            # get ideal function mapped that the test case is mapped
            idealFuncNo = self.context.mapping_test_to_ideal.get(index)
            if idealFuncNo is None:
                # if test case is not mapped to any ideal function then store test deviation as -1 and ideal function
                # as none value
                idealFunc = "None"
                deviation = -1
            else:

                # get absolute of  ideal y value - test y value
                idealFunc = "y" + str(idealFuncNo)
                idealRow = self.context.ideal_df.loc[self.context.ideal_df['x'] == x]
                yIdealValue = idealRow["y" + str(idealFuncNo)]
                deviation = abs(yIdealValue.get(yIdealValue.index[0]) - y)

            # append the mapping to test to ideal data frame
            testToIdealMap = testToIdealMap.append(
                {'X (test func)': x, 'Y (test func)': y, 'Delta Y (test func)': deviation,
                 'No. of ideal func': idealFunc}, ignore_index=True)
            index = index + 1

        # persist the test to ideal data frame to the database
        testToIdealMap.to_sql('TEST_DATA_IDEAL_FUNC_DEVIATION', self.context.connection, if_exists='replace',
                              index=False)

    def reconstruct_complete_mapping(self):
        """
        reconstruct_complete_mapping reconstruct mapping of train and ideal function and calculated the base MSE
        befpre test case is mapped to the ideal function
        """
        train_data_frames = list()
        for i in range(1, 5):
            train_data_frames.append(self.context.train_df[['x', 'y' + str(i)]])

        for train_fn, ideal_fn in self.context.mapping_train_to_ideal.items():
            temp_df = self.context.ideal_df['y' + str(ideal_fn)]
            train_data_frames[train_fn - 1] = train_data_frames[train_fn - 1].join(temp_df, how='right', rsuffix = '_')

        # calculate Base MSE
        for train_fn, ideal_fn in self.context.mapping_train_to_ideal.items():
            self.context.base_MSE['y' + str(ideal_fn)] = (train_data_frames[train_fn - 1].iloc[:,1] - train_data_frames[train_fn - 1].iloc[:,2]).pow(2).sum()
