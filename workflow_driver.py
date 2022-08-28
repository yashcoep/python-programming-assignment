from context import TaskContext
from step import Step
from workflow_next_step import WorkflowNextStep

context = TaskContext()
nextstep = Step(context).process()

while True:
    step = WorkflowNextStep.returnNextStep(nextstep,context)
    nextstep = step.process()
    if nextstep == 'Done':
        break
