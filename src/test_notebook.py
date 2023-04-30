import os
import subprocess
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from jupyter_client.kernelspec import NoSuchKernel


def install_kernel_spec():
    """
    Install the kernel spec for Python 3 in the current user's Jupyter kernels directory.
    """
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


def check_notebook_existence(notebook_path):
    """
    Check if the given notebook path exists.

    Args:
    - notebook_path (str): the path to the notebook file

    Returns:
    - bool: True if the file exists, False otherwise
    """
    return os.path.exists(notebook_path)


def execute_notebook(notebook_path):
    """
    Execute the given notebook file.

    Args:
    - notebook_path (str): the path to the notebook file
    """
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)

    os.chdir(os.path.join(os.getcwd(), "src"))

    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
    try:
        ep.preprocess(nb)
    except Exception as e:
        assert False, f"Error executing the notebook: {e}"


def test_notebook():
    """
    Test the Bus Tracker notebook by executing it and checking for errors.
    """
    main_notebook_path = "src/Bus_Tracker.ipynb"
    if not check_notebook_existence(main_notebook_path):
        print("Notebook file does not exist.")
        return
    
    EDA_notebook_path = "src/a.ipynb"
    if not check_notebook_existence(EDA_notebook_path):
        print("Notebook file does not exist.")
        return

    execute_notebook(main_notebook_path)
    execute_notebook(EDA_notebook_path)
    print("Notebook executed successfully.")


if __name__ == "__main__":
    install_kernel_spec()
    test_notebook()
    print("Test passed.")
