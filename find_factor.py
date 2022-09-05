import numpy as np
import pandas as pd
from bokeh.io import output_file
from bokeh.plotting import figure, show

from context import TaskContext
from step import Step
from workflow_next_step import WorkflowNextStep

#factors = np.arange(0.1, 3.0, 0.01)
factors = [1.25, 1.414,2.5]
column_names = ["x", "y"]
df = pd.DataFrame(columns=column_names)

count_column_names = ["factor", "0", "1", "2", "3", "4"]
count_df = pd.DataFrame(columns=count_column_names)

mse_df = pd.DataFrame()


def initCountTestToIdeal():
    context.count_test_to_ideal["0"] = 0
    context.count_test_to_ideal["1"] = 0
    context.count_test_to_ideal["2"] = 0
    context.count_test_to_ideal["3"] = 0


def find_MSE_change(factor):
    test_df = pd.read_sql_table('TEST_DATA_IDEAL_FUNC_DEVIATION', context.connection)
    cur_MSE = context.base_MSE.copy()
    for index, row in test_df.iterrows():
        if row['No. of ideal func'] is not None:
            cur_MSE[str(row['No. of ideal func'])] = cur_MSE[str(row['No. of ideal func'])] + row[
                'Delta Y (test func)'] ** 2
    mapped_count = test_df['No. of ideal func'].value_counts()
    for x in cur_MSE.keys():
        if x in mapped_count:
            cur_MSE[x] = cur_MSE[x] / (400 + mapped_count[x])
        else:
            cur_MSE[x] = cur_MSE[x] / 400
    cur_MSE['factor'] = factor
    return cur_MSE


for factor in factors:
    context = TaskContext()
    initCountTestToIdeal()
    nextstep = Step(context).process()
    context.factor = factor
    context.display = False
    while True:
        step = WorkflowNextStep.returnNextStep(nextstep, context)
        nextstep = step.process()
        if nextstep == 'Done':
            break
    cur_MSE = find_MSE_change(factor)
    mse_df = mse_df.append(cur_MSE, ignore_index=True)

    new_row = {'x': factor, 'y': len(context.mapping_test_to_ideal)}
    df = df.append(new_row, ignore_index=True)
    new_row = {'factor': factor, '0': context.count_test_to_ideal["0"], '1': context.count_test_to_ideal["1"],
               '2': context.count_test_to_ideal["2"], '3': str(context.count_test_to_ideal["3"])}
    count_df = count_df.append(new_row, ignore_index=True)
    print(new_row)

output_file('output/mapTrainToIdeal.html', title='Mapping training function to ideal function')

fig = figure(title='Mapping factor', plot_height=600, plot_width=600, toolbar_location=None)

# Draw the coordinates as circles
fig.line(x=df['x'],
         y=df['y'],
         color='green', legend='Ideal function')
fig.legend.location = 'bottom_left'
fig.legend.background_fill_color = "white"
fig.legend.background_fill_alpha = 0.3

fig.line(x=count_df["factor"],
         y=count_df["0"],
         color='blue', legend='0 mapped')

fig.line(x=count_df["factor"],
         y=count_df["1"],
         color='red', legend='1 mapped')

fig.line(x=count_df["factor"],
         y=count_df["2"],
         color='orange', legend='2 mapped')

fig.line(x=count_df["factor"],
         y=count_df["3"],
         color='purple', legend='3 mapped')
show(fig)


output_file('output/mse_change.html', title='Mapping training function to ideal function')

fig2 = figure(title='Mapping factor to mse', plot_height=600, plot_width=600, toolbar_location=None)

fig2.line(x=mse_df["factor"],
          y=mse_df["y4"],
          color='blue', legend='y1 MSE trend')

fig2.line(x=mse_df["factor"],
          y=mse_df["y6"],
          color='red', legend='y2 MSE trend')

fig2.line(x=mse_df["factor"],
          y=mse_df["y43"],
          color='orange', legend='y3 MSE trend')

fig2.line(x=mse_df["factor"],
          y=mse_df["y34"],
          color='purple', legend='y4 MSE trend')
show(fig2)
