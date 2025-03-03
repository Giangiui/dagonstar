from dagon import Workflow
from dagon.task import TaskType, DagonTask

workflow = Workflow("Taskflow-Demo")

workflow.set_dry(True)

taskA = DagonTask(TaskType.BATCH, "Hemingway", "/bin/hostname")
taskB = DagonTask(TaskType.BATCH, "Shakespeare", "/bin/date")
taskC = DagonTask(TaskType.BATCH, "Orwell", "/usr/bin/uptime")


workflow.add_task(taskA)
workflow.add_task(taskB)
workflow.add_task(taskC) 

taskA.add_dependency_to(taskB)
taskB.add_dependency_to(taskC)
taskC.add_dependency_to(taskA)

workflow.make_dependencies()

workflow.run()
