To troubleshoot **Out of Memory (OOM)** errors systematically, you can follow these steps to diagnose and identify the root cause:

---

### 1. **Check System Logs**
The kernel logs are the first place to check for OOM events. On Linux, these logs are often stored in `/var/log/syslog` or `/var/log/messages`. Use the following commands:

```bash
# For Debian-based systems:
grep -i 'oom' /var/log/syslog

# For Red Hat-based systems:
grep -i 'oom' /var/log/messages
```

Look for entries like:
```
Out of memory: Kill process 2659 (process_name) score 1000 or sacrifice child
Killed process 2659 (process_name), UID 1001, total-vm:123456kB, anon-rss:45678kB, file-rss:1234kB
```

---

### 2. **Monitor Memory Usage**
Use tools to observe which processes are consuming the most memory.

#### a. **`top` or `htop`**
Run `top` or `htop` to identify memory usage by processes:
```bash
top -o %MEM
```
Key fields:
- **RES**: Resident memory used (physical memory).
- **VIRT**: Total virtual memory used (includes swap).

#### b. **`free`**
Check the overall system memory status:
```bash
free -h
```
Key metrics:
- **Available memory**.
- **Swap usage** (high swap usage can indicate memory pressure).

#### c. **`ps`**
Find the top memory-consuming processes:
```bash
ps aux --sort=-%mem | head
```

---

### 3. **Analyze Memory Statistics**
#### a. **`dmesg` Output**
The `dmesg` command can show OOM killer activity:
```bash
dmesg | grep -i 'oom'
```
This will reveal if the kernel killed a specific process and why.

#### b. **`/proc/meminfo`**
Examine detailed memory statistics:
```bash
cat /proc/meminfo
```
Look for:
- `MemAvailable`: Free memory.
- `SwapFree`: Available swap space.
- `HighTotal` vs. `HighFree`: Kernel's high memory usage.

---

### 4. **Identify Memory Leaks**
If the memory usage of a specific process keeps increasing over time, it may indicate a **memory leak**.

#### a. **Using `pmap`**
Inspect the memory map of a specific process:
```bash
pmap -x <PID>
```
Check for unusual memory allocations.

#### b. **Using `valgrind` (for debug builds)**
Valgrind can detect memory leaks in applications:
```bash
valgrind --leak-check=full ./your_application
```

#### c. **Profiling Tools**
- **`perf`**: Analyze memory and CPU usage.
- **`strace`**: Monitor memory-related syscalls (`mmap`, `brk`).
  ```bash
  sudo strace -p <PID> -e trace=brk,mmap,munmap
  ```

---

### 5. **Check Swap Space**
A lack of swap space can exacerbate memory issues. Verify swap usage:
```bash
swapon --show
free -h
```

If swap is insufficient, consider increasing it:
```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

### 6. **Enable OOM Logging**
To capture detailed OOM information, enable logging:
```bash
echo "1" > /proc/sys/vm/oom_dump_tasks
```
This logs detailed task information for processes that triggered the OOM killer.

---

### 7. **Preventative Measures**
- **Use Limits:** Set memory usage limits using `ulimit`:
  ```bash
  ulimit -v <memory_limit_in_kilobytes>
  ```
- **cgroups:** Use cgroups to constrain memory usage of specific processes or containers.
  ```bash
  echo "<memory_limit_in_bytes>" > /sys/fs/cgroup/memory/<group_name>/memory.limit_in_bytes
  ```

---

### 8. **Analyze Core Dumps (Optional)**
If a process is terminated due to OOM, a core dump might be useful for debugging. Enable core dumps:
```bash
ulimit -c unlimited
```
Inspect the core dump using `gdb` or similar tools:
```bash
gdb ./binary core
```

---

### Summary Workflow
1. **Examine logs** (`syslog`, `dmesg`) for OOM events.
2. **Monitor memory** usage with `top`, `htop`, or `ps`.
3. **Analyze memory leaks** with `pmap`, `valgrind`, or `strace`.
4. **Check and expand swap** if necessary.
5. Apply **preventative measures** with `ulimit` or cgroups.

Would you like assistance with a specific tool or deeper analysis?