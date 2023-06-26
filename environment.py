import subprocess
from pathlib import Path

import os
import toml
import yaml

with Path("pyproject.toml").open("r") as f:
    data = toml.load(f)

# Get environment name
env_name = data["project"]["environment"]

# Export dependencies
# subprocess.PIPE tells Python to redirect the output of the command to an object
# text=True returns stdout and stderr as strings
command = f"conda env export -n {env_name}"
dependencies = subprocess.run(command.split(), stdout=subprocess.PIPE, text=True,)

# Load string yaml into a dict
dependencies = yaml.safe_load(dependencies.stdout)

env_name = dependencies["name"]
if os.environ["CONDA_DEFAULT_ENV"] != env_name:
    raise RuntimeError(
        "Current environment not the same as specified in pyproject.toml"
    )

# Remove the prefix key as its value has the local path to the environment
dependencies.pop("prefix")

# Write the dict to environment.yml file
# Keep original keys order
with Path("environment.yml").open("w") as f:
    yaml.dump(
        data=dependencies, stream=f, sort_keys=False,
    )
