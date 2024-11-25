import json
import time
import os

from dagon import Workflow
from dagon.dag_tps import DAG_TPS
from dagon.task import DagonTask, TaskType

workflow = Workflow("English-Writers-Taskflow")
workflow2 = Workflow("Italian-Writers-Taskflow")

workflow.set_dry(False)  

taskA = DagonTask(TaskType.BATCH, "Hemingway", "echo 10 > A.txt")
taskB = DagonTask(TaskType.BATCH, "Orwell", "workflow://Italian-Writers-Taskflow/Hemingway/A.txt > B.txt")

workflow.add_task(taskA)
workflow.add_task(taskB)

taskB.add_dependency_to(taskA)

metaworkflow=DAG_TPS("WritersDAG")
metaworkflow.add_workflow(workflow)
metaworkflow.add_workflow(workflow2)
metaworkflow.make_dependencies()

metaworkflow.run()

if workflow.get_dry() is False:
    
    result_filenameC = taskB.get_scratch_dir() + "/B.txt"
    while not os.path.exists(result_filenameC):
        time.sleep(1)

    with open(result_filenameC, "r") as infile:
        result = infile.readlines()
        print(result)