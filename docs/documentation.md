# Task

DagonStar can execute multiple task simultaneously and define dependency between tasks. 

As a first example, let's define a simple Python code that execute two simple tasks. These tasks launch two bash commands. 

```python
from dagon import Workflow
from dagon.task import TaskType, DagonTask

workflow = Workflow("Taskflow-Demo")

taskA = DagonTask(TaskType.BATCH, "Hemingway", "/bin/hostname")
taskB = DagonTask(TaskType.BATCH, "Shakespeare", "/bin/date")

workflow.add_task(taskA)
workflow.add_task(taskB)

workflow.run()
```



As can be seen above, for creating a new code with Dagonstar it is mandatory to import this library. 

```python
from dagon import Workflow
from dagon.task import TaskType, DagonTask
```



For correctly execution of the code it is necessary to define a Workflow. 

```python
workflow = Workflow("Taskflow-Demo")
```

Workflow for Dagonstar representing a direct acyclic graph and a set of tasks which must be executed simultaneously. 



Now can define tasks. In this example define tasks "Hemingway" and "Shakespeare", which execute two commands. 

```python
taskA = DagonTask(TaskType.BATCH, "Hemingway", "/bin/hostname")
taskB = DagonTask(TaskType.BATCH, "Shakespeare", "/bin/date")
```

For this example tasks has batch type. With this definition can execute regular bash commands, for example "/bin/hostname" and "/bin/date"



After definition of workflow and tasks can launch add_task for every definition of tasks, for insert them into specific workflow.

```python
workflow.add_task(taskA)
workflow.add_task(taskB)
```

For Dagonstar a single task representing a vertices of the graph. 



Workflow is correctly configured, now with command .run() can execute all the tasks into them.

```python
workflow.run()
```



This is the results of the execution. 

```bash
2024-10-23 10:36:59,001 root         INFO     Workflow 'Taskflow-Demo' completed in 2.8947041034698486 seconds ---
```



With this example can see a simple tasks workflow example but, with this configuration, the tasks run independently one of each other. 



For forcing dependency from tasks can use command add_dependency_to(). 

```python
taskB.add_dependency_to(taskA)
```

With this command taskB strictly depend from taskA and his execution. Until taskA doesn't finish his running, taskB doesn't start and his status is in waiting. 

For graph this command define an edge, which creates a link between two vertices. 



```python
from dagon import Workflow
from dagon.task import TaskType, DagonTask

workflow = Workflow("Taskflow-Demo")

taskA = DagonTask(TaskType.BATCH, "Hemingway", "/bin/hostname")
taskB = DagonTask(TaskType.BATCH, "Shakespeare", "/bin/date")

workflow.add_task(taskA)
workflow.add_task(taskB)

taskB.add_dependency_to(taskA)

workflow.run()
```



For this code Dagonstar doesn't check the existence of loop in the graph. 



```python
from dagon import Workflow
from dagon.task import TaskType, DagonTask

workflow = Workflow("Taskflow-Demo")

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





```bash
2024-10-24 12:11:08,345 root         DEBUG    Running workflow: Taskflow-Demo
2024-10-24 12:11:08,345 root         DEBUG    Hemingway: Status.WAITING
2024-10-24 12:11:08,346 root         DEBUG    Shakespeare: Status.WAITING
2024-10-24 12:11:08,346 root         DEBUG    Orwell: Status.WAITING
```

