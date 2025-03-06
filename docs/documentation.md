# DAGonStar

DAGonStar (Direct acyclic graph On anything) is a lightweight Python library implementing a workflow engine able to execute parallel jobs represented by direct acyclic graphs on any combination of local machines, on-premise high-performance computing clusters, containers, and cloud-based virtual infrastructures.



## Installation

Before you begin, make sure you have the following tools installed on your system:

- Git;
- Python 3.x;
- virtualenv (you can install it with pip install virtualenv).



To install DAGonStar, follow the steps below:

1. Clone repository and navigate to the project directory.

```bash
git clone https://github.com/DagOnStar/dagonstar.git
cd dagonstar
```



2. Create and activate a virtual environment.

```bash
virtualenv venv
. venv/bin/activate
```

You’ll see the virtual environment name (venv) at the beginning of the command line, indicating that the environment is active.



3. Install the dependencies. 

```bash
pip install -r requirements.txt
```

This command installs all the dependencies listed in the requirements.txt file in the virtual environment.



4. Configure the PYTHONPATH.

```bash
export PYTHONPATH=$PWD:$PYTHONPATH
```

This command sets the `PYTHONPATH` environment variable to include the current directory, allowing Python to find the project's modules.



To run the example code you need to copy the configuration file in the examples directory.

```bash
cp dagon.ini.sample examples/dagon.ini 
cd examples
```



You can then edit the `.ini` file to suit the configuration of your system.



### Troubleshooting

On some MacOS installations, `pycrypto` fails to install automatically. This is usually due to a missing `gmp` library in the default include and library path. 

Before running the requirements install, find the location of the missing library, then export the `CFLAGS` as in the example below (the actual path may be different):

```bash
export "CFLAGS=-I/usr/local/Cellar/gmp/6.2.1_1/include -L/usr/local/Cellar/gmp/6.2.1_1/lib"
```



## Taskflow

DAGonStar can execute multiple tasks simultaneously and define dependencies between tasks.

As a first example, let's define a simple Python code that runs two simple tasks. These tasks execute two bash commands.

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

> taskflow-demo.py



As shown above, the import of this library is essential for the creation of new code with DAGonStar.

```python
from dagon import Workflow
from dagon.task import TaskType, DagonTask
```



To ensure the correct execution of the code, it is necessary to define a workflow.

```python
workflow = Workflow("English-Writers")
```

A workflow in DAGonStar represents a directed acyclic graph and a collection of tasks to be executed simultaneously.



Tasks can now be defined. In this example, we define the `Hemingway` and `Shakespeare` tasks, which run two commands. 

```python
taskA = DagonTask(TaskType.BATCH, "Hemingway", "/bin/hostname")
taskB = DagonTask(TaskType.BATCH, "Shakespeare", "/bin/date")
```

In this example, the tasks are of the batch type. With this definition, they can run standard bash commands such as `/bin/hostname` and `/bin/date`.



Once the workflow and tasks have been defined, you can use `add_task` for each task definition to add it to the specific workflow.

```python
workflow.add_task(taskA)
workflow.add_task(taskB)
```

In DAGonStar, a single task represents a vertex of the graph.



The workflow is now properly configured and you can use the .run() command to execute all the tasks within it.

```python
workflow.run()
```



This is the result of the execution. 

```bash
2024-10-23 10:36:59,001 root         INFO     Workflow 'English-Writers' completed in 2.8947041034698486 seconds ---
```



## Dry 

If you want more information about the execution of each task, you can set `dry` variable.

```python
workflow.set_dry(False)
```



Declaring `set_dry(False)` before executing the workflow ensures that the execution time or any exceptions are returned for each individual task executed in the workflow.

```bash
2024-10-29 09:50:42,200 root         DEBUG    Hemingway Completed in 0.003662109375 seconds ---
2024-10-29 09:50:42,544 root         DEBUG    Shakespeare Completed in 0.00331878662109375 seconds ---
```

 

By default, `dry` variable is set to `False`. 



## Dependency

The previous example shows a simple workflow of tasks. However, with this configuration the tasks run independently of each other.

To set dependencies between tasks, you can use the `add_dependency_to()` command.

```python
taskB.add_dependency_to(taskA)
```



Using this command, `taskB` becomes strictly dependent on the execution of `taskA`. `taskB` will not begin until `taskA` has completed, and its status will remain as waiting.

In graph terms, this command defines an edge, establishing a connection between two vertices.

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

> taskflow-dependency.py



*Shakespeare*'s task waits for the completion of *Hemingway*'s task. If *Hemingway*'s task finishes, *Shakespeare*'s task will begin.

```bash
2024-10-31 09:29:31,386 root         DEBUG    Running workflow: English-Writers
2024-10-31 09:29:31,392 root         DEBUG    Hemingway: Status.WAITING
2024-10-31 09:29:31,393 root         DEBUG    Hemingway: Status.RUNNING
2024-10-31 09:29:31,393 root         DEBUG    Hemingway: Executing...
2024-10-31 09:29:31,393 root         DEBUG    Shakespeare: Status.WAITING
2024-10-31 09:29:31,394 root         DEBUG    Hemingway: Scratch directory: /tmp//1730363371394-Hemingway
2024-10-31 09:29:32,288 root         DEBUG    Hemingway Completed in 0.006635427474975586 seconds ---
2024-10-31 09:29:34,291 root         DEBUG    Hemingway: Status.FINISHED
2024-10-31 09:29:34,291 root         DEBUG    Shakespeare: Status.RUNNING
2024-10-31 09:29:34,291 root         DEBUG    Shakespeare: Executing...
2024-10-31 09:29:34,292 root         DEBUG    Shakespeare: Scratch directory: /tmp//1730363374292-Shakespeare
2024-10-31 09:29:34,737 root         DEBUG    Shakespeare Completed in 0.003768444061279297 seconds ---
2024-10-31 09:29:36,739 root         DEBUG    Shakespeare: Status.FINISHED
2024-10-31 09:29:36,739 root         INFO     Workflow 'English-Writers' completed in 5.353054523468018 seconds ---
```



> [!WARNING]
>
> DAGonStar does not check whether the necessary dependencies of a task are present, nor does it stop execution if tasks lack the necessary data for proper execution. Therefore, it is essential to ensure that all necessary dependencies are in place before executing the code.



## Loop

In the previous chapter we explored the `add_dependency_to` command and its functionality.

Now let's build on the previous example by introducing a new task and creating additional dependencies.

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

In this particular case, *Hemingway*, *Shakespeare* and *Orwell* are stuck and unable to complete their executions because they are interdependent. There is a loop.



`make_dependencies()` command can detect loops in the graph and either resolve them or report their occurrence.

```python
workflow.make_dependencies()
```



Adding this command to the previous sample code eliminates loops and ensures the correct execution of tasks within the workflow.

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

> taskflow-loop.py



In fact, if we ran the code, we would get this result.

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



## SCHEMA and DataFlow

There is a SCHEMA variable in `_init_.py` file.

```python
 SCHEMA = "workflow://"
```

This variable defines a space that tasks can use to store data and communicate with each other. 



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

> dataflow-SCHEMA.py



This example defines two tasks, *Hemingway* and *Shakespeare*. 

*Shakespeare*, to concatenate the result and create an output, takes the result from *Hemingway* in `workflow:///Hemingway/A.txt`, file defined by the Hemingway task. 

The output, stored in the file `B.txt`, can be printed after the execution of the workflow. 

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



### dataflow-sum

Now we want to run this simple Python code. 

```python
import sys

x = open(sys.argv[1],'r')
y = open(sys.argv[2],'r')

z = int(x.read()) + int(y.read())

exit(z)
```

> sum_from_file.py



`sum_from_file.py` opens two files, reads filenames given on the command line, reads the numbers into files and sums them. 



We can run a Python (or other language) script by explicitly declaring the bash command for to execute (and compile). 

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

> dataflow-sum.py



*Hemingway* and *Shakespeare* print two numbers, 10 and 7, and save them to files `A.txt` and `B.txt`.

*Orwell* runs `sum_from_file.py` and uses the workflow SCHEMA filenames and saves the result in `C.txt`.

In the end `dataflow-sum.py` print sum result. 

```bash
['17\n']
```



## JSON

DAGonStar can export and import JSON files for saving and loading workflows without having to declare them in a program file. 



### Export JSON 

After declaring the tasks and adding them to the workflow, you can export the graph structure to a JSON file using the `workflow.as_json()` command.

```python
json_Workflow = workflow.as_json()
```



The `workflow.as_json()` command saves the workflow name, task names, task types, commands and dependencies to a `json` variable.

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



The command below allows you to export the structure and tasks of a workflow to a file. This allows you to import a complete workflow without having to declare the tasks again. 

```python
with open('english-writers.json', 'w') as outfile:
    stringWorkflow = json.dumps(json_Workflow, sort_keys=True, indent=2)
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

> dataflow-loadJSON.py



`task-loadJSON.py` loads `english-writers.json`, the file created by the export in the previous example. 

After the import, you can run the workflow without any further declaration. 

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

> dataflow-loadJSON.py execution 



## Multiple Workflows

DAGonStar allows multiple workflows to split tasks, organise them, and manage their dependencies.

The declaration of workflows and tasks remains the same, but if you want to combine two or more workflows you can use `DAG_TPS()`.

```python
metaWorkflow=DAG_TPS("WritersDAG")
```

`DAG_TPS()` creates a meta workflow, a workflow of workflows. 

With `add_workflow()` you can add workflows to the `metaWorkflow`.

```python
metaWorkflow.add_workflow(workflow1)
metaWorkflow.add_workflow(workflow2)
```

Now we can treat metaWorkflow as a simple workflow. 

```python
metaWorkflow.make_dependencies()
metaWorkflow.run()
```



In `dataflow-multiplewf.py` declare two workflows, *English-Writers* and *Italian-Writers*.

*Shakespeare* in *English-Writers* saves a number to `A.txt`, *Dante* in *Italian-Writers* cat `A.txt` and saves the number to `B.txt`.

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

> dataflow-multiplewf.py



*Dante* can read the *Shakespeare* file result because it can access to the *Shakespeare*'s folder result.

*Dante* can read `A.txt` with the command `workflow://English-Writers/Shakespeare/A.txt`, where *English-Writers* is the name of the workflow, *Shakespeare* is the name of the task and `A.txt` is the file generated as output.



### dataflow-multiplewfsum

In this example we want to define three workflows. Two of the workflows return a number, while the third takes these output numbers and adds them up.

We declare the *English-Writers* workflow, which performs the same operations as declared in `dataflow-sum.py`.



The *Italian-Writers* workflow contains a single task, *Dante*. 

```python
taskD = DagonTask(TaskType.BATCH, "Dante", "gcc /path/to/file/random_number.c -o random_number; ./random_number > D.txt")
```

This task compiles and runs a .c file that generates a random number from 1 to 99. 

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

The result is exported into `D.txt` file. 



The *French-Writers* workflow contains a task called *Perec*. 

```python
taskE = DagonTask(TaskType.BATCH, "Perec", "rustc /path/to/file/sum_rust.rc; ./sum_rust workflow://English-Writers/Orwell/C.txt workflow://Italian-Writers/Dante/D.txt > E.txt")
```

This task compiles `sum_rust.rc` and runs it by passing the filenames `workflow://English-Writers/Orwell/C.txt` and `workflow://Italian-Writers/Dante/D.txt`, which contain the results of the *English-Writers* and *Italian-Writers* executions, on the command line.

`sum_rust.rc` reads numbers from the files and sums them. 

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



`dataflow-multiplewfsum.py` defines 3 workflows and manages the execution and dependencies between 5 tasks. 

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

> dataflow-multiplewfsum.py



The result of the execution is three numbers: the first and second are the result of a sum in *English-Writers* and a random number in *Italian-Writers*. The third is the sum of these two numbers.

```bash
['17\n']
['4']
['21\n']
```



## Checkpoint

DAGonStar has an internal checkpoint system, but it also offers the possibility to declare an external checkpoint if you want to explicitly check the existence of the result file of the task (and its correct execution).

To declare an explicit checkpoint, you must declare it with `TaskType.CHECKPOINT`.

```python
taskCheck = DagonTask(TaskType.CHECKPOINT, "Checkpoint", "workflow:///Task_Name/output_file")
```



Now, to access to the checkpoint file, we need to use a path like `workflow:///Checkpoint/Workflow/Task/file.txt`.



```python
task = DagonTask(TaskType.BATCH, "Task", "cat workflow:///Svevo/Italian-Writers/Pirandello/file.txt >> output.txt")
```

In this example *Svevo* is the name of the checkpoint, *Italian-Writers* is the name of the workflow and *Pirandello* is the name of the task. 

It is still possible to refer to the original output file of the task after the checkpoint has been executed.



### dataflow-checkpoint

In this example, we declare a new C program called `output-random-file.c`. 

This code generates a random number from 1 to 100 and saves it in a file called `output-file.txt`.

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



In `dataflow-checkpoint.py` declare three tasks. 

1. *Pirandello*: Compiles and runs `output-random-file.c`, which produces a file with a random number. 
2. *Svevo:* An explicit checkpoint task that backs up `output-random-file.txt`, the result of `output-random-file.c` and saves it to an equivalent file.   
3. *Calvino*: Takes the result file from *Pirandello* from the *Svevo* checkpoint and processes it with *pow2.py*.



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

> dataflow-checkpoint.py



```bash
['8']
['64.0\n']
```

> Results



## Transversal Workflow

Dagon has the property of transversality, which allows you to create dependencies in workflows on existing workflows, whether they are currently running or have already finished. This property also allows you to build workflows from workflows for joint execution.



### Requirements

To use the transversality feature of DAGonStar, it is necessary to use [DagOnService](https://github.com/DagOnStar/DagOnService/).

DagOnService is an advanced workflow registration and remote monitoring solution designed to run on Docker. To use this service, it must to be run inside a Docker container using Docker-compose.

To run the service, run the following command in the root folder:

```bash
docker-compose up --build 
```



After running the launch command, you can check the status of the code by using the check command: 

```bash
http://localhost:57000/check
```

```bash
{
    "status": "ok"
}
```



#### dagon.ini

The `dagon.ini` file as the primary configuration file for DAGonStar.

To use DagOnService, open the `dagon.ini` file and, in the [dagon_service] section, enter the IP address (or DNS name) of the host computer where the DagOnService is running and set the use parameter to True.

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

> dagon.ini example



If DagOnService and `dagon.ini` are configured correctly, there should be a workflow registration message before a workflow is executed.

```shell
2025-01-07 11:42:33,703 root         DEBUG    Workflow registration success id = 677d051947f7f78657b0582a
```



It's recommended to set `remove_dir` to `False` in the batch section.

If you prefer, you can change the default `scratch_dir_base` to another directory, such as `/home/$USER/DAGonStar/tmp/`. This is the directory where all the results are stored.



#### DagOnService 

DagOnService offers several commands that allow you to view, manage, and delete workflows.

The `list` command allows you to view all workflows that have been executed and registered within DagOnService:

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

> Results of the list command after running taskflow-demo.py



To view the tasks of a particular workflow, you can use the address service command followed by the workflow ID.

```bash
http://localhost:57000/<workflow_id>
```



To remove an entire workflow from DagOnService, simply use the delete command followed by the workflow ID.

```bash
http://localhost:57000/delete/<workflow_id>
```



### Asynchronous dependency

Once everything is set up correctly, you can take advantage of DAGonStar's transversality.

With DagOnService, you can start a workflow and, when it is completed, start another workflow that requires data from the previous one.



#### dataflow-wf-pow

`dataflow-wf1-pow.py` gets a number and produces it as output.

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

> dataflow-wf1-pow.py



`Italian-Writers` is registered in the DagOnService and can be consulted by other workflows. To test this, we can run a second workflow with a dependency on the first.

`dataflow-wf2-pow.py` takes the output number from `dataflow-wf1-pow.py` as input and raises it to a power.

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

workflowE.add_task(taskB)

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

> dataflow-wf2-pow.py



It's mandatory to use `make_dependencies()` command in the workflow that has dependencies from another workflow.



#### Run-time dependency 

In the previous example, `dataflow-wf1-pow.py` and `dataflow-wf2-pow.py` run asynchronously, but with DagOnService support, a workflow can retrieve a task from another workflow at runtime and wait for it to complete.

In the `dataflow-wf1-pow.py` example above, add a pause to the *Pirandello* task declaration. With this change, the Pirandello task will complete its execution after 30 seconds.

```python
taskA = DagonTask(TaskType.BATCH, "Pirandello", "mkdir output;echo 7 > output/f1.txt; sleep 30")	
```



While the previous workflow is still running, run the ``WF2-pow.py`` file.

The *Woolf* task, which has dependency on the Pirandello task in `dataflow-wf1-pow.py`, waits for its completion.

```python
2025-01-16 10:27:00,856 root         DEBUG    Woolf: Status.WAITING
```



Once the Pirandello tasks of the `dataflow-wf1-pow.py` workflow have finished, the `WF2-pow-wait.py` workflow will continue its execution.

```bash
2025-01-16 10:27:06,875 root         DEBUG    Pirandello Completed in 31.989572048187256 seconds ---
2025-01-16 10:27:08,878 root         DEBUG    Pirandello: Status.FINISHED
2025-01-16 10:27:08,886 root         INFO     Workflow 'Italian-Writers' completed in 34.78531789779663 seconds ---
```

> dataflow-wf1-pow.py end status



```bash
2025-01-16 10:27:09,582 root         DEBUG    Woolf Completed in 0.031539201736450195 seconds ---
2025-01-16 10:27:11,583 root         DEBUG    Woolf: Status.FINISHED
2025-01-16 10:27:11,590 root         INFO     Workflow 'English-Writers' completed in 30.706148386001587 seconds --- 
```

> dataflow-wf2-pow.py end status



## Connection

DAGonStar gives the ability to perform tasks on a remote machine using different technologies. 



### SSH 

DAGonStar allows you to perform tasks via SSH, using remote machines to execute and complete tasks.



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

   

#### Remote Task

After preconfiguration, you can add a task to the workflow that can access the remote machine. 

To do this you can add a task like this:

```python
taskA = DagonTask(TaskType.BATCH, "A", "mkdir output;hostname > output/f1.txt", ip="", ssh_username="", keypath="")
```



After declaring the instructions add a three new parameters: `ip` is the ip of the server, `ssh_username` is the username with which to access the server and `keypath` is the *id_rsa* previously generated. 



> [!WARNING]
> By now, the stager only supports the movement of data between remote machines or from a remote machine to a local machine. We are working on enable the stage in of data from a remote machine to a local machine.



#### Remote CheckPoint

As with SSH Task, you can add a checkpoint to the workflow that can be accessed on a remote machine.

After pre-configuration, you can add a remote checkpoint as with SSH Task.

```python
taskA = DagonTask(TaskType.BATCH, "A", "mkdir output;hostname > output/f1.txt", ip="", ssh_username="")
```



> [!WARNING]
>
> This functionality is in alpha stage and may not work properly.



### Cloud Task


DAGonStar supports the deployments on the following Cloud Providers:


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


Next, we need to specify the SSH parameters to enable the communication between the DAGonStar engine and the virtual machines. You can create a new SSH key or choose an existing one, previously loaded on the platform of your cloud provider's platform.

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

Then, you must declare the DAGonStar tasks using ```TaskType.CLOUD``` and pass the argument the ```instance flavour``` and ```key configuration``` dictionaries as arguments. 



You must also specify the provider and name of the instance must be indicated, as follows:


```python
taskA = DagonTask(TaskType.CLOUD, "A", "mkdir output;echo I am A > output/f1.txt", Provider.EC2, "ubuntu", ssh_key_ec2_taskA, instance_flavour=ec2_flavour, instance_name="dagonTaskA", stop_instance=True)
```



`dataflow-demo-cloud.py` have 2 tasks, `taskA` and `taskB`. During the execution of the script, two instances will be created on EC2. Note that these instances will be created using the default security group. You must configure it to enable access through SSH, which is the protocol used by DAGonStar to execute remote tasks.


> [!WARNING]
> We are working on a bug preventing DAGonStar from stopping instances. Please, remember to manually stop or terminate your instances after retrieving your data.


> [!WARNING]
> Data are not automatically downloaded to the DAGonStar main host. Please, remember to retrieve your data after the execution of the workflow is completed.




### Slurm

DAGonStar supports task deployment through SLURM, an open source cluster resource management and job scheduling system.



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

DAGonStar supports task deployment through Docker, a platform designed to help developers build, share, and run container applications. 



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

> [!WARNING]
> We are working on a bug that prevents DAGonStar from allowing communication between tasks, preventing the exchange of files. 



#### Docker-Remote Task

After the pre-configuration, a SLURM-remote task can be declared. For each task, specify the IP and username of the remote machine and the SLURM partition where the tasks will run, along with the other parameters that can also be set with local tasks. 

```python
taskA = DagonTask(TaskType.DOCKER, "A", "echo $RANDOM > output.txt", image="ubuntu:latest", ip="", ssh_username="")
```



### Globus

For Globus configuration see the `README.md` file into `/examples/dataflow/globus`.
