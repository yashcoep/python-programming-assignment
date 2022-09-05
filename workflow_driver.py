from context import TaskContext
from step import Step
from workflow_next_step import WorkflowNextStep

"""
Context will contains all data needed for a step to execute
"""
context = TaskContext()
nextstep = Step(context).process()

"""
Workflow driver class
Class job is starting point and it will return next step to execute
The order of execution is 
step -> load dataset -> find ideal function -> map test case to ideal -> display result

Any of the above step can throw error step
"""
while True:
    step = WorkflowNextStep.returnNextStep(nextstep,context)
    nextstep = step.process()
    if nextstep == 'Done':
        break
