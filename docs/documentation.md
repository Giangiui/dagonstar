# Data

virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$PWD:$PYTHONPATH




## Task

DAGonStar can execute multiple tasks simultaneously and define dependencies between tasks.

As a first example, let's define a simple Python code that executes two simple tasks. These tasks launch two bash commands.

```python
from dagon import Workflow
from dagon.task import TaskType, DagonTask

workflow = Workflow("English-Writers")

taskA = DagonTask(TaskType.BATCH, "Hemingway", "/bin/hostname")
taskB = DagonTask(TaskType.BATCH, "Shakespeare", "/bin/date")

workflow.add_task(taskA)
workflow.add_task(taskB)

workflow.run()
```

> task-demo.py



As can be seen above, to create a new code with DAGonStar, it is mandatory to import this library. 

```python
from dagon import Workflow
from dagon.task import TaskType, DagonTask
```



For correct execution of the code, it is necessary to define a Workflow. 

```python
workflow = Workflow("English-Writers")
```

A Workflow for DAGonStar represents a directed acyclic graph and a set of tasks that must be executed simultaneously.



Now can define tasks. In this example define tasks *Hemingway* and *Shakespeare*, which execute two commands. 

```python
taskA = DagonTask(TaskType.BATCH, "Hemingway", "/bin/hostname")
taskB = DagonTask(TaskType.BATCH, "Shakespeare", "/bin/date")
```

For this example tasks has batch type. With this definition can execute regular bash commands, for example `/bin/hostname` and `/bin/date`



After definition of workflow and tasks can launch add_task for every definition of tasks, for insert them into specific workflow.

```python
workflow.add_task(taskA)
workflow.add_task(taskB)
```



For DAGonStar a single task representing a vertices of the graph. 



Workflow is correctly configured, now with command `.run()` can execute all the tasks into them.

```python
workflow.run()
```



This is the results of the execution. 

```bash
2024-10-23 10:36:59,001 root         INFO     Workflow 'English-Writers' completed in 2.8947041034698486 seconds ---
```



## Dry 

If you want more information about execution of every single code you can set dry variable.

```python
workflow.set_dry(False)
```



`set_dry(False)` return execution time or exception to every single code run into workflow.

```bash
2024-10-29 09:50:42,200 root         DEBUG    Hemingway Completed in 0.003662109375 seconds ---
DRY
2024-10-29 09:50:42,544 root         DEBUG    Shakespeare Completed in 0.00331878662109375 seconds ---
```

 

For default dry variable is set to False. 



## Dependency

With this example you can see a simple tasks workflow. However, with this configuration, the tasks run independently of each other. 

To enforce dependency between tasks, you can use the command `add_dependency_to()`. 

```python
taskB.add_dependency_to(taskA)
```



With this command, taskB strictly depends on taskA and its execution. Until taskA finishes running, taskB will not start and its status will remain 'waiting'.

In graph terms this command defines an edge, creating a link between two vertices.

```python
from dagon import Workflow
from dagon.task import TaskType, DagonTask

workflow = Workflow("English-Writers")

taskA = DagonTask(TaskType.BATCH, "Hemingway", "/bin/hostname")
taskB = DagonTask(TaskType.BATCH, "Shakespeare", "/bin/date")

workflow.add_task(taskA)
workflow.add_task(taskB)

taskB.add_dependency_to(taskA)

workflow.run()
```

> task-dependency.py



Shakespeare's task is waiting the end of execution of the Hemingway's task. If Shakespeare's task ends correctly, Hemingway's task begins.

```bash
2024-10-31 09:29:31,386 root         DEBUG    Running workflow: English-Writers
2024-10-31 09:29:31,392 root         DEBUG    Hemingway: Status.WAITING
2024-10-31 09:29:31,393 root         DEBUG    Hemingway: Status.RUNNING
2024-10-31 09:29:31,393 root         DEBUG    Hemingway: Executing...
2024-10-31 09:29:31,393 root         DEBUG    Shakespeare: Status.WAITING
2024-10-31 09:29:31,394 root         DEBUG    Hemingway: Scratch directory: /tmp//1730363371394-Hemingway
DRY
2024-10-31 09:29:32,288 root         DEBUG    Hemingway Completed in 0.006635427474975586 seconds ---
2024-10-31 09:29:34,291 root         DEBUG    Hemingway: Status.FINISHED
2024-10-31 09:29:34,291 root         DEBUG    Shakespeare: Status.RUNNING
2024-10-31 09:29:34,291 root         DEBUG    Shakespeare: Executing...
2024-10-31 09:29:34,292 root         DEBUG    Shakespeare: Scratch directory: /tmp//1730363374292-Shakespeare
DRY
2024-10-31 09:29:34,737 root         DEBUG    Shakespeare Completed in 0.003768444061279297 seconds ---
2024-10-31 09:29:36,739 root         DEBUG    Shakespeare: Status.FINISHED
2024-10-31 09:29:36,739 root         INFO     Workflow 'English-Writers' completed in 5.353054523468018 seconds ---
```



DAGonStar doesn't check for the existence of a task's necessary dependencies and doesn't stop the execution if tasks don't have the necessary data for correct execution. It is necessary to verify the correct execution of tasks and the presence of dependencies before launching the code.



## Loop

In the previous chapter we can see the `add_dependency_to` command and how it works. 

Expand the previous example and introduce a new task and new dependencies.



```python
from dagon import Workflow
from dagon.task import TaskType, DagonTask

workflow = Workflow("English-Writers")

taskA = DagonTask(TaskType.BATCH, "Hemingway", "/bin/hostname")
taskB = DagonTask(TaskType.BATCH, "Shakespeare", "/bin/date")
taskC = DagonTask(TaskType.BATCH, "Orwell", "/usr/bin/uptime")

workflow.add_task(taskA)
workflow.add_task(taskB)
workflow.add_task(taskC) 

taskA.add_dependency_to(taskB)
taskB.add_dependency_to(taskC)
taskC.add_dependency_to(taskA)

workflow.run()
```



This is the result of the execution. 

```bash
2024-10-29 10:37:23,931 root         DEBUG    Running workflow: English-Writers
2024-10-29 10:37:23,932 root         DEBUG    Hemingway: Status.WAITING
2024-10-29 10:37:23,933 root         DEBUG    Shakespeare: Status.WAITING
2024-10-29 10:37:23,934 root         DEBUG    Orwell: Status.WAITING
```

In this particularly case //





To solve the problem we can use the `make_dependencies()` command. 

```python
workflow.make_dependencies()
```

This command can individuate graph's loop and resolve or report them. 

By adding this command to the previous example code, we achieve loop resolution and ensure the correct execution of tasks within the workflow.

```python
from dagon import Workflow
from dagon.task import TaskType, DagonTask

workflow = Workflow("English-Writers")

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
```

> task-loop.py



In fact, by running the code, we would obtain this result.

```bash
2024-10-29 11:17:03,747 root         DEBUG    Running workflow: English-Writers
2024-10-29 11:17:03,749 root         DEBUG    Hemingway: Status.WAITING
2024-10-29 11:17:03,749 root         DEBUG    Hemingway: Status.RUNNING
2024-10-29 11:17:03,749 root         DEBUG    Shakespeare: Status.WAITING
2024-10-29 11:17:03,749 root         DEBUG    Hemingway: Executing...
2024-10-29 11:17:03,750 root         DEBUG    Shakespeare: Status.RUNNING
2024-10-29 11:17:03,750 root         DEBUG    Orwell: Status.WAITING
2024-10-29 11:17:03,752 root         DEBUG    Shakespeare: Executing...
2024-10-29 11:17:03,752 root         DEBUG    Orwell: Status.RUNNING
2024-10-29 11:17:03,754 root         DEBUG    Orwell: Executing...
2024-10-29 11:17:03,759 root         DEBUG    Hemingway: Scratch directory: /tmp//1730197023752-Hemingway
2024-10-29 11:17:03,760 root         DEBUG    Orwell: Scratch directory: /tmp//1730197023755-Orwell
2024-10-29 11:17:03,764 root         DEBUG    Shakespeare: Scratch directory: /tmp//1730197023753-Shakespeare
2024-10-29 11:17:06,405 root         DEBUG    Orwell: Status.FINISHED
2024-10-29 11:17:06,442 root         DEBUG    Hemingway: Status.FINISHED
2024-10-29 11:17:06,496 root         DEBUG    Shakespeare: Status.FINISHED
2024-10-29 11:17:06,497 root         INFO     Workflow 'English-Writers' completed in 2.749276876449585 seconds ---
```





## SCHEMA

in `_init_.py` file there is a SCHEMA variable. 

```python
 SCHEMA = "workflow://"
```

This variable define a space that tasks can use to save data and communicate for each other. 



```python
import json
import time
import os

from dagon import Workflow
from dagon.task import DagonTask, TaskType

workflow = Workflow("English-Writers")

taskA = DagonTask(TaskType.BATCH, "Hemingway", "/bin/hostname > A.txt")
taskB = DagonTask(TaskType.BATCH, "Shakespeare", "/bin/date > B.txt; cat workflow:///Hemingway/A.txt >> B.txt")

workflow.add_task(taskA)
workflow.add_task(taskB)

taskB.add_dependency_to(taskA)

workflow.run()
```

> task-folderworkflow.py



In this example define two tasks, Hemingway and Shakespeare. 

Shakespeare, for concatenate the result and create an output, takes the result of Hemingway at `workflow:///Hemingway/A.txt`, file define by Hemingway task. 



The output, saved in `B.txt` file, can be print after the workflow execution. 

```python
if workflow.get_dry() is False:
    # set the result filename
    result_filename = taskB.get_scratch_dir() + "/B.txt"
    while not os.path.exists(result_filename):
        time.sleep(1)

    # get the results
    with open(result_filename, "r") as infile:
        result = infile.readlines()
        print(result)
```



This is the result. 

```bash
['Tue Nov  5 11:12:35 CET 2024\n', 'DESKTOP-O1T2OFK\n']
```



### sum.py

Now we want to run this simple Python code. 

```python
import sys

x = open(sys.argv[1],'r')
y = open(sys.argv[2],'r')

z = int(x.read()) + int(y.read())

exit(z)
```

> sum_from_file.py



`sum_from_file.py` open two files, read file names passed by command line, read the numbers into files and sum them. 



We can run a Python (or another language script) declare explicitly the bash command for running (and compiling). 

```python
import json
import time
import os

from dagon import Workflow
from dagon.task import DagonTask, TaskType

workflow = Workflow("English-Writers")

taskA = DagonTask(TaskType.BATCH, "Hemingway", "echo 10 > A.txt")
taskB = DagonTask(TaskType.BATCH, "Shakespeare", "echo 7 > B.txt")
taskC = DagonTask(TaskType.BATCH, "Orwell", "python3 path/to/file/sum_from_file.py workflow:///Hemingway/A.txt workflow:///Shakespeare/B.txt > C.txt")

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
```

> task-sum.py



*Hemingway* and *Shakespeare* prints two numbers, 10 and 7, and save them into `A.txt` and `B.txt` files.

*Orwell* run `sum_from_file.py` and catch file name // and save the result into `C.txt`.



In the end `task-sum.py` print sum result. 

```bash
['17\n']
```



## JSON

DAGonStar can export and import JSON file, for //



### Export JSON 

After declaring the tasks and adding them to the workflow, you can export the graph's structure in JSON file with the command `workflow.as_json().`

```python
json = workflow.as_json()
```



`workflow.as_json()` command saves workflow's name, task names, task types, commands and dependencies into a `json` variable.

```json
{
  "host": "localhost",
  "id": 0,
  "name": "English-Writers",
  "tasks": {
    "Hemingway": {
      "command": "echo 10 > A.txt",
      "name": "Hemingway",
      "nexts": [
        "Orwell"
      ],
      "prevs": [],
      "status": "READY",
      "type": "batch",
      "working_dir": null
    },
    "Orwell": {
      "command": "python3 /path/to/file/sum_from_file.py workflow:///Hemingway/A.txt workflow:///Shakespeare/B.txt > C.txt",
      "name": "Orwell",
      "nexts": [],
      "prevs": [
        "Hemingway",
        "Shakespeare"
      ],
      "status": "READY",
      "type": "batch",
      "working_dir": null
    },
    "Shakespeare": {
      "command": "echo 7 > B.txt",
      "name": "Shakespeare",
      "nexts": [
        "Orwell"
      ],
      "prevs": [],
      "status": "READY",
      "type": "batch",
      "working_dir": null
    }
  }
}
```

> english-writers.json



With the command below you can export workflow's structure and tasks into a file. This allows you to import an entire workflow without having to declare the tasks again. 

```python
with open('english-writers.json', 'w') as outfile:
    stringWorkflow = json.dumps(jsonWorkflow, sort_keys=True, indent=2)
    outfile.write(stringWorkflow)
```



### Import JSON 

DAGonStar supports loading external JSON files to import tasks and workflows using the `load_json("/path/to/file")` command. 

```python
import json
import time
import os

from dagon import Workflow
from dagon.task import DagonTask, TaskType

workflow = Workflow("LoadJSON")

workflow.set_dry(True)

workflow.load_json("english-writers.json")
    
workflow.run()
```

> task-loadJSON.py



`task-loadJSON.py` loads *english-writers.json*, the file that was previously generated by the export in the previous example. 

After the import, you can run the workflow without any other declaration. 

```bash
2024-11-07 11:19:57,839 root         DEBUG    Running workflow: English-Writers
2024-11-07 11:19:57,839 root         DEBUG    Hemingway: Status.WAITING
2024-11-07 11:19:57,839 root         DEBUG    Hemingway: Status.RUNNING
2024-11-07 11:19:57,840 root         DEBUG    Hemingway: Executing...
2024-11-07 11:19:57,840 root         DEBUG    Shakespeare: Status.WAITING
2024-11-07 11:19:57,840 root         DEBUG    Shakespeare: Status.RUNNING
2024-11-07 11:19:57,840 root         DEBUG    Orwell: Status.WAITING
2024-11-07 11:19:57,841 root         DEBUG    Shakespeare: Executing...
2024-11-07 11:19:57,841 root         DEBUG    Hemingway: Scratch directory: /tmp//1730974797840-Hemingway
2024-11-07 11:19:57,842 root         DEBUG    Shakespeare: Scratch directory: /tmp//1730974797842-Shakespeare
2024-11-07 11:19:58,263 root         DEBUG    Shakespeare Completed in 0.004199981689453125 seconds ---
2024-11-07 11:19:58,396 root         DEBUG    Hemingway Completed in 0.0049097537994384766 seconds ---
2024-11-07 11:20:00,273 root         DEBUG    Shakespeare: Status.FINISHED
2024-11-07 11:20:00,399 root         DEBUG    Hemingway: Status.FINISHED
2024-11-07 11:20:00,400 root         DEBUG    Orwell: Status.RUNNING
2024-11-07 11:20:00,400 root         DEBUG    Orwell: Executing...
2024-11-07 11:20:00,401 root         DEBUG    Orwell: Scratch directory: /tmp//1730974800401-Orwell
2024-11-07 11:20:00,942 root         DEBUG    Orwell Completed in 0.03068852424621582 seconds ---
2024-11-07 11:20:02,952 root         DEBUG    Orwell: Status.FINISHED
2024-11-07 11:20:02,952 root         INFO     Workflow 'English-Writers' completed in 5.113301515579224 seconds
```

> task-loadJSON.py execution 



## Multiple Workflows

DAGonStar allows multiple workflows to split tasks, organize them, and manage their dependencies.

The declaration of workflows and tasks remains the same, but if you want to combine two or more workflows you can use `DAG_TPS()`.

```python
metaWorkflow=DAG_TPS("WritersDAG")
```

`DAG_TPS()` create a meta workflow, a workflow of workflows. 

With `add_workflow()` you can add workflows into `metaWorkflow`.

```python
metaWorkflow.add_workflow(workflow1)
metaWorkflow.add_workflow(workflow2)
```

Now we can treat metaWorkflow like a simple workflow. 

```python
metaWorkflow.make_dependencies()
metaWorkflow.run()
```



In `task-multiple-workflow.py` declare two workflows, *English-Writers* and *Italian-Writers*.

*taskA* in *English-Writers* save a number into *A.txt*, *taskB* in *Italian-Writers* cat *A.txt* and put the number into *B.txt*.

```python
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
```

> task-multiple-workflows.py



*Dante* can read the *Shakespeare* file result because he can access to *Shakespeare*'s folder result.

*Dante* can read *A.txt* with the command *workflow://English-Writers/Shakespeare/A.txt*, where *English-Writers* is the name of the workflow, *Shakespeare* is the name of the task and *A.txt* is the file generated as output.



### task-sum-multiple-workflows

In this example, we want to declare three workflows. Two workflows return a number, the third one takes the output numbers and adds them together.

We declare the *English-Writers* workflow, which performs the same operations declared in *task-sum.py*.



The *Italian-Writers* workflow contains a single task, *Dante*. 

```python
taskD = DagonTask(TaskType.BATCH, "Dante", "gcc /path/to/file/random_number.c -o random_number; ./random_number > D.txt")
```

This task compiles and executes a .c file, which generates a random number from 1 to 99. 

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    srand(time(NULL));
    int random_number = rand() % 100 + 1;
    return random_number;
}
```

> random_number.c

The result is exported into *D.txt* file. 



The *French-Writers* workflow contains a task named *Perec*. 

```python
taskE = DagonTask(TaskType.BATCH, "Perec", "rustc /path/to/file/sum_rust.rc; ./sum_rust workflow://English-Writers/Orwell/C.txt workflow://Italian-Writers/Dante/D.txt > E.txt")
```

This task compiles *sum_rust.rc* and executes it by passing the filenames `workflow://English-Writers/Orwell/C.txt` and `workflow://Italian-Writers/Dante/D.txt`, which contain the results of the *English-Writers* and *Italian-Writers* executions, via the command line.

*sum_rust.rc* reads numbers from the files and sums them. 

```rust
use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {

    let args: Vec<String> = env::args().collect();

    let file_path1 = &args[1];
    let file_path2 = &args[2];
    
    let num1 = match read_number_from_file(file_path1) {
        Ok(number) => number,
        Err(_e) => std::process::exit(0),
    };

    let num2 = match read_number_from_file(file_path2) {
        Ok(number) => number,
        Err(_e) => std::process::exit(0),
    };

    println!("{}", num1+num2);
}

fn read_number_from_file<P>(filename: P) -> io::Result<i32>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    let mut lines = io::BufReader::new(file).lines();
    if let Some(Ok(line)) = lines.next() {
        return line.trim().parse().map_err(|e| io::Error::new(io::ErrorKind::InvalidData, e));
    }
    Err(io::Error::new(io::ErrorKind::UnexpectedEof, "File is empty"))
}

```

> sum_rust.rc



The result of the execution is three numbers: the first and second are the result of a sum in *English-Writers* and a random number in *Italian-Writers*. The third is the sum of these two numbers.

```bash
['17\n']
['4']
['21\n']
```



*task-sum-multiple-workflows.py*  //

```python
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
taskC = DagonTask(TaskType.BATCH, "Orwell", "python3 /path/to/file/sum_from_file.py workflow:///Hemingway/A.txt workflow:///Shakespeare/B.txt > C.txt")

taskD = DagonTask(TaskType.BATCH, "Dante", "gcc /path/to/file/random_number.c -o random_number; ./random_number > D.txt")

taskE = DagonTask(TaskType.BATCH, "Perec", "rustc /path/to/file/sum_rust.rc; ./sum_rust workflow://English-Writers/Orwell/C.txt workflow://Italian-Writers/Dante/D.txt > E.txt")

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
    
```

> task-sum-multiple-workflows.py



## Checkpoint

DAGonStar has an internal checkpoint system, but it also provides the possibility to declare an external checkpoint if you want to explicitly check the existence of the task's result file (and his correct execution).

To declare an explicit checkpoint, you must declare with `TaskType.CHECKPOINT`.

```python
taskCheck = DagonTask(TaskType.CHECKPOINT, "Checkpoint", "workflow:///Task_Name/output_file")
```



Now, to access to the checkpoint file, we need to use a path like `workflow:///Checkpoint/Workflow/Task/file.txt`.



```python
task = DagonTask(TaskType.BATCH, "Task", "cat workflow:///Svevo/Italian-Writers/Pirandello/file.txt >> output.txt")
```

In this example *Svevo* is the name of the checkpoint, *Italian-Writers* is the name of the workflow and *Pirandello* is the name of the task. 

It is still possible to refer to the original output file of the task after the checkpoint execution.



### task-checkpoint

In this example, we declare a new C program called `output-random-file.c`. 

This code generates a random number from 1 to 100 and saves it into a file called `output-file.txt`.

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

int main() {
  FILE *fptr;

  fptr = fopen("output-file.txt", "w");

  srand(time(NULL));
  int random_number = rand() % 100 + 1;
  
  if (fptr) {
        fprintf(fptr, "%d", random_number);
        fclose(fptr);
    }

  return 0;
}
```

> output-random-file.c



Declare a `pow2.py` script, which reads a number from a file and squares it.

```python
import sys
import math

x = open(sys.argv[1],'r')

print(math.pow(int(x.read()), 2))
```

> pow2.py



In `task-checkpoint.py` declare three tasks. 

1. *Pirandello*: Compiles and runs `output-random-file.c`, which produces a file with a random number. 
2. *Svevo:* An explicit checkpoint task that backs up `output-random-file.txt`, the result from `output-random-file.c` and saves it into an equivalent file.   
3. *Calvino*: Takes the result file of *Pirandello* from the *Svevo* checkpoint and processes it with *pow2.py*.



```python
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
```

> task-checkpoint.py



```bash
['8']
['64.0\n']
```

> Results



## Transversal Workflow

Dagon has the property of transversality, allowing you to create dependencies in workflows on existing workflows, whether they are currently executing or have already ended. This property also allows you to build workflows from workflows for joint execution.



### Requirements

To use the transversality property of DagOnStar, it is necessary to use [DagOnService](https://github.com/DagOnStar/DagOnService/).

DagOnService is an advanced solution for workflow registration and remote monitoring, designed to operate on Docker. To utilize this service, it needs to be run within a Docker container using Docker-compose.

To run the service, execute the following command in the root folder:

```bash
docker-compose up --build 
```



After executing the launch command, you can verify the status of the code by using the check command: 

```bash
http://localhost:57000/check
```

```bash
{
    "status": "ok"
}
```



### dagon.ini

The `dagon.ini` file serves as the primary configuration file for DagOnStar.



To utilize DagOnService, open the `dagon.ini` file and, in the dagon_service section, enter the IP address (or DNS name) of the host computer where the DagOn service is running and set the use parameter to True.

```ini
[dagon_service]
route = http://localhost:57000
use = True 

[ftp_pub]
ip = localhost

[dagon_ip]
ip = localhost

[batch]
scratch_dir_base=/tmp/
remove_dir=False
threads=1

[slurm]
partition=

[ec2]
key=AKIAJHPEAY3YIIDMG2NQ
secret=
region=

[digitalocean]
key=

[gce]
key=
secret=
project=

[loggers]
keys=root

[handlers]
keys=stream_handler

[formatters]
keys=formatter

[logger_root]
level=DEBUG
handlers=stream_handler

[handler_stream_handler]
class=StreamHandler
level=DEBUG
formatter=formatter
args=(sys.stderr,)

[formatter_formatter]
format=%(asctime)s %(name)-12s %(levelname)-8s %(message)s
```



If DagOnService and `dagon.ini` configured properly, there should be a workflow registration message before a workflow is executed.

```shell
2025-01-07 11:42:33,703 root         DEBUG    Workflow registration success id = 677d051947f7f78657b0582a
```



It's recommended to set `remove_dir`, under batch section, to `False`. 

If preferred, you can change the default `scratch_dir_base` to another directory, such as `/home/$USER/DagOnStar/tmp/`. This is the directory where all the results will be stored.



### DagOnService 

DagOnService offers multiple commands that allow you to view, manage, and delete workflows.

Using the list command, you can view all workflows that have been executed and registered within DagOnService:

```bash
http://localhost:57000/list
```

```json
[
    {
        "creation_at": "2025-01-07 10:42:33",
        "host": "localhost",
        "id": "677d051947f7f78657b0582a",
        "name": "English-Writers-Taskflow",
        "subscribers": [],
        "tasks": {
            "Hemingway": {
                "command": "/bin/hostname",
                "history": [
                    {
                        "datetime": "2025-01-07 10:42:33",
                        "status": "READY"
                    }
                ],
                "name": "Hemingway",
                "nexts": [],
                "prevs": [],
                "status": "FINISHED",
                "type": "batch",
                "working_dir": "/tmp//1736246553737-Hemingway"
            },
            "Shakespeare": {
                "command": "/bin/date",
                "history": [
                    {
                        "datetime": "2025-01-07 10:42:33",
                        "status": "READY"
                    }
                ],
                "name": "Shakespeare",
                "nexts": [],
                "prevs": [],
                "status": "FINISHED",
                "type": "batch",
                "working_dir": "/tmp//1736246553737-Shakespeare"
            }
        }
    }
]
```

> Results from the list command following the execution of task-demo.py



To view the tasks of a specific workflow, you can use the address service command followed by the workflow ID.

```bash
http://localhost:57000/<workflow_id>
```



To remove an entire workflow from DagOnService, simply use the delete command followed by the workflow ID.

```bash
http://localhost:57000/delete/<workflow_id>
```



### Asynchronous dependency

Once everything is set up correctly, you can take advantage of DagOnStar's transversality.

With DagOnService, you can initiate a workflow and, upon its completion, start another workflow that requires data from the previous one.



#### WF-pow.py

`WF1-pow.py` obtain a number and produce it as output.

```python
import json
import time
import os

from dagon import Workflow
from dagon.task import DagonTask, TaskType

# Create Workflow
workflowI = Workflow("Italian-Writers")

# Set the dry
workflowI.set_dry(False)

# Declare taskA
taskA = DagonTask(TaskType.BATCH, "Pirandello", "mkdir output;echo 7 > output/f1.txt")

#Add task to WorkflowI
workflowI.add_task(taskA)

workflowI.make_dependencies()

workflowI.run()
```

> WF1-pow.py



`Italian-Writers` is registered in the DagOnService and can be consulted by other workflows. To test this, we can run a second workflow with a dependency on the first.

`WF2-pow.py` take the output number from `WF1-pow.py` as input and raise it to a power.

```python
import json
import time
import os

from dagon import Workflow
from dagon.task import DagonTask, TaskType

# Create the orchestration workflow
workflowE = Workflow("English-Writers")

# Set the dry
workflowE.set_dry(False)
    
taskB = DagonTask(TaskType.BATCH, "Woolf", "python3 /path/to/file/pow2.py workflow://Italian-Writers/Pirandello/output/f1.txt >> f2.txt")

workflowE.add_task(task)

workflowE.make_dependencies()

workflowE.run()
    
if workflowE.get_dry() is False:
    # set the result filename
    result_filename = taskB.get_scratch_dir() + "/f2.txt"
    while not os.path.exists(result_filename):
        time.sleep(1)

    # get the results
    with open(result_filename, "r") as infile:
        result = infile.readlines()
        print(result)

```

> WF2-pow.py



It's mandatory, in the workflow that have requirements from another workflow, use the instruction `make_dependencies()`.



#### Run-time dependency 

In the previous example, `WF1-pow.py` and `WF2-pow.py` run asynchronously, but with DagOnService support, a workflow can retrieve a task from another workflow at runtime and wait for it to complete.

In the `WF1-pow.py` example above, add a pause to the Pirandello task declaration. With this change, the Pirandello task will complete its execution after about 30 seconds.

```python
taskA = DagonTask(TaskType.BATCH, "Pirandello", "mkdir output;echo 7 > output/f1.txt; sleep 30")	
```



While the previous workflow is still running, run the ``WF2-pow.py`` file.

Woolf task that has dependency from Pirandello task in WF1-, waiting for its completion.

```python
2025-01-16 10:27:00,856 root         DEBUG    Woolf: Status.WAITING
```



Once the Pirandello tasks of the `WF1-pow-wait.py` workflow have finished, the `WF2-pow-wait.py` workflow will continue its execution.

```bash
2025-01-16 10:27:06,875 root         DEBUG    Pirandello Completed in 31.989572048187256 seconds ---
2025-01-16 10:27:08,878 root         DEBUG    Pirandello: Status.FINISHED
2025-01-16 10:27:08,886 root         INFO     Workflow 'Italian-Writers' completed in 34.78531789779663 seconds ---
```

> WF1-pow.py ending status



```bash
2025-01-16 10:27:09,582 root         DEBUG    Woolf Completed in 0.031539201736450195 seconds ---
2025-01-16 10:27:11,583 root         DEBUG    Woolf: Status.FINISHED
2025-01-16 10:27:11,590 root         INFO     Workflow 'English-Writers' completed in 30.706148386001587 seconds --- 
```

> WF2-pow.py ending status



## Connection

Dagonstar gives the ability to perform tasks on a remote machine using different technologies. 

//





### SSH 

//

#### Pre-configuration

1. **Create an SSH key pair**

   To get started, you need to generate an SSH key pair on your local machine. Open a terminal and run the following command:

   ```bash
   ssh-keygen -t rsa -b 2048
   ```

   This will generate a public key (usually called `id_rsa.pub`) and a private key (usually called `id_rsa`) in the `~/.ssh` directory.

   

2. **Copy the Public Key to the Server**
   Now you'll need to copy the public key to the server you want to access. You can use the `ssh-copy-id` command to do this. Replace `username` and `server_ip` with your own:

   ```bash
   ssh-copy-id username@server_ip
   ```

   This command will prompt you for the server password and then copy your public key to the server's `~/.ssh/authorized_keys` file.

   

3. **Test the Key-Based Authentication**
   Try to SSH into the server without a password to test if the key-based authentication is working:

   ```bash
   ssh username@server_ip
   ```

   If everything is set up correctly, you should be able to log in without entering a password.

   Now you have successfully set up SSH access to your server without a password, using a key pair for authentication. Make sure to keep your private key safe on your local machine, and don't share it with anyone.

   

#### SSH Task

After preconfiguration, you can add a task to the workflow that can access the remote machine. 

To do this you can add a task like this:

```python
taskA = DagonTask(TaskType.BATCH, "A", "mkdir output;hostname > output/f1.txt", ip="", ssh_username="", keypath="")
```



After declaring the instructions add a three new parameters: `ip` is the ip of the server, `ssh_username` is the username with which to access the server and `keypath` is the *id_rsa* previously generated. 



> [!WARNING]
> By now, the stager only supports the movement of data between remote machines or from a remote machine to a local machine. We are working on enable the stage in of data from a remote machine to a local machine.



### Cloud Task


DagOnStar supports the deployments on the following Cloud Providers:


* Google Cloud
* Amazon EC2
* DigitalOcean




#### Pre-configuration

Depending on the cloud provider, different access tokens and keys may be required. Please refer to the provider's documentation to obtain the access tokens. 

For example, to work with EC2 you need a temporary key and a secret token. These keys have to be added to the `dagon.ini` as follows:


```conf
[ec2]
key=<my_key>
secret=<my_secret>
region=<ec2_region>
```



#### EC2 task

The ``dataflow-demo-cloud.py`` file executes a workflow composed of two tasks deployed on two virtual machines on EC2. 

The properties of the EC2 instances are configured using a dictionary, as follows:


```python
ec2_flavour = {"image": "ami-0fc5d935ebf8bc3bc", "size": "t1.micro"}
```



The ```image``` value is the ID of a valid Amazon Machine Image. To find the ID of an AMI, simply go to the AWS console and browse the AMI Catalog. 

The ID of the image is available under the name of the AMI.


The ```size``` value refers to the instance type of your virtual machine. A complete list of instance types can be found at  [https://aws.amazon.com/ec2/instance-types/](https://aws.amazon.com/ec2/instance-types/).


Next, we need to specify the SSH parameters to enable the communication between the DagOnStar engine and the virtual machines. You can create a new SSH key or choose an existing one, previously loaded on the platform of your cloud provider's platform.

To create a new key, declare a dictionary as follows:


```python
ssh_key_ec2 = {"option": cm.KeyOptions.CREATE, "key_path": "/path/to/store/key.pem", "cloud_args": {"name": "test-key2"}}
```



Note, that depending on the cloud provider, the parameters can be different. On Google Cloud and EC2, you must create the public and private keys, and then add them to the parameters of the dictionary. For example:


```python
keyPair = KeyPair.generate_RSA()


googleKeyParams = {"keypath": "/path/to/store/key.pem", "username": "dagon", "public_key": keyPair[1],
"private_key": keyPair[0]}
digitalOceanKeyParams = {"option": KeyOptions.CREATE, "keypath": "/path/to/store/key.pem",
"cloudargs": {"name": "dagon", "public_key": keyPair[1], "private_key": keyPair[0]}}
```



To use an existing key already added to EC2, you must declare a dictionary as follows:


```python
ssh_key_ec2_taskA = {"option": cm.KeyOptions.GET, "key_path": "/path/to/key.pem", "cloud_args": {"name": "dagon_services"}}
```

Then, you must declare the DagOnStar tasks using ```TaskType.CLOUD``` and pass the argument the ```instance flavour``` and ```key configuration``` dictionaries as arguments. 



You must also specify the provider and name of the instance must be indicated, as follows:


```python
taskA = DagonTask(TaskType.CLOUD, "A", "mkdir output;echo I am A > output/f1.txt", Provider.EC2, "ubuntu", ssh_key_ec2_taskA, instance_flavour=ec2_flavour, instance_name="dagonTaskA", stop_instance=True)
```



`dataflow-demo-cloud.py` have 2 tasks, `taskA` and `taskB`. During the execution of the script, two instances will be created on EC2. Note that these instances will be created using the default security group. You must configure it to enable access through SSH, which is the protocol used by DagOnStar to execute remote tasks.


> [!WARNING]
> We are working on a bug preventing DagOnStar from stopping instances. Please, remember to manually stop or terminate your instances after retrieving your data.


> [!WARNING]
> Data are not automatically downloaded to the DagOnStart main host. Please, remember to retrieve your data after the execution of the workflow is completed.




### Slurm

DagOnStar supports task deployment through SLURM, an open source cluster resource management and job scheduling system.



#### Pre-configuration

- [SLURM](https://slurm.schedmd.com/documentation.html)

To use a SLURM-based task on a remote server, configure SSH access in a similar way to SSH pre-configuration.



#### SLURM Task

To declare a local SLURM task, you must declare with `TaskType.SLURM`.

For each task, specify the SLURM partition on which the task is running, the number of tasks used in the execution if you want to run in parallel, and the memory tasks used according to the machine specs and `slurm.conf`.

```python
taskA = DagonTask(TaskType.SLURM, "A", "mkdir output; hostname > output/f1.txt", partition="long", ntasks=1, memory=8192)
```



#### SLURM-Remote Task

After the pre-configuration, a SLURM-remote task can be declared. For each task, specify the IP and username of the remote machine and the SLURM partition where the tasks will run, along with the other parameters that can also be set with local tasks. 

```python
taskA = DagonTask(TaskType.SLURM, "A", "mkdir output; hostname > output/f1.txt", partition="long", ntasks=1, memory=8192, ip="", ssh_username="")
```



### Docker

DagOnStar supports task deployment through Docker, a platform designed to help developers build, share, and run container applications. 



#### Pre-configuration

-  [Docker Engine](https://docs.docker.com/engine/install/ubuntu/)



To correctly run a task in a container, you first need to configure the base image with all the necessary dependencies for the task. Additionally, you must declare `workflow.set_dry("False")` in the code to ensure the proper execution of the task.

To use a Docker-based task on a remote server, configure SSH access in a similar way to SSH pre-configuration.



#### Docker Task

To declare a local Docker task, you must declare with `TaskType.DOCKER`.

Docker tasks can be run on new containers or on previously deployed containers. 



To run a task on a new container, you must define the task as follows:

```python
taskA = DagonTask(TaskType.DOCKER, "A", "echo $RANDOM > output.txt", image="ubuntu:24.04")
```

The Image option allows you to specify a base image on which to run the task. 

You can check the installed images present in Docker using the command `docker image ls`.



To run a task on an existing container, you must define the task as follows:

```python
taskA = DagonTask(TaskType.DOCKER, "A", "echo $RANDOM > output.txt", container_id="9eb6414f7e52")
```



You need to provide the ID of your container. You can obtain it by running the `docker ps` command in a terminal to see the IDs of the running containers. Containers must be running at the time of task execution.

In the task declaration you can declare a `remove` option. With this option, when the execution of the task is complete and it has no more references,the container is removed from the garbage collector. If you don't want this option, add a `remove=False` parameter to task. 



> [!NOTE]
> By default, each containers is deployed with a volume to the scratch directory of the tasks. So, you can access this directory to see the results of a task.

> [WARNING]
> We are working on a bug that prevents DagOnStar from allowing communication between tasks, preventing the exchange of files. 



#### Docker-Remote Task

After the pre-configuration, a SLURM-remote task can be declared. For each task, specify the IP and username of the remote machine and the SLURM partition where the tasks will run, along with the other parameters that can also be set with local tasks. 

```python
taskA = DagonTask(TaskType.DOCKER, "A", "echo $RANDOM > output.txt", image="ubuntu:latest", ip="", ssh_username="")
```

