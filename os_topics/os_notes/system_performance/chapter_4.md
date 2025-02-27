Tracepoints are a feature in the Linux kernel that enables observability at specific points in kernel code. They are *static instrumentation points*, meaning they are predefined in the kernel code at logical spots, such as the beginning and end of system calls, within scheduler events, and during disk or file system operations. Introduced in Linux kernel version 2.6.32, tracepoints offer a *stable API*, allowing developers and system administrators to monitor specific kernel events without modifying the kernel code itself.

Here’s a high-level overview of how to work with tracepoints:

### 1. **Listing Available Tracepoints**
   Use the `perf list` command to view all available tracepoints:
   ```bash
   perf list tracepoint
   ```
   This displays a long list of tracepoints grouped by category (e.g., `block`, `sched`, `scsi`), showing different areas of the kernel where tracepoints can be applied.

### 2. **Tracing with Tracepoints**
   Once you identify a tracepoint, you can start tracing events by specifying the tracepoint name with `perf`. For example:
   ```bash
   perf trace -e block:block_rq_issue
   ```
   This command monitors block I/O events at the `block:block_rq_issue` tracepoint, showing detailed information for each event.

### 3. **Filtering Tracepoint Data**
   You can also filter tracepoints based on specific conditions using the `--filter` option:
   ```bash
   perf trace -e block:block_rq_issue --filter 'bytes > 65536'
   ```
   Here, only events where the `bytes` field is greater than 65536 will be traced.

### 4. **Getting Event Arguments**
   Each tracepoint provides contextual data, which includes various arguments relevant to the event. To see the format of a tracepoint’s arguments, check the `format` file under `/sys/kernel/debug/tracing/events`. For example:
   ```bash
   cat /sys/kernel/debug/tracing/events/block/block_rq_issue/format
   ```

### 5. **Using BPF for Tracepoints**
   The `bpftrace` tool provides a more customizable way to access tracepoint data. With `bpftrace`, you can filter and format tracepoint arguments concisely:
   ```bash
   bpftrace -e 't:block:block_rq_issue { printf("size: %d bytes\n", args->bytes); }'
   ```

### 6. **Overhead Consideration**
   Tracepoints do introduce some CPU overhead, especially at high event rates (e.g., over 100,000 events per second). Testing tracepoints in a non-production environment is advised to understand their impact.

### 7. **Documentation and Source**
   Documentation for tracepoints can be found in the Linux kernel source under `Documentation/trace/tracepoints.rst`, and more details on specific tracepoints are in `include/trace/events` in the kernel source.

By enabling specific tracepoints, you can gather detailed insights into kernel operations, making tracepoints a valuable resource for performance analysis and debugging.






Common tracepoints in the Linux kernel can be categorized by system activities they monitor, such as block I/O, CPU scheduling, network packets, and file system operations. Here’s a list of common tracepoints you can typically find in `perf list tracepoint`:

### Block I/O Tracepoints
- **`block:block_rq_complete`** - Triggered when a block request completes.
- **`block:block_rq_insert`** - Triggered when a block request is added to the I/O queue.
- **`block:block_rq_issue`** - Triggered when a block request is issued to the hardware.

### Scheduler Tracepoints
- **`sched:sched_wakeup`** - Triggered when a task is woken up.
- **`sched:sched_wakeup_new`** - Triggered when a new task is created and scheduled to run.
- **`sched:sched_switch`** - Triggered when a context switch occurs between two tasks.
- **`sched:sched_process_fork`** - Triggered when a process forks (creates a new child process).
- **`sched:sched_process_exit`** - Triggered when a process exits.

### Network Tracepoints
- **`net:net_dev_queue`** - Triggered when a network packet is queued to the device.
- **`net:net_dev_xmit`** - Triggered when a network packet is transmitted.
- **`tcp:tcp_sendmsg`** - Triggered when sending a TCP message.
- **`tcp:tcp_receive`** - Triggered when receiving a TCP message.

### File System Tracepoints
- **`filemap:write_begin`** - Triggered when a file write operation begins.
- **`filemap:write_end`** - Triggered when a file write operation ends.
- **`vfs:vfs_open`** - Triggered when a file is opened.
- **`vfs:vfs_read`** - Triggered when a file is read.
- **`vfs:vfs_write`** - Triggered when a file is written.

### SCSI Tracepoints
- **`scsi:scsi_dispatch_cmd_start`** - Triggered when a SCSI command is dispatched.
- **`scsi:scsi_dispatch_cmd_done`** - Triggered when a SCSI command completes.
- **`scsi:scsi_dispatch_cmd_error`** - Triggered when there is an error in SCSI command dispatch.

### Networking SKB (Socket Buffer) Tracepoints
- **`skb:consume_skb`** - Triggered when a socket buffer (skb) is consumed.
- **`skb:kfree_skb`** - Triggered when a socket buffer is freed.

### Example Commands to List and Trace Specific Events
To view all available tracepoints, you can use:
```bash
perf list tracepoint
```

To trace a specific tracepoint, for instance `block:block_rq_issue`, you could run:
```bash
perf trace -e block:block_rq_issue
```





The command:

```bash
perf trace -e block:block_rq_issue
```

will set up `perf` to monitor the specific tracepoint `block:block_rq_issue`, which is triggered each time a block I/O request is issued to the hardware.

### What This Command Does:
1. **Monitors Block I/O Events**: It captures instances when a block I/O request is sent to the underlying storage hardware (e.g., when data is read from or written to a disk).
  
2. **Outputs Real-Time Trace Data**: As `perf trace` is running, it will output information to the console each time a `block:block_rq_issue` event occurs. The output typically includes:
   - A timestamp when the event was captured.
   - The process ID (PID) and command responsible for the I/O request.
   - Details about the I/O request (e.g., which block device, read/write operation specifics).

3. **Useful for Performance Analysis**: This helps in understanding the frequency and timing of I/O requests at the block level, which can be useful in diagnosing disk performance bottlenecks, identifying high I/O load processes, or analyzing how applications interact with storage.

### Example Output:
The output might look something like this:
```
    0.1234  [001] 12345   block:block_rq_issue: dev=8,0 sector=123456 nr_sector=8 write
    0.5678  [003] 12345   block:block_rq_issue: dev=8,0 sector=123456 nr_sector=8 read
```
In this example:
- `0.1234` and `0.5678` are timestamps.
- `[001]` and `[003]` are CPU core numbers where the events occurred.
- `12345` is the PID of the process that issued the request.
- `dev=8,0` specifies the device (e.g., `/dev/sda`).
- `sector=123456` and `nr_sector=8` detail the specific block sectors involved in the I/O operation.
- `write` or `read` denotes whether the request is a write or read operation. 

This real-time tracing can continue until you interrupt it, typically with `Ctrl+C`.




This output from `perf trace -e block:block_rq_issue` displays real-time block I/O events. Each line logs a single `block:block_rq_issue` tracepoint, representing a request issued to the block device.

Let's break down each field in a sample entry:

```
68081.807 code/3307 block:block_rq_issue(dev: 271581184, sector: 740883432, nr_sector: 32, bytes: 16384, rwbs: "WS", comm: "code", cmd: "")
```

- **68081.807**: The timestamp of the event, indicating the time in seconds since tracing began.

- **code/3307**: 
  - `code` is the name of the process that issued the request (likely an IDE, editor, or service running as "code").
  - `3307` is the process ID (PID).

- **block:block_rq_issue**: The tracepoint name being monitored, in this case, indicating a block request has been issued.

- **dev: 271581184**: The device identifier. This represents the specific block device (in hex, this would be `0x10400000` or possibly a specific NVMe or HDD device).

- **sector: 740883432**: The starting sector on the device where the I/O operation begins. In disk terms, sectors are small chunks of storage, typically 512 bytes each.

- **nr_sector: 32**: The number of sectors involved in this I/O operation. 

- **bytes: 16384**: Total bytes in the request (in this case, `32 sectors x 512 bytes` equals 16 KB).

- **rwbs: "WS"**: A summary of the I/O operation:
  - `W` indicates a write operation.
  - `S` suggests synchronous (immediate) handling.

- **comm: "code"**: The command (or process) issuing the request. In this example, `code` is the process name.

- **cmd: ""**: The command associated with this block I/O, which is empty here. This field is often empty but can contain specific commands if they were available for tracing.

### Additional Sample Entries

Let's look at other entries to see what’s happening at different points in time:

1. **`68084.170 jbd2/nvme1n1p2/361 block:block_rq_issue(..., rwbs: "WS", comm: "jbd2/nvme1n1p2-", ...)`**:
   - `jbd2/nvme1n1p2` is a journaling process for the device `nvme1n1p2`, handling write operations with synchronous behavior (`WS`).
   - This entry shows the journaling process actively writing to the device.

2. **`68084.397 kworker/0:1H-k/114 block:block_rq_issue(..., rwbs: "FF", comm: "kworker/0:1H", ...)`**:
   - The `kworker` (kernel worker thread) process is issuing a request with `rwbs: "FF"`, indicating:
     - `F` for a flush operation, usually to ensure data integrity by writing cached data to disk.
   - `kworker` processes handle background tasks, often involving disk or I/O management.

3. **`68084.896 code/3307 block:block_rq_issue(..., rwbs: "WS", comm: "code", ...)`**:
   - This shows the same `code` process issuing another write operation, possibly a save or file update.

This trace captures interactions between user processes (`code`), journaling (`jbd2`), and kernel workers (`kworker`), each issuing specific types of I/O operations on the block device. The pattern of these logs can help in diagnosing disk I/O bottlenecks or understanding which processes are generating the most disk activity.





This output from `perf trace -e block:block_rq_issue` displays real-time block I/O events. Each line logs a single `block:block_rq_issue` tracepoint, representing a request issued to the block device.

Let's break down each field in a sample entry:

```
68081.807 code/3307 block:block_rq_issue(dev: 271581184, sector: 740883432, nr_sector: 32, bytes: 16384, rwbs: "WS", comm: "code", cmd: "")
```

- **68081.807**: The timestamp of the event, indicating the time in seconds since tracing began.

- **code/3307**: 
  - `code` is the name of the process that issued the request (likely an IDE, editor, or service running as "code").
  - `3307` is the process ID (PID).

- **block:block_rq_issue**: The tracepoint name being monitored, in this case, indicating a block request has been issued.

- **dev: 271581184**: The device identifier. This represents the specific block device (in hex, this would be `0x10400000` or possibly a specific NVMe or HDD device).

- **sector: 740883432**: The starting sector on the device where the I/O operation begins. In disk terms, sectors are small chunks of storage, typically 512 bytes each.

- **nr_sector: 32**: The number of sectors involved in this I/O operation. 

- **bytes: 16384**: Total bytes in the request (in this case, `32 sectors x 512 bytes` equals 16 KB).

- **rwbs: "WS"**: A summary of the I/O operation:
  - `W` indicates a write operation.
  - `S` suggests synchronous (immediate) handling.

- **comm: "code"**: The command (or process) issuing the request. In this example, `code` is the process name.

- **cmd: ""**: The command associated with this block I/O, which is empty here. This field is often empty but can contain specific commands if they were available for tracing.

### Additional Sample Entries

Let's look at other entries to see what’s happening at different points in time:

1. **`68084.170 jbd2/nvme1n1p2/361 block:block_rq_issue(..., rwbs: "WS", comm: "jbd2/nvme1n1p2-", ...)`**:
   - `jbd2/nvme1n1p2` is a journaling process for the device `nvme1n1p2`, handling write operations with synchronous behavior (`WS`).
   - This entry shows the journaling process actively writing to the device.

2. **`68084.397 kworker/0:1H-k/114 block:block_rq_issue(..., rwbs: "FF", comm: "kworker/0:1H", ...)`**:
   - The `kworker` (kernel worker thread) process is issuing a request with `rwbs: "FF"`, indicating:
     - `F` for a flush operation, usually to ensure data integrity by writing cached data to disk.
   - `kworker` processes handle background tasks, often involving disk or I/O management.

3. **`68084.896 code/3307 block:block_rq_issue(..., rwbs: "WS", comm: "code", ...)`**:
   - This shows the same `code` process issuing another write operation, possibly a save or file update.

This trace captures interactions between user processes (`code`), journaling (`jbd2`), and kernel workers (`kworker`), each issuing specific types of I/O operations on the block device. The pattern of these logs can help in diagnosing disk I/O bottlenecks or understanding which processes are generating the most disk activity.






**Explanation:**

`kprobes` (short for "kernel probes") are a feature in the Linux kernel that allow us to trace or monitor specific parts of the kernel as they execute. They’re particularly useful for examining how the kernel functions work and for diagnosing performance issues. Introduced in Linux version 2.6.9 (2004), `kprobes` give us the ability to track nearly any kernel function or specific instructions, providing a way to analyze system behavior.

### How `kprobes` Work

`kprobes` function by dynamically modifying the code in the kernel. They add small probes (like breakpoints) at specific locations in kernel code, which are then removed when tracing is complete. This setup is useful because it doesn’t change the kernel permanently, and when not used, the kernel functions as if `kprobes` were never added.

For efficiency, `kprobes` can sometimes work alongside `Ftrace` (another tracing mechanism), reducing overhead. However, it’s considered an "unstable API" because it relies on the internal kernel functions, which can change from one version to another.

### Why Use `kprobes`?

`kprobes` are highly flexible and can monitor almost any part of the kernel, making them ideal when other tracing tools aren’t enough. They allow:
- Tracking exact kernel function entries or certain offsets (points within a function).
- Gathering in-depth performance details, such as function call durations, that may not be accessible otherwise.

**Example of `kprobes` Usage:**
Here’s a sample `bpftrace` command using `kprobes` to trace the `do_nanosleep()` function, which puts a process to sleep:

```bash
bpftrace -e 'kprobe:do_nanosleep { printf("sleep by: %s\n", comm); }'
```

This will print the process names that are executing `do_nanosleep()` (e.g., `mysqld` or `/bin/sleep`). The trace is live, and when you stop the command (using `Ctrl+C`), the probes are removed.

### Arguments with `kprobes`

You can also view arguments to the traced function. For example, with `do_nanosleep()`, the `hrtimer_mode` argument can be examined by referencing `arg1` in `bpftrace`:

```bash
bpftrace -e 'kprobe:do_nanosleep { printf("mode: %d\n", arg1); }'
```

### `kretprobes`: Tracing Function Returns

For tracking when a kernel function completes and checking its return value, we use `kretprobes`. These work similarly to `kprobes` but trace the end of a function and can provide data on its execution duration.

**Example with `kretprobes`:**
The following `bpftrace` command measures the time spent in `do_nanosleep()`:

```bash
bpftrace -e 'kprobe:do_nanosleep { @ts[tid] = nsecs; }
kretprobe:do_nanosleep /@ts[tid]/ {
  @sleep_ms = hist((nsecs - @ts[tid]) / 1000000); delete(@ts[tid]); } END { clear(@ts); }'
```

This will print a histogram of `do_nanosleep()` durations, showing how often it returns in zero milliseconds or longer intervals.

### `kprobes` vs. `tracepoints`

`kprobes` and `tracepoints` are both kernel tracing mechanisms but have different characteristics:

| Detail                    | kprobes               | Tracepoints      |
|---------------------------|-----------------------|------------------|
| Type                      | Dynamic               | Static           |
| Number of Events Available| 50,000+               | 1,000+           |
| Kernel Maintenance        | None                  | Required         |
| Disabled Overhead         | None                  | Tiny (NOPs + metadata) |
| Stability                 | No (unstable)         | Yes (stable)     |

- **Dynamic vs. Static**: `kprobes` can dynamically trace any function in the kernel, while `tracepoints` are fixed (defined in the kernel source code).
- **Overhead**: Both are efficient when not active, but `kprobes` can add higher overhead than `tracepoints` when probing within functions (rather than just at function entries).

### Summary of Key Points

1. **`kprobes` are highly flexible** and can trace almost any kernel function or instruction.
2. **No kernel maintenance is required** with `kprobes`, unlike `tracepoints`, which are embedded and maintained in the kernel.
3. **Dynamic and powerful**, `kprobes` are helpful for real-time kernel debugging and performance analysis, especially when no other tracing options work.
4. **Function Arguments and Returns**: `kprobes` can track arguments, while `kretprobes` trace function returns, making them great for measuring function durations.
5. **Higher Overhead Potential**: Although efficient when not used, active `kprobes` may cause higher overhead than `tracepoints`, depending on their application.



**Explanation in Simple Words:**
uprobes, short for user-space probes, allow for tracing of functions within user-space applications and libraries. They are similar to kprobes (which trace kernel functions) but are designed specifically for user-space processes, providing access to the internal workings of applications. uprobes became available in Linux version 3.5 (released in 2012) and are commonly used in debugging or tracing application-specific performance issues. By setting a uprobe, a tracer can monitor specific functions within an application, similar to how breakpoints work in debuggers—meaning the function executes normally unless a trace is active.

For instance, you can use a tool like `bpftrace` to list possible uprobe entry points for any application or library, such as the Bash shell. uprobes can also capture arguments of the functions they trace, providing further insight into function usage. When used with uretprobes (user-space return probes), uprobes can also trace function return values, which allows measuring the time taken by a function to execute. However, uretprobes may introduce higher CPU overheads, especially for tracking quick function calls, due to their kernel-level trapping mechanism.

---

**Summary of Key Points:**

1. **Purpose**: uprobes are probes for tracing functions within user-space applications, useful for performance monitoring and debugging.

2. **Functionality**: 
   - uprobes can trace function entries.
   - uretprobes can trace function exits and measure execution duration when used alongside uprobes.
   - uprobes dynamically create trace events without modifying application code until tracing starts.

3. **Usage Example**: Using `bpftrace`, you can trace function calls in user-space programs like Bash, retrieve arguments, and observe execution details.

4. **Overhead**: uprobes incur more CPU cost than kernel-level kprobes due to kernel trapping, with uretprobes being the costliest due to their return mechanism.

5. **Documentation**: uprobes are documented in Linux under `Documentation/trace/uprobetracer.rst`. Advanced details are found in *BPF Performance Tools* by Brendan Gregg.

**Example Command**:
To list uprobe entry points for Bash, use:
```bash
bpftrace -l 'uprobe:/bin/bash:*'
```

For tracing arguments of a specific function, such as `decode_prompt_string`, use:
```bash
bpftrace -e 'uprobe:/bin/bash:decode_prompt_string { printf("%s\n", str(arg0)); }'
```

This outputs the first argument of the `decode_prompt_string` function whenever it’s called.



Here are some practical examples of uprobes that can help monitor and debug user-space applications:

### 1. **Trace MySQL Query Execution Times**
   To observe query execution times in a MySQL server, you can set uprobes on key functions within the MySQL binary. This example traces the `dispatch_command` function to check when a command begins executing and `net_end_statement` to observe when it ends.

   ```bash
   sudo bpftrace -e '
   uprobe:/usr/sbin/mysqld:dispatch_command { @start[tid] = nsecs; }
   uretprobe:/usr/sbin/mysqld:net_end_statement /@start[tid]/ {
       printf("Query duration (ms): %d\n", (nsecs - @start[tid]) / 1000000);
       delete(@start[tid]);
   }'
   ```
   **Explanation**: This command tracks each SQL query’s execution time, giving insights into performance bottlenecks directly from the MySQL server.

### 2. **Trace Python Function Calls**
   To analyze a specific function call in Python applications, you can use uprobes on the Python binary. For instance, this example traces the `PyEval_EvalFrameEx` function, responsible for executing Python bytecode.

   ```bash
   sudo bpftrace -e '
   uprobe:/usr/bin/python3:PyEval_EvalFrameEx { @pyfunc[tid] = nsecs; }
   uretprobe:/usr/bin/python3:PyEval_EvalFrameEx /@pyfunc[tid]/ {
       printf("Python function execution time (ms): %d\n", (nsecs - @pyfunc[tid]) / 1000000);
       delete(@pyfunc[tid]);
   }'
   ```
   **Explanation**: This setup allows tracing of all Python function execution times, which is useful for pinpointing slow or frequently called functions in a Python application.

### 3. **Monitoring Bash Command Executions**
   Using uprobes with `bpftrace`, you can monitor specific Bash function calls, such as `readline` for tracking input commands or `execute_command` to track command execution.

   ```bash
   sudo bpftrace -e '
   uprobe:/bin/bash:execute_command { printf("Command executed: %s\n", str(arg0)); }'
   ```
   **Explanation**: This command outputs every command executed in a Bash session, which is useful for logging command usage or auditing purposes.

### 4. **Capture Return Values from a Function**
   Sometimes, it’s helpful to monitor return values of functions to understand their results without modifying application code. For example, tracking return values from a database library function to log query errors:

   ```bash
   sudo bpftrace -e '
   uprobe:/usr/lib/libsqlite3.so:sqlite3_exec { @start[tid] = nsecs; }
   uretprobe:/usr/lib/libsqlite3.so:sqlite3_exec /@start[tid]/ {
       printf("SQLite query execution time (ms): %d\n", (nsecs - @start[tid]) / 1000000);
       delete(@start[tid]);
   }'
   ```
   **Explanation**: This measures SQLite query execution times by attaching uprobes and uretprobes on the SQLite function `sqlite3_exec`.




   This text covers two main topics: **User-level Statically-Defined Tracing (USDT)** and **Hardware Counters (PMCs)** for performance monitoring in Linux systems. Here's a breakdown of the essential content:

### 1. **User-level Statically-Defined Tracing (USDT)**
   - **What is USDT?**
     - USDT allows applications to provide fixed points in their code (probes) for tracing performance and behavior. It’s a way to trace specific application-level events in a standardized manner.
     - It’s designed to work with user-space applications (i.e., non-kernel applications) and helps trace specific internal events or actions in programs.
   
   - **How is it different from other tracing methods?**
     - USDT is to **uprobes** (user-space probes) as kernel-space **tracepoints** are to **kprobes** (kernel-space probes).
     - USDT probes provide a stable API for observing specific actions, unlike custom logging, which doesn’t connect with other kernel-level events.

   - **Examples of USDT Probes**
     - USDT probes are pre-defined in applications and libraries, like in **OpenJDK** and **PostgreSQL**:
       - Example for OpenJDK:
         ```
         bpftrace -lv 'usdt:/usr/lib/jvm/openjdk/libjvm.so:*'
         ```
         - This lists probes in the JVM library that monitor events such as Java class loading, method compilation, and garbage collection.
   
   - **Benefits of USDT Probes**
     - Unlike standard logging, USDT allows correlating application events with lower-level system activities, such as I/O operations.
     - For example, it could reveal if a database query slowed down due to issues like file lock contention, instead of just I/O wait times.

   - **Enabling USDT**
     - Some applications include USDT probes by default; others require recompiling with an option (e.g., `--enable-dtrace-probes` for Java).

### 2. **Hardware Counters (PMCs)**
   - **What are PMCs?**
     - Performance Monitoring Counters (PMCs) are hardware-based counters on CPUs that track specific low-level events, providing insights into CPU efficiency and memory/cache usage.

   - **Types of Events Monitored by PMCs**
     - Examples include cycles (CPU ticks), instructions executed, cache hits/misses, branch predictions, and more.
   
   - **Using PMCs with `perf` Tool**
     - The `perf` command in Linux leverages PMCs to monitor and analyze system and application performance.
     - Example command:
       ```
       perf stat gzip words
       ```
       - This collects statistics on CPU utilization, context switches, instruction efficiency, etc., while running the `gzip` command.
   
   - **PMC Limitations**
     - PMCs are hardware-specific and may not be available on all cloud platforms.
     - Challenges include limited register space (only a few events can be counted simultaneously) and accuracy issues (e.g., “skid” effect, where sampled data lags slightly).
   
   - **PMC Use Cases**
     - Commonly used for diagnosing and improving application performance by identifying bottlenecks at the hardware level.

### Summary of Key Points:
   - **USDT** is valuable for monitoring specific user-space application events and can be combined with kernel events for deep insight.
   - **PMCs** provide low-level performance metrics critical for CPU and memory optimization but have hardware limitations and may be restricted on cloud instances.


This section provides details on additional sources for system observability and tracing. Here’s a summary of each:

- **MSRs (Model-Specific Registers)**: Used for monitoring hardware performance and system configuration. MSRs give insights like CPU clock rates, temperature, and power usage, although the specifics vary by processor model, BIOS settings, and virtualization. They allow precise cycle-based measurements for CPU utilization.

- **ptrace(2)**: A syscall for tracing processes, mainly used for debugging with tools like `gdb` and `strace`. It is breakpoint-based and can significantly slow down the target process. For syscall tracing, Linux has efficient tracepoints, which reduce overhead compared to ptrace.

- **Function Profiling**: Kernel functions on x86 have hooks (`mcount()` or `__fentry__()`) for tracing function calls with tools like Ftrace. These hooks default to no-operation (nop) until tracing is enabled, reducing impact on performance.

- **Network Sniffing (libpcap)**: Captures packets for network analysis, typically accessed through `/proc/net/dev` and tools like `tcpdump`. Packet capture incurs CPU and storage overheads, especially when analyzing all packets.

- **netfilter conntrack**: Part of Linux’s netfilter system, enabling network flow tracking, not limited to firewall rules. It logs connection events and is useful for detailed network traffic analysis.

- **Process Accounting**: Originally for resource usage tracking, process accounting is still used on Linux to capture data on short-lived processes that may be missed by other sampling methods, such as `/proc` snapshots. Tools like `atop` utilize this data for granular process monitoring.

- **Software Events**: These events, often related to hardware events but monitored in software, include occurrences like page faults. They are accessible through `perf_event_open(2)` and are utilized by tools like `perf` and `bpftrace`.

- **System Calls for Resource Metrics**: System calls like `getrusage(2)` allow processes to access their own resource usage statistics, providing data on CPU time, memory faults, message passing, and context switches.

Other tools and frameworks, such as **I/O accounting**, **blktrace**, **timer_stats**, **lockstat**, and **debugfs**, may also be available depending on the kernel version and configurations. For additional observability options, kernel source code may offer insight into which statistics or tracepoints are implemented.

- **Solaris Kstat Framework**: On Solaris-based systems, the kernel statistics (Kstat) framework organizes system statistics in a consistent, four-tuple structure (`module:instance:name:statistic`). Unlike Linux’s `/proc/stat`, Kstat offers a structured and binary interface, which reduces CPU overhead from text parsing. For instance, the `kstat` command can read the current number of processes using:
  ```
  $ kstat -p unix:0:system_misc:nproc
  ```



