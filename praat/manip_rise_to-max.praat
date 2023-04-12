######################
## Description data ##
######################

# textgrid has 5 interval tiers / 1 point tier #
# tier1:word (interval)#
# tier2:syll  (interval)#
# tier3:seg (interval)#
# tier4:glott (interval)#
# tier6: comments (interval)#
# tier5: f0 (point)#

################
## Setup data ##
################

## directories ##
# specify the directory from which you want to access the wav and textgrid files
d$ = "C:\Users\Andrea Hofmann\OneDrive\PhD\phd_perception_production_link\dissertation\procedure_all\exp_jnd\stimuli_to-be-manipulated\rise\cut_name2\"
# directory for saving the manipulated files
dir$ = "C:\Users\Andrea Hofmann\OneDrive\PhD\phd_perception_production_link\dissertation\procedure_all\exp_jnd\stimuli_manipulated\rise_from_bra\"

## wav-files ##
# Creates object "Strings list" containing only .wav files
strings = Create Strings as file list: "list", d$ + "*.wav"
numberOfFiles = Get number of strings
for ifile to numberOfFiles
    selectObject: strings
    fileName$ = Get string: ifile
    Read from file: d$ + fileName$
    # store basename in variable name
    name$ = selected$ ("Sound")
endfor
removeObject: strings

## textgrids ##
# Creates object "Strings list" containing only .TextGrid files
strings = Create Strings as file list: "list", d$ + "*.TextGrid"
numberOfFiles = Get number of strings
for ifile to numberOfFiles
    selectObject: strings
    fileName$ = Get string: ifile
    Read from file: d$ + fileName$
    # store basename in variable name
    name$ = selected$ ("TextGrid")
endfor
removeObject: strings

#############################################
## Read out information from original file ##
#############################################

## f0 ##
select Sound 'name$'
To Pitch: 0, 75, 600

select TextGrid 'name$'

tier5 = Get number of points: 5
for j from 1 to tier5
	select TextGrid 'name$'
	p$ = Get label of point: 5, j
	t = Get time of point: 5, j
	if p$ == "L2"
		l2t = t
		select Pitch 'name$'
		l2 = Get value at time: l2t, "Hertz", "Linear"
	elsif p$ == "H2"
		h2t = t
		select Pitch 'name$'
		h2 = Get value at time: h2t, "Hertz", "Linear"
	endif
endfor

## duration s8 (tier3) ##
select TextGrid 'name$'
tier3 = Get number of intervals... 3

for k from 1 to tier3
	select TextGrid 'name$'
	label3$ = Get label of interval: 3, k

	if label3$ == "s8"
		starts8 = Get start time of interval: 3, k
		ends8 = Get end time of interval: 3, k
		s8 = 'ends8' - 'starts8'
	endif
endfor

############################################
## Calculate values to setup manipulation ##
############################################

## f0 rise ##
# calculate rise for original file - origRise (in semitones)
origRise = 12*log2(h2/l2)

# maxRise value equals max rise2 from ch model stimuli (model_ch_rprod_l1_t02_r1_mimmi_nob_noma)
# plus 1 semitone to set the max rise a bit higher for JND task
# needed because participants could possibly answer incorrect right in the beginning
# which would lead the adaptive staircase procedure to switch to a stimulus with an even higher rise
maxRise = 14

# amount of 0.1 semitone steps to get from origRise to maxRise
# round to integer - get rid of decimal places
stepsRise = round((maxRise-origRise) / 0.1)

##################
## Manipulation ##
##################

## f0 rise continuum ##
for x from 1 to stepsRise
    select Sound 'name$'
    To Manipulation: 0.01, 75, 600
    Edit
	editor Manipulation 'name$'

    # delete all pitchpoints in name2 to the right of L2
    # put a new pitch point with the new value for H2 at 80% of the final vowel (aka s8)
    l2tpp = 'l2t' + 0.005
    # variable for positioning H2
    nh = s8/10*2
    posh2new = ends8 - nh
    # variable for deleting pitch points next to L2
    Select: 'l2tpp', 'ends8'
    Remove pitch point(s)

    # get new h2Max value for each step
    h2Max = 2^((origRise+x*0.1)/12) * l2
    # rise variable to put in filename of new file
    # this value will be relevant to find correct stimulus later in JND script
    currRise$ = fixed$ ((origRise+x*0.1), 1)
    Add pitch point at: 'posh2new', 'h2Max'

    Publish resynthesis
    Close

    # actual name = "nelli"
    name_new$ = "nelli_rise_" + currRise$
    Rename: "'name_new$'"
    Save as WAV file... 'dir$''name_new$'.wav

endfor

select all
Remove