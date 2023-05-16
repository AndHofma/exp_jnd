"""
JND Experiment Execution

This script sets up and runs a Just Noticeable Difference (JND) experiment
with tasks involving pitch, final lengthening (FL), and pause duration.
It initializes the required libraries, checks configuration paths, collects participant information,
and creates the experiment window.
The script then iterates through the randomized tasks, executing practice sessions and trials for each task
while providing appropriate on-screen feedback and instructions for the participant.

First Version by: Yana Palacheva (https://github.com/YanaPalacheva/perturbation_study/tree/main/jnd_experiment)
Adapted Version by: Andrea Hofmann
"""


from psychopy import core, visual, gui, data, event, prefs, monitors
from configuration import general_experiment_configs, randomized_tasks
from jnd_task_setup import run_jnd_task
from pathchecks import check_config_paths

prefs.hardware['audioLib'] = ['PTB', 'sounddevice', 'pyo', 'pygame']
# Check if input and output paths exist
check_config_paths(general_experiment_configs["base_stimuli_path"],
                   general_experiment_configs["task_types"],
                   general_experiment_configs["output_path"],
                   general_experiment_configs["plot_path"])  # make sure that in and out paths exist
# Show initial dialog (timestamp and date)
exp_data = {
    'subject_ID': 'subject_ID',
    'cur_date': data.getDateStr(),
    'experiment': 'JND_experiment',
}
dlg = gui.DlgFromDict(exp_data, title=f'JND Experiment', fixed=['experiment', 'cur_date'])
if not dlg.OK:
    core.quit()

run = 1

# Open the experiment window
currentMonitor = monitors.Monitor(name='testMonitor')
win = visual.Window(monitors.Monitor.getSizePix(currentMonitor),
                       monitor="testMonitor",
                       allowGUI=True,
                       fullscr=True,
                       color=(255, 255, 255)
                    )
win.flip()

# IDE output for checking
"""print(f"task list: {randomized_tasks}")"""


def get_instruction_text(task, ind):
    """
    Generates instruction text for the participant depending on the current task and the index of the task.

    Parameters:
    task (str): The current task ('pause', 'pitch', or 'FL').
    ind (int): The index of the current task (0-based).

    Returns:
    str: The instruction text to be shown to the participant.

    The function modifies the instruction text depending on whether the current task is a 'pause' or not,
    and whether it is the last task or not. For the 'pause' task, it indicates that the task duration
    will be between 18-22 minutes. For the other tasks, it indicates a duration between 10-15 minutes.
    If the task is the last one (ind == 2), it informs the participant that this is the last part. Otherwise,
    it informs the participant that they can take a break after the current task.
    """
    if ind == 2:
        last_task_text = "Dies ist der letzte Teil.\n\n"
    else:
        last_task_text = f"Danach können Sie eine Pause machen.\n\n"

    if task == 'pause':
        return f"Sehr gut!\n" \
               f"Wenn Sie noch Fragen haben, geben Sie der Versuchsleiterin Bescheid.\n\n" \
               f"Es startet der {ind + 1}. von 3 Teilen.\n" \
               f"Dieser Teil dauert zwischen 18-22 Minuten. \n" \
               f"{last_task_text}" \
               f"Beachten Sie: \n" \
               f"Die Aufgabe wird nach und nach immer schwieriger,\n " \
               f"denn die Unterschiede werden immer kleiner. \n" \
               f"Bitte antworten Sie dennoch immer so akkurat, wie möglich.\n\n" \
               f"Drücken Sie eine beliebige Taste sobald Sie bereit sind."
    else:
        return f"Sehr gut!\n" \
               f"Wenn Sie noch Fragen haben, geben Sie der Versuchsleiterin Bescheid.\n\n" \
               f"Es startet der {ind + 1}. von 3 Teilen.\n" \
               f"Dieser Teil dauert zwischen 10-15 Minuten. \n" \
               f"{last_task_text}" \
               f"Beachten Sie: \n" \
               f"Die Aufgabe wird nach und nach immer schwieriger,\n " \
               f"denn die Unterschiede werden immer kleiner. \n" \
               f"Bitte antworten Sie dennoch immer so akkurat, wie möglich.\n\n" \
               f"Drücken Sie eine beliebige Taste sobald Sie bereit sind."


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
    run_jnd_task(exp_data, task, win, run=run)
    run += 1

# Display experiment completion message
visual.TextStim(win, text='Hervorragend, Sie haben es geschafft. \n Vielen Dank! \n Drücken Sie eine beliebige Taste zum Beenden.',
                color='black',
                wrapWidth=2,
                height=0.1).draw()
win.flip()
event.waitKeys()
win.close()
core.quit()
