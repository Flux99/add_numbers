### Detailed Summary of File System Implementation

#### **Mental Models of File Systems**
- To understand file systems, focus on **two main aspects**:
  1. **Data Structures**: The on-disk structures used to organize data and metadata. 
     - Early file systems use simple structures like arrays of blocks.
     - Advanced file systems (e.g., SGI’s XFS) employ tree-based structures.
  2. **Access Methods**: How system calls like `open()`, `read()`, and `write()` map to the data structures.
     - Understanding which structures are accessed or modified during operations improves efficiency and comprehension.

#### **Overall On-Disk Organization**
1. **Disk Partitioning**:
   - Disk is divided into fixed-size blocks, commonly 4 KB each.
   - Example: A small disk with 64 blocks (each 4 KB) is addressed from `0` to `63`.

2. **Key Components of a File System**:
   - **Data Region**:
     - Reserved for user data.
     - Occupies the largest portion of the disk.
     - Example: Last 56 blocks (blocks `8` to `63`) are for user data.
   - **Inode Table**:
     - Stores metadata about files (e.g., data block mappings, file size, ownership, access rights).
     - Example: 5 blocks (blocks `3` to `7`) are reserved for inodes.
     - **Inodes**: 
       - Small structures (e.g., 256 bytes).
       - A 4 KB block can hold 16 inodes. In this example, 80 inodes (maximum files supported) are stored in the inode table.

3. **Allocation Structures**:
   - **Bitmaps**:
     - Used to track free and allocated blocks/inodes.
     - Each bit indicates the status: `0` (free) or `1` (in use).
     - **Inode Bitmap (i)**: Tracks the allocation of inodes.
     - **Data Bitmap (d)**: Tracks the allocation of data blocks.
     - Example: Bitmaps are stored in blocks `1` (inode bitmap) and `2` (data bitmap).

4. **Superblock**:
   - Contains key metadata about the file system, such as:
     - Number of inodes and data blocks (e.g., 80 and 56).
     - Start location of the inode table (e.g., block `3`).
     - Magic number identifying the file system type (e.g., `vsfs`).
   - Located in block `0` for easy access during mounting.

5. **Final Layout**:
   - The on-disk layout includes:
     ```
     Block 0: Superblock (S)
     Block 1: Inode Bitmap (i)
     Block 2: Data Bitmap (d)
     Blocks 3-7: Inode Table (I)
     Blocks 8-63: Data Region (D)
     ```

#### **Key Concepts and Operations**
- **Mounting a File System**:
  - The operating system reads the superblock first to initialize parameters and attach the volume to the file system tree.
  - Once mounted, files can be accessed, and the on-disk structures (superblock, inodes, data blocks) guide the system to locate and manage data.

- **Efficiency Considerations**:
  - Although a 4 KB block for each bitmap is overkill for small disks, it simplifies the implementation.

This foundational understanding of how data and metadata are organized, accessed, and managed on disk is essential for grasping file systems' operations and performance.


### **Inode Bitmap and Data Bitmap: Explanation and Usage**

**1. What is a Bitmap in File Systems?**
A **bitmap** is a simple data structure where each bit represents the state of an object or resource. In file systems, bitmaps are commonly used to track the allocation status of inodes and data blocks.

---

**2. Inode Bitmap**
- **Definition:** 
  The inode bitmap is a structure where each bit corresponds to an inode in the inode table.
  
- **Purpose:** 
  It is used to keep track of whether an inode is **free (0)** or **allocated (1)**.

- **Example:**
  If the inode table contains 80 inodes, the inode bitmap will have 80 bits:
  - `0`: The inode is free and can be assigned to a new file.
  - `1`: The inode is in use and contains metadata for an existing file.

- **Usage in Operations:**
  - When creating a new file: 
    - The file system scans the inode bitmap to find a free inode (bit `0`) to allocate for the file.
  - When deleting a file: 
    - The corresponding bit in the inode bitmap is reset to `0`, marking the inode as free.

---

**3. Data Bitmap**
- **Definition:** 
  The data bitmap is a structure where each bit corresponds to a block in the data region of the file system.

- **Purpose:** 
  It tracks whether a data block is **free (0)** or **in-use (1)**.

- **Example:**
  If the data region contains 56 blocks, the data bitmap will have 56 bits:
  - `0`: The block is free and available for new data.
  - `1`: The block is in use and stores file content.

- **Usage in Operations:**
  - When writing to a file: 
    - The file system scans the data bitmap to find a free block (bit `0`) to allocate for storing data.
  - When a file is deleted: 
    - The corresponding bits in the data bitmap are reset to `0`, marking those blocks as free.

---

**4. Advantages of Bitmaps**
- **Efficient Space Usage:** 
  A single bit is used to track the status of an inode or data block, making bitmaps very compact.
  
- **Fast Access:** 
  Scanning through a bitmap is quick, enabling efficient allocation and deallocation of resources.

- **Simplicity:** 
  Implementing and managing bitmaps is straightforward compared to more complex structures like free lists.

---

**5. Example Use Case**
Imagine a disk with:
- 80 inodes → Inode bitmap with 80 bits.
- 56 data blocks → Data bitmap with 56 bits.

When a new file is created:
1. The file system scans the **inode bitmap** for the first free inode.
2. The file system scans the **data bitmap** to allocate one or more data blocks.
3. Updates the respective bits in the inode and data bitmaps to `1`.

When a file is deleted:
1. The inode and its data blocks are marked as free by resetting the corresponding bits in the inode and data bitmaps to `0`.

---

### **Summary**
- **Inode Bitmap:** Tracks allocation status of inodes (metadata).
- **Data Bitmap:** Tracks allocation status of data blocks (file content).
- **Purpose:** Efficiently manage and allocate file system resources.
- **Key Benefit:** Allows the file system to quickly locate free or used inodes/blocks for file creation, deletion, or modification.





In a file system, there are several key regions that organize the data, including the **inode region**, **data region**, and **superblock**. Let me clarify the role of each and explain your specific questions regarding **inodes** and their pointers.

### 1. **Inode Region:**
The **inode region** of a file system contains the **inode table**. An inode (short for "index node") is a data structure that holds metadata about files or directories. It doesn't store the actual data of the file but instead stores information such as:

- **File type** (regular file, directory, etc.)
- **File size**
- **Permissions** (who can read, write, or execute the file)
- **Owner and group**
- **Timestamps** (e.g., file creation, modification times)
- **Pointers to data blocks** (where the actual data is stored)

Each inode is identified by a unique **inode number** (i-number) that is used to index into the inode table. 

### 2. **Inode Table:**
The **inode table** is an array of inodes stored on disk. Each inode has a fixed size (e.g., 128 bytes), and all inodes are stored in a contiguous region of the disk. The inode number (i-number) refers to the index of an inode in the inode table.

- The inode table contains metadata for all files and directories in the file system.
- If you know the inode number of a file, you can calculate its position in the inode table and read its metadata.

### 3. **Pointers Inside Each Inode:**
An inode typically contains pointers to the **data blocks** that hold the actual file contents. There are two types of pointers in an inode: **direct pointers** and **indirect pointers**.

- **Direct Pointers**: These pointers point directly to data blocks that contain the actual contents of the file. For example, if the inode has 12 direct pointers and each block is 4 KB, then the inode can directly point to up to 48 KB of file data.
  
- **Indirect Pointers**: These pointers help with larger files. An indirect pointer doesn't directly point to file data; instead, it points to another block that contains additional pointers (which point to the actual data blocks). Indirect pointers come in multiple levels:
  - **Single Indirect Pointer**: Points to a block of pointers, each pointing to data blocks.
  - **Double Indirect Pointer**: Points to a block of pointers to indirect blocks, each of which contains more pointers to data blocks.
  - **Triple Indirect Pointer**: Points to a block of pointers to double indirect blocks, further pointing to more indirect blocks, and so on.

By using direct and indirect pointers, a file system can support both small and very large files. Smaller files are stored using just direct pointers, while larger files can use multiple levels of indirection to point to more data blocks.

### 4. **Data Region:**
The **data region** of the file system is where the actual file contents are stored. Unlike the inode region, which stores metadata, the data region contains the raw bytes of the file data.

- The **data blocks** in this region contain the content of files (text, images, binaries, etc.).
- The data blocks are referenced by the pointers inside the inodes.
- Files are divided into fixed-size blocks, and these blocks are spread across the data region.

### To Summarize:
- The **inode region** contains the **inode table**. Each inode has metadata about a file, including **direct pointers** and **indirect pointers** that point to data blocks.
- **Direct pointers** point to actual data blocks, while **indirect pointers** are used for larger files, where they point to other blocks containing more pointers.
- The **data region** contains the actual content of the files, which is indexed by the pointers in the inodes.

The file system’s **structure** is organized in these regions:
1. **Superblock**: Contains the file system’s metadata (like size, block count, free space).
2. **Inode Region**: Contains the inode table, with inodes pointing to file data blocks.
3. **Data Region**: Stores the actual file data.

Thus, an inode region doesn't directly contain the data of files but contains metadata, including pointers that refer to data stored in the **data region**. The pointers in the inode can be **direct** or **indirect** (single, double, or triple). These indirect pointers allow the file system to handle files of varying sizes efficiently.



Here’s a detailed summary of the concepts covered in the text, focusing on key details relevant for your exams:

### **1. Directory Organization in File Systems (vsfs Example):**
- **Basic Structure**: In file systems like **vsfs**, directories are organized as simple lists containing pairs of **(entry name, inode number)**. Each entry in a directory refers to a file or subdirectory within it. The directory structure contains **string lengths** for file names, and may also have **reserved space** for deleted files.
  
- **Directory Entries**: Each entry in a directory contains:
  - **Inode number**: Points to the inode storing metadata for the file or directory.
  - **Record length**: Total bytes used by the entry (including any padding).
  - **String length**: Length of the file name (excluding null terminator).
  - **File name**: The actual name of the file or subdirectory.

- **Special Directory Entries**:
  - **`.` (dot)**: Represents the current directory.
  - **`..` (dot-dot)**: Represents the parent directory.

- **Directory Example**: If a directory `dir` has three files (`foo`, `bar`, `foobar_is_a_pretty_longname`), the directory’s data blocks may look like:
  ```
  inum | reclen | strlen | name
  ---- | -------| -------| ----
    5   |   12  |    4   | foo
    13  |   12  |    4   | bar
    24  |   36  |   28   | foobar_is_a_pretty_longname
  ```

- **Deletion**: When a file is deleted (e.g., via `unlink()`), it may leave gaps in the directory's data block. The record length allows the file system to reuse space from deleted entries by marking it as free or reserved (e.g., by using a reserved inode number like `0`).

---

### **2. Linked-List Based Allocation in File Systems:**
- **Linked Allocation**: A simpler approach to storing files is using a **linked list** where each block contains a pointer to the next block in the file. This avoids having multiple pointers for each block in the inode. 
  - Each inode only needs a pointer to the first block of the file. 
  - If the file is larger than a single block, additional pointers are added to each block to link to the next one.
  
- **Problems with Linked Allocation**:
  - **Performance**: Linked allocation can perform poorly for random access and file reads, as each block requires scanning through the chain of pointers.
  - **Solution**: To improve random access, some file systems use an **in-memory table** of next pointers (the equivalent of a **File Allocation Table**, or FAT). This table stores the next pointers for blocks, so random access to files becomes more efficient by first checking the table in memory and then accessing the data block directly.

- **FAT File System**: The FAT file system, historically used by Windows, is based on a linked allocation approach where each file’s blocks are linked through pointers, and a table (the **FAT**) keeps track of which blocks belong to which files.

---

### **3. Directories as Special Files:**
- **Directories in File Systems**: Directories are treated as special types of files. They also have inodes, which contain metadata about the directory (such as its type). The inode for a directory typically points to data blocks that contain directory entries (pairs of filenames and inode numbers).
- **Storage in Data Blocks**: These directory entries are stored in **data blocks** of the file system (which reside in the data block region).

- **Directory Structures**: Although directories are often stored as simple lists of directory entries, file systems can use more sophisticated structures like **B-trees** to store directories, making file creation operations (and file lookups) faster.

---

### **4. Free Space Management:**
- **Importance of Free Space Management**: A file system must track which **inodes** and **data blocks** are free and which are occupied, to ensure space can be allocated efficiently when a new file or directory is created.
  
- **Bitmaps**: In **vsfs**, free space is tracked using two **bitmaps**: one for inodes and one for data blocks.
  - Each bitmap bit represents a block or inode, where `1` means it is in use, and `0` means it is free.
  
- **Allocation of Inodes and Data Blocks**:
  - When a new file is created, the file system searches the bitmap for a free inode and allocates it to the new file. The inode is then marked as used.
  - Similarly, a free data block is located and allocated for the file's data. Once allocated, the block is marked as in use in the bitmap.

- **Pre-allocation for Performance**: Some file systems (like **ext2** and **ext3** in Linux) use a pre-allocation strategy where contiguous blocks are allocated for a file. This reduces fragmentation and improves performance by keeping file data blocks close together on disk.

- **Other Allocation Strategies**: Some file systems may use more advanced data structures like **B-trees** to manage free space, which allows efficient space management and faster allocation of blocks.

---

### **5. Key Points to Remember for Exam:**
- **Directory entries** store pairs of **(name, inode number)** and have additional attributes such as **record length** and **string length**.
- **Inode structure** contains file metadata, including pointers to the **data blocks** of the file, which may be direct or indirect (single, double, or triple).
- **Linked allocation** (used in FAT file systems) links blocks through pointers, but this can be inefficient for random access. In-memory tables improve this by caching pointer information.
- **Free space management** in file systems uses **bitmaps** to track which inodes and data blocks are free and which are occupied. Efficient allocation strategies like **pre-allocation** improve performance.
- **Directories** are treated as special files and contain entries pointing to other files or directories via their inode numbers.

This summary captures the key points you’ll need to understand for your exams, covering directory structures, inode management, file allocation schemes, and free space management in file systems.



### Summary of File System Access Paths: Reading and Writing

Understanding the process of reading and writing files is critical to understanding how file systems operate. In this section, we explore the flow of operations that occur when a file is accessed for reading or writing. The file system uses various structures like inodes, directories, bitmaps, and data blocks to manage and interact with files.

---

### 1. **Reading a File from Disk**
When reading a file (e.g., `/foo/bar`), the file system follows these steps:

- **Open the File**: 
  - To open a file, the file system first needs to locate its **inode**. This is done by traversing the file path. For example, in a path like `/foo/bar`, the file system starts at the **root** directory (`/`).
  - The **inode** of the root directory is a known value (usually `2` in UNIX systems). The system will read the block containing the root inode, which points to the data blocks of the root directory.

- **Directory Traversal**:
  - The file system reads through the directory's data blocks to find the entry for `foo`. Once the directory entry for `foo` is found, the inode number for `foo` is located (e.g., `44`).
  - The file system repeats this process for the directory entry `bar` under `foo`, eventually obtaining the inode for `bar`.

- **Reading the File**:
  - Once the inode for `bar` is found, the file system reads the data blocks for `bar`. It consults the inode to find the block pointers and reads the blocks in sequence.
  - As each block is read, the inode’s **last-accessed time** may be updated.
  
- **Closing the File**: 
  - When done, the file is closed, and the file descriptor is deallocated. No further disk I/O is needed at this point.

### Key Takeaways from File Reading:
- **Traversal Costs**: The amount of I/O depends on the file path length. For each additional directory in the path, additional I/O operations (reading inode and directory data) are required.
- **Efficiency Impact**: The cost increases with long paths and large directories.

---

### 2. **Writing a File to Disk**
Writing to a file is a more complex process because it may involve allocating new blocks. Here's how it works:

- **Opening the File**: 
  - Like reading, the file must first be opened, and the inode information is read into memory.

- **Allocating Blocks**:
  - When writing, if the data block is being overwritten, no allocation is needed. However, if new blocks are needed (e.g., for appending data), the system must find a free block.
  - The file system updates the **bitmap** (to mark the block as used), the **inode** (with the new block’s address), and writes the data block.

- **Write I/O Operations**:
  - Writing involves multiple I/O operations:
    1. Read the data bitmap to find a free block.
    2. Write to the data bitmap to mark the block as allocated.
    3. Read the inode to update it with the new block address.
    4. Write the inode back to disk.
    5. Write the actual data block to disk.

### Key Takeaways from File Writing:
- **Write Costs**: Each write operation generally results in **five I/O operations**:
  1. Read the bitmap.
  2. Write the bitmap.
  3. Read the inode.
  4. Write the inode.
  5. Write the data block.
  
- **File Creation**:
  - When creating a file, the system must allocate not only a new data block but also a new inode. The steps for file creation are as follows:
    1. Read the inode bitmap to find a free inode.
    2. Write to the inode bitmap to mark it as allocated.
    3. Write the inode data to disk.
    4. Update the directory entry to include the new file.
    5. Update the directory inode if necessary.
  
  - The number of I/Os required to create a file is substantial (about **10 I/O operations**), making file creation particularly I/O intensive.

### 3. **Challenges in File System I/O**:
- **High I/O Overhead**: The I/O cost of even basic operations like opening or writing to a file is quite high due to the need to read and update multiple structures (bitmaps, inodes, data blocks, etc.).
- **Efficiency Trade-offs**: To reduce the high costs associated with file access, file systems need to use strategies to minimize unnecessary I/Os. This involves optimizing disk access patterns and structuring data for efficient retrieval.

---

### 4. **Key Strategies for Reducing File System I/O Costs**:
- **Caching**: Frequently accessed data (e.g., inodes, directory entries) is often cached in memory to reduce the need for disk access.
- **Block Allocation Optimizations**: File systems can use techniques like block grouping to reduce fragmentation and minimize disk seeks.
- **Efficient Directory Structures**: To speed up directory lookups, file systems may employ balanced tree structures (like B-trees) for directories rather than linear searches.
- **Pre-allocation**: File systems can pre-allocate blocks or extend file space to reduce fragmentation and the need for repeated allocations.

---

### Conclusion:
The operations for reading and writing files in a file system involve a series of I/O operations to access and update various structures, including inodes, directories, and bitmaps. While reading mainly involves traversing directories and accessing data blocks, writing requires more complex operations, particularly block allocation. These I/O operations can add up quickly, especially when creating or updating files. Optimizing file system I/O is essential to improve the performance of file systems.






Summary of Caching and Buffering in File Systems
Introduction to Caching and Buffering
Performance Problem: Reading and writing files can be slow due to multiple I/O operations required to access data on disk.
Caching: Most file systems use system memory (DRAM) to cache important blocks to improve performance.
File Open Example Without Caching
I/O Traffic: Opening a file requires multiple reads for each level in the directory hierarchy. For a long pathname (e.g., /1/2/3/.../100/file.txt), this could result in hundreds of reads just to open the file.
Early File Systems
Fixed-Size Cache: Early systems implemented a fixed-size cache (about 10% of total memory) to hold popular blocks.
Cache Management: Strategies like Least Recently Used (LRU) were used to decide which blocks to keep in the cache.
Limitations of Static Partitioning
Wastefulness: Static partitioning can lead to wasted memory if the file system does not need the allocated cache space at a given time.
Unused Pages: Unused pages in the file cache cannot be repurposed for other uses.
Modern Systems and Dynamic Partitioning
Unified Page Cache: Modern operating systems use a dynamic partitioning approach, integrating virtual memory pages and file system pages into a unified page cache.
Flexible Memory Allocation: This allows for more flexible memory allocation based on current needs, improving overall resource utilization.
Caching Effects on File Operations
Subsequent File Opens: After the initial file open, subsequent opens will mostly hit the cache, significantly reducing I/O operations.
Caching Effects on Writes
Write Traffic: Unlike reads, writes must go to disk to ensure data persistence.
Write Buffering: Write buffering allows the system to delay writes, which can lead to several performance benefits:
Batching Updates: Multiple updates can be batched into fewer I/O operations.
Scheduling I/Os: The system can schedule writes more efficiently.
Avoiding Writes: Delaying writes can avoid unnecessary writes, such as when a file is created and then immediately deleted.
Write Buffering Duration
Time Frame: Most modern file systems buffer writes in memory for 5 to 30 seconds.
Trade-Off: While this improves performance, it poses a risk of data loss if the system crashes before the updates are written to disk.
Durability vs. Performance Trade-Off
Immediate Durability: If immediate durability is required, the system must commit data to disk, resulting in slower writes.
Buffered Writes: If some data loss is acceptable, writes can be buffered, improving perceived performance but risking data loss in case of a crash.
Application Requirements: Understanding the specific needs of applications is crucial for making the right trade-off. For example, losing recent web browser downloads may be acceptable, but losing part of a financial transaction is not.
Application-Specific Considerations
Databases: Applications like databases often require immediate durability and may bypass the file system's buffering by using methods like fsync(), direct I/O, or raw disk interfaces to ensure data integrity.
Conclusion











41.7
A Few Other Things About FFS
FFS introduced a few other innovations too. In particular, the design-
ers were extremely worried about accommodating small files; as it turned
out, many files were 2KB or so in size back then, and using 4KB blocks,
while good for transferring data, was not so good for space efficiency.
This internal fragmentation could thus lead to roughly half the disk be-
ing wasted for a typical file system.
The solution the FFS designers hit upon was simple and solved the
problem. They decided to introduce sub-blocks, which were 512-byte
O PERATING
S YSTEMS
[V ERSION 1.01]
WWW. OSTEP. ORGL OCALITY AND T HE FAST F ILE S YSTEM
8
9
10
7
4
11
Spindle
6
5
4
3
11
2
10
5
9
03
18
11
Spindle
0
6
2
7
1
Figure 41.3: FFS: Standard Versus Parameterized Placement
little blocks that the file system could allocate to files. Thus, if you created
a small file (say 1KB in size), it would occupy two sub-blocks and thus not
waste an entire 4KB block. As the file grew, the file system will continue
allocating 512-byte blocks to it until it acquires a full 4KB of data. At that
point, FFS will find a 4KB block, copy the sub-blocks into it, and free the
sub-blocks for future use.
You might observe that this process is inefficient, requiring a lot of ex-
tra work for the file system (in particular, a lot of extra I/O to perform the
copy). And you’d be right again! Thus, FFS generally avoided this pes-
simal behavior by modifying the libc library; the library would buffer
writes and then issue them in 4KB chunks to the file system, thus avoid-
ing the sub-block specialization entirely in most cases.
A second neat thing that FFS introduced was a disk layout that was
optimized for performance. In those times (before SCSI and other more
modern device interfaces), disks were much less sophisticated and re-
quired the host CPU to control their operation in a more hands-on way.
A problem arose in FFS when a file was placed on consecutive sectors of
the disk, as on the left in Figure 41.3.
In particular, the problem arose during sequential reads. FFS would
first issue a read to block 0; by the time the read was complete, and FFS
issued a read to block 1, it was too late: block 1 had rotated under the
head and now the read to block 1 would incur a full rotation.
FFS solved this problem with a different layout, as you can see on the
right in Figure 41.3. By skipping over every other block (in the example),
FFS has enough time to request the next block before it went past the
disk head. In fact, FFS was smart enough to figure out for a particular
disk how many blocks it should skip in doing layout in order to avoid the
extra rotations; this technique was called parameterization, as FFS would
figure out the specific performance parameters of the disk and use those
to decide on the exact staggered layout scheme.
You might be thinking: this scheme isn’t so great after all. In fact, you
will only get 50% of peak bandwidth with this type of layout, because
you have to go around each track twice just to read each block once. For-
tunately, modern disks are much smarter: they internally read the entire
c 2008–19, A RPACI -D USSEAU
T HREE
E ASY
P IECES12
L OCALITY AND T HE FAST F ILE S YSTEM
T IP : M AKE T HE S YSTEM U SABLE
Probably the most basic lesson from FFS is that not only did it intro-
duce the conceptually good idea of disk-aware layout, but it also added
a number of features that simply made the system more usable. Long file
names, symbolic links, and a rename operation that worked atomically
all improved the utility of a system; while hard to write a research pa-
per about (imagine trying to read a 14-pager about “The Symbolic Link:
Hard Link’s Long Lost Cousin”), such small features made FFS more use-
ful and thus likely increased its chances for adoption. Making a system
usable is often as or more important than its deep technical innovations.
track in and buffer it in an internal disk cache (often called a track buffer
for this very reason). Then, on subsequent reads to the track, the disk will
just return the desired data from its cache. File systems thus no longer
have to worry about these incredibly low-level details. Abstraction and
higher-level interfaces can be a good thing, when designed properly.
Some other usability improvements were added as well. FFS was one
of the first file systems to allow for long file names, thus enabling more
expressive names in the file system instead of the traditional fixed-size
approach (e.g., 8 characters). Further, a new concept was introduced
called a symbolic link. As discussed in a previous chapter [AD14b] ,
hard links are limited in that they both could not point to directories (for
fear of introducing loops in the file system hierarchy) and that they can
only point to files within the same volume (i.e., the inode number must
still be meaningful). Symbolic links allow the user to create an “alias” to
any other file or directory on a system and thus are much more flexible.
FFS also introduced an atomic rename() operation for renaming files.
Usability improvements, beyond the basic technology, also likely gained
FFS a stronger user base.

create a detailed summary and make sure you dont miss any important details/topic because i have to study for my exams





Crash Consistency: FSCK and Journaling
As we’ve seen thus far, the file system manages a set of data structures to
implement the expected abstractions: files, directories, and all of the other
metadata needed to support the basic abstraction that we expect from a
file system. Unlike most data structures (for example, those found in
memory of a running program), file system data structures must persist,
i.e., they must survive over the long haul, stored on devices that retain
data despite power loss (such as hard disks or flash-based SSDs).
One major challenge faced by a file system is how to update persis-
tent data structures despite the presence of a power loss or system crash.
Specifically, what happens if, right in the middle of updating on-disk
structures, someone trips over the power cord and the machine loses
power? Or the operating system encounters a bug and crashes? Because
of power losses and crashes, updating a persistent data structure can be
quite tricky, and leads to a new and interesting problem in file system
implementation, known as the crash-consistency problem.
This problem is quite simple to understand. Imagine you have to up-
date two on-disk structures, A and B, in order to complete a particular
operation. Because the disk only services a single request at a time, one
of these requests will reach the disk first (either A or B). If the system
crashes or loses power after one write completes, the on-disk structure
will be left in an inconsistent state. And thus, we have a problem that all
file systems need to solve:
T HE C RUX : H OW T O U PDATE T HE D ISK D ESPITE C RASHES
The system may crash or lose power between any two writes, and
thus the on-disk state may only partially get updated. After the crash,
the system boots and wishes to mount the file system again (in order to
access files and such). Given that crashes can occur at arbitrary points
in time, how do we ensure the file system keeps the on-disk image in a
reasonable state?
12
C RASH C ONSISTENCY: FSCK AND J OURNALING
In this chapter, we’ll describe this problem in more detail, and look
at some methods file systems have used to overcome it. We’ll begin by
examining the approach taken by older file systems, known as fsck or the
file system checker. We’ll then turn our attention to another approach,
known as journaling (also known as write-ahead logging), a technique
which adds a little bit of overhead to each write but recovers more quickly
from crashes or power losses. We will discuss the basic machinery of
journaling, including a few different flavors of journaling that Linux ext3
[T98,PAA05] (a relatively modern journaling file system) implements.
42.1
A Detailed Example
To kick off our investigation of journaling, let’s look at an example.
We’ll need to use a workload that updates on-disk structures in some
way. Assume here that the workload is simple: the append of a single
data block to an existing file. The append is accomplished by opening the
file, calling lseek() to move the file offset to the end of the file, and then
issuing a single 4KB write to the file before closing it.
Let’s also assume we are using standard simple file system structures
on the disk, similar to file systems we have seen before. This tiny example
includes an inode bitmap (with just 8 bits, one per inode), a data bitmap
(also 8 bits, one per data block), inodes (8 total, numbered 0 to 7, and
spread across four blocks), and data blocks (8 total, numbered 0 to 7).
Here is a diagram of this file system:
Bitmaps
Inodes
Data Blocks
I[v1]
Inode Data
Da
0 1 2 3 4 5 6 7
0
1
2
3
4
5
6
7
If you look at the structures in the picture, you can see that a single inode
is allocated (inode number 2), which is marked in the inode bitmap, and a
single allocated data block (data block 4), also marked in the data bitmap.
The inode is denoted I[v1], as it is the first version of this inode; it will
soon be updated (due to the workload described above).
Let’s peek inside this simplified inode too. Inside of I[v1], we see:
owner
: remzi
permissions : read-write
size
: 1
pointer
: 4
pointer
: null
pointer
: null
pointer
: null
In this simplified inode, the size of the file is 1 (it has one block al-
located), the first direct pointer points to block 4 (the first data block of
O PERATING
S YSTEMS
[V ERSION 1.01]
WWW. OSTEP. ORGC RASH C ONSISTENCY: FSCK AND J OURNALING
3
the file, Da), and all three other direct pointers are set to null (indicating
that they are not used). Of course, real inodes have many more fields; see
previous chapters for more information.
When we append to the file, we are adding a new data block to it, and
thus must update three on-disk structures: the inode (which must point
to the new block and record the new larger size due to the append), the
new data block Db, and a new version of the data bitmap (call it B[v2]) to
indicate that the new data block has been allocated.
Thus, in the memory of the system, we have three blocks which we
must write to disk. The updated inode (inode version 2, or I[v2] for short)
now looks like this:
owner
: remzi
permissions : read-write
size
: 2
pointer
: 4
pointer
: 5
pointer
: null
pointer
: null
The updated data bitmap (B[v2]) now looks like this: 00001100. Finally,
there is the data block (Db), which is just filled with whatever it is users
put into files. Stolen music perhaps?
What we would like is for the final on-disk image of the file system to
look like this:
Bitmaps
Inodes
Data Blocks
I[v2]
Inode Data
0 1 2 3 4 5 6 7
0
1
2
3
DaDb
45
6
7
To achieve this transition, the file system must perform three sepa-
rate writes to the disk, one each for the inode (I[v2]), bitmap (B[v2]), and
data block (Db). Note that these writes usually don’t happen immedi-
ately when the user issues a write() system call; rather, the dirty in-
ode, bitmap, and new data will sit in main memory (in the page cache
or buffer cache) for some time first; then, when the file system finally
decides to write them to disk (after say 5 seconds or 30 seconds), the file
system will issue the requisite write requests to the disk. Unfortunately,
a crash may occur and thus interfere with these updates to the disk. In
particular, if a crash happens after one or two of these writes have taken
place, but not all three, the file system could be left in a funny state.
Crash Scenarios
To understand the problem better, let’s look at some example crash sce-
narios. Imagine only a single write succeeds; there are thus three possible
outcomes, which we list here:
c 2008–19, A RPACI -D USSEAU
T HREE


Just the data block (Db) is written to disk. In this case, the data is
on disk, but there is no inode that points to it and no bitmap that
even says the block is allocated. Thus, it is as if the write never
occurred. This case is not a problem at all, from the perspective of
file-system crash consistency1 .
• Just the updated inode (I[v2]) is written to disk. In this case, the
inode points to the disk address (5) where Db was about to be writ-
ten, but Db has not yet been written there. Thus, if we trust that
pointer, we will read garbage data from the disk (the old contents
of disk address 5).
Further, we have a new problem, which we call a file-system in-
consistency. The on-disk bitmap is telling us that data block 5 has
not been allocated, but the inode is saying that it has. The disagree-
ment between the bitmap and the inode is an inconsistency in the
data structures of the file system; to use the file system, we must
somehow resolve this problem (more on that below).
• Just the updated bitmap (B[v2]) is written to disk. In this case, the
bitmap indicates that block 5 is allocated, but there is no inode that
points to it. Thus the file system is inconsistent again; if left unre-
solved, this write would result in a space leak, as block 5 would
never be used by the file system.
There are also three more crash scenarios in this attempt to write three
blocks to disk. In these cases, two writes succeed and the last one fails:
• The inode (I[v2]) and bitmap (B[v2]) are written to disk, but not
data (Db). In this case, the file system metadata is completely con-
sistent: the inode has a pointer to block 5, the bitmap indicates that
5 is in use, and thus everything looks OK from the perspective of
the file system’s metadata. But there is one problem: 5 has garbage
in it again.
• The inode (I[v2]) and the data block (Db) are written, but not the
bitmap (B[v2]). In this case, we have the inode pointing to the cor-
rect data on disk, but again have an inconsistency between the in-
ode and the old version of the bitmap (B1). Thus, we once again
need to resolve the problem before using the file system.
• The bitmap (B[v2]) and data block (Db) are written, but not the
inode (I[v2]). In this case, we again have an inconsistency between
the inode and the data bitmap. However, even though the block
was written and the bitmap indicates its usage, we have no idea
which file it belongs to, as no inode points to the file.
1
O PERATING
S YSTEMS
[V ERSION 1.01]
However, it might be a problem for the user, who just lost some data!
WWW. OSTEP. ORGC RASH C ONSISTENCY: FSCK AND J OURNALING
5
The Crash Consistency Problem
Hopefully, from these crash scenarios, you can see the many problems
that can occur to our on-disk file system image because of crashes: we can
have inconsistency in file system data structures; we can have space leaks;
we can return garbage data to a user; and so forth. What we’d like to do
ideally is move the file system from one consistent state (e.g., before the
file got appended to) to another atomically (e.g., after the inode, bitmap,
and new data block have been written to disk). Unfortunately, we can’t
do this easily because the disk only commits one write at a time, and
crashes or power loss may occur between these updates. We call this
general problem the crash-consistency problem (we could also call it the
consistent-update problem).
create a detailed summary and make sure you dont miss any important details/topic because i have to study for my exams


