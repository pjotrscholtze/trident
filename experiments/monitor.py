import threading
import time
import subprocess
def squeue():
    return subprocess.getoutput("squeue -l")

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
    
    def update(self, job):
        res = []
        if self.state != job.state:
            res.append(("state", self.state, job.state))
            self.state = job.state
        if self.nodes != job.nodes:
            res.append(("nodes", self.nodes, job.nodes))
            self.nodes = job.nodes
        if self.nodelist != job.nodelist:
            res.append(("nodelist", self.nodelist, job.nodelist))
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

    def _make_message(self, updates: (str, any), new_jobs, job_count):
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

