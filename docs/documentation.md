# Data





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

in `\_init\_.py` file there is a SCHEMA variable. 

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

To declare an explicit checkpoint, you need to declare a task with `TaskType.CHECKPOINT`.

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

