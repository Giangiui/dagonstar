from dagon import Workflow
from dagon.task import TaskType, DagonTask

workflow = Workflow("English-Writers-Taskflow")

workflow.set_dry(False)

taskA = DagonTask(TaskType.BATCH, "Hemingway", "/bin/hostname")
taskB = DagonTask(TaskType.BATCH, "Shakespeare", "/bin/date")

workflow.add_task(taskA)
workflow.add_task(taskB)

workflow.run()