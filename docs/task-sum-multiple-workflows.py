import json
import time
import os

from dagon import Workflow
from dagon.dag_tps import DAG_TPS
from dagon.task import DagonTask, TaskType

workflow = Workflow("English-Writers")
workflow2 = Workflow("Italian-Writers")
workflow3 = Workflow("French-Writers")

workflow.set_dry(False)  

taskA = DagonTask(TaskType.BATCH, "Hemingway", "echo 10 > A.txt")
taskB = DagonTask(TaskType.BATCH, "Shakespeare", "echo 7 > B.txt")
taskC = DagonTask(TaskType.BATCH, "Orwell", "python3 /path/to/folder/sum_from_file.py workflow:///Hemingway/A.txt workflow:///Shakespeare/B.txt > C.txt")

taskD = DagonTask(TaskType.BATCH, "Dante", "gcc /path/to/folder/random_number.c -o random_number; ./random_number > D.txt")

taskE = DagonTask(TaskType.BATCH, "Perec", "rustc /path/to/folder/sum_rust.rc; ./sum_rust workflow://English-Writers/Orwell/C.txt workflow://Italian-Writers/Dante/D.txt > E.txt")

workflow.add_task(taskA)
workflow.add_task(taskB)
workflow.add_task(taskC)
workflow2.add_task(taskD)
workflow3.add_task(taskE)

taskC.add_dependency_to(taskA)
taskC.add_dependency_to(taskB)

metaworkflow=DAG_TPS("WritersDAG")
metaworkflow.add_workflow(workflow)
metaworkflow.add_workflow(workflow2)
metaworkflow.add_workflow(workflow3)
metaworkflow.make_dependencies()

metaworkflow.run()

if workflow.get_dry() is False:
    
    result_filenameC = taskC.get_scratch_dir() + "/C.txt"
    result_filenameD = taskD.get_scratch_dir() + "/D.txt"
    result_filenameE = taskE.get_scratch_dir() + "/E.txt"

    while not os.path.exists(result_filenameC) and not os.path.exists(result_filenameD) and not os.path.exists(result_filenameE):
        time.sleep(1)

    with open(result_filenameC, "r") as infile:
        result = infile.readlines()
        print(result)
    
    with open(result_filenameD, "r") as infile:
        result = infile.readlines()
        print(result)
    
    with open(result_filenameE, "r") as infile:
        result = infile.readlines()
        print(result)
    
