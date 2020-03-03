import sys
import random
import math

cpumem = None  # global variable for the total amt of memory
pagesize = None  # global variable for the size of a page
jobnum = None  # global variable for the total number of jobs
pagetable = []  # global array for page table
jobQ = []  # global array for Job Queue (stores jobs that haven't had memory allocated/executed)
readyQ = []  # global array for Ready Queue (stores jobs that have had memory allocated but aren't being executed
runningQ = []  # global array for Running Queue (stores a single job which is being executed)
finList = []  # global array for Finished Jobs (stores all the jobs as they finish executing completely)


# The Job Queue holds all of the jobs that are waiting to have pages allocated (they haven't been run yet)
# Creates Job object instances and appends them to Job Queue
def initJobQueue():
    for x in range(jobnum):
        jobQ.append(Job((str(x)), minrun, maxrun, minmem, maxmem))


# pushJob, checks to see if any job from the Job Queue can allocate pages in the pagetable.
# if so, the job's arrival time is recorded and its pages are allocated
# and pops the job from the Job Queue and appends it to the Ready Queue
#
# the timeslice parameter is merely there to keep track of the current time slice when the round robin runs
# so that arrival times are accurate
def pushJob(timeslice):
    x = 0
    while x < len(jobQ):
        if jobQ[x].allocatePages():
            jobQ[x].arrival = timeslice
            readyQ.append(jobQ.pop(x))
            x = x - 1
        x = x + 1


# Helper function to check if there's enough free space in the pagetable for a Job
# parameter 'numpage' is the number of pages a specific job needs to allocate
# if there's enough space in the pagetable (counter >= numpage) then return back numpage. Otherwise return False
def enoughPages(numpage):
    counter = 0
    for entry in range(len(pagetable)):
        if pagetable[entry] == '.':
            counter = counter + 1

    if counter >= numpage:
        return numpage
    else:
        return False


# When a job finishes executing its pages in memory need to be freed up
# This function just takes a job name (number) as a parameter and searches through
# the pagetable for any entries that match that job identifier,
# which are then changed to the free space indicator ' . '
def freePageSpace(job_name):
    print("Freeing up memory...")
    for x in range(len(pagetable)):
        if pagetable[x] == job_name:
            pagetable[x] = '.'


# This function removes the next job in line of the Job Queue and places it into the Running Queue
# only one job should be in Running Queue at any given time
def readytorunning():
    print("Moving Job {0} from Ready to Running \n".format(readyQ[0].job))
    runningQ.append(readyQ.pop(0))


# The executeJob function simulates a single time slice
# A job will either run or complete in any given time slice
#
# Run time is updated by decrementing the job object's runtime by one
# if the job does NOT complete, then pop the job from running Queue and append back to ready Queue
#
# if the job completed (run time = 0) mark completion time, ...
# ... free the page space that job was using, pop the job from Running Queue and append it to the Finished Queue
#
# The timeslice parameter is merely there to keep track of the current time slice when the round robin runs
# so that completion times are accurate
def executeJob(timeslice):
    if runningQ[0] is not None:
        runningQ[0].runT = runningQ[0].runT - 1
        print("RUNNING: Job {0}\n".format(runningQ[0].job))
        if runningQ[0].runT == 0:
            print("COMPLETED: Job {0}\n".format(runningQ[0].job))
            runningQ[0].completion = timeslice
            freePageSpace(runningQ[0].job)
            finList.append(runningQ.pop())
        else:
            readyQ.append(runningQ.pop())


# This function just wraps together all the previous functions into one that implements the Round Robin Algorithm
# push jobs onto ready queue if it can be done,
# Move the next job in ReadyQ to RunningQ
# 'Execute' Job
# repeat until no more jobs are to be executed
def roundRobin():
    counter = 0
    while len(finList) < jobnum:
        print("=======Time Slice: {0}========".format(counter))
        pushJob(counter)
        printReadyQueue()
        readytorunning()
        executeJob(counter)
        printPagetable()
        counter = counter + 1


# prints the ready queue
#  Job name|run time
def printReadyQueue():
    print("Ready Queue: ")
    for x in range(len(readyQ)):
        print("Job " + readyQ[x].job + "|runtime: " + str(readyQ[x].runT))
    print("\n")


# prints the page table
# groups them into 16 entries per line
def printPagetable():
    for x in range(1, len(pagetable) + 1):
        print(pagetable[x - 1], end=" ")
        if x % 16 == 0:
            print("\n")

    print("\n")


# prints out the Job Queue
# all the jobs that are waiting to have pages allocated and executed
def printJobQueue():
    if len(jobQ) != 0:
        print("\nJob Queue: ")
        print(" / Job #    /  Runtime /   Memory / ")
        for i in range(len(jobQ)):
            print(jobQ[i])
        print("")
    else:
        print("NOTE: No more jobs to queue!\n")


# prints out the finished list of jobs
# sorted by least to greatest completion time
def printResults():
    print("Job Information: ")
    print("| Job # | |Arrival| |Completed|")
    for x in range(len(finList)):
        print("Job:  {0}     {1}        {2}".format(finList[x].job, finList[x].arrival, finList[x].completion))


# Job Obect
class Job:
    arrival = 0  # arrival time of job
    completion = 0  # completion time of job

    # job object initializer
    def __init__(self, name, min_run, max_run, min_mem, max_mem):
        self.job = name
        self.runT = random.randrange(min_run, max_run)  # randomly picks a number between the min and max range
        self.mem = random.randrange(min_mem, max_mem)

    # equivalent to overridden .toString | just prints out the job object nicely
    def __repr__(self):
        return "| Job {0}, Runtime: {1}, MEM: {2} |".format(self.job, self.runT, self.mem)

    # Method to handle allocating pages
    def allocatePages(self):
        pagesForJob = math.ceil(self.mem / pagesize)  # gets the number of pages a job needs

        pageBool = enoughPages(
            pagesForJob)  # if there's enough pages returns back the number of pages needed, else returns false

        if not pageBool:
            return False
        else:
            self.setPage(pageBool)
            return True

    # Sets the page entries to the number of the job
    def setPage(self, numberOfPages):  # sets the pages to the corresponding job number
        pagecount = 0
        for i in range(len(pagetable)):
            if pagetable[i] == '.' and pagecount < numberOfPages:
                pagetable[i] = self.job
                pagecount = pagecount + 1


# 1. size of computer memory, 2. size of a page, 3. # of jobs,
# 4. min run time, 5. max run time  6. min memory, 7. max memory
if __name__ == '__main__':
    # initialize all command line arguments to respective global variables
    cpumem = int(sys.argv[1])
    if cpumem % int(sys.argv[2]) == 0:
        pagesize = int(sys.argv[2])
    else:
        # makes sure that mem size is even multiple of page size
        print("The memory size must be an even multiple of the page size")
        sys.exit()

    jobnum = int(sys.argv[3])
    minrun = int(sys.argv[4])
    maxrun = int(sys.argv[5])
    minmem = int(sys.argv[6])
    maxmem = int(sys.argv[7])

    # initialize the page table to all free spaces (.)
    pagetable = ['.'] * math.ceil((cpumem / pagesize))

    # print out of the parameters
    print("Simulator Parameters: \n Memory Size: {0} \n Page Size: {1} \n Random Seed: ".format(cpumem, pagesize))
    print(" Number of jobs: {0} \n Runtime (min - max): {1}-{2} \n Memory (min - max): {3}-{4}".format(jobnum, minrun,
                                                                                                       maxrun, minmem,
                                                                                                       maxmem))
    # initialize job queue
    initJobQueue()
    # quick printout of jobs in job queue
    printJobQueue()
    # preform round robin process
    roundRobin()
    # finally print the results
    printResults()
