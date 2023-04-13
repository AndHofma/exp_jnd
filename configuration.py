"""
This module contains the functions and configurations required to run the Just Noticeable Difference (JND) task
It provides functionality for randomizing task order, generating task-specific configurations,
and calculating appropriate step sizes for each trial.
"""

from resources import pitch_FL_text, pause_text
import random


# General experiment configurations
general_experiment_configs = {"task_types": ["pitch", "FL", "pause"],
                              "num_runs": 2,
                              "num_trials_each_run": 100,
                              "base_stimuli_path": 'audio/',  # input path is generated as base_stimuli_path+task name
                              "output_path": 'results/'}


# Randomize the order of tasks - between subjects design
randomized_tasks = random.sample(general_experiment_configs["task_types"],
                                 k=len(general_experiment_configs["task_types"]))


def get_task_specific_config(task):
    """
        Get task-specific configuration settings.

        Args:
            task (str): The task name ("pitch", "FL", or "pause").

        Returns:
            dict: A dictionary containing task-specific configuration settings.
    """
    config = {"task": "", "stim_prefix": "", "instructions": "",
              "stimuli_path": "",
              "baseline": 0, "initial_difference": 0}
    if task == "pitch":
        config['task'] = "pitch"
        config['stim_prefix'] = f'nelli_ch_rise'
        config['baseline'] = 0.0
        config['initial_difference'] = 13.1
    elif task == "pause":
        config['task'] = "pause"
        config['stim_prefix'] = f'lilli_lisa_ch_{task}'
        config['baseline'] = 0.005
        config['initial_difference'] = 0.545
    elif task == "FL":
        config['task'] = "FL"
        config['stim_prefix'] = f'mimmi_ch_{task}'
        config['baseline'] = 0.002
        config['initial_difference'] = 0.162
    else:
        raise Exception(f"No configs for task {task} specified")

    # Assign task-specific instructions
    if randomized_tasks[0] == 'pitch' or randomized_tasks[0] == 'FL':
        config['instructions'] = pitch_FL_text
    elif randomized_tasks[0] == 'pause':
        config['instructions'] = pause_text

    config["stimuli_path"] = f"{general_experiment_configs['base_stimuli_path']}audio-{task}/ch/"
    return config


def get_step_size(task, first_incorrect=False, test_difference=5.0):
    """
        Get the step size for the specified task.

        Args:
            task (str): The task name ("pitch", "FL", or "pause").
            first_incorrect (bool, optional): Whether the first incorrect response has occurred. Default is False.
            test_difference (float, optional): The current difference between test and baseline stimuli. Default is 5.0.

        Returns:
            float: The step size for the task.
    """
    if task == "pitch":
        if test_difference <= 2:
            return 0.1
        elif first_incorrect:
            return 0.3
        else:
            return 0.5
    if task == "FL":
        if test_difference <= 0.02:
            return 0.001
        elif first_incorrect:
            return 0.003
        else:
            return 0.005
    if task == "pause":
        if test_difference <= 0.095:
            return 0.005
        elif first_incorrect:
            return 0.010
        else:
            return 0.015
