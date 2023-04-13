"""
JND Experiment Execution

This script sets up and runs a Just Noticeable Difference (JND) experiment
with tasks involving pitch, final lengthening (FL), and pause duration.
It initializes the required libraries, checks configuration paths, collects participant information,
and creates the experiment window.
The script then iterates through the randomized tasks, executing practice sessions and trials for each task
while providing appropriate on-screen feedback and instructions for the participant.

Written by: Yana Palacheva (https://github.com/YanaPalacheva/perturbation_study/tree/main/jnd_experiment)
Adapted by: Andrea Hofmann
"""


from psychopy import core, visual, gui, data, event, prefs, monitors
from configuration import general_experiment_configs, randomized_tasks
from jnd_task_setup import run_jnd_task
from pathchecks import check_config_paths

prefs.hardware['audioLib'] = ['PTB', 'sounddevice', 'pyo', 'pygame']
# Check if input and output paths exist
check_config_paths(general_experiment_configs["base_stimuli_path"],
                   general_experiment_configs["task_types"],
                   general_experiment_configs["output_path"])  # make sure that in and out paths exist
# Show initial dialog (timestamp and date)
exp_data = {'subject': 'SUBJECT_ID', 'cur_date': data.getDateStr()}
dlg = gui.DlgFromDict(exp_data, title=f'JND Experiment', fixed=['cur_date'])
if not dlg.OK:
    core.quit()
# Open the experiment window
currentMonitor = monitors.Monitor(name='testMonitor')
win = visual.Window(monitors.Monitor.getSizePix(currentMonitor),
                       monitor="testMonitor",
                       allowGUI=True,
                       fullscr=False,
                       color=(255, 255, 255)
                    )
win.flip()

# IDE output for checking
"""print(f"task list: {randomized_tasks}")"""

# Iterate through randomized tasks and execute practice sessions and trials
for ind, task in enumerate(randomized_tasks):
    # IDE output for checking
    """print(f"nr task: {ind}")
    print(f"task: {task}")"""

    # Run practice session
    run_jnd_task(exp_data, task, win, session_type='practice')

    # give some on-screen feedback?
    visual.TextStim(win, text=f"Sehr gut!\n"
                              f"Wenn Sie noch Fragen haben, \n geben Sie der Versuchsleiterin Bescheid.\n\n"
                              f"Es startet der {ind+1}. von 3 Teilen.\n\n"
                              f"Jeder der 3 Teile besteht aus 2 Blöcken.\n"
                              f"Sie können nach jedem Block eine Pause machen.\n\n"
                              f"Drücken Sie eine beliebige Taste sobald Sie bereit sind.",
                    color='black',
                    wrapWidth=2,
                    height=0.1).draw()

    win.flip()
    event.waitKeys()  # wait for participant to react by pressing spacebar
    win.flip()

    # Run the experiment
    run_jnd_task(exp_data, task, win)

# Display experiment completion message
visual.TextStim(win, text='Hervorragend, Sie haben es geschafft. \n Vielen dank! \n Drücken Sie eine beliebige Taste zum Beenden.',
                color='black',
                wrapWidth=2,
                height=0.1).draw()
win.flip()
event.waitKeys()
win.close()
core.quit()
