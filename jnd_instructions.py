"""
This module, named jnd_instructions.py, contains the strings for the instruction text to be displayed to the participants
in a listening task, and a function to generate the instruction text based on the task type and index.

Constants:
    pitch_FL_text (str): Instruction text for tasks related to the pitch and Fundamental Frequency (FL).
    pause_text (str): Instruction text for tasks related to pauses.

Functions:
    get_instruction_text(task: str, ind: int) -> str: Returns the instruction text for a particular task, given the
    task type and index.

Note:
    The instruction texts are in German and guide the participant through a task involving listening to sequences of
    names or word groups, and identifying which one is different from the others.
    The 'get_instruction_text' function generates the appropriate instruction text for the current task, and modifies
    it based on whether it's the last task or not, and whether the task involves 'pause' or not.
    In the pause task, participants are informed that the task duration will be between 18-22 minutes, and for other
    tasks, they are informed of a duration between 10-15 minutes.
"""


pitch_FL_text = """
Sie hören nachfolgend denselben Namen dreimal.
Ein Name ist immer anders als die beiden anderen. \n
Manchmal ist der ERSTE Name anders - nach dem Muster ABB.
Manchmal ist der DRITTE Name anders - nach dem Muster BBA. \n
Nachdem alle drei Namen vorgespielt wurden, wählen Sie bitte, \n welcher anders war, als die anderen beiden.
Wenn Sie denken, der ERSTE Name ist anders, \n drücken Sie \u2190 den Pfeil nach links auf der Tastatur.
Wenn Sie denken, der DRITTE Name ist anders, \n drücken Sie \u2192 den Pfeil nach rechts auf der Tastatur.\n
Drücken Sie 'Enter', dann starten die Übungsbeispiele.
"""

pause_text = """
Sie hören nachfolgend dieselbe Wortgruppe dreimal. 
Eine Wortgruppe ist immer anders als die beiden anderen. \n
Manchmal ist die ERSTE Wortgruppe anders - nach dem Muster ABB.
Manchmal ist die DRITTE Wortgruppe anders - nach dem Muster BBA. \n
Nachdem alle drei Wortgruppen vorgespielt wurden, wählen Sie bitte, \n welche anders war, als die anderen beiden.
Wenn Sie denken, die ERSTE Wortgruppe ist anders, \n drücken Sie \u2190 den Pfeil nach links auf der Tastatur.
Wenn Sie denken, die DRITTE Wortgruppe ist anders, \n drücken Sie \u2192 den Pfeil nach rechts auf der Tastatur.\n
Drücken Sie eine 'Enter', dann starten die Übungsbeispiele.
"""

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
               f"Dieser Teil dauert ca. 18 Minuten. \n" \
               f"{last_task_text}" \
               f"Beachten Sie: \n" \
               f"Die Aufgabe wird nach und nach immer schwieriger,\n " \
               f"denn die Unterschiede werden immer kleiner. \n" \
               f"Bitte antworten Sie dennoch immer so akkurat, wie möglich.\n\n" \
               f"Drücken Sie eine 'Enter' sobald Sie bereit sind."
    else:
        return f"Sehr gut!\n" \
               f"Wenn Sie noch Fragen haben, geben Sie der Versuchsleiterin Bescheid.\n\n" \
               f"Es startet der {ind + 1}. von 3 Teilen.\n" \
               f"Dieser Teil dauert ca. 8 Minuten. \n" \
               f"{last_task_text}" \
               f"Beachten Sie: \n" \
               f"Die Aufgabe wird nach und nach immer schwieriger,\n " \
               f"denn die Unterschiede werden immer kleiner. \n" \
               f"Bitte antworten Sie dennoch immer so akkurat, wie möglich.\n\n" \
               f"Drücken Sie eine 'Enter' sobald Sie bereit sind."
