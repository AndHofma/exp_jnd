"""
This module, named pathchecks.py, contains functions for verifying the existence of specific directories and files
required for audio tasks.

Functions:
    check_config_paths(base_input_path: str, tasks: list, output_path: str, plot_path: str) -> None: Checks the
    existence of specified directories and raises exceptions with appropriate error messages if any of the directories
    do not exist.
    stimulus_exists(stim_path: str) -> bool: Checks if a stimulus file exists at a specified path and returns a boolean
    indicating the result.

Note:
    This module provides utility functions for ensuring the appropriate setup and existence of required files and
    directories for conducting audio tasks.
    If directories or files are not found where expected, it raises exceptions with clear error messages to facilitate
    troubleshooting and setup.
"""

import os


def check_config_paths(base_input_path, tasks, output_path, plot_path):
    """
    Checks the existence of specific directories required for audio tasks.

    Parameters:
    base_input_path (str): The base path for the input directory.
    tasks (list): A list of task names.
    output_path (str): The path for the output directory.
    plot_path (str): The path for the plot directory.
    pics_path (str): The path for pictures directory.

    Returns:
    None

    Raises:
    Exception: If the base input directory, or a task-specific input directory does not exist.
               If the output or plot directories do not exist, they are created.
    """

    # Check if the base input directory exists
    if not os.path.exists(base_input_path):
        # Raise exception if not
        print("base input path:", base_input_path)
        raise Exception("No input folder detected. Please make sure that "
                        "'base_stimuli_path' is correctly set in the configurations")
    # Iterate through tasks and check if the corresponding input folder exists
    for task in tasks:
        if not os.path.exists(f'{base_input_path}/audio-{task}'):
            raise Exception(f"No input folder for task {task} detected. Please "
                            f"create it or remove task {task} from the configurations")
    # Check if the output directory exists, if not, create it
    if not os.path.exists(output_path):
        os.mkdir(output_path)
        # Check if the output directory exists, if not, create it
    if not os.path.exists(plot_path):
        os.mkdir(plot_path)


def stimulus_exists(stim_path):
    """
    Checks if a stimulus file exists at a given path.

    Parameters:
    stim_path (str): The path of the stimulus file.

    Returns:
    bool: True if the file exists at the given path, False otherwise.
    """

    # Check if the stimulus file exists at the given path
    if not os.path.isfile(stim_path):
        return False  # File does not exist, return False
    return True  # File exists, return True
