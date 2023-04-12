from psychopy import core, visual, gui, data, event, prefs, monitors
from configuration import general_experiment_configs, randomized_tasks
from jnd_task_setup import run_jnd_task
from pathchecks import check_config_paths

prefs.hardware['audioLib'] = ['PTB', 'sounddevice', 'pyo', 'pygame']

check_config_paths(general_experiment_configs["base_stimuli_path"],
                   general_experiment_configs["task_types"],
                   general_experiment_configs["output_path"])  # make sure that in and out paths exist

# show initial dialog (timestamp and date)
exp_data = {'subject': 'SUBJECT_ID', 'cur_date': data.getDateStr()}
dlg = gui.DlgFromDict(exp_data, title=f'JND Experiment', fixed=['cur_date'])
if not dlg.OK:
    core.quit()

# open the experiment window
currentMonitor = monitors.Monitor(name='testMonitor')
win = visual.Window(monitors.Monitor.getSizePix(currentMonitor),
                       monitor="testMonitor",
                       allowGUI=True,
                       fullscr=False,
                       color=(255,255,255),
                       colorSpace='rgb')
win.flip()

print(f"task list: {randomized_tasks}")

for ind, task in enumerate(randomized_tasks):
    print(f"nr task: {ind}")
    print(f"task: {task}")
    # run practice session
    run_jnd_task(exp_data, task, win, session_type='practice')

    # give some on-screen feedback?
    visual.TextStim(win, text=f"Sehr gut!\n"
                              f"Wenn Sie noch Fragen haben, \n geben Sie der Versuchsleiterin Bescheid.\n\n"
                              f"Es startet der {ind+1}. von 3 Teilen.\n\n"
                              f"Jeder der 3 Teile besteht aus 3 Blöcken.\n"
                              f"Sie können nach jedem Block eine Pause machen.\n\n"
                              f"Drücken Sie eine beliebige Taste sobald Sie bereit sind.", color='black', colorSpace='rgb',wrapWidth=2,height=0.1).draw()

    win.flip()
    event.waitKeys()  # wait for participant to react by pressing spacebar
    win.flip()

    # run the experiment
    run_jnd_task(exp_data, task, win, session_type='trial')

visual.TextStim(win, text='Hervorragend, Sie haben es geschafft. \n Vielen dank! \n Drücken Sie eine beliebige Taste zum Beenden.', color='black', colorSpace='rgb',wrapWidth=2,height=0.1).draw()
win.flip()
event.waitKeys()
win.close()
core.quit()