import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Patch, Rectangle, Circle
from matplotlib.legend_handler import HandlerPatch

def logistic(x, k, x0):
    return 1 / (1 + np.exp(-k * (x - x0)))

def staircase_adaptive(initial_value, max_trials, step_size):
    pitch = initial_value
    pitches = [pitch]
    correct_responses = []
    reversals = []
    correct_count = 0
    incorrect_count = 0
    two_down_one_up_started = False
    trial_count = 0
    direction = -1  # -1 for down, 1 for up

    while trial_count < max_trials and len(reversals) < 12:
        threshold = np.mean(pitches[-6:]) if len(reversals) >= 6 else initial_value
        k = 0.8  # Steepness of the logistic function
        x0 = initial_value * 0.8  # Midpoint of the logistic function
        p_correct = logistic(pitch, k, x0)
        correct = random.random() < p_correct

        correct_responses.append(correct)

        if correct:
            if not two_down_one_up_started:
                new_direction = -1
                pitch -= step_size
            else:
                correct_count += 1
                if correct_count == 2:
                    new_direction = -1
                    pitch -= step_size
                    correct_count = 0
                else:
                    new_direction = direction
        else:
            new_direction = 1
            pitch += step_size
            incorrect_count += 1
            correct_count = 0
            if not two_down_one_up_started:
                two_down_one_up_started = True
            else:
                reversals.append(trial_count)

        if direction != new_direction and trial_count > 0:
            reversals.append(trial_count)
        direction = new_direction

        pitches.append(pitch)
        trial_count += 1

    return pitches, correct_responses, reversals

def create_visualization():
    initial_value = 16.7
    max_trials = 100
    step_size = 0.5

    pitches, correct_responses, reversals = staircase_adaptive(initial_value, max_trials, step_size)
    threshold = np.mean(pitches[-6:]) if len(reversals) >= 6 else initial_value
    reversal_pitches = [pitches[reversal] for reversal in reversals]
    print("Reversal pitch values:", reversal_pitches)

    plt.figure(figsize=(10, 5))
    plt.plot(pitches, color='black', linestyle='-', linewidth=1)
    plt.axhline(y=threshold, color='gray', linestyle='--', linewidth=1)

    for i, (pitch, correct) in enumerate(zip(pitches, correct_responses)):
        marker = 'o' if i in reversals else 's'
        color = 'green' if correct else 'red'
        plt.scatter(i, pitch, marker=marker, color=color, s=50, edgecolors='black')
        if i in reversals:
            plt.annotate(f"{round(pitch, 1)}", (i, pitch), textcoords="offset points", xytext=(0, 10), ha='center',
                         fontsize=9)

    class CircleHandler(HandlerPatch):
        def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):
            center = width // 2, height // 2
            p = Circle(xy=center, radius=height / 4, facecolor=orig_handle.get_facecolor(),
                       edgecolor=orig_handle.get_edgecolor(), linewidth=orig_handle.get_linewidth())
            self.update_prop(p, orig_handle, legend)
            p.set_transform(trans)
            return [p]

    class RectangleHandler(HandlerPatch):
        def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):
            p = Rectangle(xy=(xdescent, ydescent), width=width, height=height, facecolor=orig_handle.get_facecolor(),
                          edgecolor=orig_handle.get_edgecolor(), linewidth=orig_handle.get_linewidth())
            self.update_prop(p, orig_handle, legend)
            p.set_transform(trans)
            return [p]

    staircase_line = mlines.Line2D([], [], color='black', linestyle='-', linewidth=1, label='Staircase')
    threshold_line = mlines.Line2D([], [], color='gray', linestyle='--', linewidth=1,
                                   label=f'Threshold (mean last 6 reversals) = {round(threshold, 2)}')

    correct_patch = Patch(facecolor='green', label='Correct Response', linewidth=1, edgecolor='black')
    incorrect_patch = Patch(facecolor='red', label='Incorrect Response', linewidth=1, edgecolor='black')
    reversal_patch = Patch(facecolor='white', label='Reversal', linewidth=1, edgecolor='black')

    plt.xlabel('Trial Number')
    plt.ylabel('Stimulus Feature Difference')
    plt.title('Adaptive Staircase Design - Switching to 2-down-1-up after First Incorrect Response')
    plt.legend(handles=[staircase_line, threshold_line, correct_patch, incorrect_patch, reversal_patch],
               handler_map={reversal_patch: CircleHandler(), correct_patch: RectangleHandler(), incorrect_patch: RectangleHandler()},
               loc='upper right')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    create_visualization()
