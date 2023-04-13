"""
JND procedure to evaluate JND threshold for 3 different prosodic parameters on a subject basis
- final lengthening (FL) of the 2nd vowel in name: "Mimi" - relative to the whole name duration
- pause after name1 within a name coordinate of the kind "name1 [pause] and name2"
- pitch / f0 rise from syllable 1 to syllable 2 in name: "Nelli"

1-down-1-up protocol up to the first incorrect response - 2-down-1-up thereafter

odd-one-out forced-choice task with 3 sequentially auditory presented stimuli

* AXB pattern (AAB or ABB sequences, randomly chosen)
"""


from psychopy import sound, visual, event, core
import random
import time
from librosa import get_duration
from configuration import get_step_size, get_task_specific_config, general_experiment_configs
from pathchecks import stimulus_exists
from jnd_visualization import create_visualization


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
    if task == 'pitch':
        value = round(value, 1)
        value_suffix = str(value).replace('.', '_')
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
            task (str): The type of task, either 'pitch' or 'duration'.
            win (visual.Window): The PsychoPy window used for displaying the stimuli.
            session_type (str, optional): The type of session, either 'trial' or 'practice'. Defaults to 'trial'.

        Raises:
            Exception: If the session type is neither 'trial' nor 'practice'.
    """
    # AAB pattern pic
    global AAB
    AAB = visual.ImageStim(win,
                           image='pic/pic_right_correct_BBA.png',
                           pos=(0.5, -0.7),
                           name='AAB_pic')

    # ABB pattern pic
    global ABB
    ABB = visual.ImageStim(win,
                           image='pic/pic_left_correct_ABB.png',
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

    exp_config = get_task_specific_config(task)
    path_prefix = f'{exp_config["stimuli_path"]}{exp_config["stim_prefix"]}'

    # Assuming data.getDateStr() returns a string like "2023-03-28_13h10.02.144"
    date_time_str = exp_data['cur_date']
    date_time_parts = date_time_str.split('_')
    global date
    date = date_time_parts[0]  # "2023-03-28"
    time_full = date_time_parts[1]  # "13h10.02.144"
    # To get the time in hh:mm format, split time string by ':' and join the first two parts
    time_parts = time_full.split('.')
    global hh_mm
    hh_mm = time_parts[0]  # "13h10"

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
    """
    # Iterate through the runs
    for run in range(1, general_experiment_configs['num_runs'] + 1):
        # IDE output for checking
        """print(f"num_runs: {range(general_experiment_configs['num_runs'])}")
        print(f"run: {run}")"""
        # Generate stimulus paths
        baseline_stimulus = generate_stimulus_path(path_prefix, exp_config["baseline"], exp_config["task"])
        test_value = exp_config["baseline"] + exp_config["initial_difference"]
        test_stimulus = generate_stimulus_path(path_prefix, test_value, exp_config["task"])

        # Initialize variables for the staircase procedure
        current_difference = exp_config["initial_difference"]
        differences = [current_difference]
        first_incorrect = False
        step_size = get_step_size(exp_config["task"], first_incorrect)
        two_down_one_up = False
        correct_in_a_row = 1
        correct_responses = []
        trial_index = 0  # the number of trials aka choices
        reversals = 0  # number of times the direction of the staircase is changed (up/down or down/up or none/down)
        reversals_list = [reversals]
        previous_correct = [True]
        last_two_combinations = []  # to make sure there's no more than 3 in a row (AAB or ABB)

        # Set up the output file
        output_filename = f"JND_{exp_config['task']}_{exp_data['subject']}_{date}_{hh_mm}_run_{run}.csv"
        experiment_output = open(general_experiment_configs['output_path'] + output_filename, 'w')
        experiment_output.write('subject,'
                                'date,'
                                'task,'
                                'session_type,'
                                'run,'
                                'trial,'
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
        while trial_index <= general_experiment_configs["num_trials_each_run"] and reversals <= 14 and baseline_stimulus != test_stimulus:  # stop conditions

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
            stimulus_A.play()
            time.sleep(get_duration(filename=recording_A) + 1)  # inter stimulus interval 1s
            stimulus_X.play()
            time.sleep(get_duration(filename=recording_X) + 1)  # inter stimulus interval 1s
            stimulus_B.play()
            time.sleep(get_duration(filename=recording_B) + 0.2)  # after 3rd stimulus wait 200ms

            # Draw response options on screen
            AAB.draw()
            rightArrow.draw()
            ABB.draw()
            leftArrow.draw()
            win.flip()
            keys = event.waitKeys()

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
                first_incorrect = True
                two_down_one_up = True
                correct_in_a_row = 0
                direction = 'up'
                new_difference = current_difference + step_size
                correct_responses.append(correct)
            win.flip()
            core.wait(1)  # inter trial interval

            # write the trial data to the output file
            experiment_output.write(','.join([exp_data['subject'],
                                              exp_data['cur_date'],
                                              exp_config['task'],
                                              session_type,
                                              str(run),
                                              str(trial_index + 1),
                                              recording_A,
                                              recording_X,
                                              recording_B,
                                              participant_choice,
                                              str(correct),
                                              str(current_difference),
                                              str(step_size),
                                              str(reversals),
                                              direction]) + '\n')
            experiment_output.flush()

            # prepare for the next iteration
            trial_index += 1
            current_difference = round(new_difference, 3)
            differences.append(current_difference)
            step_size = get_step_size(exp_config["task"], first_incorrect, test_difference=current_difference)
            # IDE output for checking
            """print("current-difference: " + str(current_difference) + " at " + str(trial_index))
            print("step_size: " + str(step_size) + " at " + str(trial_index))"""

            # counts as reversal only when sequence True-False or False-True-True
            if (previous_correct[trial_index-1] == True and correct == False) or (
                    previous_correct[trial_index-2] == False and previous_correct[trial_index-1] == True and correct == True):
                reversals += 1
            previous_correct.append(correct)
            reversals_list.append(reversals)
            test_stimulus = generate_stimulus_path(path_prefix, exp_config['baseline'] + current_difference,
                                                   exp_config["task"])

        # Create visualization for the current run
        create_visualization(differences, correct_responses, reversals_list, exp_config["task"], exp_data['subject'], exp_data['cur_date'], run)

        # after each run
        if run < general_experiment_configs['num_runs']:
            pause_text = f"Sie haben {run} von 3 Blöcken geschafft.\n Drücken Sie eine Taste, sobald Sie bereit sind, weiterzumachen."
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

    # Close the output file
    experiment_output.close()


def run_practice_session(path_prefix, exp_data, exp_config, win):
    """
        Run a practice session for the experiment.

        Args:
            path_prefix (str): The path prefix for the stimulus files.
            exp_data (dict): A dictionary containing experiment data (e.g., subject, date).
            exp_config (dict): A dictionary containing experiment configuration (e.g., baseline, task).
            win (visual.Window): A PsychoPy window object for rendering stimuli.
    """
    session_type = "practice"
    # Initialize variables
    correct_responses_count = 0  # Incremented; practice session stops after 4 correct responses
    run = 0  # Practice session has only one run
    current_difference = exp_config["initial_difference"]
    first_incorrect = False
    step_size = get_step_size(exp_config["task"], first_incorrect)
    two_down_one_up = False
    correct_in_a_row = 1
    trial_index = 1  # number of trials
    reversals = -1  # number of times the direction of the staircase is changed (up/down or down/up or none/down)
    previous_direction = 'none'  # this is why reversals has to be set to -1

    # Generate baseline and test stimulus paths
    baseline_stimulus = generate_stimulus_path(path_prefix, exp_config["baseline"], exp_config["task"])
    test_value = exp_config["baseline"] + exp_config["initial_difference"]
    test_stimulus = generate_stimulus_path(path_prefix, test_value, exp_config["task"])

    # List to ensure there's no more than 3 in a row (AAB or ABB)
    last_two_combinations = []

    # Output file as csv with all relevant variable data
    output_filename = f"JND_{exp_config['task']}_{exp_data['subject']}_{date}_{hh_mm}_practice.csv"
    experiment_output = open(general_experiment_configs['output_path'] + output_filename, 'w')
    experiment_output.write(
        'subject,'
        'date,'
        'task,'
        'session_type,'
        'run,'
        'trial,'
        'recording_A,'
        'recording_X,'
        'recording_B,'
        'response,'
        'correct,'
        'difference,'
        'step-size,'
        'reversals,'
        'direction\n')

    # Display instructions and wait
    instructions = visual.TextStim(win,
                                   color='black',
                                   wrapWidth=2,
                                   height=0.1,
                                   text=exp_config["instructions"])

    instructions.draw()
    win.flip()  # display the message
    event.waitKeys()  # wait until button is pressed
    win.flip()

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
        stimulus_A.play()
        time.sleep(get_duration(filename=recording_A) + 1)  # inter stimulus interval 1s
        stimulus_X.play()
        time.sleep(get_duration(filename=recording_X) + 1)  # inter stimulus interval 1s
        stimulus_B.play()
        time.sleep(get_duration(filename=recording_B) + 0.2)  # after 3rd stimulus wait 200ms

        # Draw response options on screen
        AAB.draw()
        rightArrow.draw()
        ABB.draw()
        leftArrow.draw()
        win.flip()
        keys = event.waitKeys()

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
            first_incorrect = True
            two_down_one_up = True
            correct_in_a_row = 0
            direction = 'up'
            new_difference = current_difference + step_size

        win.flip()
        core.wait(1)  # inter trial interval

        # Write trial data to output file
        experiment_output.write(','.join([exp_data['subject'],
                                          exp_data['cur_date'],
                                          exp_config['task'],
                                          session_type,
                                          str(run),
                                          str(trial_index + 1),
                                          recording_A,
                                          recording_X,
                                          recording_B,
                                          participant_choice,
                                          str(correct),
                                          str(current_difference),
                                          str(step_size),
                                          str(reversals),
                                          direction]) + '\n')
        experiment_output.flush()

        # prepare for the next iteration
        trial_index += 1
        current_difference = round(new_difference, 3)
        step_size = get_step_size(exp_config["task"], first_incorrect, test_difference=current_difference)

        # IDE output for checking
        """print("current-difference: " + str(current_difference) + " at " + str(trial_index))
        print("step_size: " + str(step_size) + " at " + str(trial_index))"""

        # Update reversal count and previous_direction
        if (previous_direction == 'down' and direction == 'up') or (
                previous_direction == 'up' and direction == 'down') or (
                previous_direction == 'none' and direction == 'down'):
            reversals += 1
        previous_direction = direction
        test_stimulus = generate_stimulus_path(path_prefix, exp_config['baseline'] + current_difference,
                                               exp_config["task"])

    # Close the output file
    experiment_output.close()
