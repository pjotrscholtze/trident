import json
from glob import glob
import os
import logging
import monitor
import subprocess
import urllib.request    
import urllib.parse    
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")

CONFIG = {}
with open("config.json", "r") as f: CONFIG = json.load(f)

def telegram_inform(message: str):
    params = {
        "parse_mode": "markdown",
        "text": message,
        "chat_id": CONFIG["chat_id"]
    }
    query_string = urllib.parse.urlencode(params)
    data = query_string.encode("ascii")
    url = "https://api.telegram.org/bot%s/sendMessage" % CONFIG["secret"]

    with urllib.request.urlopen(url, data) as response: response.read()

class Project:
    def __init__(self, name: str, description: str, script):
        self.name = name
        self.description = description
        self.script = script

    def _project_path(self) -> str: return "/var/scratch/pse740/" + self.name

    def exists(self) -> bool:
        return os.path.exists(self._project_path())

    def submit(self) -> str:
        sbatch_file = self._project_path() + "/sbatch.sh"
        sbatch_output_file = self._project_path() + "/slurm-%j.out"
        os.mkdir(self._project_path())
        with open(sbatch_file, "w") as f:
            f.writelines("\n".join(self.script).replace("$PROJECT_PATH", self._project_path()))
        cmd = "sbatch %s -o %s" % (sbatch_file, sbatch_output_file)
        stdout = subprocess.getoutput(cmd)
        with open(self._project_path() + "/job_id", "w") as f:
            f.writelines([stdout])

        return stdout[len("Submitted batch job "):]


def get_projects():
    names = []
    for p in glob("experiments/projects/*.json"):
        with open(p, "r") as f:
            data = json.load(f)
            if isinstance(data, dict):
                p = Project(**data)
                if p.name in names: raise Exception("Project name should always be unique!")
                names.append(p.name)
                yield p
            else:
                for item in data:
                    p = Project(**item)
                    if p.name in names: raise Exception("Project name should always be unique!")
                    names.append(p.name)
                    yield p

jm = monitor.JobMonitor(telegram_inform)
jm.start()

projects = list(get_projects())
logging.info("Found %d experiments to check" % len(projects))
for project in projects:
    logging.info("Project '%s' %s" % (project.name,
        "has been submitted before" if project.exists() else \
                "has not yet been submitted"))
    if not project.exists():
        logging.info("Submitting now...")
        job_id = project.submit()
        logging.info("Done running on job id: %s" % job_id)
