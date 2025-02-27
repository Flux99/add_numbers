### Summary: Files and Directories

#### **Key Abstractions in Storage Virtualization**
1. **File**:
   - A file is a linear array of bytes, which can be read or written.
   - Each file has a **low-level name** (e.g., inode number in UNIX systems) that the user is usually unaware of.
   - The file system is responsible for storing data persistently and retrieving it accurately, regardless of the file type (e.g., text, image, code).

2. **Directory**:
   - A directory also has a low-level name (inode number) but contains a list of `(user-readable name, low-level name)` pairs.
   - Directories can refer to files or other directories, forming a **hierarchical structure** or directory tree.
   - The root directory in UNIX systems is `/`, and subdirectories are separated by `/`.

#### **Directory Hierarchy**
- Users can build an arbitrary directory tree by placing directories inside other directories.
- Example:
  - A file named `bar.txt` in the directory `foo`, which is inside the root `/`, has an **absolute pathname** `/foo/bar.txt`.
  - Multiple files or directories can have the same name if they are in different locations within the hierarchy (e.g., `/foo/bar.txt` and `/bar/foo/bar.txt`).

#### **Naming in File Systems**
- **Uniform Naming**:
  - In UNIX systems, almost everything (files, devices, pipes, processes) is named through the file system, making it simpler and more modular.
- **File Name Parts**:
  - File names often have two parts: a base name (e.g., `bar`) and an extension (e.g., `.txt`), separated by a period.
  - The extension is typically a convention to indicate the file type (e.g., `.c` for C code, `.jpg` for images). There is no enforcement of file type based on the name.

#### **Advantages of the File System**
- Provides a unified, convenient naming system for all files and resources.
- Enables easy access to files on various devices (disk, USB, CD-ROM) under a single directory tree.

---

### **File System Interface**
1. **Creating, Accessing, and Deleting Files**:
   - The file system interface allows users to perform basic operations like creating, reading, writing, and deleting files.
   
2. **Unlink()**:
   - A mysterious system call used to remove files. Its function will become clear upon deeper study.

---

### **Tips for Understanding File Systems**
1. **Think Carefully About Naming**:
   - Naming is crucial in system design, as it is the first step to accessing any resource.
   - Consistent and meaningful naming simplifies user interaction with the file system.
   
2. **Directories and Files**:
   - Both can have similar names if located in different parts of the directory tree.

---

This overview emphasizes the abstraction of files and directories, their naming conventions, hierarchical structures, and the role of the file system interface in creating and managing them.





### Summary: File Operations in Unix

#### **Creating Files**
1. **`open()`**: Used to create files by passing the `O_CREAT` flag. Example:
   ```c
   int fd = open("foo", O_CREAT|O_WRONLY|O_TRUNC, S_IRUSR|S_IWUSR);
   ```
   - **Flags**:
     - `O_CREAT`: Creates the file if it doesn’t exist.
     - `O_WRONLY`: Opens the file in write-only mode.
     - `O_TRUNC`: Truncates existing content to zero bytes if the file exists.
   - **Permissions**: Third parameter specifies file permissions (e.g., readable/writable by the owner).

2. **`creat()`**: An older alternative to `open()` for file creation. Equivalent to:
   ```c
   int fd = creat("foo");
   ```
   Internally, it uses `open()` with `O_CREAT | O_WRONLY | O_TRUNC`.

3. **File Descriptor**:
   - Returned by `open()` or `creat()`.
   - An integer unique to the process, used to reference the file for operations like `read()` and `write()`.

#### **Reading and Writing Files**
1. **Reading Files**:
   - Open the file in read mode (e.g., `O_RDONLY`).
   - Use the `read()` system call:
     ```c
     ssize_t read(int fd, void *buf, size_t count);
     ```
     - Reads `count` bytes into `buf`.
     - Returns the number of bytes read or 0 if EOF is reached.

2. **Writing Files**:
   - Open the file in write mode (e.g., `O_WRONLY`).
   - Use the `write()` system call:
     ```c
     ssize_t write(int fd, const void *buf, size_t count);
     ```
     - Writes `count` bytes from `buf` to the file.

3. **Closing Files**:
   - Always close files using `close(fd)` after operations to release resources.

#### **System Tools**
- **`strace`**: Monitors system calls made by a program.
  - Example: `strace cat foo` traces how `cat` opens, reads, and writes the file.
  - Useful options:
    - `-f`: Follows forked processes.
    - `-t`: Adds timestamps.
    - `-e trace=open,close,read,write`: Filters specific system calls.

#### **Understanding File Descriptors**
- **Pre-defined File Descriptors**:
  - `0`: Standard input.
  - `1`: Standard output.
  - `2`: Standard error.
  - First file opened by a process will usually use descriptor `3`.

#### **Open File Table**
1. **Per-process Descriptor Array**:
   - Each process tracks open files in a structure like:
     ```c
     struct proc {
         struct file *ofile[NOFILE]; // Array of open files
     };
     ```
2. **System-wide Open File Table**:
   - Tracks:
     - File reference.
     - Current offset.
     - Read/write permissions.

#### **Tips for Practice**
- Experiment with `strace` to trace how commands like `cat` or `dd` interact with files.
- Write small programs to practice file operations (`open`, `read`, `write`, `close`).




### Summary: Reading and Writing Files Non-Sequentially

1. **Sequential vs Random Access**:
   - So far, file access has been sequential (read/write from start to end).
   - Random access allows reading or writing at specific offsets in a file, useful for cases like building and using an index over a text document.

2. **The `lseek()` System Call**:
   - Used to set the file offset for reading or writing at a specific location.
   - **Prototype**:
     ```c
     off_t lseek(int fildes, off_t offset, int whence);
     ```
   - **Parameters**:
     - `fildes`: File descriptor.
     - `offset`: The position to set within the file.
     - `whence`: How the offset is interpreted:
       - `SEEK_SET`: Sets the offset to `offset` bytes from the beginning.
       - `SEEK_CUR`: Sets the offset to the current position plus `offset`.
       - `SEEK_END`: Sets the offset to the end of the file plus `offset`.

3. **File Offset**:
   - Each open file has a "current offset," tracked by the OS.
   - This offset determines where the next read or write begins.
   - The offset is updated:
     - Automatically after a read/write.
     - Manually using `lseek()`.

4. **Implementation Details**:
   - The offset is stored in a `struct file`, which also tracks:
     - Reference count (`ref`).
     - Read/write permissions.
     - The associated inode pointer (`ip`).
   - Example structure:
     ```c
     struct file {
         int ref;
         char readable;
         char writable;
         struct inode *ip;
         uint off;
     };
     ```
   - All open files are managed in the **Open File Table (OFT)**, which is an array in the OS with one lock per entry.

5. **Examples**:
   - **Sequential Reading**:
     - The offset starts at 0 and increases with each read/write.
     - Reading past the end of the file returns 0 (indicating EOF).
   - **Multiple File Descriptors**:
     - Each `open()` call creates a new file descriptor with its own offset in the OFT.
     - Offsets for different descriptors are updated independently.
   - **Using `lseek()`**:
     - Example:
       ```c
       fd = open("file", O_RDONLY);
       lseek(fd, 200, SEEK_SET);  // Set offset to 200
       read(fd, buffer, 50);      // Read 50 bytes starting at offset 200
       ```
     - The `lseek()` call explicitly sets the offset; the subsequent read updates it further.

6. **Important Note on Disk Seeks**:
   - The `lseek()` system call **does not perform a disk seek**; it only updates the offset in OS memory.
   - Disk seeks occur during actual I/O operations (e.g., a read/write to a part of a file on a different disk track).

By understanding `lseek()` and its behavior, you can efficiently manage file access for tasks like random data retrieval or indexed lookups.





### Summary: Shared File Table Entries with `fork()` and `dup()`

#### **File Descriptor and Open File Table**
- File descriptors are typically a one-to-one mapping to entries in the **open file table**. Each process accessing a file gets its own entry, maintaining an independent file offset.
- When two processes access the same file, they usually have separate file table entries unless special conditions apply.

#### **Shared File Table Entries with `fork()`**
- When a process creates a child process using `fork()`, **file table entries are shared** between the parent and child. 
- This sharing includes:
  - The same open file entry.
  - Shared reference count.
  - Shared file offset.

##### **Example Code**
```c
int fd = open("file.txt", O_RDONLY);
assert(fd >= 0);
int rc = fork();
if (rc == 0) { // Child process
    rc = lseek(fd, 10, SEEK_SET); // Adjust file offset
    printf("child: offset %d\n", rc);
} else if (rc > 0) { // Parent process
    (void) wait(NULL); // Wait for child to finish
    printf("parent: offset %d\n", (int) lseek(fd, 0, SEEK_CUR)); // Check file offset
}
```
- **Output**:
  ```
  child: offset 10
  parent: offset 10
  ```
- The child process adjusts the file offset using `lseek()`, which also affects the parent because they share the same file table entry.
  
##### **Diagram Explanation**
- Both parent and child processes point to the same open file table entry, which refers to the inode of the file.
- The reference count in the open file table entry ensures it is only removed when **both processes close the file** or exit.

#### **Use Cases of Sharing**
- Useful for cooperative tasks where multiple processes work on a single output file without extra coordination.

#### **Shared File Table Entries with `dup()`**
- The `dup()` system call creates a new file descriptor pointing to the **same file table entry** as an existing descriptor.
- **Example Code**:
```c
int fd = open("README", O_RDONLY);
assert(fd >= 0);
int fd2 = dup(fd);
// fd and fd2 refer to the same file table entry
```
- Both descriptors (`fd` and `fd2`) can be used interchangeably.

#### **Use Case of `dup()`**
- Frequently used in UNIX shells for tasks like output redirection.

#### **Key Points**
1. **`fork()` Sharing**:
   - Parent and child processes share open file table entries, meaning any change to file offset by one process affects the other.
2. **`dup()` Sharing**:
   - Within the same process, multiple file descriptors can point to the same file table entry, making them interchangeable.
3. **Reference Count**:
   - The shared file table entry is removed only when all processes or descriptors referencing it are closed.

### Why This Matters
- Understanding shared file table entries is crucial for designing programs that involve file handling in a multi-process environment.
- Familiarity with `fork()` and `dup()` behaviors ensures efficient file manipulation and avoids unintended side effects.





### Summary of Renaming Files and Getting File Information

#### Renaming Files
- **Purpose**: To change the name of a file.
- **Command-Line Usage**: The `mv` command renames files (e.g., `mv foo bar` renames `foo` to `bar`).
- **System Call**: The underlying system call is `rename(char *old, char *new)`, which:
  - Takes two arguments: the current name (`old`) and the new name (`new`).
  - Is **atomic**: If the system crashes during renaming, the file retains either the old name or the new name, ensuring no intermediate state.
- **Atomic Rename Example**: 
  1. A file editor like `emacs` creates a temporary file (`foo.txt.tmp`).
  2. Writes new contents to the temporary file.
  3. Flushes the file to disk using `fsync()` to ensure data safety.
  4. Renames the temporary file to the original file name using `rename()`, atomically replacing the old file with the updated version.

#### Getting Information About Files
- **Purpose**: To retrieve metadata about a file.
- **System Calls**:
  - `stat(pathname, struct stat *buf)` and `fstat(int fd, struct stat *buf)`:
    - Provide details about the file in a `stat` structure.
- **Metadata Fields in `stat` Structure**:
  - `st_dev`: ID of the device containing the file.
  - `st_ino`: Inode number.
  - `st_mode`: File permissions.
  - `st_nlink`: Number of hard links.
  - `st_uid` and `st_gid`: User and group IDs of the file owner.
  - `st_rdev`: Device ID (for special files).
  - `st_size`: File size in bytes.
  - `st_blksize`: Block size for I/O.
  - `st_blocks`: Number of blocks allocated.
  - `st_atime`, `st_mtime`, `st_ctime`: Times of last access, modification, and status change.
- **Command-Line Tool**: The `stat` command displays file metadata.
  - Example:
    ```bash
    echo hello > file
    stat file
    ```
    Output includes details like file size, number of blocks, device ID, inode, permissions, owner, and timestamps.
- **Inodes**:
  - A data structure used by file systems to store file metadata.
  - Reside on disk; active inodes are cached in memory for faster access.

This summary highlights the critical aspects of file renaming and metadata retrieval necessary for understanding file system operations.


### Summary: Files and Directories in Operating Systems

#### 1. **Removing Files**
- Files are deleted using the system call **`unlink()`**, not `remove()` or `delete()`.
- The `unlink()` system call removes the mapping of the file name to its inode.
- The name "unlink" reflects how file systems allow multiple directory entries (names) to point to the same inode.

#### 2. **Creating Directories**
- Use the system call **`mkdir()`** to create directories.
- Example: `mkdir("foo", 0777)` creates a directory named `foo`.
- An empty directory contains two special entries:
  - `.`: Refers to itself.
  - `..`: Refers to the parent directory.
- These entries are visible using the `ls -a` command.

#### 3. **Powerful Commands (Tip: Be Careful)**
- The `rm` command can remove files and directories:
  - `rm *`: Deletes all files in the current directory.
  - `rm -rf *`: Recursively deletes all files and subdirectories.
- **Warning**: Running `rm -rf *` at the root level (`/`) can delete the entire file system.

#### 4. **Reading Directories**
- Directories are read using a set of calls: **`opendir()`**, **`readdir()`**, and **`closedir()`**.
- Example program:
  ```c
  DIR *dp = opendir(".");
  struct dirent *d;
  while ((d = readdir(dp)) != NULL) {
      printf("%lu %s\n", (unsigned long) d->d_ino, d->d_name);
  }
  closedir(dp);
  ```
- The `struct dirent` structure contains:
  - `d_name`: Filename.
  - `d_ino`: Inode number.
  - Other metadata like offset (`d_off`), record length (`d_reclen`), and file type (`d_type`).

#### 5. **Additional Details**
- **`stat()`**: Used to gather more detailed information about files, such as size and permissions.
- **`ls` Command**:
  - Default: Lists file names.
  - `-l` flag: Uses `stat()` for detailed information.
  - Use `strace` on `ls` to observe system calls.

### Key Takeaways
- **`unlink()`** removes a file by severing its directory entry.
- Directories are managed by system calls like **`mkdir()`** and **`readdir()`**, ensuring the file system maintains metadata integrity.
- Powerful commands like `rm -rf` require caution to prevent catastrophic data loss.



### **Summary: File and Directory Operations in UNIX**

#### **Deleting Directories**
- **`rmdir()`** is used to delete directories, but it only works if the directory is empty (contains only `.` and `..`).
- If the directory is not empty, the `rmdir()` call fails, making directory deletion safer compared to file deletion.

---

#### **Hard Links**
- **Purpose:** Hard links allow multiple names (aliases) for the same file, linking them to the same inode.
- **System Call:** `link(oldpath, newpath)` creates a hard link. The `ln` command can be used from the terminal.
  - Example:
    ```bash
    echo hello > file
    ln file file2
    ```
    Both `file` and `file2` refer to the same inode, containing "hello".
- **Key Points:**
  - Hard links do not duplicate file content; they merely create additional directory entries pointing to the same inode.
  - Deleting a name (using `unlink()` or `rm`) decrements the reference count in the inode but does not delete the file until the count reaches zero.
- **Reference Count:** Visible using `stat()`. When links are created or removed, the reference count in the inode changes accordingly.
  - Example:
    ```bash
    ln file file2
    ln file2 file3
    rm file
    ```
    The file remains accessible through `file2` and `file3` until all references are deleted.

---

#### **Symbolic Links (Soft Links)**
- **Purpose:** Symbolic links overcome the limitations of hard links (e.g., no cross-partition linking, no directory links).
- **System Call:** `ln -s target linkname` creates a symbolic link.
  - Example:
    ```bash
    ln -s file file2
    ```
    Here, `file2` is a soft link pointing to `file`.
- **Key Characteristics:**
  - A symbolic link is a separate file of type `l` (link), storing the pathname of the target file.
  - The size of the symbolic link corresponds to the length of the pathname it stores.
  - Unlike hard links, symbolic links may break if the target file is removed, resulting in a **dangling reference**.
    - Example:
      ```bash
      rm file
      cat file2  # Error: No such file or directory
      ```

---

### **Key Differences: Hard Links vs Symbolic Links**
| Feature                | Hard Links                                      | Symbolic Links                                |
|------------------------|-------------------------------------------------|----------------------------------------------|
| **File Type**          | Same as the target file (regular file, etc.)    | A special file storing the pathname          |
| **Cross-Partition**    | Not supported                                  | Supported                                    |
| **Directories**        | Not supported                                  | Supported                                    |
| **Inode Sharing**      | Shares the same inode with the target           | Does not share inode; separate inode         |
| **Effect of Deletion** | File persists until all links are removed       | Link becomes a dangling reference if target is removed |

---

#### **Practical Usage**
- Use **hard links** when you need multiple aliases for a file within the same partition.
- Use **symbolic links** when working across partitions or linking to directories.

This concise yet detailed overview captures the fundamental operations and key distinctions, ensuring clarity for your exam preparation.


### Summary of 39.16: Permission Bits and Access Control Lists (ACLs)

---

#### **Introduction**
- Operating systems virtualize physical resources (CPU, memory, disk) to ensure safe and secure sharing.
- Unlike CPU and memory, file systems allow files to be shared among users and processes, requiring mechanisms to manage varying degrees of access.

---

#### **Permission Bits in UNIX**
- Permissions control who can access a file and how. The output of `ls -l` shows permissions.
  - Example: `-rw-r--r--` for `foo.txt`.
    - **First character**: File type (`-` for regular files, `d` for directories, `l` for symbolic links, etc.).
    - **Next nine characters**: Permission bits divided into three groups:
      1. **Owner**: `rw-` (read/write for the owner).
      2. **Group**: `r--` (read-only for group members).
      3. **Others**: `r--` (read-only for others).

---

#### **Changing Permissions**
- Use `chmod` to change permissions.
  - Example: `chmod 600 foo.txt` sets permissions to `rw-------`:
    - `6`: Read (4) + Write (2) for the owner.
    - `0`: No access for group or others.

---

#### **The Execute Bit**
- **For files**: Determines whether the file can be executed.
  - Example: A shell script (`hello.csh`) won’t execute unless the execute bit is set.
    - Setting: `chmod 700 hello.csh` (execute permission for the owner).
- **For directories**: Allows:
  1. Changing into the directory (`cd`).
  2. Creating files (with the writable bit).

---

#### **Beyond Basic Permissions: Access Control Lists (ACLs)**
- Some file systems (e.g., AFS) use ACLs for more granular access control.
- ACLs enable specific permissions for individual users or groups.
  - Example (AFS):
    - `fs listacl private` shows the access list for the directory `private`:
      - `system:administrators`: Full rights (`rlidwka`).
      - `remzi`: Full rights (`rlidwka`).
    - To give another user (e.g., `andrea`) read and lookup access:
      - Command: `fs setacl private/ andrea rl`.

---

#### **Superuser Access**
- In local file systems, the superuser (`root`) can access all files, regardless of permissions.
- In distributed file systems like AFS, administrators (e.g., `system:administrators`) have similar privileged access.
  - **Risk**: If an attacker gains superuser access, they can bypass all privacy and security guarantees.

---

### Key Takeaways
1. Permission bits in UNIX manage access for the **owner**, **group**, and **others**.
2. `chmod` modifies permission bits; the execute bit is critical for running programs and directory access.
3. ACLs provide more specific control over who can access a resource, surpassing the limitations of permission bits.
4. Superusers or privileged groups can bypass all permissions, presenting a potential security risk.

---

This summary captures all the crucial details for exam preparation.

### Summary: Making and Mounting a File System

---

### **1. Making a File System**
- **Tool Used:** `mkfs` (make file system).
- **Input Requirements:**
  - A device (e.g., `/dev/sda1`).
  - A file system type (e.g., `ext3`).
- **Output:** Writes an empty file system onto the disk, starting with a root directory.
- Example command: `mkfs -t ext3 /dev/sda1`.

---

### **2. Mounting a File System**
- **Purpose:** Makes a file system accessible within the unified directory tree.
- **Tool Used:** `mount` (calls the `mount()` system call).
- **Process:**
  - Mount a file system to an existing directory (mount point).
  - The new file system is "pasted" onto the directory tree at the mount point.
- **Example:** 
  - Command: `mount -t ext3 /dev/sda1 /home/users`.
  - After mounting:
    - Root of `/dev/sda1` is accessible at `/home/users/`.
    - Subdirectories and files (e.g., `a/foo` and `b/foo`) are accessed as `/home/users/a/foo` and `/home/users/b/foo`.

---

### **3. Viewing Mounted File Systems**
- **Command:** `mount`
- **Output Example:**
  ```
  /dev/sda1 on / type ext3 (rw)
  proc on /proc type proc (rw)
  sysfs on /sys type sysfs (rw)
  ```
- Mix of different file systems (e.g., disk-based `ext3`, temporary `tmpfs`, distributed `AFS`) all unified into a single directory tree.

---

### **4. TOCTTOU Problem (Time Of Check To Time Of Use)**
- **Definition:** A race condition between checking a file's properties and performing an operation on it.
- **Example Exploit:**
  - A privileged service (e.g., mail service running as root) checks a file (via `lstat()`) to confirm it's regular and owned by a user.
  - Attacker renames the file (e.g., to `/etc/passwd`) between the check and the update, causing privileged operations on unintended files.
- **Impact:** Escalation of privileges (e.g., adding a root account by modifying `/etc/passwd`).

---

### **5. Solutions to TOCTTOU**
- **Partial Mitigations:**
  - Reduce the need for root privileges in services.
  - Use the `O_NOFOLLOW` flag to prevent following symbolic links.
- **Ideal Solution (Not Widely Available):**
  - Use **transactional file systems** to prevent state changes during operations.

---

### **6. Key Takeaways**
- The **`mkfs` tool** creates an empty file system on a device.
- The **`mount` command** integrates file systems into a single, accessible directory tree.
- The **TOCTTOU problem** poses significant security risks in multitasking environments and requires careful coding practices or advanced file system features to mitigate.

