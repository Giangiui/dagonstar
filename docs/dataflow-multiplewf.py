import json
import time
import os

from dagon import Workflow
from dagon.dag_tps import DAG_TPS
from dagon.task import DagonTask, TaskType

workflow_eng = Workflow("English-Writers")
workflow_ita = Workflow("Italian-Writers")

workflow_eng.set_dry(False)  
workflow_ita.set_dry(False)

taskA = DagonTask(TaskType.BATCH, "Shakespeare", "echo 10 > A.txt")
taskB = DagonTask(TaskType.BATCH, "Dante", "cat workflow://English-Writers/Shakespeare/A.txt > B.txt")

workflow_eng.add_task(taskA)
workflow_ita.add_task(taskB)

metaworkflow=DAG_TPS("WritersDAG")
metaworkflow.add_workflow(workflow_eng)
metaworkflow.add_workflow(workflow_ita)
metaworkflow.make_dependencies()
metaworkflow.run()

if workflow_eng.get_dry() is False and workflow_ita.get_dry() is False:
    
    result_filenameC = taskB.get_scratch_dir() + "/B.txt"
    while not os.path.exists(result_filenameC):
        time.sleep(1)

    with open(result_filenameC, "r") as infile:
        result = infile.readlines()
        print(result)
