import time
# from projects import Project
from monitor import JobMonitor, Job
import logging
import datetime
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")



class JobLimit:
    def __init__(self, longq_limit: int, defq_limit: int):
        self.longq_limit = longq_limit
        self.defq_limit = defq_limit

class Scheduler:
    WORKING_HOURS_LIMIT = JobLimit(3, 0)
    NON_WORKING_HOURS_LIMIT = JobLimit(3, 2)

    def __init__(self, jm: JobMonitor):
        self.jm = jm
        self._jobs = []
        self._last_update = -1

    def add_job(self, project):
        logging.info("Adding project: '%s'" %project.name)
        self._jobs.append(project)

    def get_limit(self):
        limit = Scheduler.NON_WORKING_HOURS_LIMIT
        hour = datetime.datetime.now().hour
        if hour >= 8 and hour < 20:
            limit = Scheduler.WORKING_HOURS_LIMIT
        return limit
    
    def get_job_counts(self):
        while self._last_update == self.jm._itt_count:
            time.sleep(1)
        self._last_update = self.jm._itt_count
        
        longq = 0
        defq = 0
        for job in self.jm.jobs:
            longq += int(self.jm.jobs[job].partition == "longq")
            defq += int(self.jm.jobs[job].partition == "deqf")
        return longq, defq

    def max_eta(self):
        max_job_time = len(self._jobs) / ((Scheduler.NON_WORKING_HOURS_LIMIT.defq_limit + Scheduler.WORKING_HOURS_LIMIT.defq_limit) / 2)
        return max_job_time * 15

    def start(self):
        while True:
            limit = self.get_limit()
            longq_count, defq_count = self.get_job_counts()
            partition = "longq"
            if limit.defq_limit - defq_count > 0:
                partition = "defq"
            new_jobs_count = min((limit.defq_limit - defq_count) + (limit.longq_limit - longq_count), len(self._jobs))
            if new_jobs_count:
                new_jobs = self._jobs[0: new_jobs_count]
                self._jobs = self._jobs[new_jobs_count:]
                logging.info("Submitting %d jobs %d jobs left" % (new_jobs_count, len(self._jobs)))
                # #SBATCH -p longq
                for job in new_jobs:
                    job.submit(partition)
                msg = "Max eta: %d" % self.max_eta()
                logging.info(msg)
                self.jm.message_callback(msg)
            time.sleep(1)

# if __name__ == "__main__":
#     jm = JobMonitor(lambda x: x+"")
#     jm.start()

#     s = Scheduler(jm)
#     for i in range(0,5):
#         s.add_job(Project("t", "desc",[], "",""))

#     s.start()