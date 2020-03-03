import sys
import random
import math


class Job:
    arrival = 0
    completion = 0

    def __init__(self, name, min_run, max_run, min_mem, max_mem):
        self.job = name
        self.runT = random.randrange(min_run, max_run)
        self.mem = random.randrange(min_mem, max_mem)

    def __repr__(self):
        return "| Job {0}, Runtime: {1}, MEM: {2} |".format(self.job, self.runT, self.mem)

    def allocatePages(self):
        pagesForJob = math.ceil(self.mem / pagesize)  # gets the number of pages a job needs

        pageBool = enoughPages(pagesForJob)   #if there's enough pages returns back the number of pages needed, else returns false

        if not pageBool:
            return False
        else:
            self.setPage(pageBool)
            return True

    def setPage(self, numberOfPages):  # sets the pages to the corresponding job number
        pagecount = 0
        for i in range(len(pagetable)):
            if pagetable[i] == '.' and pagecount < numberOfPages:
                pagetable[i] = self.job
                pagecount = pagecount+1


def enoughPages(numpage):
    counter = 0
    for entry in range(len(pagetable)):
        if pagetable[entry] == '.':
            counter = counter + 1

    if counter >= numpage:
        return numpage
    else:
        return False


def initJobQueue():
    for x in range(jobnum):
        jobQ.append(Job((str(x)), minrun, maxrun, minmem, maxmem))


def pushJob(timeslice):
    x = 0
    while x < len(jobQ):
        if jobQ[x].allocatePages():
            jobQ[x].arrival = timeslice
            readyQ.append(jobQ.pop(x))
            x = x - 1
        x = x + 1


def printPagetable():
    for x in range(1, len(pagetable) + 1):
        print(pagetable[x - 1], end=" ")
        if x % 16 == 0:
            print("\n")

    print("\n")


def printReadyQueue():
    print("Ready Queue: ", end=" ")
    for x in range(len(readyQ)):
        print("Job " + readyQ[x].job + "|", end=" ")
    print("\n")


def printJobQueue():
    if len(jobQ) != 0:
        print("\nJob Queue: ")
        print(" / Job #    /  Runtime /   Memory / ")
        for i in range(len(jobQ)):
             print(jobQ[i])
    else:
        print("NOTE: No more jobs to queue!")


def freePageSpace(job_name):
    print("Freeing up memory...")
    for x in range(len(pagetable)):
        if pagetable[x] == job_name:
            pagetable[x] = '.'


def readytorunning():
    print("Moving Job {0} from Ready to Running".format(readyQ[0].job))
    runningQ.append(readyQ.pop(0))


def executeJob(timeslice):
    if runningQ[0] is not None:
        runningQ[0].runT = runningQ[0].runT - 1
        print("RUNNING: Job {0}".format(runningQ[0].job))
        if runningQ[0].runT == 0:
            print("COMPLETED: Job {0}".format(runningQ[0].job))
            runningQ[0].completion = timeslice
            freePageSpace(runningQ[0].job)
            finList.append(runningQ.pop())
        else:
            readyQ.append(runningQ.pop())


def roundRobin():
    counter = 0
    while len(finList) < jobnum:
        print("=====Time Slice: {0}======".format(counter))
        printJobQueue()
        pushJob(counter)
        printReadyQueue()
        readytorunning()
        executeJob(counter)
        printPagetable()
        counter = counter + 1


def printResults():
    print("| Job # | |Arrival| |Completed|")
    for x in range(len(finList)):
        print("Job:  {0}     {1}        {2}".format(finList[x].job, finList[x].arrival, finList[x].completion))


cpumem = None
pagesize = None
jobnum = None
pagetable = []
jobQ = []
readyQ = []
runningQ = []
finList = []

# 1. size of computer memory, 2. size of a page, 3. # of jobs,
# 4. min run time, 5. max run time  6. min memory, 7. max memory
if __name__ == '__main__':

    cpumem = int(sys.argv[1])
    if cpumem % int(sys.argv[2]) == 0:
        pagesize = int(sys.argv[2])
    else:
        print("The memory size must be an even multiple of the page size")
        sys.exit()

    jobnum = int(sys.argv[3])
    minrun = int(sys.argv[4])
    maxrun = int(sys.argv[5])
    minmem = int(sys.argv[6])
    maxmem = int(sys.argv[7])

    pagetable = ['.'] * math.ceil((cpumem / pagesize))

    print("Simulator Parameters: \n Memory Size: {0} \n Page Size: {1} \n Random Seed: ".format(cpumem, pagesize))
    print(" Number of jobs: {0} \n Runtime (min - max): {1}-{2} \n Memory (min - max): {3}-{4}".format(jobnum, minrun,
                                                                                                       maxrun, minmem,
                                                                                                       maxmem))

    initJobQueue()
    roundRobin()
    printResults()
