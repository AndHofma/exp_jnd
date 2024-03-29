"""
jnd_task_setup.py

This module contains functions to set up and run a Just-Noticeable-Difference (JND) task.
This is used to estimate the smallest difference in a given attribute (like brightness or volume) that a
participant can perceive.

It uses the psychopy library to generate a graphical user interface and to display the stimuli.

Functions:
----------

- get_participant_info(): Collect participant details using a dialog box. Returns a dictionary with participant info.

- generate_stimulus_path(path_prefix, value, task): Generates the path for a stimulus based on a given path_prefix,
value and task.
    Depending on the task type, the function rounds the value to a specific decimal point, converts the decimal to
    an underscore, and appends it to the path_prefix.

- run_jnd_task(exp_data, task, win, session_type='trial'): Runs the JND task. Takes experiment data, task type,
window and session type as input.
    Sets up a global visual stimulus, gets the task specific configuration, generates the stimulus path, and then
    runs the task according to the session type (trial or practice).

- run_trial_session(path_prefix, exp_data, exp_config, session_type, win): Runs a trial session of the JND task.
Takes path_prefix, experiment data, experiment configuration, session type and window as input.
    During the session, stimuli are presented to the participant and their responses are recorded.

- run_practice_session(path_prefix, exp_data, exp_config, win): Runs a practice session of the JND task. It is
similar to run_trial_session, but with fewer trials and additional feedback for participants.
"""


# Import necessary libraries
from psychopy import prefs
# Set the audio library preference
prefs.hardware['audioLib'] = ['ptb', 'sounddevice', 'pygame', 'pyo']
# Now, import sound
from psychopy import sound, visual, event, core, gui
import random
import time
import datetime
from librosa import get_duration
from jnd_configuration import get_step_size, get_task_specific_config, general_experiment_configs
from jnd_path import stimulus_exists
from jnd_visualization import create_visualization, calculate_threshold
import os


def get_participant_info():
    """
    Open a dialogue box with 3 fields: current date and time, subject_ID and experiment name.
    Returns a dictionary with the entered information.
    """
    exp_data = {
        'experiment': 'jnd_experiment',
        'cur_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'subject': 'subject_ID'
    }
    # Dialogue box to get participant information
    info_dialog = gui.DlgFromDict(dictionary=exp_data,
                                  title='Just-Noticeable-Difference Experiment',
                                  fixed=['experiment', 'cur_date']
                                  )

    if info_dialog.OK:
        return exp_data
    else:
        core.quit()


def generate_stimulus_path(path_prefix, value, task):
    """
        Generate the stimulus file path based on the given value and task.

        This function adjusts the precision of the value based on the task type
        and appends it to the path prefix to create the full stimulus file path.
        It then checks if the stimulus file exists before returning the file path.

        Args:
            path_prefix (str): The prefix of the stimulus file path.
            value (float): The value used to identify the stimulus file.
            task (str): The type of task, either 'pitch' or 'duration'.

        Returns:
            str: The generated stimulus file path if the file exists.

        Raises:
            Exception: If the stimulus file does not exist.
    """
    if task == 'FL':
        value = round(value, 4)
        value_suffix = str(value).replace('.', '_')
        decimal_places = str(value)[::-1].find('.')
        if decimal_places == 3:
            value_suffix += '0'
        elif decimal_places == 2:
            value_suffix += '00'
        elif decimal_places == 1:
            value_suffix += "000"
        elif decimal_places == -1:  # no decimal places
            value_suffix += "0000"
    else:
        value = round(value, 3)
        value_suffix = str(value).replace('.', '_')
        decimal_places = str(value)[::-1].find('.')
        if decimal_places == 2:
            value_suffix += '0'
        elif decimal_places == 1:
            value_suffix += "00"
        elif decimal_places == -1:  # no decimal places
            value_suffix += "000"

    stim_path = f'{path_prefix}_{value_suffix}.wav'
    if stimulus_exists(stim_path):
        return stim_path
    raise Exception(f'No stimulus found: {stim_path}')


def run_jnd_task(exp_data, task, win, session_type='trial'):
    """
        Run the Just-Noticeable Difference (JND) task for the given task type and session type.

        This function initializes the visual stimuli and then runs either the trial or practice session
        based on the given session type.

        Args:
            exp_data (dict): The experiment data containing relevant information.
            test_nr (int): number of tests that are run.
            task (str): The type of task, either 'pitch' or 'duration'.
            win (visual.Window): The PsychoPy window used for displaying the stimuli.
            session_type (str, optional): The type of session, either 'trial' or 'practice'. Defaults to 'trial'.

        Raises:
            Exception: If the session type is neither 'trial' nor 'practice'.
    """
    # AAB pattern pic
    global AAB
    AAB = visual.ImageStim(win,
                           image=general_experiment_configs["pics_path"] + 'pic_right_correct_BBA.png',
                           pos=(0.5, -0.7),
                           name='AAB_pic')

    # ABB pattern pic
    global ABB
    ABB = visual.ImageStim(win,
                           image=general_experiment_configs["pics_path"] + 'pic_left_correct_ABB.png',
                           pos=(-0.5, -0.7),
                           name='ABB_pic')

    # arrow right
    global rightArrow
    rightArrow = visual.TextStim(win,
                                 text='\u2192',
                                 pos=(0.5, 0),
                                 height=0.6,
                                 color='black',
                                 name='right_arrow')

    # arrow left
    global leftArrow
    leftArrow = visual.TextStim(win,
                                text='\u2190',
                                pos=(-0.5, 0),
                                height=0.6,
                                color='black',
                                name='left_arrow')

    # pics recording
    global audio_center
    # Center position
    audio_center = visual.ImageStim(win,
                                  image=general_experiment_configs["pics_path"] + 'audio.png',
                                  pos=(0, 0),
                                  name='audio_center')

    exp_config = get_task_specific_config(task)
    path_prefix = f'{exp_config["stimuli_path"]}{exp_config["stim_prefix"]}'

    if session_type == 'trial':
        run_trial_session(path_prefix, exp_data, exp_config, session_type, win)
    elif session_type == 'practice':
        run_practice_session(path_prefix, exp_data, exp_config, win)
    else:
        raise Exception(f"Run type can be either 'trial' or 'practice', received {type}")


def run_trial_session(path_prefix, exp_data, exp_config, session_type, win):
    """
        Run the trial session of the Just-Noticeable Difference (JND) task.

        This function iterates through the trials in the task, generates the stimuli, and records the participant's
        responses. It also handles the staircase procedure, adaptive step sizes, and stopping conditions.

        Args:
            path_prefix (str): The path prefix for the stimulus files.
            exp_data (dict): The experiment data containing relevant information.
            exp_config (dict): The configuration dictionary for the specific task.
            session_type (str): The type of session, either 'trial' or 'practice'.
            win (visual.Window): The PsychoPy window used for displaying the stimuli.
            test_nr (int): number of tests that are run.
    """
    # Generate stimulus paths
    baseline_stimulus = generate_stimulus_path(path_prefix, exp_config["baseline"], exp_config["task"])
    test_value = exp_config["baseline"] + exp_config["initial_difference"]
    test_stimulus = generate_stimulus_path(path_prefix, test_value, exp_config["task"])

    # Initialize variables for the staircase procedure
    current_difference = exp_config["initial_difference"]
    differences = []
    first_incorrect = False
    step_size = get_step_size(exp_config["task"])
    two_down_one_up = False
    correct_in_a_row = 1
    correct_responses = []
    trial_index = 0  # the number of trials aka choices
    incorrect_trials = 0  # for the first two trials if incorrect-they are repeated-the direction is not switched
    reversals = 0  # number of times the direction of the staircase is changed (up/down or down/up or down/none/up or up/none/down)
    reversals_list = [reversals]
    previous_direction = ['down']
    last_two_combinations = []  # to make sure there's no more than 3 in a row (AAB or ABB)

    start_time = time.time()  # record for each task - start timer
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%H:%M:%S')

    # path setup results per participant
    # Define the path in results for each subject
    subj_path_results = os.path.join(general_experiment_configs['output_path'], exp_data['subject'])
    # Create the directory if it doesn't exist
    if not os.path.exists(subj_path_results):
        os.makedirs(subj_path_results)

    # Set up the output file
    output_filename = os.path.join(subj_path_results,
                                   f"JND_{exp_config['task']}_{exp_data['subject']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

    with open(output_filename, 'w') as experiment_output:
        # Write to file here
        experiment_output.write(
            'experiment,'
            'subjectID,'
            'date,'
            'task,'
            'session_type,'
            'trial,'
            'start_time,'
            'end_time,'
            'duration,'
            'recording_A,'
            'recording_X,'
            'recording_B,'
            'response,'
            'correct,'
            'difference,'
            'step-size,'
            'reversals,'
            'direction\n')

        # Main loop for each trial
        while trial_index <= general_experiment_configs["num_trials"] and reversals <= 18 and baseline_stimulus != test_stimulus:  # stop conditions

            # randomization phase
            recording_A, recording_B = random.sample([baseline_stimulus, test_stimulus], k=2)
            AB_dict = {'left': recording_B, 'right': recording_A}
            x_key = random.choice(['left', 'right'])
            current_combination = f"left{x_key}right"

            # making sure: same pattern AAB or ABB not more than twice in a row
            if len(last_two_combinations) < 2:
                last_two_combinations.append(current_combination)
            elif last_two_combinations[0] == last_two_combinations[1]:
                while current_combination == last_two_combinations[0]:
                    x_key = random.choice(['left', 'right'])
                    current_combination = f"left{x_key}right"
                last_two_combinations[0] = last_two_combinations[1]
                last_two_combinations[1] = current_combination

            recording_X = AB_dict[x_key]

            # listening phase
            stimulus_A = sound.Sound(recording_A)
            stimulus_B = sound.Sound(recording_B)
            stimulus_X = sound.Sound(recording_X)

            # Play stimulus_A and show rec_center - stays on until all stimuli played
            stimulus_A.play()
            audio_center.draw()
            win.flip()
            time.sleep(get_duration(filename=recording_A) + 0.7)  # inter stimulus interval 700ms
            # Play stimulus_X
            stimulus_X.play()
            time.sleep(get_duration(filename=recording_X) + 0.7)  # inter stimulus interval 700ms
            # Play stimulus_B
            stimulus_B.play()
            time.sleep(get_duration(filename=recording_B) + 0.2)  # after 3rd stimulus wait 200ms
            win.flip()

            # Draw response options on screen
            AAB.draw()
            rightArrow.draw()
            ABB.draw()
            leftArrow.draw()
            win.flip()
            keys = event.waitKeys(keyList=['left', 'right'])

            # evaluation phase
            key_choice_map = {'left': 'left', 'right': 'right'}
            participant_choice = key_choice_map.get(keys[0], None)
            if participant_choice == x_key:  # correct
                correct = True
                correct_in_a_row += 1
                correct_responses.append(correct)
                if not two_down_one_up:
                    direction = 'down'
                    new_difference = current_difference - step_size
                else:
                    if correct_in_a_row >= 2 and correct_in_a_row % 2 == 0:
                        direction = 'down'
                        new_difference = current_difference - step_size
                    else:
                        direction = 'none'
                        new_difference = current_difference
            else:  # false
                correct = False
                correct_responses.append(correct)
                if current_difference == exp_config["initial_difference"]:  # no direction change if at max difference level
                    direction = 'none'
                    new_difference = current_difference  # Keep new_difference the same
                else:  # no direction change if trial 1-2 incorrect-test difference not out of range
                    first_incorrect = True
                    two_down_one_up = True
                    correct_in_a_row = 0
                    direction = 'up'
                    new_difference = current_difference + step_size
                incorrect_trials += 1  # Increment the incorrect_trials counter
            win.flip()
            if exp_config["task"]== 'pause':
                core.wait(1.5)  # inter trial interval
                end_time = time.time()
                end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
                duration = end_time - start_time
                # Convert duration to hours, minutes, and seconds
                hours, remainder = divmod(duration, 3600)
                minutes, seconds = divmod(remainder, 60)
                # Format the duration string without the fractional part
                duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))
            else:
                core.wait(1)  # inter trial interval
                end_time = time.time()
                end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
                duration = end_time - start_time
                # Convert duration to hours, minutes, and seconds
                hours, remainder = divmod(duration, 3600)
                minutes, seconds = divmod(remainder, 60)
                # Format the duration string without the fractional part
                duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

            # write the trial data to the output file
            experiment_output.write(','.join([
                exp_data['experiment'],
                exp_data['subject'],
                exp_data['cur_date'],
                exp_config['task'],
                session_type,
                str(trial_index + 1),
                start_time_str,
                end_time_str,
                duration_str,
                os.path.basename(recording_A),
                os.path.basename(recording_X),
                os.path.basename(recording_B),
                participant_choice,
                str(correct),
                str(current_difference),
                str(step_size),
                str(reversals),
                direction]) + '\n')

            experiment_output.flush()
            differences.append(current_difference)

            # prepare for the next iteration
            trial_index += 1
            current_difference = round(new_difference, 4)
            step_size = get_step_size(exp_config["task"], test_difference=current_difference)
            # IDE output for checking
            """print("current-difference: " + str(current_difference) + " at " + str(trial_index))
            print("step_size: " + str(step_size) + " at " + str(trial_index))"""
            # counts as reversal only when sequence True-False or False-True-True
            if (
                    (previous_direction[trial_index - 1] == 'down' and direction == 'up') or
                    (previous_direction[trial_index - 1] == 'up' and direction == 'down') or
                    (previous_direction[trial_index - 2] == 'down' and previous_direction[trial_index - 1] == 'none' and direction == 'up') or
                    (previous_direction[trial_index - 2] == 'up' and previous_direction[trial_index - 1] == 'none' and direction == 'down') or
                    (trial_index >= 3 and previous_direction[trial_index - 3] == 'up' and previous_direction[trial_index - 2] == 'none' and previous_direction[trial_index - 1] == 'none' and direction == 'down')
    ):
                reversals += 1

            previous_direction.append(direction)
            reversals_list.append(reversals)
            test_stimulus = generate_stimulus_path(path_prefix, exp_config['baseline'] + current_difference,
                                                   exp_config["task"])

    # Close the output file
    experiment_output.close()

    # To get the selected_reversals value for the legend
    # Calculate the reversal differences
    reversal_indices = [i - 1 for i in range(1, len(reversals_list)) if reversals_list[i] != reversals_list[i - 1]]
    reversal_difference = [differences[index] for index in reversal_indices]
    # Calculate the threshold values and get the selected_reversals
    mean_threshold, median_threshold, selected_reversals = calculate_threshold(reversal_difference)

    # Create visualization for the current test
    create_visualization(differences, correct_responses, reversals_list, exp_config["task"], exp_data['subject'])


def run_practice_session(path_prefix, exp_data, exp_config, win):
    """
        Run a practice session for the experiment.

        Args:
            path_prefix (str): The path prefix for the stimulus files.
            exp_data (dict): A dictionary containing experiment data (e.g., subjectID, date, experiment).
            exp_config (dict): A dictionary containing experiment configuration (e.g., baseline, task).
            win (visual.Window): A PsychoPy window object for rendering stimuli.
    """
    session_type = "practice"
    # Initialize variables
    correct_responses_count = 0  # Incremented; practice session stops after 4 correct responses
    run = 0  # Practice session has only one run
    current_difference = exp_config["initial_difference"]
    first_incorrect = False
    step_size = get_step_size(exp_config["task"])
    two_down_one_up = False
    correct_in_a_row = 1
    trial_index = 0  # number of trials
    incorrect_trials = 0  # for the first two trials if incorrect-they are repeated-the direction is not switched
    reversals = 0  # number of times the direction of the staircase is changed (up/down or down/up or none/down)

    # Generate baseline and test stimulus paths
    baseline_stimulus = generate_stimulus_path(path_prefix, exp_config["baseline"], exp_config["task"])
    test_value = exp_config["baseline"] + exp_config["initial_difference"]
    test_stimulus = generate_stimulus_path(path_prefix, test_value, exp_config["task"])

    # List to ensure there's no more than 3 in a row (AAB or ABB)
    last_two_combinations = []

    # Display instructions and wait
    instructions = visual.TextStim(win,
                                   color='black',
                                   wrapWidth=2,
                                   height=0.1,
                                   text=exp_config["instructions"])

    instructions.draw()
    win.flip()  # display the message
    event.waitKeys(keyList=['return'])  # wait until button is pressed
    win.flip()

    start_time = time.time()  # record duration of run of each task - start timer
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%H:%M:%S')

    # path setup results per participant
    # Define the path in results for each subject
    subj_path_results = os.path.join(general_experiment_configs['output_path'], exp_data['subject'])
    print(f'subject path: {subj_path_results}')
    # Create the directory if it doesn't exist
    if not os.path.exists(subj_path_results):
        os.makedirs(subj_path_results)
        print(f'subject path created')
    print(f'subject path not created')
    # Set up the output file
    output_filename = os.path.join(subj_path_results,
                                   f"JND_{exp_config['task']}_{exp_data['subject']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_practice.csv")

    with open(output_filename, 'w') as experiment_output:
        # Write to file here
        experiment_output.write(
            'experiment,'
            'subjectID,'
            'date,'
            'task,'
            'session_type,'
            'run,'
            'trial,'
            'start_time,'
            'end_time,'
            'duration,'
            'recording_A,'
            'recording_X,'
            'recording_B,'
            'response,'
            'correct,'
            'difference,'
            'step-size,'
            'reversals,'
            'direction\n')

        # Continue until 4 correct responses are reached
        while correct_responses_count < 4:
            # randomization phase
            recording_A, recording_B = random.sample([baseline_stimulus, test_stimulus], k=2)
            AB_dict = {'left': recording_B, 'right': recording_A}
            x_key = random.choice(['left', 'right'])
            current_combination = f"left{x_key}right"

            # Update last_two_combinations
            if len(last_two_combinations) < 2:
                last_two_combinations.append(current_combination)
            elif last_two_combinations[0] == last_two_combinations[1]:
                while current_combination == last_two_combinations[0]:
                    x_key = random.choice(['left', 'right'])
                    current_combination = f"left{x_key}right"
                last_two_combinations[0] = last_two_combinations[1]
                last_two_combinations[1] = current_combination

            recording_X = AB_dict[x_key]

            # listening phase
            stimulus_A = sound.Sound(recording_A)
            stimulus_B = sound.Sound(recording_B)
            stimulus_X = sound.Sound(recording_X)
            # Play stimulus_A and show rec_center
            stimulus_A.play()
            audio_center.draw()
            win.flip()
            time.sleep(get_duration(filename=recording_A) + 0.7)  # inter stimulus interval 500ms
            # Play stimulus_X
            stimulus_X.play()
            time.sleep(get_duration(filename=recording_X) + 0.7)  # inter stimulus interval 500ms
            # Play stimulus_B
            stimulus_B.play()
            time.sleep(get_duration(filename=recording_B) + 0.2)  # after 3rd stimulus wait 200ms
            win.flip()

            # Draw response options on screen
            AAB.draw()
            rightArrow.draw()
            ABB.draw()
            leftArrow.draw()
            win.flip()
            keys = event.waitKeys(keyList=['left', 'right'])

            # evaluation phase
            key_choice_map = {'left': 'left', 'right': 'right'}
            participant_choice = key_choice_map.get(keys[0], None)

            # Check if participant's choice is correct
            if participant_choice == x_key:  # correct
                feedback = visual.TextStim(win, text="Richtig!",
                                           color='black',
                                           wrapWidth=2,
                                           height=0.2)
                feedback.draw()
                win.flip()
                core.wait(1)
                correct = True
                correct_in_a_row += 1
                correct_responses_count += 1
                if not two_down_one_up:
                    direction = 'down'
                    new_difference = current_difference - step_size
                else:
                    if correct_in_a_row >= 2:
                        direction = 'down'
                        new_difference = current_difference - step_size
                    else:
                        direction = 'none'
                        new_difference = current_difference
            else:
                feedback = visual.TextStim(win, text="Falsch, versuchen Sie es bitte nochmal.",
                                           color='black',
                                           wrapWidth=2,
                                           height=0.2)
                feedback.draw()
                win.flip()
                core.wait(1)
                correct = False
                if current_difference == exp_config["initial_difference"]:  # no direction change if at max difference level
                    direction = 'none'
                    new_difference = current_difference  # Keep new_difference the same
                else:  # no direction change if trial 1-2 incorrect-test difference not out of range
                    first_incorrect = True
                    two_down_one_up = True
                    correct_in_a_row = 0
                    direction = 'up'
                    new_difference = current_difference + step_size

            win.flip()
            core.wait(1)  # inter trial interval

            end_time = time.time()
            end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
            duration = end_time - start_time
            # Convert duration to hours, minutes, and seconds
            hours, remainder = divmod(duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            # Format the duration string without the fractional part
            duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

            # Write trial data to output file
            experiment_output.write(','.join([
                exp_data['experiment'],
                exp_data['subject'],
                exp_data['cur_date'],
                exp_config['task'],
                session_type,
                str(run),
                str(trial_index),
                start_time_str,
                end_time_str,
                duration_str,
                os.path.basename(recording_A),
                os.path.basename(recording_X),
                os.path.basename(recording_B),
                participant_choice,
                str(correct),
                str(current_difference),
                str(step_size),
                str(reversals),
                direction]) + '\n')
            experiment_output.flush()

            # prepare for the next iteration
            trial_index += 1
            current_difference = round(new_difference, 4)
            step_size = get_step_size(exp_config["task"], test_difference=current_difference)

            # IDE output for checking
            """print("current-difference: " + str(current_difference) + " at " + str(trial_index))
            print("step_size: " + str(step_size) + " at " + str(trial_index))"""

            test_stimulus = generate_stimulus_path(path_prefix, exp_config['baseline'] + current_difference,
                                                   exp_config["task"])

    # Close the output file
    experiment_output.close()
