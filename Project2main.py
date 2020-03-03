import sys
import random
import math


class Job:
    def __init__(self, name, min_run, max_run, min_mem, max_mem):
        self.job = name
        self.runT = random.randrange(min_run, max_run)
        self.mem = random.randrange(min_mem, max_mem)

    def __repr__(self):
        return "[{0}, time: {1}, mem: {2}]".format(self.job, self.runT, self.mem)

    def allocatePages(self):
        temp = math.ceil(self.mem / pagesize)  # gets the number of pages a job needs

        for k in range(len(pagetable)):         # loop through entire pagetable
            if pagetable[k] == '.':             # find the first free space
                if temp + k <= len(pagetable):  # make sure there's continous page space
                    for j in range(k, temp + k):  # make sure there's continous free page space
                        if pagetable[j] != '.':
                            break                # if there's not continous free space break out and try the next
                                                 # position

                    self.setPage(k, k + temp)  # if there is continous free space,
                                                # then set those pages to the corresponding job number
                    return True
        return False

    def setPage(self, start, end):  # sets the pages to the corresponding job number
        for i in range(start, end):
            pagetable[i] = self.job


cpumem = None
pagesize = None
jobnum = None
pagetable = []
jobQ = []
readyQ = []
runningQ = []


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

    for x in range(jobnum):
        jobQ.append(Job((str(x)), minrun, maxrun, minmem, maxmem))
        if jobQ[x].allocatePages():
            readyQ.append(jobQ[x])

    print(readyQ)
    print(pagetable)

    print("\nJob Queue: ")
    print(" / Job #    /  Runtime /   Memory / ")
    for i in range(len(jobQ)):
        print(jobQ[i])
