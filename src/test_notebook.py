"""
This module contains the main function of "Bus Tracker".
"""

import os
import subprocess
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from jupyter_client.kernelspec import NoSuchKernel

subprocess.run(
    [
        "python",
        "-m",
        "ipykernel",
        "install",
        "--user",
        "--name",
        "python3",
        "--display-name",
        "Python 3",
    ]
)


# Path to the notebook to test
notebook_path = "src/Bus_Tracker.ipynb"

if os.path.exists(notebook_path):
    print("File exists")
else:
    print("File does not exist")


def test_notebook():
    "test the BUS Tracker notebook"
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)

    os.chdir(os.path.join(os.getcwd(), "src"))

    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
    try:
        ep.preprocess(nb)
    except Exception as e:
        assert False, f"Error executing the notebook: {e}"


if __name__ == "__main__":
    test_notebook()
    print("Everything passed")
