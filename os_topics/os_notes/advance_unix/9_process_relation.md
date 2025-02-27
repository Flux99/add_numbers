


this is the start
### Summary: Process Relationships (Chapter 9)

#### 9.1 Introduction

This chapter explores the relationships between processes in UNIX-like systems. Key concepts include:
- **Parent and Child Processes**: Every process has a parent, which is typically the initial kernel-level process (process ID 1). The parent is notified when the child terminates and can retrieve the child’s exit status.
- **Process Groups and Sessions**: Process groups are collections of related processes, and POSIX introduced sessions, which are a broader concept of managing related processes. The chapter discusses how login shells and the processes they spawn fit into these structures.
- **Signals**: The chapter explains the relationship between processes in terms of signals, which are used to communicate between processes. A basic understanding of UNIX signals is needed to fully grasp the content.

#### 9.2 Terminal Logins

Terminal logins are crucial in UNIX systems, as they represent the interaction between a user and the system.

- **Early UNIX Systems**: Initially, users logged in via dumb terminals (local or remote), which were connected through devices like DH-11 and DZ-11. These terminals had a fixed limit on the number of simultaneous logins.
  
- **Windowing Systems**: As windowing systems emerged, graphical terminals were introduced to emulate character-based terminals. On some platforms, the windowing system is started automatically after login, whereas on others, it requires a manual login.

- **Login Procedure**: The process of logging in through a terminal typically follows these steps:
  1. The `init` process reads `/etc/ttys` (or equivalent file) to configure terminals.
  2. For each terminal that allows login, `init` spawns the `getty` program.
  3. The `getty` program opens the terminal device, prompts for the user’s login name, and invokes the `login` program once the username is entered.
  4. The `login` program performs user authentication (password verification) and, if successful, invokes the login shell, completing the login process.

##### BSD Terminal Login Procedure
- The BSD login process has remained largely unchanged for over 35 years.
- The system administrator configures terminal devices using `/etc/ttys`, which defines the parameters for the `getty` program.
- `init` is responsible for managing terminal login sessions by forking a `getty` process per terminal device.
  
##### The Login Program
- **Authentication**: The `login` program checks the username, prompts for a password, and verifies the password using cryptographic techniques. If authentication fails, `login` will restart the login process.
- **Post-login Actions**: After successful authentication, `login` performs several actions:
  - Changes to the user’s home directory.
  - Sets permissions for the terminal device.
  - Initializes the environment (e.g., `HOME`, `SHELL`, `USER`).
  - Calls `setuid` to change user privileges and invokes the login shell.
  
  The login shell is invoked with a special flag (e.g., `-sh`) to indicate it is a login shell, prompting it to modify its behavior accordingly.

- **Modern Authentication (PAM)**: Modern UNIX systems like FreeBSD, Linux, Mac OS X, and Solaris support Pluggable Authentication Modules (PAM), which offer flexibility in configuring various authentication methods.

##### Mac OS X Terminal Login
- The login procedure on Mac OS X is similar to BSD but with some differences:
  - The work of `init` is performed by `launchd`.
  - A graphical-based login screen is presented from the start.

##### Linux Terminal Login
- The Linux login process is derived from the BSD procedure but has some key differences:
  - Linux uses a variety of configurations, including `/etc/inittab` (for older systems) or `/etc/init` (for systems using Upstart).
  - Terminal configuration varies depending on the Linux distribution.

##### Solaris Terminal Login
- Solaris supports two forms of terminal logins: 
  1. **Getty Style**: Similar to BSD.
  2. **TTymon Style**: Introduced in SVR4, this method is used for terminal logins, providing a consistent way to administer terminal services.

  In both styles, `init` or its equivalent is the parent process for the login shell. The difference lies in the use of `ttymon` for terminal login processes instead of `getty`.

#### Key Concepts and Differences

- **Terminal Device**: The device representing the terminal that the user interacts with during login. It is opened by `getty` or `ttymon`.
- **Login Shell**: The shell that is invoked after successful authentication. It reads user-specific startup files to configure the environment and display the prompt.

#### 9.3 Terminal Devices and File Descriptors

- **File Descriptors**: The login shell inherits file descriptors for the terminal device, allowing it to read and write to the terminal.
- **Terminal Devices for Different Systems**: Different UNIX-like systems (BSD, Linux, Mac OS X, Solaris) have slight variations in how terminal devices and login processes are configured, but the underlying concepts remain similar.

### Conclusion

Understanding the relationships between processes during terminal logins is fundamental to grasping how UNIX-like systems handle user sessions. The parent-child process structure, along with the use of process groups and sessions, forms the backbone of process management. The detailed login procedures, especially the role of `init`, `getty`, and `login`, ensure that users are authenticated securely before gaining access to a shell where they can execute commands.

By mastering these relationships and processes, you will gain insights into how user sessions are established and managed in UNIX-like systems, which is essential knowledge for system administrators and anyone working with UNIX.




### Detailed Summary of Network Logins (Section 9.3)

Network logins differ from traditional terminal logins mainly due to the connection type and the software mechanisms involved. Below is a detailed breakdown of the concepts and process flows described in the section:

#### 1. **Key Differences Between Terminal and Network Logins**:
   - **Terminal Logins**: In a traditional terminal login, `init` knows which terminal devices are available and spawns a `getty` process for each terminal device. Each login attempt on a terminal is handled by a process dedicated to that device.
   - **Network Logins**: For network logins, since the connection isn't point-to-point like a serial terminal, a more flexible approach is used. Network login requests are handled through kernel network interface drivers, and the system doesn't know ahead of time how many connections will occur. Instead of waiting for a process dedicated to each login, the system waits for incoming network connection requests.

#### 2. **Pseudo Terminals**:
   - **Pseudo Terminal**: To handle network logins like terminal logins, a pseudo terminal is used to emulate the behavior of a serial terminal. It maps terminal operations to network operations and vice versa, allowing software designed for terminal logins to work with network logins as well.

#### 3. **Network Logins in BSD Systems**:
   - **The Role of `inetd`**: In BSD systems, the `inetd` process (Internet superserver) is responsible for managing network logins. The process waits for network connection requests and spawns the appropriate programs when a connection request arrives.
     - During system startup, `init` invokes a shell that runs the `/etc/rc` script. This script starts `inetd`, which then waits for incoming network connection requests.
   - **Network Login via TELNET**: 
     - The sequence begins when a TELNET client initiates a TCP connection to a server.
     - `inetd` handles the request and starts the TELNET server (`telnetd`).
     - `telnetd` opens a pseudo terminal, forks itself into two processes: the parent handles the network connection, while the child executes the login program.
     - The login program performs steps like setting the user’s environment and privileges, and then execs the login shell.
     - The user is now logged in and can interact with the system as though they were using a local terminal.
     - The setup involves the network connection being established between the TELNET client and the TELNET server (`telnetd`), with data exchanged through the TELNET application protocol.

   - **Diagram**:
     - A process flow diagram is provided (Figure 9.4) showing how `inetd` forks and executes `telnetd`, which further interacts with the `login` program and the shell. The processes are connected through a pseudo terminal device.

#### 4. **Arrangement of Processes After a Network Login**:
   - After the login process completes, the user’s login shell operates through a pseudo terminal device, not directly through a physical terminal.
   - The key observation is that both terminal and network logins lead to the same final setup: a login shell with its standard input, output, and error connected to a terminal or a pseudo terminal device.
   - The pseudo terminal mechanism helps emulate the terminal-like interaction for network logins.

#### 5. **Mac OS X Network Logins**:
   - Mac OS X (based on FreeBSD) uses a similar process to BSD for network logins, but it uses `launchd` to manage system services (including the TELNET daemon).
   - TELNET is disabled by default on Mac OS X and can be enabled via `launchctl`.
   - The preferred method for network login on Mac OS X is using `ssh` (secure shell), which is more secure than TELNET.

#### 6. **Linux Network Logins**:
   - Network logins under Linux are similar to BSD systems, but Linux often uses `xinetd`, a more advanced version of `inetd`.
   - `xinetd` provides more granular control over the services it starts, compared to `inetd`.

#### 7. **Solaris Network Logins**:
   - Solaris uses a similar process to BSD and Linux for network logins. The key difference is that Solaris’ `inetd` runs as a "restarter" in the Service Management Facility (SMF), a framework that manages and monitors system services.
   - The restarter daemon ensures that services are automatically restarted if they fail, adding an extra layer of service reliability.
   - Like BSD, Solaris still uses the `inetd` service for handling network logins, but it is integrated into the SMF system for service management and monitoring.

#### 8. **Service Management Facility (SMF) in Solaris**:
   - The **SMF** in Solaris is a service management framework that allows for the management of system services, including their start, stop, and automatic restart in case of failure.
   - The `inetd` service in Solaris is a part of this framework and is monitored by the SMF’s master restarter, which starts the necessary processes.

#### 9. **Common Steps in Network Login Across Systems**:
   - The general flow of network logins is as follows across systems like BSD, Linux, Solaris, and Mac OS X (except for small differences in service management):
     1. **init** starts the system and spawns a shell script (`/etc/rc`).
     2. **inetd** (or `xinetd` in Linux) is started by `init` and waits for incoming TCP connections.
     3. When a network connection arrives (e.g., for TELNET), **inetd** forks and executes the corresponding server (e.g., `telnetd`).
     4. **telnetd** opens a pseudo terminal, forks again, and the child process executes the login program.
     5. The login program sets up the user environment and executes the user’s login shell.

### Conclusion:
Network logins across different systems (BSD, Mac OS X, Linux, Solaris) follow similar principles, but with slight variations in the details like service management. The key concept is the use of a pseudo terminal to emulate terminal behavior and handle communication between network processes and the user login shell. The underlying mechanism involves a server process waiting for network requests and spawning appropriate programs to handle the login.

For exams, focus on the overall process of network logins (including the use of `inetd`, `telnetd`, and pseudo terminals) and understand how different operating systems handle these logins with slight variations in service management.




### Detailed Summary of Process Groups and Sessions (Section 9.4 & 9.5)

#### **9.4 Process Groups**

1. **Process Group Definition**:
   - A process group is a collection of one or more processes that can receive signals from the same terminal.
   - Each process group has a **unique process group ID (PGID)**.
   - Process group IDs are positive integers stored in a `pid_t` type, similar to process IDs.

2. **Functions Related to Process Groups**:
   - **getpgrp()**:
     - Returns the process group ID of the calling process.
     - Syntax: 
       ```c
       pid_t getpgrp(void);
       ```

   - **getpgid(pid_t pid)**:
     - Returns the process group ID of the process with the specified `pid`.
     - If `pid == 0`, it behaves like `getpgrp()` and returns the process group ID of the calling process.
     - Syntax: 
       ```c
       pid_t getpgid(pid_t pid);
       ```

3. **Process Group Leader**:
   - Each process group has a **process group leader**, which is the process whose **process ID equals the process group ID**.
   - The leader can create processes and other groups, but the group persists as long as at least one process is in the group.

4. **Creating and Managing Process Groups**:
   - A process can create or join a process group using the **setpgid()** function.
   - **setpgid()** sets the process group ID of a specified process (`pid`). If the process is the group leader, the `pid` and `pgid` are equal.
   - **setpgid()** Syntax:
     ```c
     int setpgid(pid_t pid, pid_t pgid);
     ```
     - If `pid == 0`, the process ID of the calling process is used.
     - If `pgid == 0`, the process ID specified by `pid` is used as the process group ID.
     - A process can only set its own process group ID or that of its children.

5. **Race Conditions in Process Group Creation**:
   - To avoid race conditions when assigning a process to a group, the parent process should set the process group ID of the child after a `fork`.
   - Both processes will have the correct process group set, ensuring no conflicts.

6. **Signals and Process Groups**:
   - Signals can be sent to a process or an entire process group. The method for sending signals to groups will be covered in Chapter 10.

#### **9.5 Sessions**

1. **Session Definition**:
   - A session is a collection of one or more process groups.
   - A session can be visualized as a collection of jobs (groups of related processes).
   - Example:
     - A shell pipeline with multiple processes can form a session with several process groups.

2. **Creating a New Session**:
   - A process can create a new session by calling the **setsid()** function.
   - **setsid()** does three things:
     1. The calling process becomes the **session leader** of the new session.
     2. The process becomes the **process group leader** of a new process group, with the same process ID as the calling process.
     3. The process has no controlling terminal. If the process had a controlling terminal before, the association is broken.
   
   - **setsid()** Syntax:
     ```c
     pid_t setsid(void);
     ```
     - If successful, it returns the **process group ID** of the new session. Otherwise, it returns `-1` on error.

3. **Important Considerations with setsid()**:
   - A process that is already a process group leader cannot call `setsid()`. To avoid this error, the typical practice is to:
     1. Call `fork()`.
     2. Have the parent process terminate and the child continue.
     3. This ensures the child is not a process group leader and can safely create a new session.
   
4. **Session Leader and Session ID**:
   - The **session leader** is the first process to create the session, and it is the only process in the new session initially.
   - While the Single UNIX Specification does not use the term "session ID," it refers to the **process group ID of the session leader** as a form of session identification.
   - The **getsid()** function retrieves the process group ID of a process's session leader.

   - **getsid()** Syntax:
     ```c
     pid_t getsid(pid_t pid);
     ```
     - If `pid == 0`, the function returns the process group ID of the calling process's session leader.

5. **Session Grouping and Controlling Terminals**:
   - When a process calls `setsid()`, it loses its controlling terminal if it had one previously.
   - This is important in the context of daemon processes, which need to run without a controlling terminal.

### **Key Concepts Summary**

- **Process Groups**:
  - Collection of processes that can receive signals from the same terminal.
  - Each process group has a unique ID.
  - Process group leader is the process whose ID equals the group ID.

- **Session**:
  - Collection of process groups.
  - A session is created by calling `setsid()`.
  - The calling process becomes the session leader and is placed in its own process group.

- **Control of Process Groups and Sessions**:
  - Functions like `getpgrp()`, `getpgid()`, `setpgid()`, `setsid()`, and `getsid()` manage process group and session behavior.
  - A process can set its process group ID or the process group ID of its children, but it cannot change its group after calling `exec()`.
  
### **Study Tips**
- Understand the relationship between processes, process groups, and sessions.
- Focus on the usage of functions like `setpgid()`, `getpgid()`, `setsid()`, and `getsid()`.
- Remember the difference between **process group ID** and **session leader process group ID**.
- Pay attention to how controlling terminals are handled, especially when creating daemon processes.

This should cover all the essential points regarding **process groups** and **sessions**, providing a solid understanding for exam preparation.








### Detailed Summary: **Controlling Terminal, Process Groups, Sessions, and Related Concepts**

In Unix-like operating systems, **sessions**, **process groups**, and the **controlling terminal** are essential components for managing processes, controlling terminal input/output, and handling job control. Understanding these concepts is crucial for process management, especially when dealing with terminal-based input/output and signal handling.

#### **1. Controlling Terminal**
A **controlling terminal** is the terminal device (or pseudo-terminal) associated with a **session**. It serves as the interface for user interaction with the system, and processes within the session interact with it for input and output.

- **Controlling Process**: The **session leader** that establishes the connection to the controlling terminal is called the **controlling process**. This process controls the terminal, managing input and output between the session and the terminal.

- **Terminal Allocation**: A session can have only one controlling terminal. The allocation of the controlling terminal varies between different Unix implementations:
  - **System V**: Allocates the controlling terminal when the session leader opens the first terminal device, as long as the `O_NOCTTY` flag is not specified.
  - **BSD**: Allocates the controlling terminal when the session leader uses the `TIOCSCTTY` ioctl command, usually after calling `setsid()` to ensure the process is a session leader without a controlling terminal.
  - **Mac OS X (derived from BSD)**: Behaves like System V for controlling terminal allocation.

#### **2. Session and Process Groups**
A **session** is a collection of processes, typically created by a **session leader**. A session can have multiple **process groups**, each of which is a collection of processes that can be managed together.

- **Session Leader**: The first process in the session that creates the session and has no controlling terminal until a terminal is allocated.
  
- **Process Groups**:
  - A **process group** consists of one or more processes that can receive signals together. Each process group has a **process group ID (PGID)**, which is the PID of the **process group leader**.
  - There are two types of process groups within a session:
    - **Foreground Process Group**: The group of processes currently interacting with the terminal. It is the group that receives terminal input and terminal-generated signals.
    - **Background Process Groups**: All other process groups in the session that are not interacting with the terminal.

#### **3. Foreground and Background Process Groups**
- A session has a **foreground process group** and one or more **background process groups**.
  - **Foreground Process Group**: The process group currently controlling the terminal for input/output. When you press keys like **Control-C** or **Control-backslash**, signals are sent to all processes in the foreground process group.
  - **Background Process Groups**: Any process groups that are not the foreground process group. They do not receive terminal input or terminal-generated signals.

- **Signals**:
  - When the **interrupt key** (often **Control-C**) is pressed, the interrupt signal is sent to all processes in the **foreground process group**.
  - When the **quit key** (often **Control-backslash**) is pressed, the quit signal is sent to all processes in the **foreground process group**.
  - A **hang-up signal** is sent to the **controlling process (session leader)** if a modem or network disconnect occurs.

#### **4. Controlling Terminal Functions**
- **open("/dev/tty")**: A program can use this function to guarantee that it is talking to the controlling terminal, even if the standard input/output is redirected. If the program does not have a controlling terminal, the open will fail.

- **getpass()**: An example of a program that interacts with the controlling terminal is `getpass()`, which reads a password without echoing input to the screen. This function interacts with the controlling terminal to handle secure password entry.

#### **5. tcgetpgrp, tcsetpgrp, and tcgetsid Functions**
These functions are used to manage **foreground process groups** and **session leader's process group ID** in relation to the controlling terminal.

1. **tcgetpgrp**:
   - **Prototype**: `pid_t tcgetpgrp(int fd);`
   - **Purpose**: Returns the **process group ID of the foreground process group** associated with the terminal.
   - **Return**: If successful, it returns the **PGID** of the foreground process group. If there is an error, it returns `-1`.

2. **tcsetpgrp**:
   - **Prototype**: `int tcsetpgrp(int fd, pid_t pgrpid);`
   - **Purpose**: Sets the **foreground process group ID** to `pgrpid` for the terminal associated with the file descriptor `fd`.
   - **Return**: Returns `0` if successful, `-1` on error.
   - **Conditions**: The `pgrpid` must refer to a process group in the **same session**. The file descriptor `fd` must refer to the controlling terminal of the session.

3. **tcgetsid**:
   - **Prototype**: `pid_t tcgetsid(int fd);`
   - **Purpose**: Returns the **process group ID of the session leader** for the session associated with the terminal referred to by `fd`.
   - **Return**: The **session leader's PGID** if successful, `-1` on error.

#### **6. Job Control**
Job control allows users to manage processes running in the background and foreground. The **foreground process group** is responsible for interacting with the terminal and receiving signals like interrupts. The **background process groups** do not interact with the terminal directly.

- Job control is essential for terminal-based user interfaces, enabling users to control and manage processes, stop and resume processes, and manage signals between foreground and background jobs.

#### **7. Summary of Key Concepts**
- **Controlling Terminal**: A terminal device or pseudo-terminal associated with a session, managed by the session leader (controlling process).
- **Session Leader**: The process that creates the session and may acquire the controlling terminal.
- **Process Groups**: Collections of processes that can receive signals together; the **foreground process group** interacts with the terminal.
- **Foreground vs Background Process Groups**: The foreground group handles terminal input/output, while background groups do not.
- **Signals**: Terminal signals like **interrupt** (Control-C) and **quit** (Control-backslash) are sent to processes in the foreground process group.
- **tcgetpgrp/tcsetpgrp/tcgetsid**: Functions that help manage process groups and session leader information in relation to the controlling terminal.

### **Key Differences in Controlling Terminal Allocation**
- **System V**: Allocates the controlling terminal when the session leader opens the first terminal device, provided the `O_NOCTTY` flag is not used.
- **BSD**: Allocates the controlling terminal when the session leader uses the `TIOCSCTTY` ioctl command.
- **Mac OS X**: Allocates the controlling terminal similarly to **System V**.

### **Practical Example: Using `/dev/tty` and `getpass()`**
When a program like `crypt` requires user input for passwords, even if the standard input is redirected (e.g., via a pipeline), it still needs to read from the controlling terminal. This is done by opening `/dev/tty`, which refers to the controlling terminal, ensuring secure password entry.

---

By understanding the role of the **controlling terminal**, **sessions**, and **process groups**, along with functions like `tcgetpgrp`, `tcsetpgrp`, and `tcgetsid`, you'll be able to manage and control processes more effectively, especially in environments requiring job control and terminal interaction. This knowledge is crucial for system administration, process management, and building interactive command-line programs.



### Detailed Summary of Job Control (Section 9.8)

#### **Introduction to Job Control:**
Job control is a feature in UNIX-like systems that allows users to manage processes running in the terminal, enabling the user to run jobs in the foreground or background. This feature was introduced in BSD (Berkeley Software Distribution) around 1980 and is supported in most modern shells. POSIX (Portable Operating System Interface) has standardized job control, and it's now a required feature of POSIX.1.

#### **Requirements for Job Control:**
1. **Shell Support:** The shell must support job control (e.g., C shell, Korn shell, Bourne shell, or Bash).
2. **Terminal Driver Support:** The kernel’s terminal driver must support job control functionality.
3. **Kernel Support:** The kernel must be able to send job-control signals (e.g., `SIGTSTP`, `SIGCONT`, `SIGINT`, etc.).

#### **Overview of Job Control in POSIX:**
Job control allows a user to launch and manage jobs (groups of processes) in the terminal. A **job** typically refers to a group of processes initiated by a single command (e.g., `vi main.c` is a job with one process). Jobs can be run in the **foreground** or **background**.

- **Foreground Job:** A job that is actively interacting with the terminal, receiving input and displaying output.
- **Background Job:** A job that runs without interacting with the terminal (it doesn’t require user input).

#### **Types of Jobs and Commands:**
- **Foreground Job Example:**
  ```sh
  vi main.c
  ```
  The `vi` command runs in the foreground and directly interacts with the terminal.

- **Background Job Example:**
  ```sh
  make all &
  pr *.c | lpr &
  ```
  Here, the `make all` and `pr *.c | lpr` commands are background jobs, denoted by the `&` symbol. Background jobs run independently of the terminal's user input.

#### **Job Control in Shells:**
Various shells support job control, and their implementation may vary slightly:
- **C Shell (csh):** Fully supports job control.
- **Bourne Shell (sh):** Does not initially support job control but does in modern versions (e.g., SVR4 Bourne shell with `jsh`).
- **Korn Shell (ksh):** Supports job control.
- **Bash (Bourne Again Shell):** Supports job control.

When a background job starts, the shell assigns a **job identifier (jid)** and shows the **process ID (PID)**:
Example:
```sh
$ make all > Make.out &
[1] 1475
$ pr *.c | lpr &
[2] 1490
```
Here, the job `make all > Make.out &` is job 1 with PID 1475, and `pr *.c | lpr &` is job 2 with PID 1490.

#### **Job Status Reporting:**
- The shell typically prints job status only when it is about to show the prompt, not while you're entering commands.
- When a background job finishes, the shell shows a message like:
  ```sh
  [1] + Done make all > Make.out
  [2] + Done pr *.c | lpr
  ```

#### **Terminal Driver and Special Characters:**
The terminal driver plays a key role in job control. It can send special signals to the foreground process group based on keypresses:
- **SIGINT** (Interrupt) – Sent by pressing **Ctrl+C**.
- **SIGQUIT** (Quit) – Sent by pressing **Ctrl+\**.
- **SIGTSTP** (Stop) – Sent by pressing **Ctrl+Z** to suspend the foreground process.

#### **Foreground and Background Jobs Interaction with the Terminal:**
- **Foreground Process Group:** Only the foreground job receives terminal input (such as keyboard input). It has direct access to the terminal.
- **Background Process Group:** Background jobs do not receive terminal input and can only write output to the terminal. If a background job attempts to read from the terminal, the terminal driver sends it the `SIGTTIN` signal (stopping the job).
  
#### **Handling Stopped Background Jobs (SIGTTIN):**
- If a background job tries to read from the terminal, the terminal driver detects this and sends the **SIGTTIN signal** to stop the background job.
  - **Example:** 
    ```sh
    $ cat > temp.foo &
    [1] 1681
    [1] + Stopped (SIGTTIN)
    ```
    Here, the `cat` job is stopped because it tried to read from the terminal, which it can't do since it is running in the background.

#### **Bringing Stopped Jobs into the Foreground (fg Command):**
To bring a stopped background job back to the foreground, the user can use the `fg` command:
```sh
$ fg %1
```
This resumes the stopped job in the foreground. The shell sends the `SIGCONT` signal to continue the process, and the job is now in the foreground.

#### **Disallowing Background Jobs from Accessing the Terminal:**
- By default, background jobs can output to the controlling terminal.
- Using the `stty` command, we can prevent background jobs from writing to the terminal:
  ```sh
  $ stty tostop
  $ cat temp.foo &
  ```
  When `stty tostop` is enabled, the background job will be stopped with a **SIGTTOU** signal when it tries to write to the terminal. This prevents background jobs from cluttering the terminal with output.

#### **Example of Stopped Background Job Due to SIGTTOU:**
```sh
$ stty tostop
$ cat temp.foo &
[1] 1721
[1] + Stopped(SIGTTOU)
```
The `cat` job is stopped because it tried to write to the terminal while running in the background.

To bring the job into the foreground and allow it to complete:
```sh
$ fg %1
```
This command resumes the job in the foreground, and it completes as expected.

#### **Summary of Job Control Features:**
- **Foreground Job:** Interacts with the terminal, receives user input, and outputs to the terminal.
- **Background Job:** Runs without terminal interaction, does not receive input, and can write to the terminal only if allowed.
- **Job Control Commands:**
  - **fg %job_number:** Bring a stopped or background job into the foreground.
  - **bg %job_number:** Continue a stopped job in the background.
  - **jobs:** List all jobs and their statuses.

#### **Job Control and Terminal Communication:**
The terminal driver ensures that only the foreground job receives terminal input. Background jobs can be stopped if they try to read from or write to the terminal. Job control also enables users to control which jobs interact with the terminal and which run in the background, allowing for more flexible and efficient process management.

### **Job Control’s Relevance Today:**
While job control was originally developed before windowing systems became common, it is still important in POSIX systems. Job control remains a standard feature for handling processes in terminals. Even though windowing systems reduce the need for job control, many users still find it helpful for managing multiple processes.

#### **Important Commands and Signals in Job Control:**
- **SIGINT:** Interrupt signal (Ctrl+C)
- **SIGQUIT:** Quit signal (Ctrl+\)
- **SIGTSTP:** Suspend signal (Ctrl+Z)
- **SIGTTIN:** Signal sent when a background job tries to read from the terminal.
- **SIGTTOU:** Signal sent when a background job tries to write to the terminal.

### Conclusion:
Job control is a powerful feature that allows users to manage processes in a terminal efficiently. By understanding how foreground and background process groups interact with the terminal and how to use job control commands, users can handle multiple jobs more effectively in UNIX-like systems.



### Summary of **Shell Execution of Programs**

This section focuses on how shells execute programs, the concepts of **process groups**, **controlling terminals**, **sessions**, and how these elements interact with each other. The examples use the **Bourne shell** (on Solaris) and a **job-control shell** (on Linux, specifically **Bash**). Key concepts like background jobs, pipelines, process groups, and controlling terminals are explained in the context of these shells.

---

#### **1. Shell Execution without Job Control (Bourne Shell)**
- In the **Bourne shell** on Solaris (which doesn’t support job control), when we execute a simple command, the **ps** command is used to display process information.
- The command:
  ```bash
  ps -o pid,ppid,pgid,sid,comm
  ```
  provides the **PID**, **PPID** (Parent Process ID), **PGID** (Process Group ID), **SID** (Session ID), and the **command name**.
  
  Example output:
  ```
  PID  PPID  PGID  SID  COMMAND
  949  947   949   949  sh
  949  949   949   949  ps
  ```

  - **PID (Process ID)**: Unique ID of each process.
  - **PPID (Parent Process ID)**: ID of the parent process (the shell in this case).
  - **PGID (Process Group ID)**: Groups processes together that can receive signals collectively.
  - **SID (Session ID)**: Identifies the session that the processes belong to.
  - **COMMAND**: The name of the command executed.

- In the above example, both **ps** and the shell are in the same **session** and **foreground process group** (PID 949).

#### **2. Process Groups and Job Control**
- When a shell doesn't support job control:
  - All processes run in the **foreground process group**.
  - For background processes, no new process groups are created; the shell does not take control of the terminal for background jobs.
  - Background jobs are still assigned the **same process group** and **controlling terminal** as the shell.
  
  Example:
  ```bash
  ps -o pid,ppid,pgid,sid,comm &
  ```

  In this case, the shell’s process group ID remains the same as the background process. Both share the same controlling terminal.

#### **3. Pipelines in the Bourne Shell**
- A **pipeline** (multiple commands connected with `|`) causes each command in the pipeline to run in the **same process group**.
  - For example, when running:
    ```bash
    ps -o pid,ppid,pgid,sid,comm | cat1
    ```
    The `ps` and `cat1` commands are in the same **process group** (PGID 949).
    
    Output:
    ```
    PID   PPID  PGID  SID  COMMAND
    949   947   949   949  sh
    949   949   949   949  ps
    ```

- The **shell** forks a copy of itself, which then forks the other processes in the pipeline.

#### **4. Background Process Access to Controlling Terminal**
- If a background process attempts to access the controlling terminal:
  - In **job-controlled shells**, it would trigger the signal `SIGTTIN`.
  - In **non-job-controlled shells** (e.g., the Bourne shell), the shell automatically redirects the background process’s standard input to `/dev/null`, causing the process to immediately read an **EOF** (end of file), which results in the process terminating.

- Example:
  ```bash
  cat > temp.foo &
  ```

  - Here, if the background `cat` tries to read from the terminal, it would get an **EOF** from `/dev/null` and terminate.

#### **5. Special Case: Opening `/dev/tty` in Background**
- If a background process specifically opens `/dev/tty` to interact with the controlling terminal (e.g., for reading user input), the result may not be as expected.
  
  Example:
  ```bash
  crypt < salaries | lpr &
  ```

  - In this case, the **crypt** program opens `/dev/tty`, reads from the terminal for a password, but since the shell is also interacting with `/dev/tty`, it reads the password input and tries to execute the next line as a command.
  - This can result in **incorrect behavior**, with the shell interpreting the password input as a command.

#### **6. Job-Controlled Shell (Bash on Linux)**
- In **job-control shells** (like **Bash** on Linux), the shell manages job control by creating **process groups** for each command, especially for background jobs and pipelines.
- The command:
  ```bash
  ps -o pid,ppid,pgid,sid,tpgid,comm
  ```
  provides additional information, including the **TPGID** (Terminal Process Group ID), which is associated with the session’s controlling terminal.
  
  Example output:
  ```
  PID   PPID  PGID  SID   TPGID  COMMAND
  2837  2818  2837  2837  5796   bash
  2837  2837  5796  5796  5796   ps
  ```

- In this case, both the **ps** command and the shell belong to the same **process group** and **session**. The foreground process group is identified by the **TPGID**.

#### **7. Background Process in Job-Controlled Shell**
- When running a command in the background in a job-controlled shell:
  ```bash
  ps -o pid,ppid,pgid,sid,tpgid,comm &
  ```
  - The **ps** command is placed in its own process group.
  - The **foreground process group** of the shell is identified by the **TPGID**.

#### **8. Pipeline in Job-Controlled Shell**
- When executing a pipeline:
  ```bash
  ps -o pid,ppid,pgid,sid,tpgid,comm | cat1
  ```
  - The shell places both processes (`ps` and `cat1`) in a **new process group**.
  - The process group becomes the **foreground process group**, and both processes are members of it.

  Output:
  ```
  PID   PPID  PGID  SID   TPGID  COMMAND
  2837  2818  2837  2837  5799   bash
  2837  2837  5799  5799  5799   ps
  2837  2837  5799  5799  5799   cat1
  ```

#### **9. Background Pipeline in Job-Controlled Shell**
- When running a background pipeline, like:
  ```bash
  ps -o pid,ppid,pgid,sid,tpgid,comm | cat1 &
  ```
  - Both the **ps** and **cat1** commands are placed into the **same background process group**.
  - The shell remains in the **foreground** process group.

  Output:
  ```
  PID   PPID  PGID  SID   TPGID  COMMAND
  2837  2818  2837  2837  5801   bash
  2837  2837  5801  5801  5801   ps
  2837  2837  5801  5801  5801   cat1
  ```

#### **Key Concepts Recap**
- **Process Groups**: A way to group processes together so that they can receive signals collectively.
- **Controlling Terminal**: A terminal device associated with a process group, which allows processes to interact with the terminal.
- **Session**: A collection of processes, with a controlling terminal (optional). A session can have one foreground process group.
- **Job Control**: In shells with job control, processes can be run in the background, placed in different process groups, and managed accordingly (foreground or background).
- **TPGID**: The Terminal Process Group ID, which identifies the process group that has control of the terminal.

---

This detailed breakdown should cover all the crucial topics in the chapter on shell execution of programs.


Here's a **detailed summary** of Section **9.10: Orphaned Process Groups** from your provided text. This summary ensures that all key details are covered, helping you prepare for your exams effectively.

---

## **Orphaned Process Groups**
### **Introduction**
- When a process's **parent terminates**, the process becomes an **orphan** and is **adopted by the init process (PID 1)**.
- This is a common scenario and usually does not cause issues.
- However, if an **entire process group** is orphaned, special handling is required by **POSIX.1** to prevent indefinite suspension.

---

## **Example Scenario**
- A **parent process (PID 6099)** forks a **child process (PID 6100)**.
- The parent then **terminates**, leaving the child orphaned.
- If the child process was **stopped (e.g., using job control and SIGTSTP)** before the parent terminated, the process **may never be resumed**.
- POSIX.1 has specific rules to handle this situation.

---

## **Process Group Orphaning Example**
- Assume:
  - A **login shell (PID 2837)** starts another shell or command (which gets **PID 6099**).
  - The **new shell or process (PID 6099)** then forks a child (**PID 6100**).
  - The child inherits the same **process group (6099)** as its parent.
- **Key points:**
  - The **parent (6099) sleeps** for 5 seconds.
  - The **child (6100)** sets up a signal handler for **SIGHUP**.
  - The **child stops itself** by sending `SIGTSTP` to itself.
  - The **parent (6099) exits**, orphaning the child.

---

## **Key POSIX.1 Rules for Orphaned Process Groups**
### **Definition of an Orphaned Process Group**
- A **process group** is **orphaned** if:
  - The **parent of every process in the group** is either:
    1. **A member of the same process group**, OR
    2. **Not part of the group’s session**.
- The process group is **not orphaned** as long as there is at least **one parent in a different process group but in the same session** (which could restart stopped processes).
- In this case, when the parent terminates, the **child is left in an orphaned process group**.

---

## **POSIX.1 Handling of Orphaned Process Groups**
1. **If a process group is orphaned and contains stopped processes:**
   - Every process in the group **receives SIGHUP (Hangup Signal)**.
   - After `SIGHUP`, every process in the group **receives SIGCONT (Continue Signal)**.
   - The `SIGHUP` signal informs the process that it is orphaned.
   - The `SIGCONT` signal **resumes execution** of any stopped processes.
   - If `SIGHUP` is not caught, the **default action terminates the process**.
   - To prevent termination, a **signal handler must be set**.

---

## **Expected Program Output**
- The program prints **process details** before and after orphaning.
- **Example output** when running the program:
  ```
  $ ./a.out
  parent: pid = 6099, ppid = 2837, pgrp = 6099, tpgrp = 6099
  child: pid = 6100, ppid = 6099, pgrp = 6099, tpgrp = 6099
  ```
  After orphaning:
  ```
  SIGHUP received, pid = 6100
  child: pid = 6100, ppid = 1, pgrp = 6099, tpgrp = 2837
  read error 5 on controlling TTY
  ```
  - **Key observations:**
    - The child's **PPID changed to 1** (adopted by init).
    - The **child received SIGHUP** (confirmed by the handler).
    - The **terminal process group (TPGID) changed to 2837** (the login shell).
    - The child **fails to read input** (error code 5, `EIO`).

---

## **Handling Terminal Input in an Orphaned Process Group**
- When a **process in a background process group** attempts to **read from the controlling terminal**, the kernel normally sends **SIGTTIN** (to stop it).
- **However, orphaned process groups cannot be stopped**.
- Instead, POSIX.1 **requires the read to return an error** (`EIO`, error code 5).
- This prevents the child from waiting indefinitely for input.

---

## **Conclusion**
- Orphaned process groups **must be handled carefully** to avoid leaving processes permanently stopped.
- POSIX.1 ensures that **stopped orphaned processes are resumed** using `SIGHUP` and `SIGCONT`.
- An orphaned process group that tries to read from the terminal **fails with an error** instead of stopping.

---

### **Key Takeaways for Exams**
1. **Orphaned process groups** occur when **all parents of a process group exit**.
2. **Stopped orphaned processes** receive `SIGHUP` followed by `SIGCONT`.
3. If an orphaned process tries to **read from the terminal**, it gets an `EIO` error instead of `SIGTTIN`.
4. **POSIX.1 ensures orphaned processes are resumed** to prevent indefinite suspension.
5. The **`SIGHUP` signal can be caught** to prevent default termination.

---

This summary captures **all key details** from your text and highlights important exam topics. Let me know if you need any clarifications! 🚀


Here's a detailed summary of Section 9.11 (FreeBSD Implementation) and Section 9.12 (Summary) to help you with your exam preparation.  

---

## **Summary of FreeBSD Implementation of Sessions and Process Groups (Section 9.11)**  

### **Overview:**  
The FreeBSD operating system implements process sessions, process groups, and controlling terminals using various kernel data structures. This section describes these structures and their relationships.  

### **Key Data Structures in FreeBSD:**  
1. **Session Structure (`session`)** – Represents a session (a collection of process groups).  
   - `s_count`: Number of process groups in the session. When it reaches 0, the structure is freed.  
   - `s_leader`: Pointer to the `proc` structure of the session leader (the first process that called `setsid`).  
   - `s_ttyvp`: Pointer to the `vnode` structure of the controlling terminal.  
   - `s_ttyp`: Pointer to the `tty` structure of the controlling terminal.  
   - `s_sid`: Session ID (same as the PID of the session leader).  

   **When `setsid()` is called:**  
   - A new `session` structure is allocated.  
   - `s_count` is set to 1.  
   - `s_leader` is set to the calling process.  
   - `s_sid` is set to the process ID (PID).  
   - `s_ttyvp` and `s_ttyp` are set to `NULL` because the session starts without a controlling terminal.  

2. **TTY Structure (`tty`)** – Represents terminal devices (both physical and pseudo-terminals).  
   - `t_session`: Points to the `session` structure that owns this terminal.  
   - `t_pgrp`: Points to the `pgrp` structure of the foreground process group.  
   - `t_termios`: Stores terminal attributes like baud rate, echo settings, and special characters.  
   - `t_winsize`: Stores terminal window size (`winsize` structure).  

   **Functionality:**  
   - When a session's terminal loses its connection, the kernel sends a `SIGHUP` signal to the session leader.  
   - Special characters like `CTRL+C` (interrupt), `CTRL+\` (quit), and `CTRL+Z` (suspend) send signals to the foreground process group.  
   - When the window size changes, `SIGWINCH` is sent to the foreground process group.  

3. **Process Group Structure (`pgrp`)** – Represents a process group.  
   - `pg_id`: Process group ID.  
   - `pg_session`: Pointer to the `session` structure that this process group belongs to.  
   - `pg_members`: Linked list of all `proc` structures (processes) in the process group.  

   **Finding the foreground process group:**  
   - Start from `session` → Follow `s_ttyp` to get the `tty` structure → Follow `t_pgrp` to get the `pgrp` structure.  

4. **Process Structure (`proc`)** – Represents an individual process.  
   - `p_pid`: Process ID.  
   - `p_pptr`: Pointer to the parent process.  
   - `p_pgrp`: Pointer to the `pgrp` structure of the process group.  
   - `p_pglist`: Linked list pointers to other processes in the same process group.  

5. **Vnode Structure (`vnode`)** – Represents the controlling terminal device file (`/dev/tty`).  
   - When a process accesses `/dev/tty`, it goes through the `vnode` structure.  

---

## **Summary of Process Relationships (Section 9.12)**  

### **Key Takeaways:**  
- A session consists of multiple process groups.  
- Process groups are used for job control in Unix shells.  
- A controlling terminal (`/dev/tty`) is assigned to a session and interacts with the foreground process group.  
- Signals (such as `SIGHUP`, `SIGINT`, `SIGQUIT`, `SIGWINCH`) play a crucial role in process and terminal interactions.  
- The next chapter discusses signals in Unix in detail.  

---

This summary covers all the key points in Section 9.11 and 9.12. Let me know if you need any more details! 🚀

