# specify the directory from which you want to access the wav and textgrid files
input_directory$ = "C:\Users\NOLA\OneDrive\PhD\exp_jnd\stimuli\manipulated\audio-pitch\0_005st\"
# directory for saving the processed files
output_directory$ = "C:\Users\NOLA\OneDrive\PhD\exp_jnd\stimuli\manipulated\audio-pitch\0_005-st_fadeOut_TESTSTIMULI\"

# Create a Strings object containing the list of WAV files
Create Strings as file list: "wav_list", input_directory$ + "*.wav"

n = Get number of strings

# Process each WAV file
for i from 1 to n
    select Strings wav_list
    filename$ = Get string: i
    Read from file: input_directory$ + filename$
    sound_name$ = selected$("Sound")

    # Apply 80ms offset cosine ramp
    end_time = Get end time
    offset_ramp_time = 0.08
    Formula: "if x > (end_time - offset_ramp_time) then self * cos((x - (end_time - offset_ramp_time)) / offset_ramp_time * pi / 2) else self endif"

    # Save the modified WAV file
    Save as WAV file: output_directory$ + sound_name$ + ".wav"

endfor

# Clean up
select all
Remove
