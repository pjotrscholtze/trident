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
with open("./config.json", "r") as f: CONFIG = json.load(f)

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
    def __init__(self, name: str, description: str, script, github_url: str, github_checkout: str):
        self.name = name
        self.description = description
        self.script = script
        self.github_url = github_url
        self.github_checkout = github_checkout

    def _project_path(self) -> str: return "/var/scratch/pse740/" + self.name
    def _build_cache_path(self) -> str: return "/var/scratch/pse740/cache/"
    def _database_path(self) -> str: return "/var/scratch/pse740/db/"

    def exists(self) -> bool:
        return os.path.exists(self._project_path())
    
    def _setup_git(self, project_path, checkout):
        subprocess.call("git pull", cwd=project_path, shell=True)
        subprocess.call("git checkout %s" % checkout, cwd=project_path, shell=True)

    def get_commit_hash(self): return subprocess.getoutput("git rev-parse HEAD")

    def build_trident(self, project_path):
        subprocess.call("cmake . -DSPARQL=1", cwd=project_path, shell=True)
        subprocess.call("make", cwd=project_path, shell=True)

    def submit(self) -> str:
        sbatch_file = self._project_path() + "/sbatch.sh"
        project_commit_hash_file = self._project_path() + "/project-commit-hash.txt"
        sbatch_output_file = self._project_path() + "/slurm-%j.out"
        os.mkdir(self._project_path())
        with open(sbatch_file, "w") as f:
            f.writelines("\n".join(self.script). \
                replace("$PROJECT_PATH", self._project_path()). \
                replace("$BUILD_CACHE_PATH", self._build_cache_path()). \
                replace("$DATABASE_PATH", self._database_path()))
        
        telegram_inform("Setting up git for %s (%s @ %s)" % (self.name, self.github_url, self.github_checkout))
        self._setup_git(self._project_path() + "/trident", self.github_checkout)

        with open(project_commit_hash_file, "w") as f: f.writelines([self.get_commit_hash()])

        telegram_inform("Building trident for %s" % self.name)
        self.build_trident(self._build_cache_path() + "/trident")
        telegram_inform("Finished building trident for %s" % self.name)

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
