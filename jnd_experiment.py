"""
jnd_experiment.py

This module sets up and executes a Just Noticeable Difference (JND) experiment involving tasks related to pitch,
final lengthening (FL), and pause duration.
The JND experiment evaluates the JND threshold for three different prosodic parameters on a subject basis,
specifically final lengthening (FL) of the second vowel in the name "Mimi" relative to the whole name duration,
pause after name1 within a name coordinate of the kind "name1 [pause] and name2", and pitch / f0 rise from
syllable 1 to syllable 2 in the name "Nelli".

The experiment follows the 1-down-1-up protocol up to the first incorrect response, and a 2-down-1-up protocol
thereafter.
It utilizes an odd-one-out forced-choice task with three sequentially auditory presented stimuli, following the AXB
pattern (AAB or ABB sequences, randomly chosen).

The module checks the necessary paths for input and output, collects participant information, creates an experiment
window, and then iterates through the randomized tasks, executing practice sessions and trials for each task while
providing appropriate on-screen feedback and instructions for the participant.

Functions:
----------
- main: The entry point of the script. It initializes required configurations, collects participant information,
creates the experiment window, and executes the experiment tasks in randomized order.

Module Level Imports:
---------------------
- psychopy: A library for creating psychology stimuli in Python. It's used to handle the window, events, and the
core of the application.
- configuration: A module which sets up configurations for the experiment.
- jnd_task_setup: A module that sets up the JND task, it provides a function to run the task and another to get
participant information.
- pathchecks: A module that verifies if input and output paths exist.
- instructions: A module that returns the instruction text for a given task.

Original Version by: Yana Palacheva (https://github.com/YanaPalacheva/perturbation_study/tree/main/jnd_experiment)
Adapted Version by: Andrea Hofmann
"""



from psychopy import core, visual, event
from configuration import general_experiment_configs, randomized_tasks, create_window
from jnd_task_setup import run_jnd_task, get_participant_info
from pathchecks import check_config_paths
from instructions import get_instruction_text


# Check if input and output paths exist
check_config_paths(general_experiment_configs["base_stimuli_path"],
                   general_experiment_configs["task_types"],
                   general_experiment_configs["output_path"],
                   general_experiment_configs["plot_path"])  # make sure that in and out paths exist

# load parameter value from function to be set to 1 - parameter will be iterated later
test_nr = 1

# Open participant information GUI
exp_data = get_participant_info()

# Create the window
win = create_window()

win.flip()

# Iterate through randomized tasks and execute practice sessions and trials
for ind, task in enumerate(randomized_tasks):
    # Run practice session
    run_jnd_task(exp_data, task, win, session_type='practice')

    # Display the appropriate instruction text based on the task
    instruction_text = get_instruction_text(task, ind)
    visual.TextStim(win, text=instruction_text,
                    color='black',
                    wrapWidth=2,
                    height=0.1).draw()

    win.flip()
    event.waitKeys()  # wait for participant to react by pressing spacebar
    win.flip()

    # Run the experiment
    run_jnd_task(exp_data, task, win)

    # after each task
    if test_nr <= 2:
        pause_text = f"Sie haben {test_nr} von 3 Tests geschafft.\n Drücken Sie eine Taste, sobald Sie bereit sind, weiterzumachen."
        # display instructions and wait
        pause_stimulus = visual.TextStim(win,
                                         color='black',
                                         wrapWidth=2,
                                         height=0.1,
                                         text=pause_text)

        pause_stimulus.draw()
        win.flip()
        event.waitKeys()
        win.flip()

    test_nr += 1

# Display experiment completion message
visual.TextStim(win, text='Hervorragend, Sie haben es geschafft. \n Vielen Dank! \n Drücken Sie eine beliebige Taste zum Beenden.',
                color='black',
                wrapWidth=2,
                height=0.1).draw()
win.flip()
event.waitKeys()
win.close()
core.quit()
