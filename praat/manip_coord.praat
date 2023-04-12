###########################################
# Manipulation script for Coordinates
# manip_coord.praat
#
# 19-11-2018, written by Clara Huttenlauch
# 03-12-2018: corrected for reference values
# 04-12-2018: adapted: no maxP, but instead maxLR (max values of lengthening AND f0-range, min pause duration)
# 05-12-2018: max2 in nob is replaced by maxLR (no change in manip, only in naming)
#
# f0: maximum value on name2 is manipulated to achieve the desired pitch range
#     all pitch points following l2 in name2 are deleted. the new h2 is set at the position of 80% in the vowel
#
# s8: the duration of the final vowel in name2 is manipulated to achieve the desired lengthening
#     the lengthening is calculated relative to the duration of name (which changes when s8 is manipulated)
#
# p3: the duration of the pause after name2 is manipulated to achieve the desired relative duration
#     the duration is calculated relative to the duration of the utterance (which changes when s8 and p3 are manipulated)
#     this applies to different degrees to the cases when all cues are min or max, s8 is max and the p3 is min, or s8 is min and p3 is max
#
# the script outputs a table with the original and new values
########################################### 

form Please enter values for manipulation
comment Maximum values for the bracket condition
integer Bra_Range_Max_(st) 12
integer Bra_Length_Max_(%) 52
integer Bra_Pause_Max_(%) 23

comment Minimum values for the bracket condition
integer Bra_Range_Min_(st) 9
integer Bra_Length_Min_(%) 36
integer Bra_Pause_Min_(%) 3

comment Maximum values for the no bracket condition
integer Nob_Range_Max_(st) 7
integer Nob_Length_Max_(%) 45
#integer Nob_Pause_Max_(%) 

comment Minimum values for the no bracket condition
integer Nob_Range_Min_(st) 3
integer Nob_Length_Min_(%) 27
integer Nob_Pause_Min_(%) 0

endform

## change names of variables from form
maxrangeBra = bra_Range_Max
maxlengthBra = bra_Length_Max
# percentage of the rest of name2 (name2 - s8)
rn2MaxBra = 100 - 'maxlengthBra'
maxpauseBra = bra_Pause_Max
# percentage of utterance excluding pause3
ruttMaxBra = 100 - 'maxpauseBra'
minrangeBra = bra_Range_Min
minlengthBra = bra_Length_Min
rn2MinBra = 100 - 'minlengthBra'
minpauseBra = bra_Pause_Min
ruttMinBra = 100 - 'minpauseBra'

maxrangeNob = nob_Range_Max
maxlengthNob = nob_Length_Max
rn2MaxNob = 100 - 'maxlengthNob'
#maxpauseNob = nob_Pause_Max
minrangeNob = nob_Range_Min
minlengthNob = nob_Length_Min
rn2MinNob = 100 - 'minlengthNob'
minpauseNob = nob_Pause_Min
ruttMinNob = 100 - 'minpauseNob'


clearinfo

# for checking the values
#printline length: 'maxlengthBra' 'rn2MaxBra' 'minlengthBra' 'rn2MinBra', 'maxlengthNob' 'rn2MaxNob' 'minlengthNob' 'rn2MinNob'
#printline pause: 'maxpauseBra' 'ruttMaxBra' 'minpauseBra' 'ruttMinBra', 'minpauseNob' 'ruttMinNob'


# specify the directory from which you want to access the soundfiles
d$ = "/Users/bgw/ownCloud/B01_Experimente/WP3_Experiment7&8_Leipzig/WP3_Experiment8/Stimuli_Exp8_selection/annotated/"

# directory for saving the manipulated files
dir$ = "/Users/bgw/ownCloud/B01_Experimente/WP3_Experiment7&8_Leipzig/WP3_Experiment8/Manipulation/no_maxP/"

# opens the wav-files from a file
Create Strings as file list... list 'd$'*.wav


# query number of objects in the stringslist and store in variable n
n = Get number of strings
printline number of strings: 'n'

# create Table for data
Create Table with column names: "table", n, "filename condition h2orig l2orig s8orig n2orig p3orig uttorig h2max h2min s8max s8min n2max n2min p3max p3min p3Lmax uttmax uttmin uttLmax diffs8 diffp3 diffutt"

# for-loop, goes through each object in the list
for i from 1 to n
	select Strings list
	filename$ = Get string... 'i'
	Read from file... 'd$''filename$'
	# store basename in variable name
	name$ = selected$ ("Sound")
	Read from file... 'd$''name$'.TextGrid

	# query information on condition
	select Sound 'name$'
	condition$ = mid$(name$,14,3)

	select Table table
	Set string value: i, "filename", name$
	Set string value: i, "condition", condition$

## Read out values in original file ##
	
	## F0 ##
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

	## duration segments (tier3) ##
	select TextGrid 'name$'
	tier3 = Get number of intervals... 3
	tier3.1 = 'tier3' - 1

	p3 = 0
	startp3 = 0
	endp3 = 0

	for k from 2 to tier3.1
		select TextGrid 'name$'
		label3$ = Get label of interval: 3, k

		if label3$ == "s8"
			starts8 = Get start time of interval: 3, k
			ends8 = Get end time of interval: 3, k
			s8 = 'ends8' - 'starts8'
		elsif label3$ == "p3"
			startp3 = Get start time of interval: 3, k
			endp3 = Get end time of interval: 3, k
			p3 = 'endp3' - 'startp3'
		endif
	endfor

	## duration name2 and utterance (tier1) ##
	select TextGrid 'name$'
	tier1 = Get number of intervals... 1
	tier1.1 = 'tier1' - 1

	for l from 2 to tier1.1
		select TextGrid 'name$'
		label1$ = Get label of interval: 1, l

		if label1$ == "name2"
			startn2 = Get start time of interval: 1, l
			endn2 = Get end time of interval: 1, l
			n2 = 'endn2' - 'startn2'
			# duration of rest of name2 (without s8)
			rn2 = 'n2' - 's8'
		endif

		startutt = Get start time of interval: 1, 2
		endutt = Get end time of interval: 1, tier1.1
		utt = 'endutt' - 'startutt'	
		# duration of rest of utterance (without pause3)
		rutt = 'utt' - 'p3'	
	endfor

	select Table table
	Set numeric value: i, "h2orig", 'h2:3'
	Set numeric value: i, "l2orig", 'l2:3'
	Set numeric value: i, "s8orig", 's8:3'
	Set numeric value: i, "n2orig", 'n2:3'
	Set numeric value: i, "p3orig", 'p3:3'
	Set numeric value: i, "uttorig", 'utt:3'

## Calculate new values ##

	if condition$ == "bra"

		# new value of f0-range
		h2newMax = 2^(maxrangeBra/12) * l2
		h2newMin = 2^(minrangeBra/12) * l2

		# new value of s8
		s8newMax = (maxlengthBra/rn2MaxBra) * rn2
		# factor for lengthening of s8
		facs8newMax = s8newMax/s8
		s8newMin = (minlengthBra/rn2MinBra) * rn2
		facs8newMin = s8newMin/s8
		# new values for duration of name2
		n2Max = rn2 + s8newMax
		n2Min = rn2 + s8newMin

		# new value of p3
		# duration of utterance without pause, considering new values of s8
		ruttMax = rutt - s8 + s8newMax - p3
		ruttMin = rutt - s8 + s8newMin - p3
		# all cues to max
		p3newMax = (maxpauseBra/ruttMaxBra) * ruttMax
		# factor for lengthening of the pause
		facp3newMax = p3newMax/p3
		# all cues to min
		p3newMin = (minpauseBra/ruttMinBra) * ruttMin
		facp3newMin = p3newMin/p3
		# final lengthening to max, pause duration to min (maxL)
		p3newMaxL = (minpauseBra/ruttMinBra) * ruttMax
		facp3newMaxL = p3newMaxL/p3
		# new values for duration of the utterance
		uttMax = ruttMax + p3newMax
		uttMin = ruttMin + p3newMin
		uttLMax = ruttMax + p3newMaxL

		# compute difference values
		diffs8 = s8newMax - s8newMin
		diffp3 = p3newMax - p3newMin
		diffutt = uttMax - uttMin

		select Table table
		Set numeric value: i, "h2max", 'h2newMax:3'
		Set numeric value: i, "h2min", 'h2newMin:3'
		Set numeric value: i, "s8max", 's8newMax:3'
		Set numeric value: i, "s8min", 's8newMin:3'
		Set numeric value: i, "n2max", 'n2Max:3'
		Set numeric value: i, "n2min", 'n2Min:3'
		Set numeric value: i, "p3max", 'p3newMax:3'
		Set numeric value: i, "p3min", 'p3newMin:3'
		Set numeric value: i, "p3Lmax", 'p3newMaxL:3'
		Set numeric value: i, "uttmax", 'uttMax:3'
		Set numeric value: i, "uttmin", 'uttMin:3'
		Set numeric value: i, "uttLmax", 'uttLMax:3'
		Set numeric value: i, "diffs8", 'diffs8:2'
		Set numeric value: i, "diffp3", 'diffp3:2'
		Set numeric value: i, "diffutt", 'diffutt:2'

	elsif condition$ == "nob"

		# new value of f0-range
		h2newMax = 2^(maxrangeNob/12) * l2
		h2newMin = 2^(minrangeNob/12) * l2

		# new value of s8
		s8newMax = (maxlengthNob/rn2MaxNob) * rn2
		# factor for lengthening of s8
		facs8newMax = s8newMax/s8
		s8newMin = (minlengthNob/rn2MinNob) * rn2
		facs8newMin = s8newMin/s8
		# new values for duration of name2
		n2Max = rn2 + s8newMax
		n2Min = rn2 + s8newMin

		# new value of p3
		# duration of utterance without pause, considering new values of s8
		ruttMax = rutt - s8 + s8newMax - p3
		ruttMin = rutt - s8 + s8newMin - p3
		#p3newMax = (maxpauseNob/ruttMaxNob) * ruttMax
		# factor for lengthening of the pause
		#facp3newMax = p3newMax/p3
		p3newMin = (minpauseNob/ruttMinNob) * ruttMin
		facp3newMin = p3newMin/p3
		# new values for duration of the utterance
		uttMax = ruttMax + p3newMin
		uttMin = ruttMin + p3newMin

		# compute difference values
		diffs8 = s8newMax - s8newMin
		#diffp3 = p3newMax - p3newMin
		diffutt = uttMax - uttMin

		select Table table
		Set numeric value: i, "h2max", 'h2newMax:3'
		Set numeric value: i, "h2min", 'h2newMin:3'
		Set numeric value: i, "s8max", 's8newMax:3'
		Set numeric value: i, "s8min", 's8newMin:3'
		Set numeric value: i, "n2max", 'n2Max:3'
		Set numeric value: i, "n2min", 'n2Min:3'
		Set string value: i, "p3max", "NA"
		Set numeric value: i, "p3min", 'p3newMin:3'
		Set string value: i, "p3Lmax", "NA"
		Set numeric value: i, "uttmax", 'uttMax:3'
		Set numeric value: i, "uttmin", 'uttMin:3'
		Set string value: i, "uttLmax", "NA"
		Set numeric value: i, "diffs8", 'diffs8:2'
		Set numeric value: i, "diffp3", 0
		Set numeric value: i, "diffutt", 'diffutt:2'

	endif
	

#printline 'name$' condition: 'condition$'; new h2 max: 'h2newMax:2' min: 'h2newMin:2'; s8 max: 's8newMax:3' min: 's8newMin:3'; p3 max: 'p3newMax:3' min: 'p3newMin:3'
#printline 'name$' condition: 'condition$'; orig h2 old: 'h2:2' l2: 'l2:2'; s8 old: 's8:3' n2: 'n2:3'; p3 old: 'p3:3' utt: 'utt:3'


##################
## Manipulation ##
##################

#########################################################################
## All 3 cues Min ##
	select Sound 'name$'
	To Manipulation: 0.01, 75, 600
	Edit
	editor Manipulation 'name$'

## pitch ##
	# delete all pitchpoints in name2 to the right of L2
	# put a new pitch point with the new value for H2 at 80% of the final vowel
	# variable for deleting pitch points next to L2
	l2tpp = 'l2t' + 0.005
	# variable for positioning H2
	nh = s8/10*2
	posh2new = ends8 - nh
	Select: 'l2tpp', 'ends8'
	Remove pitch point(s)
	Add pitch point at: 'posh2new', 'h2newMin'
	pause delete unwanted pitch points

## duration s8 ##
	# duration points at the start and end points of s8 
	# and then two additional points with the factor of lengthening or shortening
	# within ten percent of the duration of s8
	# the four points should build a trapezium
	dps8 = s8/10
	innerstarts8 = starts8 + dps8
	innerends8 = ends8 - dps8
	Add duration point at: 'starts8', 1
	Add duration point at: 'ends8', 1
	Add duration point at: 'innerstarts8', 'facs8newMin'
	Add duration point at: 'innerends8', 'facs8newMin'

	if condition$ == "nob" and p3 == 0
	# if there is no pause in the nob condition, then nothing needs to be manipulated.
	# for the nobs with pause, this will be deleted.

	else
	## duration of pause ##
		# duration points at the start and end points of p3 
		# and then two additional points with the factor of lengthening or shortening
		# within ten percent of the duration of p3
		# the four points should build a trapezium
	
		dpp3 = p3/10
		innerstartp3 = startp3 + dpp3
		innerendp3 = endp3 - dpp3
		Add duration point at: 'startp3', 1
		Add duration point at: 'endp3', 1
		Add duration point at: 'innerstartp3', 'facp3newMin'
		Add duration point at: 'innerendp3', 'facp3newMin'
	endif
pause in Min
	
	Publish resynthesis
	Close
	name_new$ = name$ + "_min3"
	Rename: "'name_new$'"
	Save as WAV file... 'dir$''name_new$'.wav

#########################################################################
## Length and f0-Range Max, Pause Min ##
	select Manipulation 'name$'
	Edit
	editor Manipulation 'name$'

## pitch ##
	# delete all pitchpoints in name2 to the right of L2
	# put a new pitch point with the new value for H2 at 80% of the final vowel
	Select: 'l2tpp', 'ends8'
	Remove pitch point(s)
	Add pitch point at: 'posh2new', 'h2newMax'

## duration s8 ##
	# duration points at the start and end points of s8 are already set 
	# delete two additional points and set with new values
	Select: 'innerstarts8', 'innerends8'
	Remove duration point(s)
	Add duration point at: 'innerstarts8', 'facs8newMax'
	Add duration point at: 'innerends8', 'facs8newMax'

## duration of pause ##
	# pause is still set to min value for max lengthening

pause now in Length and f0-range Max

	Publish resynthesis
	Close
	name_new$ = name$ + "_maxLR"
	Rename: "'name_new$'"
	Save as WAV file... 'dir$''name_new$'.wav

if condition$ == "bra"

#########################################################################
## All 3 cues Max ##
	select Manipulation 'name$'
	Edit
	editor Manipulation 'name$'

## pitch ##
	# is still set to Max

## duration s8 ##
	# ist still set to Max

## duration of pause ##
	# duration points at the start and end points of p3 
	# and then two additional points with the factor of lengthening or shortening
	# within ten percent of the duration of p3
	# the four points should build a trapezium
	Select: 'innerstartp3', 'innerendp3'
	Remove duration point(s)
	Add duration point at: 'innerstartp3', 'facp3newMax'
	Add duration point at: 'innerendp3', 'facp3newMax'
pause now in Max Bra
	
	Publish resynthesis
	Close
	name_new$ = name$ + "_max3"
	Rename: "'name_new$'"
	Save as WAV file... 'dir$''name_new$'.wav

#########################################################################
## f0-Range Max, Pause3 and Length Min ##
	select Manipulation 'name$'
	Edit
	editor Manipulation 'name$'

## pitch ##
	# is still set from before to Max
	
## duration s8 ##
	# duration points at the start and end points of s8 are already set 
	# delete the two additional points and set with new values
	Select: 'innerstarts8', 'innerends8'
	Remove duration point(s)
	Add duration point at: 'innerstarts8', 'facs8newMin'
	Add duration point at: 'innerends8', 'facs8newMin'

## duration of pause ##
	# duration points at the start and end points of p3 are already set 
	# delete the two additional points and set new values
	Select: 'innerstartp3', 'innerendp3'
	Remove duration point(s)
	Add duration point at: 'innerstartp3', 'facp3newMin'
	Add duration point at: 'innerendp3', 'facp3newMin'
pause now in Range Max	

	Publish resynthesis
	Close
	name_new$ = name$ + "_maxR"
	Rename: "'name_new$'"
	Save as WAV file... 'dir$''name_new$'.wav

#########################################################################
## Length s8 Max, Pause3 and f0-Range Min ##
	select Manipulation 'name$'
	Edit
	editor Manipulation 'name$'

## pitch ##
	# delete all pitchpoints in name2 to the right of L2
	# put a new pitch point with the new value for H2 at 80% of the final vowel, which is lengthened
	Select: 'l2tpp', 'ends8'
	Remove pitch point(s)
	Add pitch point at: 'posh2new', 'h2newMin'

## duration s8 ##
	# duration points at the start and end points of s8 are already set 
	# delete the two additional points and set with new values
	Select: 'innerstarts8', 'innerends8'
	Remove duration point(s)
	Add duration point at: 'innerstarts8', 'facs8newMax'
	Add duration point at: 'innerends8', 'facs8newMax'

## duration of pause ##
	# needs to be adjusted, because the duration of the whole utterance is manipulated by lengthening s8
	# duration points at the start and end points of p3 are already set
	# delete the two additional points and set new values
	Select: 'innerstartp3', 'innerendp3'
	Remove duration point(s)
	Add duration point at: 'innerstartp3', 'facp3newMaxL'
	Add duration point at: 'innerendp3', 'facp3newMaxL'

pause now in Length Max
	
	Publish resynthesis
	Close
	name_new$ = name$ + "_maxL"
	Rename: "'name_new$'"
	Save as WAV file... 'dir$''name_new$'.wav

endif
endfor

select Table table
Save as tab-separated file... 'dir$'_values_manipulation2018_12_05.txt

select all
minus Strings list
Remove

