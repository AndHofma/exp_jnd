###########################################
#
# Script to Extract Information for Analysis
# taken from Experiment 1 Coordinates
# adapted for Stimuli for Perception 20-11-18
# analysis_stim_ch.praat
# 
# SFB1287, Project B01
#
# 26-2-18, written by Clara Huttenlauch
# modified 28-06-18
# modified 05-07-18
# modified 26-07-18
#
# script extracts durational and f0 measurements from TextGrids
# script calculates several variables
#
# the following tiers exist:
# tier 1, interval: word(s) (contains only labels: name1, und1, name2, und2, name3, pause1-4)
# tier 2, interval: syll(ables)
# tier 3, interval: seg(ments)
# tier 4, interval: word2/glott annotation of glottalised speech in the region of names1 and 2 and und1 and 2, annotated "glott"
# tier 5, point: f0 (min and max f0 on each name)
# tier 6, interval: comments
#
# annotation:
# tier 5, L(ow)1 and H(igh)1 an name1, L2 and H2 on name2
# in most cases: L followed by H, sometimes H before L
#
# analysis:
# f0-movement in semitones on name1 and name2: rise1 and rise2
# direction of f0-movement: f0n1 and f0n2 (rise or fall)
# slope of the rising movement on name2; slopen2
#
# duration is in ms
# s1dur = duration of segment 1
# c1dur	= duration of coordination 1
# p1dur = duration of pause 1
# pause1 und1 pause2, pause3 und2 pause4
# duration of name1+pause1 (n1p1dur) and name2+pause3 (n2p3dur)
#
# duration of segments 1-4 and 5-8 relative to the duration of name1 and name2, respectively (in percent)
# s1reln1, s2reln1, s3reln1, s4reln1, and s5reln2, s6reln2, s7reln2, s8reln2
# duration of syllables 1 and 2 of name1 and of syllables 1 and 2 of name2 relative to the duration of name1 and name2, respectively
# syll1reln1, syll2reln1, syll1reln2, syll2reln2
# duration of pause3
# duration of pause3 relative to utterance duration (without hesitations)
#
# duration of the whole utterance in milliseconds
# duration of constituent 1 (name1 + und1 + name2) = cons1dur
# duration of constituent 2 (und2 + name3) = cons2dur
#
## diffs4 = difference between the last segment of the first name across one condition
# within the same speaker / participantID and one context (i.e. C01): s4dur(bra) - s4dur(nob)
#
# formant values for F1 and F2 in the last vowel of name1 and name2
# F1s4 = F1 of segment 4 (last segment of name1)
#
#
###########################################

clearinfo

# specify the directory from which you want to access the soundfiles
d$ = "C:\Users\Andrea Hofmann\OneDrive\PhD\phd_perception_production_link\dissertation\procedure_all\exp_jnd\stimuli_exp8_ch\"

# opens the wav-files from a file
Create Strings as file list... list 'd$'*.wav


# query number of objects in the stringslist and store in variable n
n = Get number of strings
printline number of strings: 'n'

# create Table for data
Create Table with column names: "table", n, "filename participantID context block trial condition L1 L1t H1 H1t rise1 f0n1 slopen1 L2 L2t H2 H2t rise2 f0n2 slopen2 s1dur s1reln1 s2dur s2reln1 s3dur s3reln1 s4dur s4reln1 s4glott syll1reln1 syll2reln1 s5dur s5reln2 s6dur s6reln2 s7dur s7reln2 s8dur s8reln2 s8glott syll1reln2 syll2reln2 s9dur s10dur s11dur s12dur p1dur n1p1dur p2dur p3dur p3relutt n2p3dur p4dur c1dur c2dur cons1dur cons2dur cons1u2 utt_dur(ms) hes comments"


# for-loop, goes through each object in the list
for i from 1 to n
	select Strings list
	filename$ = Get string... 'i'
	Read from file... 'd$''filename$'
	# store basename in variable name
	name$ = selected$ ("Sound")
	Read from file... 'd$''name$'.wav

	# query information about participantID, context, condition, item/name2 in soundname
	select Sound 'name$'
	participantID$ = left$(name$,2)
	context$ = mid$(name$,4,3)
	block$ = mid$(name$,8,2)
	trial$ = mid$(name$,11,3)
	condition$ = right$(name$,3)
	item$ = mid$(name$,8,5)
	# filename without the condition and without information about trialnumber
	item1.2$ = left$ (name$,10)
	item2$ = item1.2$ + item$

	select Table table
	Set string value: i, "filename", name$

	Set string value: i, "participantID", participantID$
	Set string value: i, "context", context$
	Set string value: i, "block", block$
	Set string value: i, "trial", trial$
	Set string value: i, "condition", condition$
#	Set string value: i, "name1", name1$
#	Set string value: i, "name2", item$
#	Set string value: i, "item2", item2$

	select Sound 'name$'
	# read in the corresponding TextGrid
	Read from file... 'd$''name$'.TextGrid

############## F0 ################
	
	select Sound 'name$'
	To Pitch: 0, 75, 600

# all values to 0
l1t = 0
l1 = 0
h1t = 0
h1 = 0
l2t = 0
l2 = 0
h2t = 0
h2 = 0
	
	select TextGrid 'name$'
	tier5 = Get number of points: 5
	for j from 1 to tier5
		select TextGrid 'name$'
		p$ = Get label of point: 5, j
		t = Get time of point: 5, j

		if p$ == "L1"
			l1t = t
			select Pitch 'name$'
			l1 = Get value at time: l1t, "Hertz", "Linear"
		elsif p$ == "H1"
			h1t = t
			select Pitch 'name$'
			h1 = Get value at time: h1t, "Hertz", "Linear"
		elsif p$ = "L2"
			l2t = t
			select Pitch 'name$'
			l2 = Get value at time: l2t, "Hertz", "Linear"
		elsif p$ = "H2"
			h2t = t
			select Pitch 'name$'
			h2 = Get value at time: h2t, "Hertz", "Linear"
		else
			printline check point 'p$', it's whether L1, L2 nor H1, H2 in 'name$'
		endif

	endfor
	
	# calculate rise1 and rise2 (in semitones)
	rise1 = 12*log2(h1/l1)
	rise2 = 12*log2(h2/l2)

	# calculate slope of rise1 and rise2
	# time between l1 and h1
	lhn1 = 'h1t' - 'l1t'
	slopen1 = 'rise1' / 'lhn1'

	#time between l2 and h2
	lhn2 = 'h2t' - 'l2t'
	slopen2 = 'rise2' / 'lhn2'

	select Table table
	Set numeric value: i, "L1", 'l1:2'
	Set numeric value: i, "L1t", 'l1t:2'
	Set numeric value: i, "H1", 'h1:2'
	Set numeric value: i, "H1t", 'h1t:2'
	Set numeric value: i, "rise1", 'rise1:2'
	Set numeric value: i, "slopen1", 'slopen1:3'
	Set numeric value: i, "L2", 'l2:2'
	Set numeric value: i, "L2t", 'l2t:2'
	Set numeric value: i, "H2", 'h2:2'
	Set numeric value: i, "H2t", 'h2t:2'
	Set numeric value: i, "rise2", 'rise2:2'
	Set numeric value: i, "slopen2", 'slopen2:3'

	# check whether f0 high is before or after f0 low
	# add "rise" or "fall" to table
	if h1t < l1t
		Set string value: i, "f0n1", "fall"
	elsif h1t > l1t
		Set string value: i, "f0n1", "rise"
	endif

	if h2t < l2t
		Set string value: i, "f0n2", "fall"
	elsif h2t > l2t
		Set string value: i, "f0n2", "rise"
	endif
		
############## Segment duration ################
# duration in milliseconds

p1dur = 0
p3dur = 0

	select TextGrid 'name$'
	tier3 = Get number of intervals... 3
	tier3.1 = 'tier3' - 1

	m = 1
	o = 1
	for k from 2 to tier3.1
		select TextGrid 'name$'
		label3$ = Get label of interval: 3, k

		# segments
		if label3$ == "s'm'"

			start = Get start time of interval: 3, k
			end = Get end time of interval: 3, k
			dur = ('end' - 'start') * 1000
			select Table table
			Set numeric value: i, "s'm'dur", 'dur:2'

			# save values in variables for measuring vowel quality
			# and for measuring duration of constituents
			if label3$ == "s1"
				s1start = start
				s1dur = dur
			elsif label3$ == "s2"
				s2dur = dur
			elsif label3$ == "s3"
				s3dur = dur
			elsif label3$ == "s4"
				s4start = start
				s4end = end
				s4dur = dur
			elsif label3$ == "s5"
				s5dur = dur
			elsif label3$ == "s6"
				s6dur = dur
			elsif label3$ == "s7"
				s7dur = dur
			elsif label3$ == "s8"
				s8start = start
				s8end = end
				s8dur = dur
			elsif label3$ == "s12"
				s12end = end
			endif
			

			m = 'm' + 1
		# pauses
		elsif label3$ == "p1" or label3$ == "p2" or label3$ == "p3" or label3$ == "p4"

			o$ = right$(label3$,1)
			start = Get start time of interval: 3, k
			end = Get end time of interval: 3, k
			dur = ('end' - 'start') * 1000
			select Table table
			Set numeric value: i, "p'o$'dur", 'dur:2'

		# save duration of pause3 for further calculations
			if label3$ == "p1"
				p1dur = dur
			elsif label3$ == "p3"
				p3dur = dur
			endif

		# "und"
		elsif label3$ == "c'o'"

			start = Get start time of interval: 3, k
			end = Get end time of interval: 3, k
			dur = ('end' - 'start') * 1000
			select Table table
			Set numeric value: i, "c'o'dur", 'dur:2'

			# save value for measuring duration of second constituent
			if label3$ == "c2"
				c2start = start
			endif

			o = 'o' + 1
		endif

	endfor

############## Relative duration of segments 1-4 and segments 5-8 ################
# duration of a segment relative to the duration of the whole name
# 0.5 means, that the segment lasts half of the whole name

# set p3dur to 0, for the case it does not exist
#p3dur = 0

# calculation of duration of syllables
syll1n1 = 's1dur' + 's2dur'
syll2n1 = 's3dur' + 's4dur'
syll1n2 = 's5dur' + 's6dur'
syll2n2 = 's7dur' + 's8dur'

	select TextGrid 'name$'
	tier1 = Get number of intervals... 1
	for p from 1 to tier1
		select TextGrid 'name$'
		label1$ = Get label of interval: 1, p

		# duration of segments 1-4 and syllables 1 and 2 of name1 relative to the duration of name1
		if label1$ == "name1"	
			n1start = Get start time of interval: 1, p
			n1end = Get end time of interval: 1, p
			n1dur = ('n1end' - 'n1start') * 1000
			
			s1reln1 = 's1dur' / 'n1dur' * 100
			s2reln1 = 's2dur' / 'n1dur' * 100 
			s3reln1 = 's3dur' / 'n1dur' * 100
			s4reln1 = 's4dur' / 'n1dur' * 100
			syll1reln1 = 'syll1n1' / 'n1dur' * 100
			syll2reln1 = 'syll2n1' / 'n1dur' * 100
			
			# duration name1 plus pause1
			n1p1dur = 'n1dur' + 'p1dur'

			select Table table
			Set numeric value: i, "s1reln1", 's1reln1:3'
			Set numeric value: i, "s2reln1", 's2reln1:3'
			Set numeric value: i, "s3reln1", 's3reln1:3'
			Set numeric value: i, "s4reln1", 's4reln1:3'
			Set numeric value: i, "syll1reln1", 'syll1reln1:3'
			Set numeric value: i, "syll2reln1", 'syll2reln1:3'
			Set numeric value: i, "n1p1dur", 'n1p1dur:3'

		# duration of segments 5-8 and syllables 1 and 2 of name2 relative to the duration of name2
		elsif label1$ == "name2"
			n2start = Get start time of interval: 1, p
			n2end = Get end time of interval: 1, p
			n2dur = ('n2end' - 'n2start') * 1000

			s5reln2 = 's5dur' / 'n2dur' * 100
			s6reln2 = 's6dur' / 'n2dur' * 100
			s7reln2 = 's7dur' / 'n2dur'	 * 100	
			s8reln2 = 's8dur' / 'n2dur' * 100
			syll1reln2 = 'syll1n2' / 'n2dur' * 100
			syll2reln2 = 'syll2n2' / 'n2dur' * 100

			# duration name2 plus pause3
			n2p3dur = 'n2dur' + 'p3dur'

			select Table table
			Set numeric value: i, "s5reln2", 's5reln2:3'
			Set numeric value: i, "s6reln2", 's6reln2:3'
			Set numeric value: i, "s7reln2", 's7reln2:3'
			Set numeric value: i, "s8reln2", 's8reln2:3'
			Set numeric value: i, "syll1reln2", 'syll1reln2:3'
			Set numeric value: i, "syll2reln2", 'syll2reln2:3'
			Set numeric value: i, "n2p3dur", 'n2p3dur:3'
		endif
	endfor
	

############## Speech rate ################
# duration of the utterance in milliseconds
	
	select TextGrid 'name$'
	tier3 = Get number of intervals... 3

	begin = Get end time of interval: 3, 1
	end = Get start time of interval: 3, tier3

	## query tier 6 for hesitations ("hes")
	## substract the duration of the hesitation from the utterance duration
	hes$ = "no"
	dhess = 0
	tier6 = Get number of intervals... 6
	tier6.1 = 'tier6' - 1
	for r from 2 to tier6.1
		label6$ = Get label of interval: 6, r

		if label6$ == "hes"
		# set hes$ variable to yes
		hes$ = "yes"
		start6 = Get start time of interval: 6, r
		end6 = Get end time of interval: 6, r
		dhess = ('end6' - 'start6') * 1000

		select Table table
		Set numeric value: i, "hes", 1
		select TextGrid 'name$'
		endif
	endfor

	utt_dur = ('end' - 'begin') * 1000 - 'dhess'

	# calculate duration of pause3 relative to utterance duration
	# in percent
	p3relutt = 'p3dur' / 'utt_dur' * 100
	
	select Table table
	Set numeric value: i, "utt_dur(ms)", 'utt_dur:2'
	Set numeric value: i, "p3relutt", 'p3relutt:3'

# duration of constituent 1 (name1 + und1 + name2)

	cons1dur = ('s8end' - 's1start') * 1000
	# check whether hesitation falls within the interval and substract in that case
	if hes$ == "yes"
		if start6 < s8end and end6 < s8end
			cons1dur = 'cons1dur' - 'dhess'
		endif
	endif
	Set numeric value: i, "cons1dur", 'cons1dur:2'

# duration of constituent 2 (und2 + name3)

	cons2dur = ('s12end' - 'c2start') * 1000
	# check whether hesitation falls within the interval and substract in that case
	if hes$ == "yes"
		if start6 > c2start and end6 > c2start
			cons2dur = 'cons2dur' - 'dhess'
		endif
	endif
	Set numeric value: i, "cons2dur", 'cons2dur:2'

# duration of both constituents without pause3

	cons1u2 = 'cons1dur' + 'cons2dur'
	Set numeric value: i, "cons1u2", 'cons1u2:2'
	#cons1u2p3 = 'cons1dur' + 'p3dur' + 'cons2dur'
	#Set numeric value: i, "cons1u2p3", 'cons1u2p3:2'


############## Comments ################
		
	comments$ = ""

	select TextGrid 'name$'
	# query the number of labelled intervals on tier 6
	filled = Count intervals where: 6, "matches (regex)", "\l"

	if filled > 0

		for s from 2 to tier6.1

			label6$ = Get label of interval: 6, s
			comments$ = comments$ + " " + label6$

		endfor
	endif

	select Table table
	if comments$ <> ""
		Set string value: i, "comments", comments$
	else 
		Set string value: i, "comments", "NA"
	endif

printline succesfully run 'name$'
endfor

dir$ = "C:\Users\Andrea Hofmann\OneDrive\PhD\phd_perception_production_link\dissertation\procedure_all\exp_jnd\"
select Table table
Save as tab-separated file... 'dir$'values_exp8_ch.csv


select all
minus Strings list
minus Table table
Remove







