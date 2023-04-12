# Perception-Production-Link_Name-Coordinates/jnd_task
## Step-by-step guide on running the jnd_task properly

The staircase algorithm follows a similar approach as Smith et al. in [Contributions of Auditory and Somatosensory Feedback to Vocal Motor Control](https://pubs.asha.org/doi/full/10.1044/2020_JSLHR-19-00296) by Smith et al. 
We used [PsychoPy](https://www.psychopy.org/) to set up the experiment.

This README file provides a comprehensive guide to setting up and running the experimental task 
for the ***just-noticeable-difference task*** from the dissertation project **Perception-Production-Link in 
Prosody for Disambiguation**.
The jnd_task is composed of different modules that call each other to create the complete task. 
Follow the steps below in the given order to ensure a successful setup and execution.

### 1. GitHub
To download the project files from GitHub, follow these steps:

* Install Git on your computer by downloading it from the following link if you have a Windows system: https://git-scm.com/download/win
  * Choose 32 or 64-bit, whereas **64-bit** is the **most common one**

* After installing Git, open the Command Prompt (CMD) on your computer.

### 2. Opening Windows Command Prompt
The Command Prompt is a program on Windows computers used to execute commands. 
To open it, follow these steps:

* Press **Win + R** keys to open the *Run* dialog box.
* Type *cmd* and press Enter.

### 3. Downloading Project Files from GitHub
* Navigate to the folder where you want to download the project files using the *cd* command in the Windows command prompt. 
* Replace your_desired_folder with the path to the folder:
  * `cd your_desired_folder`
* Clone the GitHub repository by running the following command:
  * `git clone your_github_repository_url`
  * The project files will be downloaded to a folder named after the repository within the specified folder.

### 4. Checking Python Installation and Version
* To check if Python is installed on your computer and determine its version, open the Windows Command Prompt (if not still open) and run the following command:
  * `python --version`
* If Python is installed, the command will display the installed version (e.g., "Python 3.8.15"). 
* If Python is not installed, the command will not be recognized.

### 5. Creating a Virtual Environment with Python 3.8
* To create a virtual environment with Python 3.8, first, make sure you have Python 3.8 installed on your computer.
* If not, download and install it for Windows (most commonly 64-bit): https://www.python.org/downloads/release/python-3810/
* Open the Windows Command Prompt.
* Navigate to the project folder using the *cd* command. 
* Replace *your_project_folder* with the path to your project folder:
  * `cd your_project_folder`
* Run the following command to create the virtual environment. 
* Replace *your_env_name* with your desired name for the virtual environment (e.g. *jnd_env*):
  * `py -3.8 -m venv your_env_name` (e.g. `py -3.8 -m venv jnd_env`)
* After the virtual environment is created, activate it with the following command:
  * `your_env_name\Scripts\activate` (e.g. `jnd_env\Scripts\activate`)

### 6. Installing Python Packages from requirements.txt
* To install the required Python packages from the requirements.txt file, run the following command in the activated virtual environment:
  * `pip install -r requirements.txt`
* This command will install all the necessary packages listed in the requirements.txt file.

### 7. Running the Experiment
To start and run the experiment, follow these steps:

* Ensure the virtual environment is activated (you should see the virtual environment name in the command prompt).
* Navigate to the folder containing the main Python script for the experiment using the *cd* command, if you're not already there.
* Run the main Python script by typing the following command:
  * `python jnd_experiment.py`

### 8. Experiment-Start
* First, a small dialogue window will appear. 
* Enter the subject id and press "OK". 
* The results will be recorded in the file "JND_*TaskName*\_*SUBJECT_ID*\_*timestamp*\_run_*Nr*.csv" in the "**results**" folder.
* The plots will be stored in the file "*SUBJECT_ID*\_*timestamp*\_*TaskName*\_*Nr*.png" in the "**plots**" folder.
