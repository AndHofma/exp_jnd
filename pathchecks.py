"""
Verify existence of audio file directories / files in the directories
"""

import os


def check_config_paths(base_input_path, tasks, output_path):
    """
        Function checks the existence of specific directories and raises
        exceptions with appropriate error messages if any of the directories are not found.
    """
    # Check if the base input directory exists
    if not os.path.exists(base_input_path):
        # Raise exception if not
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


def stimulus_exists(stim_path):
    """
        Function checks if a stimulus file exists at the given path and returns a boolean value.
    """
    # Check if the stimulus file exists at the given path
    if not os.path.isfile(stim_path):
        return False  # File does not exist, return False
    return True  # File exists, return True
