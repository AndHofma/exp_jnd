"""
This module contains the functions and configurations required to run the Just Noticeable Difference (JND) task
It provides functionality for randomizing task order, generating task-specific configurations,
and calculating appropriate step sizes for each trial.
"""

from resources import pitch_FL_text, pause_text
import random
from psychopy import monitors, visual


# General experiment configurations
general_experiment_configs = {"task_types": ["pitch", "FL", "pause"],
                              "num_trials": 10,
                              "base_stimuli_path": 'audio/',  # input path is generated as base_stimuli_path+task name
                              "output_path": 'results/',
                              "plot_path": 'plots/'}


# Randomize the order of tasks - between subjects design
randomized_tasks = random.sample(general_experiment_configs["task_types"],
                                 k=len(general_experiment_configs["task_types"]))


def create_window():
    """
    Create and initialize the experiment window.

    Returns:
    win : A PsychoPy visual.Window object for the experiment.
    """
    # Create a monitor object
    currentMonitor = monitors.Monitor(name='testMonitor')

    # Create and return a window for the experiment
    return visual.Window(monitors.Monitor.getSizePix(currentMonitor),
                         monitor="testMonitor",
                         allowGUI=True,
                         fullscr=True,
                         color=(255, 255, 255)
                         )


def get_task_specific_config(task):
    """
        Get task-specific configuration settings.

        Args:
            task (str): The task name ("pitch", "FL", or "pause").

        Returns:
            dict: A dictionary containing task-specific configuration settings.
    """
    config = {"task": "",
              "stim_prefix": "",
              "instructions": "",
              "stimuli_path": "",
              "baseline": 0,
              "initial_difference": 0}
    if task == "pitch":
        config['task'] = "pitch"
        config['stim_prefix'] = f'nelli_ch_rise'
        config['baseline'] = 0.000
        config['initial_difference'] = 13.112
    elif task == "pause":
        config['task'] = "pause"
        config['stim_prefix'] = f'lilli_lisa_ch_{task}'
        config['baseline'] = 0.000
        config['initial_difference'] = 0.550
    elif task == "FL":
        config['task'] = "FL"
        config['stim_prefix'] = f'mimmi_ch_{task}'
        config['baseline'] = 0.0000
        config['initial_difference'] = 0.1639
    else:
        raise Exception(f"No configs for task {task} specified")

    # Assign task-specific instructions
    if task == 'pitch' or task == 'FL':
        config['instructions'] = pitch_FL_text
    elif task == 'pause':
        config['instructions'] = pause_text

    config["stimuli_path"] = f"{general_experiment_configs['base_stimuli_path']}audio-{task}/"
    return config


def get_step_size(task, test_difference=13.0000):
    """
        Get the step size for the specified task.

        Args:
            task (str): The task name ("pitch", "FL", or "pause").
            test_difference (float, optional): The current difference between test and baseline stimuli. Default is 5.0.

        Returns:
            float: The step size for the task.
    """
    if task == "pitch":
        if test_difference <= 0.312:
            return 0.005
        elif test_difference <= 1.412:
            return 0.100
        elif test_difference <= 5.612:
            return 0.300
        else:
            return 0.500
    elif task == "pause":
        if test_difference <= 0.060:
            return 0.001
        elif test_difference <= 0.120:
            return 0.005
        elif test_difference <= 0.300:
            return 0.015
        else:
            return 0.025
    elif task == "FL":
        if test_difference <= 0.0169:
            return 0.0003
        elif test_difference <= 0.0457:
            return 0.0018
        elif test_difference <= 0.0889:
            return 0.0036
        else:
            return 0.0075

