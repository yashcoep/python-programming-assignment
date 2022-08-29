from step import Step
import pandas as pd

# Bokeh Libraries
from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.layouts import column


class DisplayDataBokeh(Step):
    def __init__(self, context):
        """
        constructor for the DisplayDataBokeh class
        :param context: workflow context containing necessary details to process steps
        :return: DisplayDataBokeh object
        """
        print(self.__class__)
        self.step_name = "DisplayDataBokeh"
        self.context = context

    def process(self):
        """
        Display data using Bokeh
        After process completion 2 html will be created
        mapTestToIdeal.html -> Mapping train data to ideal function
        mapTrainToIdeal.html -> Mapping test point to ideal function
        :return: next step name string
        """
        if not self.context.display:
            return "Done"
        try:
            # Output the visualization directly in the notebook
            output_file('output/mapTrainToIdeal.html', title='Mapping training function to ideal function')

            plots = []
            for i in range(4):
                fig = figure(
                    title='Mapping Train y' + str(i + 1) + ' to ideal y' + str(
                        self.context.mapping_train_to_ideal[i + 1]),
                    plot_height=600, plot_width=600,
                    toolbar_location=None)

                # Draw the coordinates as circles
                fig.line(x=self.context.ideal_df['x'],
                         y=self.context.ideal_df['y' + str(self.context.mapping_train_to_ideal[i + 1])],
                         color='green', legend='Ideal function')

                fig.circle(x=self.context.train_df['x'],
                           y=self.context.train_df['y' + str(i + 1)],
                           color='red', size=2, alpha=0.5,
                           legend='Train Dataset')
                fig.legend.location = 'bottom_left'
                fig.legend.background_fill_color = "white"
                fig.legend.background_fill_alpha = 0.3
                plots.append(fig)
            show(column(*plots))

            output_file('output/mapTestToIdeal.html', title='Mapping test point to ideal function')
            dflist = self.mapTestDataToIdeal()

            plots = []
            for i in range(4):
                for ind in dflist[i].index:
                    x = dflist[i]['x'][ind]
                    y = dflist[i]['y'][ind]
                    fig = figure(
                        title='Mapping test point (' + str(x) + " , " + str(y) + ') to ideal y' + str(
                            self.context.mapping_train_to_ideal[i + 1]),
                        plot_height=600, plot_width=600,
                        toolbar_location=None)

                    # Draw the coordinates as circles
                    fig.line(x=self.context.ideal_df['x'],
                             y=self.context.ideal_df['y' + str(self.context.mapping_train_to_ideal[i + 1])],
                             color='green', legend='Ideal function')

                    fig.circle(x=x,
                               y=y,
                               color='red', size=10, alpha=0.5,
                               legend='Test point')

                    fig.legend.location = 'bottom_left'
                    fig.legend.background_fill_color = "white"
                    fig.legend.background_fill_alpha = 0.3

                    plots.append(fig)
            show(column(*plots))
            return "Done"

        except Exception as e1:
            print("Error occurred " + e1)
            return "ErrorStep"

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
        dflist = [df1, df2, df3, df4]
        return dflist