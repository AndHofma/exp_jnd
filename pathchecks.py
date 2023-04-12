import os

def check_config_paths(base_input_path, tasks, output_path):
    if not os.path.exists(base_input_path):
        raise Exception("No input folder detected. Please make sure that "
                        "'base_stimuli_path' is correctly set in the configurations")
    for task in tasks:
        if not os.path.exists(f'{base_input_path}/audio-{task}'):
            raise Exception(f"No input folder for task {task} detected. Please "
                            f"create it or remove task {task} from the configurations")
    if not os.path.exists(output_path):
        os.mkdir(output_path)


def stimulus_exists(stim_path):
    if not os.path.isfile(stim_path):
        return False
    return True