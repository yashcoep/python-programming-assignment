from display_plot_bokeh import DisplayDataBokeh
from error_handle_step import ErrorStep
from find_ideal_function import FindIdealFunction
from load_dataset import LoadDataset
from map_test_to_ideal_function import MapTestDataToIdealFunction


class WorkflowNextStep:
    @staticmethod
    def returnNextStep(curStep, context):
        if curStep == "LoadDataset":
            return LoadDataset(context)

        if curStep == "FindIdealFunction":
            return FindIdealFunction(context)

        if curStep == "MapTestDataToIdealFunction":
            return MapTestDataToIdealFunction(context)

        if curStep == "DisplayDataBokeh":
            return DisplayDataBokeh(context)

        if curStep == "ErrorStep":
            return ErrorStep(context)
