import threading
import time
import subprocess
import os.path
import logging
from glob import glob
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")

def squeue():
    return subprocess.getoutput("squeue -l")

class Job:
    def __init__(self, jobid, partition, name, user, state, time, time_limi,
        nodes, nodelist, *kwargs):
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

    def get_experiment_dir(self):
        found = None
        for job_id_file in glob("/var/scratch/pse740/*/job_id"):
            with open(job_id_file, "r") as f:
                if f.readline() == "Submitted batch job %s" % self.jobid:
                    found = os.path.dirname(job_id_file)
                    break
        return found

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
        self._finished = []
        self.message_callback = message_callback
        self._itt_count = 0

    def start(self):
        threading.Thread(target = self._start).start()

    def _start(self):
        while True:
            updates = [] # type: (str, List[(str, str, str)])
            new_jobs = [] # type: List[Job]
            job_count = 0
            job_names = []
            for job in get_jobs_of_user(squeue(), "pse740"):
                job_names.append(job.name)
                job_count += 1
                if job.jobid not in self.jobs:
                    self.jobs[job.jobid] = job
                    new_jobs.append(job)
                else:
                    changes = self.jobs[job.jobid].update(job)
                    if changes: updates.append((job.name, changes))
            
            just_finished_jobs = []
            for name in self.jobs:
                if name not in self._finished and name not in job_names:
                    self._finished.append(name)
                    just_finished_jobs.append(name)

            msg = self._make_message(updates, new_jobs, job_count, just_finished_jobs)
            if msg:
                self.message_callback(msg)
                logging.info(msg)
            if self._itt_count % 10 == 0:
                logging.info("Still checking round #%d" % self._itt_count)
            time.sleep(1)
            self._itt_count += 1

    def _make_message(self, updates: (str, any), new_jobs, job_count, just_finished_jobs):
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
        if just_finished_jobs:
            if res: res.append(" ")
            res.append("*Just finished:*")
            for jobname in just_finished_jobs:
                dir = self.jobs[jobname].get_experiment_dir()
                if dir:
                    res.append("- %s | last few lines:```" % jobname)
                    stdout = subprocess.getoutput("tail %s/slurm_*.out -n 10" % dir)
                    res += stdout.split("\n")
                    res.append("```")
                else:
                    res.append("- %s" % jobname)

        if self._itt_count % 600 == 0:
            res.append("Still monitoring _%d_ jobs" % job_count)
        return "\n".join(res)

