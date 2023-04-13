"""
Plotting staircase for each run in each task per participant - save plot as *.png
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Patch, Rectangle, Circle
from matplotlib.legend_handler import HandlerPatch


def create_visualization(differences, correct_responses, reversals_list, task, subject, date, run, file_format='png'):
    """
        Create and save a visualization of an adaptive staircase experiment with given data.
        :param differences: List of difference values between stimuli for each trial.
        :param correct_responses: List of boolean values indicating if the response was correct for each trial.
        :param reversals_list: List of reversal points in the experiment.
        :param task: String representing the name of the task.
        :param subject: String representing the subject identifier.
        :param date: String representing the date of the experiment.
        :param run: String representing the run number.
        :param file_format: Optional, the file format for saving the plot, default is 'png'.
    """
    # Calculate the threshold value = mean of difference values at last 6 reversals
    threshold = np.mean(differences[-6:]) if len(reversals_list) >= 6 else differences[0]
    # Identify the index positions where the reversals_list values change
    reversal_indices = [i-1 for i in range(1, len(reversals_list)) if reversals_list[i] != reversals_list[i - 1]]

    # Output in IDE - for checking
    """reversal_difference = [differences[index] for index in reversal_indices]
    print("Difference values at reversal_indices:", reversal_difference)"""

    # Initialize the plot
    plt.figure(figsize=(10, 5))
    plt.plot(differences, color='black', linestyle='-', linewidth=1)
    plt.axhline(y=threshold, color='gray', linestyle='--', linewidth=1)

    # Plot the data points with corresponding markers and colors
    for i, (difference, correct) in enumerate(zip(differences, correct_responses)):
        marker = 'o' if i in reversal_indices else 's'
        color = 'green' if correct else 'red'
        plt.scatter(i, difference, marker=marker, color=color, s=50, edgecolors='black')
        if i in reversal_indices:
            plt.annotate(f"{round(difference, 3)}", (i, difference), textcoords="offset points", xytext=(0, 10),
                         ha='center',
                         fontsize=9)

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
                                   label=f'Threshold (mean last 6 reversals_list) = {round(threshold, 2)}')

    correct_patch = Patch(facecolor='green', label='Correct Response', linewidth=1, edgecolor='black')
    incorrect_patch = Patch(facecolor='red', label='Incorrect Response', linewidth=1, edgecolor='black')
    reversal_patch = Patch(facecolor='white', label='Reversal', linewidth=1, edgecolor='black')

    # Set labels and title
    plt.xlabel('Trial Number')
    plt.ylabel(task + ' difference')
    plt.title('Adaptive Staircase Design - Switching to 2-down-1-up after First Incorrect Response')
    # Add the legend to the plot
    plt.legend(handles=[staircase_line, threshold_line, correct_patch, incorrect_patch, reversal_patch],
               handler_map={reversal_patch: CircleHandler(),
                            correct_patch: RectangleHandler(),
                            incorrect_patch: RectangleHandler()},
               loc='upper right')
    plt.grid(True)

    # Save the plot as a file
    file_name = f"plots/{subject}_{date}_{task}_{run}.{file_format}"
    plt.savefig(file_name, dpi=300, bbox_inches='tight')

    # Show the plot
    plt.show()


if __name__ == "__main__":
    create_visualization()
