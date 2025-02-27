### Process Scheduling - Summary

#### Introduction:
The **process scheduler** is a kernel subsystem that manages the execution of processes in a multitasking operating system like Linux. It decides which process runs, when it runs, and for how long, allocating finite processor resources among the runnable processes. The scheduler ensures efficient use of CPU time, giving the illusion that multiple processes are running simultaneously.

#### Key Concepts:

1. **Multitasking**:
   - A multitasking operating system can interleave the execution of multiple processes. This allows processes to appear as though they are running concurrently on **single-processor** systems and actually run concurrently on **multi-processor** systems.
   - Processes can block or sleep, waiting for events (e.g., keyboard input, network data). These processes, although in memory, are not runnable until some condition occurs, like data being received.

2. **Runnable and Waiting Processes**:
   - When there are more runnable processes than processors, some processes must wait for CPU time. The scheduler decides which process to run next, ensuring that one process is always running if there are runnable processes available.

3. **Types of Multitasking**:
   - **Cooperative Multitasking**:
     - In cooperative multitasking, a process voluntarily yields control of the CPU to allow other processes to run. The scheduler cannot force a process to stop; it must **yield** explicitly.
     - Problems with cooperative multitasking:
       - Processes may monopolize CPU time, preventing others from running.
       - A hung process that never yields can block the entire system.
     - **Examples**: Older systems like Mac OS 9 and Windows 3.1 used cooperative multitasking, which is now considered inefficient and unstable.
   - **Preemptive Multitasking**:
     - In preemptive multitasking, the operating system forcibly interrupts a running process and gives the CPU to another process. The scheduler decides when a process should stop and when a new one should begin, which is known as **preemption**.
     - A **timeslice** is the amount of time each process is allowed to run before being preempted.
     - This method is more efficient and ensures that no single process can monopolize CPU time, allowing fairer scheduling of tasks.
     - **Examples**: Linux and most modern operating systems use preemptive multitasking.

4. **Timeslice**:
   - The **timeslice** is the maximum duration a process is allowed to run before being preempted by the scheduler. It ensures that processes share CPU time fairly.
   - The timeslice is typically **predetermined** but can also be dynamically adjusted based on factors like process behavior or system policy.

5. **Linux Scheduler**:
   - Linux uses a **fair scheduler** that doesn't rely on fixed timeslices. Instead, it dynamically calculates timeslices based on factors such as process priority and behavior.
   - This "fair" approach helps prevent any process from unfairly monopolizing the CPU, maintaining overall system fairness and responsiveness.

6. **Preemption**:
   - **Preemption** refers to the OS forcibly suspending a running process to start a different process. This is essential in preemptive multitasking to ensure all processes get a chance to run.
   - The timeslice is a critical concept here, determining how long a process runs before being preempted.

#### Summary Comparison:
- **Cooperative Multitasking**: 
  - Processes must voluntarily yield the CPU.
  - Can lead to inefficiency if a process refuses to yield.
  - Less control over process execution.
- **Preemptive Multitasking**:
  - The OS forcibly interrupts running processes.
  - Ensures fair CPU allocation and system responsiveness.
  - Preferred for modern systems like Linux.

#### Conclusion:
The process scheduler is essential for multitasking systems, ensuring that multiple processes share the CPU efficiently. Linux and most modern operating systems use **preemptive multitasking** to avoid the issues associated with **cooperative multitasking**. The scheduler ensures that processes run in a fair and timely manner, maximizing the use of the processor and maintaining system stability. The concept of the **timeslice** and **preemption** are central to how the scheduler functions in preemptive multitasking systems.





### **Detailed Summary: Linux’s Process Scheduler**

#### **Evolution of Linux’s Process Scheduler**

1. **Initial Scheduler (Pre-2.5 Kernel)**:
   - The early Linux scheduler (before version 2.5) was simple and straightforward but inefficient for systems with multiple processors or many runnable processes.
   - It was easily understandable but didn’t scale well.

2. **O(1) Scheduler (Introduced in Kernel 2.5)**:
   - The O(1) scheduler was introduced to overcome the previous scheduler's limitations.
   - **Constant-time algorithm**: The scheduler calculates timeslices in constant time, regardless of the number of processes or processors.
   - **Per-processor runqueues**: The scheduler works independently on each processor, improving performance on multiprocessor systems.
   - **Ideal for servers**: The O(1) scheduler performed well on systems without interactive applications (i.e., server environments).

3. **Interactive Process Problems**:
   - **Interactive processes**: Applications that involve user interactions (e.g., graphical user interface apps).
   - **Problem**: O(1) scheduler didn’t perform well for these applications, as it couldn’t optimize for low latency or fast response time.

4. **Rotating Staircase Deadline Scheduler**:
   - Introduced to improve interactive performance by incorporating **fair scheduling** principles.
   - It aimed to balance the scheduling of interactive and processor-bound processes.

5. **Completely Fair Scheduler (CFS)**:
   - Introduced in **kernel 2.6.23** to replace the O(1) scheduler.
   - Based on **fair scheduling** principles (derived from queuing theory) to give each process an equitable share of CPU time.
   - The goal was to improve **interactive performance** and maintain system efficiency.

---

### **Key Concepts of Scheduling**

#### **Policy and Its Importance**
- **Scheduling Policy** determines the behavior of the scheduler, specifying when a process should run.
- It influences system responsiveness and resource utilization.
- A well-designed scheduler balances two main goals:
  1. **Low Latency**: Ensuring fast process response times, especially for interactive processes.
  2. **High Throughput**: Maximizing overall system utilization and processing power.

#### **Types of Processes**
1. **I/O-bound Processes**:
   - Spend most of their time waiting on I/O operations (e.g., keyboard input, network activity).
   - These processes have low processor utilization but require rapid scheduling for responsiveness.
   - Examples: GUI applications, web browsers.

2. **Processor-bound Processes**:
   - These processes spend most of their time actively executing code and do not block on I/O requests.
   - They tend to run for longer periods without interruption.
   - Examples: Programs performing heavy computations, like `ssh-keygen` or mathematical calculations in `MATLAB`.

3. **Mixed Processes**:
   - Some processes can exhibit both I/O-bound and processor-bound behavior at different times (e.g., the X Window system, word processors).
  
The scheduler aims to satisfy both needs: giving fast response to I/O-bound processes while not starving processor-bound processes.

---

#### **Process Priority and Scheduling**

1. **Priority-based Scheduling**:
   - Processes are ranked by priority, and higher-priority processes run before lower-priority ones.
   - In Linux, **priority** is divided into two ranges:
     - **Nice values**: Range from -20 (highest priority) to +19 (lowest priority), with 0 being the default.
       - The **nice value** affects the **proportion of CPU time** a process can consume.
     - **Real-time priority**: Range from 0 to 99, where higher values represent higher priority.
       - Real-time processes always have priority over non-real-time processes.
   - Real-time priority is useful for tasks with strict timing requirements (e.g., audio/video processing).

2. **Nice Values in Linux**:
   - **Lower nice values** (more negative) result in higher priority, while **higher nice values** (more positive) lead to lower priority.
   - The **nice value** influences how much CPU time a process receives relative to others.

3. **Real-time Priorities**:
   - Used for tasks that require guaranteed execution within a certain timeframe.
   - These tasks run with higher priority than normal tasks, regardless of their nice values.

---

#### **Timeslice (Quantum) and Its Importance**

1. **Timeslice (Quantum)**:
   - The **timeslice** refers to the amount of time a process runs before it is preempted.
   - A **long timeslice** can negatively impact interactive performance because processes (like GUI apps) might be blocked for too long.
   - A **short timeslice** increases the overhead of switching between processes, reducing system efficiency.
   - **Linux CFS (Completely Fair Scheduler)** doesn’t assign static timeslices. Instead, it allocates **proportions of CPU time** to processes.

2. **CFS’s Proportional Allocation**:
   - In CFS, each process is assigned a **proportion of the CPU** based on its **nice value** and system load.
   - If a process is underusing its allocated time, it can be preempted by other processes that are ready to run.

3. **Processor Time Allocation**:
   - **I/O-bound processes** (like a text editor) will receive immediate access to CPU time when they become active, even if they have not used their full allocation.
   - **Processor-bound processes** (like a video encoder) will be allowed to run longer as they typically require continuous CPU time.

---

#### **CFS in Action**

1. **Scenario: Text Editor vs. Video Encoder**:
   - **Text Editor (I/O-bound)**: Spends most of its time waiting for user input and needs fast response time when the user presses a key.
   - **Video Encoder (Processor-bound)**: Consumes a large portion of the CPU, performs heavy calculations, and doesn’t have strict timing requirements.

   - In Linux CFS, both processes are given equal portions of the CPU (e.g., 50% each). However, the text editor rarely uses its full share, so when it wakes up (e.g., upon a keypress), CFS will preempt the video encoder, giving the text editor immediate access to the CPU. After the text editor processes the keypress, it sleeps again, allowing the video encoder to resume its processing.

2. **CFS Goal**:
   - The CFS scheduler tries to **ensure fairness** by making sure each process gets a proportionate share of CPU time while prioritizing **interactive tasks** that require fast response times.

---

### **Summary of Key Points**
1. The **O(1) scheduler** was efficient for server workloads but performed poorly for interactive applications. It was replaced by the **Completely Fair Scheduler (CFS)** in kernel version **2.6.23**, which introduced fair scheduling and prioritized interactive processes.
2. **Scheduler Policy** governs when and how processes are run, affecting system responsiveness and overall throughput.
3. **I/O-bound** and **processor-bound processes** have different scheduling needs, and Linux aims to balance the two for optimal performance.
4. **Priority-based scheduling** is used to determine which processes get to run first. Linux uses **nice values** and **real-time priorities** to manage process execution.
5. The **timeslice** determines how long a process runs before being preempted, and CFS assigns CPU time proportionally to processes.
6. In interactive scenarios, CFS prioritizes fast response for I/O-bound tasks while allowing processor-bound tasks to run when they can.

By balancing fairness and responsiveness, the **CFS scheduler** ensures efficient process scheduling in modern Linux systems.

### **Linux Scheduling Algorithm Overview**

The Linux process scheduler manages the allocation of CPU time to processes, ensuring fairness and efficiency. The scheduling system in Linux is modular and allows different scheduling algorithms to handle different types of processes. This modularity is known as **scheduler classes**. 

### **Scheduler Classes**

Scheduler classes enable the use of different scheduling algorithms for different types of processes. The Linux kernel iterates over each scheduler class in order of priority. The highest-priority scheduler class with a runnable process is selected to run next. 

- The **Completely Fair Scheduler (CFS)** is the default scheduler class for normal processes, referred to as **SCHED_NORMAL** in Linux (or **SCHED_OTHER** in POSIX).
- Other scheduler classes exist for different process types, such as **real-time processes**, which are scheduled differently from normal processes.

### **Traditional Unix Scheduling**

Traditional Unix systems use concepts of **process priority** and **timeslices**. 
- **Priority** is how important a process is and determines how frequently it is scheduled to run.
- **Timeslice** is how long a process is allowed to run before another process is scheduled.

Unix systems typically assign processes a **nice value**, which influences their priority. A higher nice value corresponds to a lower priority and vice versa.

### **Problems with Traditional Scheduling**

Several issues arise from using nice values and timeslices in traditional Unix scheduling:

1. **Suboptimal switching behavior**:
   - Example: If a normal priority process has a timeslice of 100 milliseconds and a low-priority process has 5 milliseconds, the low-priority process will be allowed to run only a tiny fraction of the time, even if it is the only process running. This creates inefficient scheduling behavior.
   
2. **Relative nice value impact**:
   - The difference in timeslices between processes with small differences in nice values can lead to disproportionate scheduling. A small change in nice value may cause a large difference in timeslices, making relative priorities confusing.

3. **Absolute timeslice assignment**:
   - Absolute timeslices must be mapped to the system's timer tick, which introduces the risk of inefficient use of CPU time due to floor and ceiling limitations on timeslice length.

4. **Wake-up priority boost**:
   - In Unix scheduling, waking up a sleeping process may give it an immediate priority boost, which could lead to some tasks receiving an unfair amount of CPU time.

### **Completely Fair Scheduler (CFS)**

CFS aims to solve the shortcomings of traditional scheduling by eliminating fixed timeslices and instead assigning **proportions of processor time** to each process based on their **weight**. The key idea is to model process scheduling as if the system had a perfectly multitasking processor, where each process would receive an equal share of the CPU time. 

#### **Core Concepts of CFS**:

1. **Perfect Multitasking Model**:
   - In an ideal system, processes would run simultaneously for infinitely small durations, with each process getting an equal share of the CPU. In a practical system, CFS approximates this behavior by assigning a proportional share of CPU time based on process weight.

2. **Weights and Nice Values**:
   - Instead of using fixed timeslices, CFS assigns a **weight** to each process based on its nice value. 
     - Lower nice values (higher priority) get higher weights and thus more CPU time.
     - Higher nice values (lower priority) get lower weights and thus less CPU time.
   - The weight of a process determines the fraction of processor time it gets, based on the total weight of all runnable processes.
  
3. **Target Latency**:
   - CFS uses a target latency to approximate the time each process should run before switching. The target latency represents the ideal amount of time to run processes in a perfect multitasking environment.
   - **Target latency** (default 20 ms) is the time interval within which CFS tries to schedule all runnable processes.
   - Processes are scheduled for durations that are proportional to their weights. For instance, if there are two tasks with the same priority, each runs for half of the target latency (10 ms if the target latency is 20 ms). For four tasks, each runs for 5 ms, and so on.

4. **Granularity and Switching**:
   - **Minimum Granularity**: To prevent excessive switching overhead when the number of runnable processes is large, CFS imposes a **minimum granularity** (default 1 ms). This ensures that even if there are many runnable processes, each process will run for at least 1 ms.

5. **Fairness**:
   - **CFS ensures fairness** by distributing CPU time proportionally to the process weight, based on relative nice values.
   - The more processes there are, the smaller each process's allocated time slice, but CFS strives to avoid unfairness as much as possible.

6. **Impact of Nice Values**:
   - CFS eliminates the issue of **absolute timeslices** tied to nice values. Instead, it uses the **relative difference** in nice values to allocate CPU time. 
   - A process with a nice value of 5 will receive less time than a process with a nice value of 0, but the exact proportion depends on the weights of all runnable processes.

#### **Practical Example of CFS Scheduling**:

- **Two processes**:
  - If two processes have equal nice values (say, 0), both will get 50% of the CPU time (target latency = 20 ms, each runs for 10 ms).
  
- **Different nice values**:
  - If one process has a nice value of 0 and another has a nice value of 5, the process with a lower priority (higher nice value) will run for a shorter duration. With a target latency of 20 ms, the first process might run for 15 ms, and the second process for 5 ms.

### **Challenges in CFS**

- **Very large number of processes**: As the number of processes grows, the timeslice each process receives decreases. This can lead to excessive context switching, though the minimum granularity helps limit this effect.
- **Imperfect fairness**: While CFS strives to achieve fairness, the inherent limitations of approximating multitasking and overhead from context switching introduce minor unfairness, particularly with extremely high numbers of runnable processes.

### **Summary of Key CFS Principles**:

- **Proportional allocation**: Processes are allocated CPU time proportionally based on their weights, which depend on their nice values.
- **Target latency**: CFS aims to approximate perfect multitasking by using a target latency to determine the duration for which processes run.
- **Fairness**: Processes receive a fair share of CPU time, and CFS tries to maintain this fairness even as the number of processes changes.
- **Minimum granularity**: To reduce excessive switching costs, CFS enforces a minimum granularity on timeslices.
  
### **Conclusion**

The **Completely Fair Scheduler (CFS)** in Linux represents a shift from traditional Unix scheduling. By assigning each process a proportion of the CPU based on its relative priority and minimizing the impact of absolute timeslice assignments, CFS provides a more efficient and fair scheduling mechanism, particularly in systems with many processes. The trade-off for fairness is a variable switching rate, which is managed using parameters like the target latency and minimum granularity. This provides a balance between responsiveness and system performance, ensuring that all processes receive a fair share of CPU time based on their priorities.



Here’s a detailed summary of **Linux CFS Scheduling Implementation**:

### 1. **Time Accounting**

- **Purpose**: All process schedulers track the time a process runs. CFS doesn't use the concept of a timeslice but accounts for process time via `sched_entity` structure. This structure is part of the `task_struct`, the process descriptor in Linux.
  
- **Key Structure: `sched_entity`**:
  - Tracks process accounting.
  - Fields include:
    - `vruntime`: Virtual runtime (normalized time accounting).
    - `sum_exec_runtime`: Total execution time.
    - `exec_start`: Last execution start time.
    - `on_rq`: Whether the task is on the run queue.
    - `last_wakeup`: Last wakeup time.
    - And several other variables related to stats and migrations.

- **Virtual Runtime (`vruntime`)**:
  - `vruntime` is a normalized measure of how long a task has run, adjusted for how many runnable tasks there are.
  - **Units**: Nanoseconds.
  - CFS aims for tasks with the same priority to have the same `vruntime`, indicating fair CPU usage.
  - **Update Mechanism**: The `update_curr()` function manages `vruntime`. It computes the runtime of the current task (`delta_exec`) and updates its `vruntime` based on the weighted value of the time spent.

  ```c
  static void update_curr(struct cfs_rq *cfs_rq) {
      struct sched_entity *curr = cfs_rq->curr;
      u64 now = rq_of(cfs_rq)->clock;
      unsigned long delta_exec;
      if (unlikely(!curr))
          return;

      delta_exec = (unsigned long)(now - curr->exec_start);
      if (!delta_exec)
          return;

      __update_curr(cfs_rq, curr, delta_exec);
      curr->exec_start = now;
  }
  ```

  - **`__update_curr()`**: This function calculates the weighted execution time (`delta_exec_weighted`) and updates `vruntime`. It adjusts for the number of runnable tasks using `min_vruntime`.

### 2. **Process Selection**

CFS selects processes based on `vruntime`. The process with the smallest `vruntime` gets selected next. This selection is efficient due to a red-black tree, a self-balancing binary search tree, used to store processes.

- **Red-Black Tree**:
  - Stores runnable processes with their `vruntime` as keys.
  - Efficiently finds the process with the smallest `vruntime`, as it is always located at the leftmost node of the tree.
  
  ```c
  static struct sched_entity *__pick_next_entity(struct cfs_rq *cfs_rq) {
      struct rb_node *left = cfs_rq->rb_leftmost;
      if (!left)
          return NULL;
      return rb_entry(left, struct sched_entity, run_node);
  }
  ```

- **Selecting the Next Process**:
  - CFS runs the process represented by the leftmost node in the red-black tree, which is the one with the smallest `vruntime`.

### 3. **Enqueuing a Process (Adding to the Tree)**

When a process becomes runnable (wakes up or is created), it is added to the red-black tree via the `enqueue_entity()` function. 

- **Steps**:
  1. **`enqueue_entity()`**: Updates the process's runtime stats and calls `__enqueue_entity()` to insert it into the tree.
  2. **`__enqueue_entity()`**: Traverses the tree to find the correct position for the process based on its `vruntime`. If the process is the leftmost node, `rb_leftmost` is updated. The node is then linked into the tree, and balancing is performed via `rb_insert_color()`.

  ```c
  static void __enqueue_entity(struct cfs_rq *cfs_rq, struct sched_entity *se) {
      struct rb_node **link = &cfs_rq->tasks_timeline.rb_node;
      struct rb_node *parent = NULL;
      struct sched_entity *entry;
      s64 key = entity_key(cfs_rq, se);
      int leftmost = 1;

      while (*link) {
          parent = *link;
          entry = rb_entry(parent, struct sched_entity, run_node);

          if (key < entity_key(cfs_rq, entry)) {
              link = &parent->rb_left;
          } else {
              link = &parent->rb_right;
              leftmost = 0;
          }
      }

      if (leftmost)
          cfs_rq->rb_leftmost = &se->run_node;

      rb_link_node(&se->run_node, parent, link);
      rb_insert_color(&se->run_node, &cfs_rq->tasks_timeline);
  }
  ```

  - **Key Logic**:
    - The while loop navigates the tree based on the `vruntime` of the process (`key`).
    - If moving to the right, the process is not the leftmost node.
    - If it moves only left, the process becomes the new leftmost node.

- **Tree Insertion**:
  - Once the position is found, the process is inserted into the tree, and the tree is rebalanced to maintain its self-balancing properties.

### 4. **Scheduler Entry Point**

When a process is selected, the entry point involves picking the task with the smallest `vruntime` and switching the CPU context to run it. The scheduler checks if there are any tasks to run and chooses the next process based on `vruntime`. If no runnable tasks exist, the idle task is chosen.

- **Idle Task**: If no runnable processes are available, the idle task is scheduled.

### 5. **Sleeping and Waking Up**

Processes may become blocked and enter a sleeping state. When they wake up, they are added back to the red-black tree. 

- **Waking up**: When a process wakes up, it is enqueued back to the run queue with the appropriate accounting for its wake-up time.
- **Sleeping**: When a process sleeps, it is removed from the run queue, and the scheduler selects the next task with the smallest `vruntime`.

### Summary of Key Components:

1. **`sched_entity`**:
   - Stores key accounting data such as `vruntime`, `sum_exec_runtime`, and execution stats.

2. **Virtual Runtime (`vruntime`)**:
   - CFS uses `vruntime` to track how long a process has run and adjusts for fairness by normalizing it based on the number of runnable tasks.

3. **Red-Black Tree**:
   - CFS uses a red-black tree to store runnable processes, enabling efficient selection of the next task (the one with the smallest `vruntime`).

4. **Process Selection**:
   - The process with the smallest `vruntime` (leftmost in the red-black tree) is selected to run next.

5. **Process Insertion**:
   - When a process becomes runnable (wakes up), it is added to the tree using `enqueue_entity()`, which ensures it is placed correctly based on its `vruntime`.

By maintaining the process list in a red-black tree, CFS ensures fair process scheduling with efficient selection of the next task to run.


Here is a **detailed summary** of the key concepts from your provided text on **Linux Process Scheduling**, focusing on **Completely Fair Scheduler (CFS), process removal, task selection, sleeping, waking up, and wait queues**.  

---

# **Detailed Summary of Linux Process Scheduling**

## **1. Removing Processes from the Red-Black Tree**
Processes are removed from the **red-black tree** when they **block** (become unrunnable) or **terminate** (cease to exist). The function responsible for removing processes is:

### **`dequeue_entity()`**
This function handles the removal of a process from the red-black tree and updates various scheduling parameters:

- **Updates run-time statistics** using `update_curr(cfs_rq)`.
- Calls `update_stats_dequeue(cfs_rq, se)` to update statistics for the entity.
- Clears any scheduling buddies via `clear_buddies(cfs_rq, se)`.
- If the process being removed is **not the currently running process**, it calls `__dequeue_entity(cfs_rq, se)`, which performs the actual removal.
- `account_entity_dequeue(cfs_rq, se)` accounts for the entity's removal from the scheduling queue.
- Updates **min_vruntime** using `update_min_vruntime(cfs_rq)`.
- If the process is **not going to sleep**, it adjusts its **virtual runtime**.

### **`__dequeue_entity()`**
This function performs the **actual removal** from the red-black tree.

- If the process being removed is the **leftmost node** in the red-black tree:
  - It finds the **next** leftmost node using `rb_next(&se->run_node)`.
  - Updates the `rb_leftmost` pointer.
- Calls `rb_erase(&se->run_node, &cfs_rq->tasks_timeline)`, which removes the process from the **red-black tree**.

Removing a process is **simpler** than adding it because the **rbtree implementation already provides `rb_erase()`**.

---

## **2. Scheduler Entry Point (`schedule()`)**
The main **entry point** for process scheduling is the `schedule()` function, defined in `kernel/sched.c`.

- It is a **generic function** that **works across multiple scheduling classes**.
- It finds the **highest priority** scheduler class with a runnable process.
- Calls `pick_next_task()`, which selects the **next process to run**.

### **`pick_next_task()`**
- Loops through **all scheduler classes** in **priority order**, starting with the highest priority.
- Calls the `pick_next_task()` function for each class until it finds a runnable process.
- Uses an **optimization**:  
  - If all runnable processes belong to CFS (`rq->nr_running == rq->cfs.nr_running`), it directly calls `fair_sched_class.pick_next_task(rq)`.

### **CFS Task Selection**
- The **CFS implementation** of `pick_next_task()` calls `pick_next_entity()`, which ultimately calls `__pick_next_entity()`.
- `__pick_next_entity()` selects the **leftmost node** from the red-black tree, which represents the **next process to run**.

---

## **3. Sleeping and Waking Up**
Processes can **go to sleep** when they wait for an event, such as:

- **File I/O operations** (e.g., waiting for data from disk).
- **User input** (e.g., waiting for keyboard input).
- **Waiting for a semaphore** in kernel synchronization.

A **sleeping process**:
- **Removes itself from the red-black tree**.
- **Calls `schedule()`** to select another process to execute.

### **Sleeping States**
There are **two states** associated with sleeping:

1. **`TASK_INTERRUPTIBLE`**:
   - The process can be **awakened by signals** (e.g., keyboard interrupt, system signal).
2. **`TASK_UNINTERRUPTIBLE`**:
   - The process **ignores signals** and wakes up only when the expected event occurs.

Both types of sleeping processes **sit on a wait queue**.

---

## **4. Wait Queues**
A **wait queue** is a list of processes waiting for an event to occur. It is represented in the kernel by `wake_queue_head_t`.

- A process **adds itself** to a wait queue and marks itself as **not runnable**.
- When the event occurs, all processes in the wait queue are **awakened**.

### **Correct Sleeping Implementation**
Sleeping should be implemented carefully to **avoid race conditions**.

- Some **old sleep interfaces** had a **race condition** where a process might **miss** an event and **sleep indefinitely**.
- The **recommended method** follows a structured approach:

#### **Correct Sleep Implementation Code**
```c
/* 'q' is the wait queue we wish to sleep on */
DEFINE_WAIT(wait);
add_wait_queue(q, &wait);

while (!condition) {
    /* Set the process state */
    prepare_to_wait(&q, &wait, TASK_INTERRUPTIBLE);

    /* Check if a signal is received */
    if (signal_pending(current))
        /* Handle signal */

    schedule();
}

/* Remove process from wait queue */
finish_wait(&q, &wait);
```

### **Steps Explained**
1. **Create a wait queue entry** using `DEFINE_WAIT(wait)`.
2. **Add process to wait queue** using `add_wait_queue(q, &wait)`.
3. **Set process state** to `TASK_INTERRUPTIBLE` or `TASK_UNINTERRUPTIBLE` using `prepare_to_wait()`.
4. **Check if a signal wakes up the process**.
5. **If the condition is not met**, the process calls `schedule()` to sleep.
6. **When the condition occurs**, the process removes itself from the queue using `finish_wait()`.

### **Example: `inotify_read()` Function**
The function `inotify_read()` in `fs/notify/inotify/inotify_user.c` is a **real-world example** of wait queue usage.

```c
static ssize_t inotify_read(struct file *file, char __user *buf,
                            size_t count, loff_t *pos) {
    struct fsnotify_group *group;
    struct fsnotify_event *kevent;
    DEFINE_WAIT(wait);

    group = file->private_data;
    while (1) {
        prepare_to_wait(&group->notification_waitq, &wait, TASK_INTERRUPTIBLE);
        mutex_lock(&group->notification_mutex);
        kevent = get_one_event(group, count);
        mutex_unlock(&group->notification_mutex);

        if (kevent) {
            ret = copy_event_to_user(group, kevent, buf);
            fsnotify_put_event(kevent);
            if (ret < 0) break;
            continue;
        }

        if (file->f_flags & O_NONBLOCK) break;
        if (signal_pending(current)) break;
        schedule();
    }
    finish_wait(&group->notification_waitq, &wait);
    return ret;
}
```
- This function **adds itself to a wait queue** and **waits for events** in a loop.
- It **handles signals** and **ensures no race conditions**.
- Uses **locks** to access the event queue.

---

## **5. Waking Up a Sleeping Process**
The function `wake_up()` is responsible for **waking up all tasks waiting** on a given wait queue.

- Calls `try_to_wake_up()`, which:
  - Sets the process **state to `TASK_RUNNING`**.
  - Calls `enqueue_task()`, which **re-adds** the process to the **red-black tree**.
  - If the **awakened task has a higher priority**, it sets `need_resched` to force a reschedule.

### **Spurious Wake-Ups**
- Sometimes, a task **wakes up without the expected event occurring**.
- This is called a **spurious wake-up**.
- Thus, **sleeping should always be inside a loop** that ensures the condition is **truly met** before continuing execution.

---

# **Final Thoughts**
This summary covered:
✔ **Removing processes from the red-black tree**  
✔ **Process selection in `schedule()`**  
✔ **Sleeping and task states (`TASK_INTERRUPTIBLE`, `TASK_UNINTERRUPTIBLE`)**  
✔ **Correct wait queue usage**  
✔ **Waking up processes and handling race conditions**  

By understanding these topics, you gain a **solid grasp** of how **Linux schedules and manages processes efficiently**. 🚀



Here’s a detailed summary of **Preemption and Context Switching** to help you with your exams:  

---

# **Preemption and Context Switching**  

## **1. Context Switching**  
Context switching refers to the process of switching from one runnable task to another. This operation is performed by the `context_switch()` function, which is located in `kernel/sched.c`. The function is called by `schedule()` when the scheduler selects a new process to run.  

### **Roles of `context_switch()`**  
It performs two primary functions:  
1. **Switches Virtual Memory Mapping:**  
   - Calls `switch_mm()` (defined in `<asm/mmu_context.h>`) to update the virtual memory mappings from the old process to the new process.  
2. **Switches Processor State:**  
   - Calls `switch_to()` (declared in `<asm/system.h>`) to switch the processor state, including saving/restoring stack information, processor registers, and any other architecture-specific states.  

### **When Does the Kernel Call `schedule()`?**  
- The kernel cannot rely solely on explicit calls to `schedule()` by processes, as this would allow user-space processes to run indefinitely.  
- Instead, the kernel uses the **`need_resched`** flag to indicate when a reschedule is required.  

---

## **2. `need_resched` Flag and Scheduling**  
- The `need_resched` flag signals the kernel to invoke the scheduler as soon as possible because another process is ready to run.  
- This flag is modified by:  
  - `scheduler_tick()`: When a process should be preempted.  
  - `try_to_wake_up()`: When a higher-priority process is awakened.  
- Upon returning to user-space or from an interrupt, the kernel checks `need_resched`. If it is set, `schedule()` is invoked.  

### **Why Is `need_resched` Per-Process Instead of Global?**  
- Initially, before Linux 2.2, `need_resched` was a global flag.  
- In Linux 2.2 and 2.4, it was moved inside `task_struct`.  
- In Linux 2.6, it was optimized to a **single-bit flag inside `thread_info`**, improving performance by keeping it cache-hot and reducing access time.  

### **Functions for Manipulating `need_resched`**  
| Function | Purpose |  
|----------|---------|  
| `set_tsk_need_resched()` | Sets the `need_resched` flag for a process. |  
| `clear_tsk_need_resched()` | Clears the `need_resched` flag for a process. |  
| `need_resched()` | Checks if `need_resched` is set (returns `true` if set, `false` otherwise). |  

---

## **3. User Preemption**  
User preemption occurs when the kernel is about to return to user-space, detects that `need_resched` is set, and invokes the scheduler to switch tasks.  

### **When Does User Preemption Occur?**  
1. **Returning from a System Call:**  
   - If the kernel is returning from a system call and `need_resched` is set, it invokes the scheduler before switching back to user-space.  
2. **Returning from an Interrupt Handler:**  
   - If the kernel is returning from an interrupt handler to user-space and `need_resched` is set, a more appropriate task is scheduled.  

- These return paths are architecture-specific and are usually implemented in assembly (e.g., in `entry.S`).  

---

## **4. Kernel Preemption**  
- **Linux is a fully preemptive kernel (since version 2.6), unlike many other Unix-based systems.**  
- In non-preemptive kernels, once kernel code starts executing, it runs until completion.  
- In preemptive kernels, kernel execution can be interrupted **if it is safe to do so** (i.e., no critical locks are held).  

### **When Is It Safe to Preempt Kernel Execution?**  
- A kernel task **can be preempted if it is not holding a lock**.  
- The kernel uses **locks as markers of non-preemptible regions**.  
- If no locks are held, the kernel assumes that the current code is **reentrant** and can be safely preempted.  

### **Preemption Counter (`preempt_count`)**  
- Each process’s `thread_info` structure has a **preemption counter (`preempt_count`)** to track lock acquisition:  
  - **Counter starts at 0.**  
  - **Increments** when a lock is acquired.  
  - **Decrements** when a lock is released.  
  - If `preempt_count == 0`, the kernel is preemptible.  

- When an **interrupt returns to kernel-space**, it checks:  
  - If `need_resched` is set.  
  - If `preempt_count == 0`.  
  - If both conditions are met, the scheduler is invoked. Otherwise, execution continues as normal.  

- If a task releases its last lock (`preempt_count` becomes 0), the unlock code checks `need_resched`. If set, it invokes the scheduler.  

### **When Does Kernel Preemption Occur?**  
1. **When an Interrupt Handler Exits:**  
   - Before returning to kernel-space, if `need_resched` is set and `preempt_count == 0`, a reschedule occurs.  
2. **When Kernel Code Becomes Preemptible Again:**  
   - If kernel execution reaches a state where no locks are held, preemption can occur.  
3. **When a Task in the Kernel Explicitly Calls `schedule()`:**  
   - A task can voluntarily yield control by calling `schedule()`.  
4. **When a Task in the Kernel Blocks:**  
   - If a task cannot proceed (e.g., waiting for I/O), it blocks and calls `schedule()`, allowing another task to run.  

---

## **Summary and Key Takeaways**  

| Topic | Details |  
|--------|---------|  
| **Context Switching** | `context_switch()` in `kernel/sched.c` switches process state and memory. |  
| **Virtual Memory Mapping** | `switch_mm()` updates the virtual memory mappings of processes. |  
| **Processor State Switching** | `switch_to()` switches CPU registers and stack information. |  
| **Need for `schedule()`** | The kernel calls `schedule()` when `need_resched` is set to select a new process. |  
| **`need_resched` Flag** | Indicates when a process should be rescheduled; stored in `thread_info` since Linux 2.6. |  
| **User Preemption** | Happens when returning from a system call or interrupt handler. |  
| **Kernel Preemption** | Kernel tasks can be preempted if no locks are held (`preempt_count == 0`). |  
| **Preemption Counter (`preempt_count`)** | Tracks the number of locks held by a process to determine if preemption is safe. |  
| **When Kernel Preemption Occurs** | - When an interrupt handler exits.  
  - When kernel code becomes preemptible.  
  - When a task explicitly calls `schedule()`.  
  - When a task blocks. |  

---

This summary includes **all important details** while keeping it structured for easy revision. Let me know if you need further clarifications! 🚀



who sets need_resched ?
kernel or user space ?  


The **kernel** sets `need_resched`, not user-space.  

### **Who Sets `need_resched`?**
- The `need_resched` flag is set by the **scheduler** inside the **kernel** when a task should be preempted.
- User-space **does not** directly manipulate `need_resched`; it is entirely managed by the kernel.

### **How `need_resched` is Set?**
1. **By `scheduler_tick()`**  
   - This function runs periodically (on every timer tick) and determines if the currently running process has used up its time slice.
   - If so, it sets `need_resched` to indicate that a context switch should happen.

2. **By `try_to_wake_up()`**  
   - When a **higher-priority** process is woken up (e.g., after being blocked), `need_resched` is set to signal that the scheduler should run and allow the higher-priority task to execute.

### **When is `need_resched` Checked?**
- **When returning to user-space** (after a system call or an interrupt).  
- **Before returning from an interrupt handler** (if `need_resched` is set, the scheduler runs).  
- **Before resuming kernel execution** (if kernel preemption is enabled, the scheduler checks if it's safe to switch tasks).  

### **Functions for Managing `need_resched`**
| Function                  | Purpose |
|--------------------------|---------|
| `set_tsk_need_resched()` | Sets `need_resched` for a process |
| `clear_tsk_need_resched()` | Clears `need_resched` |
| `need_resched()` | Checks if `need_resched` is set (returns true/false) |

### **Conclusion**
- The **kernel** sets `need_resched`, not user-space.  
- It is used to **signal the scheduler** that a context switch should occur.  
- It is checked when **returning to user-space**, **after interrupts**, or **when kernel preemption is enabled**.



Completely Fair Scheduler (CFS) stores task data in the bst tree then it doesn't have queue like real time  Scheduler like FIFO and RR

Yes, you are correct! The **Completely Fair Scheduler (CFS)**, which is the default scheduler for normal (non-real-time) tasks in Linux, does **not** use a queue like real-time schedulers (FIFO and Round-Robin). Instead, it uses a **Red-Black Tree** (a self-balancing Binary Search Tree, BST) to manage tasks efficiently.  

Here’s a detailed comparison:  

### **1. CFS (Completely Fair Scheduler)**
- **Data Structure:** Red-Black Tree (BST)
- **Scheduling Strategy:** Fairness-based (ensures each process gets CPU time proportionally)
- **Queue:** No explicit queue, tasks are sorted in a Red-Black Tree by their **virtual runtime** (`vruntime`).
- **Selection:** The process with the **smallest vruntime** (leftmost node in the tree) gets scheduled first.
- **Preemption:** Happens when a newly arriving task has a smaller vruntime than the current running task.
- **Timeslice:** Dynamically calculated based on task weight (`nice` value) and system load.

### **2. Real-Time Schedulers (SCHED_FIFO and SCHED_RR)**
- **Data Structure:** **Queue-based** (Runqueues)
- **SCHED_FIFO (First-In, First-Out)**
  - Uses a simple **FIFO queue**.
  - A running task continues **until it blocks, exits, or a higher-priority task preempts it**.
  - No timeslices (can run indefinitely unless preempted).
- **SCHED_RR (Round-Robin)**
  - Similar to SCHED_FIFO but **with timeslices**.
  - When a task’s **timeslice expires**, it moves to the **end of the queue** if another task of the same priority is waiting.
  
### **Key Differences**
| Feature          | CFS (Normal Tasks)  | SCHED_FIFO (RT) | SCHED_RR (RT) |
|----------------|----------------|----------------|----------------|
| **Data Structure** | Red-Black Tree (BST) | FIFO Queue | FIFO Queue |
| **Preemption** | Based on `vruntime` | Only by higher-priority tasks | By timeslice expiration |
| **Timeslice** | Dynamically allocated | No timeslice (runs indefinitely) | Fixed timeslice |
| **Task Selection** | Leftmost node in BST | First in the queue | Round-Robin |
| **Priority** | `nice` values (-20 to +19) | Static priority (1–99) | Static priority (1–99) |

### **Conclusion**
- **CFS** is optimized for **fairness** and ensures every process gets CPU time based on its weight.
- **Real-time schedulers (FIFO & RR)** prioritize **deterministic execution** over fairness, using simple **queues** for fast and predictable scheduling.

For exam preparation, make sure you understand:
1. The difference between CFS and real-time schedulers.
2. How the Red-Black Tree helps in fair scheduling.
3. How SCHED_FIFO and SCHED_RR use queues.
4. The impact of priorities in real-time scheduling.

Let me know if you need more details! 🚀

