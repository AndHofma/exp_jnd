"""
Plotting staircase for each run in each task per participant - save plot as *.png
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Patch, Rectangle, Circle
from matplotlib.legend_handler import HandlerPatch
from configuration import *
import os
from datetime import datetime


def calculate_threshold(reversals, num_reversals=6):
    if len(reversals) < num_reversals:
        selected_reversals = reversals
    else:
        selected_reversals = reversals[-num_reversals:]

    mean_threshold = np.mean(selected_reversals)
    median_threshold = np.median(selected_reversals)

    return mean_threshold, median_threshold, selected_reversals


def create_visualization(differences, correct_responses, reversals_list, task, subject, file_format='png'):
    """
        Create and save a visualization of an adaptive staircase experiment with given data.
        :param differences: List of difference values between stimuli for each trial.
        :param correct_responses: List of boolean values indicating if the response was correct for each trial.
        :param reversals_list: List of reversal points in the experiment.
        :param task: String representing the name of the task.
        :param subject: String representing the subject identifier.
        :param file_format: Optional, the file format for saving the plot, default is 'png'.
    """

    # Identify the index positions where the reversals_list values change
    reversal_indices = [i-1 for i in range(1, len(reversals_list)) if reversals_list[i] != reversals_list[i - 1]]

    # Create a list of reversal differences using the reversal_indices
    reversal_difference = [differences[index] for index in reversal_indices]

    # Output in IDE - for checking
    #print("Difference values at reversal_indices:", reversal_difference)

    # Calculate the threshold value = mean and median of difference values at last 6 reversals
    mean_threshold, median_threshold, selected_reversals = calculate_threshold(reversal_difference)

    # Initialize the plot
    plt.figure(figsize=(10, 5))
    plt.plot(differences, color='black', linestyle='-', linewidth=1)
    y_min = min(differences) - 0.1 * (max(differences) - min(differences)) # adapt y-axis to scale of the data
    y_max = max(differences) + 0.1 * (max(differences) - min(differences))
    plt.ylim(y_min, y_max)
    plt.axhline(y=mean_threshold, color='gray', linestyle='--', linewidth=1)

    # Plot the data points with corresponding markers and colors
    for i, (difference, correct) in enumerate(zip(differences, correct_responses)):
        marker = 'o' if i in reversal_indices else 's'
        color = 'green' if correct else 'red'
        plt.scatter(i, difference, marker=marker, color=color, s=30, edgecolors='black')
        if i in reversal_indices:
            text_offset_y = 10 if i % 2 == 0 else -20  # Alternating the text position above and below the marker
            plt.annotate(f"{round(difference, 3)}", (i, difference), textcoords="offset points",
                         xytext=(0, text_offset_y),
                         ha='center',
                         fontsize=8)


    # Custom legend handlers
    class CircleHandler(HandlerPatch):
        """
            Custom legend handler class for circle-shaped patches.
            Inherits from matplotlib.legend_handler.HandlerPatch.
            """
        def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):
            """
            Create a circle-shaped artist for the legend.

            :param legend: The legend instance.
            :param orig_handle: The original patch object.
            :param xdescent: X-coordinate offset for the circle artist.
            :param ydescent: Y-coordinate offset for the circle artist.
            :param width: Width of the bounding box for the artist.
            :param height: Height of the bounding box for the artist.
            :param fontsize: Font size for the legend.
            :param trans: Transformation applied to the artist.
            :return: List containing the circle artist.
            """
            center = width // 2, height // 2
            p = Circle(xy=center, radius=height / 4, facecolor=orig_handle.get_facecolor(),
                       edgecolor=orig_handle.get_edgecolor(), linewidth=orig_handle.get_linewidth())
            self.update_prop(p, orig_handle, legend)
            p.set_transform(trans)
            return [p]

    class RectangleHandler(HandlerPatch):
        """
        Custom legend handler class for rectangle-shaped patches.
        Inherits from matplotlib.legend_handler.HandlerPatch.
        """
        def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):
            """
            Create a rectangle-shaped artist for the legend.

            :param legend: The legend instance.
            :param orig_handle: The original patch object.
            :param xdescent: X-coordinate offset for the rectangle artist.
            :param ydescent: Y-coordinate offset for the rectangle artist.
            :param width: Width of the bounding box for the artist.
            :param height: Height of the bounding box for the artist.
            :param fontsize: Font size for the legend.
            :param trans: Transformation applied to the artist.
            :return: List containing the rectangle artist.
            """
            p = Rectangle(xy=(xdescent, ydescent), width=width, height=height, facecolor=orig_handle.get_facecolor(),
                          edgecolor=orig_handle.get_edgecolor(), linewidth=orig_handle.get_linewidth())
            self.update_prop(p, orig_handle, legend)
            p.set_transform(trans)
            return [p]

    # Create legend elements
    staircase_line = mlines.Line2D([], [], color='black', linestyle='-', linewidth=1, label='Staircase')
    threshold_line = mlines.Line2D([], [], color='gray', linestyle='--', linewidth=1,
                                   label=f'Threshold (mean: {round(mean_threshold, 2)}, '
                                         f'median: {round(median_threshold, 2)} of {(len(selected_reversals))} reversals)')

    correct_patch = Patch(facecolor='green', label='Correct Response', linewidth=1, edgecolor='black')
    incorrect_patch = Patch(facecolor='red', label='Incorrect Response', linewidth=1, edgecolor='black')
    reversal_patch = Patch(facecolor='white', label='Reversal', linewidth=1, edgecolor='black')

    # Set labels and title
    plt.xlabel('Trial Number')
    plt.ylabel(task + ' difference')
    plt.title(f'Just-Noticeable Difference Adaptive Staircase Task for subject: {subject} and cue: {task} ')
    # Add the legend to the plot
    plt.legend(handles=[staircase_line, threshold_line, correct_patch, incorrect_patch, reversal_patch],
               handler_map={reversal_patch: CircleHandler(),
                            correct_patch: RectangleHandler(),
                            incorrect_patch: RectangleHandler()},
               loc='upper right')
    plt.grid(True)

    # path setup results per participant
    # Define the path in results for each subject
    subj_path_plots = os.path.join(general_experiment_configs['plot_path'], subject)
    # Create the directory if it doesn't exist
    if not os.path.exists(subj_path_plots):
        os.makedirs(subj_path_plots)

    # Get the current date and time
    now = datetime.now()
    # Format it as a string
    date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
    # Set up the output file
    file_name = f"{subject}_{date_string}_{task}.{file_format}"
    plt.savefig(os.path.join(subj_path_plots, file_name), dpi=300, bbox_inches='tight')

    # Show the plot
    # plt.show()
    return selected_reversals

