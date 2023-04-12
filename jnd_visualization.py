import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Patch, Rectangle, Circle
from matplotlib.legend_handler import HandlerPatch

def create_visualization(differences, correct_responses, reversals_list, task, subject, date, run, file_format='png'):
    threshold = np.mean(differences[-6:]) if len(reversals_list) >= 6 else differences[0]
    # Identify the index positions where the reversals_list values change
    reversal_indices = [i-1 for i in range(1, len(reversals_list)) if reversals_list[i] != reversals_list[i - 1]]
    reversal_difference = [differences[index] for index in reversal_indices]
    print("Difference values at reversal_indices:", reversal_difference)

    plt.figure(figsize=(10, 5))
    plt.plot(differences, color='black', linestyle='-', linewidth=1)
    plt.axhline(y=threshold, color='gray', linestyle='--', linewidth=1)

    for i, (difference, correct) in enumerate(zip(differences, correct_responses)):
        marker = 'o' if i in reversal_indices else 's'
        color = 'green' if correct else 'red'
        plt.scatter(i, difference, marker=marker, color=color, s=50, edgecolors='black')
        if i in reversal_indices:
            plt.annotate(f"{round(difference, 3)}", (i, difference), textcoords="offset points", xytext=(0, 10),
                         ha='center',
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
                                   label=f'Threshold (mean last 6 reversals_list) = {round(threshold, 2)}')

    correct_patch = Patch(facecolor='green', label='Correct Response', linewidth=1, edgecolor='black')
    incorrect_patch = Patch(facecolor='red', label='Incorrect Response', linewidth=1, edgecolor='black')
    reversal_patch = Patch(facecolor='white', label='Reversal', linewidth=1, edgecolor='black')

    plt.xlabel('Trial Number')
    plt.ylabel(task + ' difference')
    plt.title('Adaptive Staircase Design - Switching to 2-down-1-up after First Incorrect Response')
    plt.legend(handles=[staircase_line, threshold_line, correct_patch, incorrect_patch, reversal_patch],
               handler_map={reversal_patch: CircleHandler(), correct_patch: RectangleHandler(), incorrect_patch: RectangleHandler()},
               loc='upper right')
    plt.grid(True)

    # Save the plot as a file
    file_name = f"{subject}_{date}_{task}_{run}.{file_format}"
    plt.savefig(file_name, dpi=300, bbox_inches='tight')

    # Show the plot
    plt.show()

if __name__ == "__main__":
    create_visualization()