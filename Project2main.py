import sys
import random


class Job:
    def __init__(self, name, min_run, max_run, min_mem, max_mem):
        self.job = name
        self.runT = random.randrange(min_run, max_run)
        self.mem = random.randrange(min_mem, max_mem)

    def __repr__(self):
        return "Job: [name: {0}, time: {1}, mem: {2}]".format(self.job, self.runT, self.mem)


cpumem = None
pagesize = None
jobnum = None
readyQ = []
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

    print("Simulator Parameters: \n Memory Size: {0} \n Page Size: {1} \n Random Seed: ".format(cpumem, pagesize))
    print(" Number of jobs: {0} \n Runtime (min - max): {1}-{2} \n Memory (min - max): {3}-{4}".format(jobnum, minrun,
                                                                                                       maxrun, minmem,
                                                                                                       maxmem))

    for x in range(jobnum):
        readyQ.append(Job(("Job " + str(x)), minrun, maxrun, minmem, maxmem))

    print("\nJob Queue: ")
    print(" / Job #  / Runtime  / Memory / ")
    for i in range(len(readyQ)):
        print("| {0}        {1}      {2}".format(readyQ[i].job, readyQ[i].runT, readyQ[i].mem))
