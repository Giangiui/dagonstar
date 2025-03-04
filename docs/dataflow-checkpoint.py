import json
import time
import os

from dagon import Workflow
from dagon.task import DagonTask, TaskType

workflow = Workflow("Italian-Writers")

taskA = DagonTask(TaskType.BATCH, "Pirandello", "gcc /path/to/file/output-random-file.c -o output-random-file; ./output-random-file")
taskCheck = DagonTask(TaskType.CHECKPOINT, "Svevo", "workflow:///Pirandello/output-random-file.txt")
taskB = DagonTask(TaskType.BATCH, "Calvino", "python3 /path/to/file/pow2.py workflow:///Svevo/Italian-Writers/Pirandello/output-random-file.txt > output.txt")

workflow.add_task(taskA)
workflow.add_task(taskCheck)
workflow.add_task(taskB)

taskCheck.add_dependency_to(taskA)
taskB.add_dependency_to(taskCheck)

workflow.run()

if workflow.get_dry() is False:
        # set the result filename
        result_filenameA = taskA.get_scratch_dir() + "/output-random-file.txt"
        while not os.path.exists(result_filenameA):
            time.sleep(1)

        # get the results
        with open(result_filenameA, "r") as infile:
            result = infile.readlines()
            print(result)


        result_filenameB = taskB.get_scratch_dir() + "/output.txt"
        while not os.path.exists(result_filenameB):
            time.sleep(1)
       
        # get the results
        with open(result_filenameB, "r") as infile:
            result = infile.readlines()
            print(result)