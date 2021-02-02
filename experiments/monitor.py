import threading
import time
from typing import List
def squeue():
    return """Tue Feb  2 15:53:41 2021
             JOBID PARTITION     NAME     USER    STATE       TIME TIME_LIMI  NODES NODELIST(REASON)
           2928162      knlq  bgs.job   wwe300  PENDING       0:00 7-00:00:00      1 (Resources)
           2932072      knlq  bgs.job   wwe300  PENDING       0:00 7-00:00:00      1 (Priority)
           2932073      knlq  bgs.job   wwe300  PENDING       0:00 7-00:00:00      1 (Priority)
           2932074      knlq  bgs.job   wwe300  PENDING       0:00 7-00:00:00      1 (Priority)
           2932075      knlq  bgs.job   wwe300  PENDING       0:00 7-00:00:00      1 (Priority)
           2932293      defq Pretrain   rwr850  PENDING       0:00  15:00:00      5 (BeginTime)
           2910117      defq prun-job  jurbani  RUNNING 3-06:59:27 4-04:01:00      1 node001
           2910282      defq prun-job  jurbani  RUNNING 3-06:41:16 4-04:01:00      1 node002
           2910283      defq prun-job  jurbani  RUNNING 3-06:41:05 4-04:01:00      1 node024
           2910284      defq prun-job  jurbani  RUNNING 3-06:41:00 4-04:01:00      1 node025
           2910286      defq prun-job  jurbani  RUNNING 3-06:40:27 4-04:01:00      1 node051
           2914304      defq prun-job   mao540  RUNNING 2-16:08:37 4-04:01:00      1 node026
           2918004      knlq  bgs.job   wwe300  RUNNING    8:48:42 7-00:00:00      1 node077
           2928161      knlq  bgs.job   wwe300  RUNNING    6:31:06 7-00:00:00      1 node076
           2928773      defq prun-job   ajs870  RUNNING    8:20:39 1-06:01:00      1 node052
           2932041      defq prun-job   ajs870  RUNNING    5:43:02 1-00:01:00      2 node[004-005]
           2932060      proq synthlp.   wwe300  RUNNING    5:17:38 5-00:00:00      1 node069
           2932061      proq synthlp.   wwe300  RUNNING    5:17:29 5-00:00:00      1 node070
           2932067      defq  067.job   ppz600  RUNNING    5:15:56   6:00:00      1 node053
           2932093      defq  665.job   ppz600  RUNNING    5:00:18   6:00:00      1 node061
           2932096      defq  667.job   ppz600  RUNNING    4:58:40   6:00:00      1 node057
           2932105      defq 1245.job   ppz600  RUNNING    4:52:49 1-00:00:00      1 node058
           2932107      defq 1247.job   ppz600  RUNNING    4:52:49 1-00:00:00      1 node060
           2932132      defq 1265.job   ppz600  RUNNING    4:30:58 1-00:00:00      1 node054
           2932133      defq 1267.job   ppz600  RUNNING    4:30:55 1-00:00:00      1 node055
           2932155      defq 1447.job   ppz600  RUNNING    4:10:11 1-00:00:00      1 node063
           2932156      defq 1445.job   ppz600  RUNNING    4:09:21  12:00:00      1 node064
           2932160      defq 1465.job   ppz600  RUNNING    4:02:40 1-00:00:00      1 node065
           2932168      defq  067.job   ppz600  RUNNING    3:55:45  12:00:00      1 node062
           2932170      defq run-quer   pse740  RUNNING    3:55:22   6:40:00      1 node066
           2932217      defq 1245.job   ppz600  RUNNING    3:05:51 1-00:00:00      1 node068
           2932393      proq       ae   ama228  RUNNING    1:19:37 20-20:00:00      1 node071
           2932397      defq yago3-10   wwe300  RUNNING    1:16:38 7-00:00:00      1 node006
           2932398      defq yago3-10   wwe300  RUNNING    1:16:34 7-00:00:00      1 node046
           2932456      defq prun-job  ppp2047  RUNNING      13:57     16:00      2 node[059,067]
"""
class Job:
    def __init__(self, jobid, partition, name, user, state, time, time_limi,
        nodes, nodelist):
        self.jobid = jobid
        self.partition = partition
        self.name = name
        self.user = user
        self.state = state
        self.time = time
        self.time_limi = time_limi
        self.nodes = nodes
        self.nodelist = nodelist
    
    def update(self, job) -> List:
        res = []
        if self.state != job.state:
            res.append("state", self.state, job.state)
            self.state = job.state
        if self.nodes != job.nodes:
            res.append("nodes", self.nodes, job.nodes)
            self.nodes = job.nodes
        if self.nodelist != job.nodelist:
            res.append("nodelist", self.nodelist, job.nodelist)
            self.nodelist = job.nodelist
        return res

    @staticmethod
    def prase_row(row):
        return Job(*row)
def get_jobs(data):
    HEADER_ENDING = "NODELIST(REASON)"
    rows = data[data.index(HEADER_ENDING)+len(HEADER_ENDING)+1:].split("\n")

    return [Job.prase_row(row) for row in [row.strip().split() for row in rows] if row]
        

def get_jobs_of_user(data, username):
    return [job for job in get_jobs(data) if job.user == username]


class JobMonitor:
    def __init__(self, message_callback):
        self.jobs = {}
        self.message_callback = message_callback
        self._itt_count = 0

    def start(self):
        threading.Thread(target = self._start).start()

    def _start(self):
        while True:
            updates = [] # type: (str, List[(str, str, str)])
            new_jobs = [] # type: List[Job]
            job_count = 0
            for job in get_jobs_of_user(squeue(), "pse740"):
                job_count += 1
                if job.name not in self.jobs:
                    self.jobs[job.name] = job
                    new_jobs.append(job)
                else:
                    changes = self.jobs[job.name].update(job)
                    if changes: updates.append((job.name, changes))

            msg = self._make_message(updates, new_jobs, job_count)
            if msg: self.message_callback(msg)
            time.sleep(1)

    def _make_message(self, updates: (str, List), new_jobs: List[Job], job_count):
        res = []
        if new_jobs:
            res.append("*New jobs:*")
            for job in new_jobs:
                res.append("- %s [%s]" % (job.name, job.state))
        if updates:
            if res: res.append(" ")
            res.append("*Job updates:*")
            for job in updates:
                for change in job[1]:
                    res.append("- %s ['%s': '%s' -> '%s']" % (job[0], change[0], change[1], change[2]))
        if self._itt_count == 600:
            self._itt_count = 0
            if not res:
                res.append("Still monitoring _%d_ jobs" % job_count)
        self._itt_count += 1
        return "\n".join(res)

