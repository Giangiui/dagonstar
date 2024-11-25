import json
import time
import os

from dagon import Workflow
from dagon.task import DagonTask, TaskType

workflow = Workflow("English-Writers-Taskflow")

taskA = DagonTask(TaskType.BATCH, "Hemingway", "echo 10 > A.txt")
taskB = DagonTask(TaskType.BATCH, "Shakespeare", "echo 7 > B.txt")
taskC = DagonTask(TaskType.BATCH, "Orwell", "python3 /home/giangiui/dagonstar/documentation/task/sum.py workflow:///Hemingway/A.txt workflow:///Shakespeare/B.txt > C.txt")

workflow.add_task(taskA)
workflow.add_task(taskB)
workflow.add_task(taskC)

taskC.add_dependency_to(taskA)
taskC.add_dependency_to(taskB)

workflow.run()

if workflow.get_dry() is False:
    # set the result filename
    result_filename = taskC.get_scratch_dir() + "/C.txt"
    while not os.path.exists(result_filename):
        time.sleep(1)

    # get the results    
    with open(result_filename, "r") as infile:
        result = infile.readlines()
        print(result)