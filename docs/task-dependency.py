from dagon import Workflow
from dagon.task import TaskType, DagonTask

workflow = Workflow("Taskflow-Demo")

taskA = DagonTask(TaskType.BATCH, "Hemingway", "/bin/hostnamee")
taskB = DagonTask(TaskType.BATCH, "Shakespeare", "/bin/date")

workflow.add_task(taskA)
workflow.add_task(taskB)

taskB.add_dependency_to(taskA)

workflow.run()