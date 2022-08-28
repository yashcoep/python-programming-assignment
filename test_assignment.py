import unittest

from context import TaskContext
from find_ideal_function import FindIdealFunction
from step import Step
from workflow_next_step import WorkflowNextStep


class TestAssignment(unittest.TestCase):
    def test_workflow(self):
        step = WorkflowNextStep.returnNextStep("LoadDataset", None)
        self.assertIsNotNone(step)

        step = WorkflowNextStep.returnNextStep("FindIdealFunction", None)
        self.assertIsInstance(step, FindIdealFunction)

    def test_load_dataset(self):
        context = TaskContext()
        nextstep = Step(context).process()
        while True:
            step = WorkflowNextStep.returnNextStep(nextstep, context)
            nextstep = step.process()
            if nextstep == 'Done':
                break

        self.assertTrue(len(context.mapping_train_to_ideal) == 4)
        self.assertFalse(context.ideal_df.empty)
        self.assertFalse(context.train_df.empty)
        self.assertFalse(context.test_df.empty)
        self.assertTrue(len(context.mapping_test_to_ideal) != 0)


if __name__ == '__main__':
    unittest.main()
