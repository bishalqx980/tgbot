import os
from subprocess import run as srun

UPSTREAM_REPO = "https://github.com/bishalqx980/tgbot"
UPSTREAM_BRANCH = "main"

print(f"Updating repo to latest commit...\nUPSTREAM_REPO: {UPSTREAM_REPO}\nUPSTREAM_BRANCH: {UPSTREAM_BRANCH}")
if os.path.exists(".git"):
    try:
        srun(["rm", "-rf", ".git"]) # linux only
    except Exception as e:
        print(f"{e}\nmost probably you are using windows...")

commands = [
    "git init",
    "git config --global user.name bishalqx980",
    "git config --global user.email bishalqx680@gmail.com",
    "git add .",
    "git commit -m update",
    f"git remote add origin {UPSTREAM_REPO}",
    "git fetch origin",
    f"git reset --hard origin/{UPSTREAM_BRANCH}"
]

for command in commands:
    process = srun(command, capture_output=True, text=True, shell=True)
    #print(process.stdout or process.stderr)

if process.returncode == 0:
    print(f"Successfully updated with latest commit from {UPSTREAM_REPO}")
else:
    print("Something went wrong! repo not updated...")
