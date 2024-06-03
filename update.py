import os
import subprocess

repo = "https://github.com/bishalqx980/tgbot"
folder_name = "tgbot"
config_path = "config.env"
commands = []
found_config_env = False

if os.path.exists(config_path):
    with open(config_path, "r") as f:
        config_env = f.read()
        found_config_env = True
else:
    print(f"Error: {config_path} not found...")
    exit(1)

if os.path.exists(folder_name):
    commands.append(f"rmdir /s /q {folder_name}")

commands.append(f"git clone {repo} {folder_name}")
print(f"Started cloning {repo}")
for command in commands:
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(process.stdout or process.stderr)

if found_config_env:
    with open(f"{folder_name}/config.env", "w") as f:
        f.write(config_env)

print("Repository has been updated to latest commit...")
