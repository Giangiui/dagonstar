import json
import time
import os

from dagon import Workflow
from dagon.task import DagonTask, TaskType

workflow = Workflow("English-Writers-Taskflow")

taskA = DagonTask(TaskType.BATCH, "Hemingway", "/bin/hostname > A.txt")
taskB = DagonTask(TaskType.BATCH, "Shakespeare", "/bin/date > B.txt; cat workflow:///Hemingway/A.txt >> B.txt")

workflow.add_task(taskA)
workflow.add_task(taskB)

taskB.add_dependency_to(taskA)

workflow.run()

if workflow.get_dry() is False:
    # set the result filename
    result_filename = taskB.get_scratch_dir() + "/B.txt"
    while not os.path.exists(result_filename):
        time.sleep(1)

    # get the results
    with open(result_filename, "r") as infile:
        result = infile.readlines()
        print(result)