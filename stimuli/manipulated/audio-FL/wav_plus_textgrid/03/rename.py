import os
import re

# 1. Open a folder on my laptop
path = "/Users/Andrea Hofmann/OneDrive/PhD/phd_perception_production_link/dissertation/procedure_all/exp_jnd/stimuli_manipulated/audio-FL/wav_plus_textgrid/03"
os.chdir(path)

# 2. Read in all files from the folder that are from type wav
files = os.listdir(path)

# 3. Safe all filenames from all these wav files. They should not include the .wav part
filenames = []
for file in files:
    if file.endswith(".wav"):
        filenames.append(file)

# 4. Look for regular expression in each filename, which is a dot.
# 5. Exchange this dot with an underline
# 6. Save each new filename in the original folder
for filename in filenames:
    new_filename = re.sub("\.", "_", filename)
    os.rename(filename, new_filename)

# 1. Open a folder on my laptop
path = "/Users/Andrea Hofmann/OneDrive/PhD/phd_perception_production_link/dissertation/procedure_all/exp_jnd/stimuli_manipulated/audio-FL/wav_plus_textgrid/03"
os.chdir(path)

# 2. Read in all files from the folder that are from type wav
files = os.listdir(path)
filenames = []
for file in files:
    if file.endswith("_wav"):
        filenames.append(file)

# 4. Look for regular expression in each filename, which is a dot.
# 5. Exchange this dot with an underline
# 6. Save each new filename in the original folder
for filename in filenames:
    new_filename = filename[:-4] + ".wav"
    os.rename(filename, new_filename)