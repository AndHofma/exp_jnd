######################
## Description data ##
######################

# textgrid has 5 interval tiers / 1 point tier #
# tier1: word (interval)#
# tier2: syll  (interval)#
# tier3: seg (interval)#
# tier4: glott (interval)#
# tier6: comments (interval)#
# tier5: f0 (point)#

################
## Setup data ##
################

## directories ##
# specify the directory from which you want to access the wav and textgrid files
d$ = "C:\Users\Andrea Hofmann\OneDrive\PhD\phd_perception_production_link\dissertation\procedure_all\exp_jnd\stimuli_to-be-manipulated\FL\cut_name2\ch\"
# directory for saving the manipulated files
dir$ = "C:\Users\Andrea Hofmann\OneDrive\PhD\phd_perception_production_link\dissertation\procedure_all\exp_jnd\stimuli_manipulated\audio-FL\wav_plus_textgrid\ch\"

# opens the wav-files from a file
Create Strings as file list... list 'd$'*.wav

# query number of objects in the stringslist and store in variable n
n = Get number of strings
printline number of strings: 'n'

# for-loop, goes through each object in the list
for i from 1 to n
	select Strings list
	filename$ = Get string... 'i'
	Read from file... 'd$''filename$'
	# store basename in variable name
	name$ = selected$ ("Sound")
	Read from file... 'd$''name$'.TextGrid

#############################################
## Read out information from original file ##
#############################################

    ## duration s8 (tier3) ##
    select TextGrid 'name$'
    tier3 = Get number of intervals... 3

    for k from 1 to tier3
        select TextGrid 'name$'
        label3$ = Get label of interval: 3, k

        if label3$ == "s5"
            starts5 = Get start time of interval: 3, k
            ends5 = Get end time of interval: 3, k
            s5 = 'ends5' - 'starts5'
        elsif label3$ == "s6"
            starts6 = Get start time of interval: 3, k
            ends6 = Get end time of interval: 3, k
            s6 = 'ends6' - 'starts6'
        elsif label3$ == "s7"
            starts7 = Get start time of interval: 3, k
            ends7 = Get end time of interval: 3, k
            s7 = 'ends7' - 'starts7'
        elsif label3$ == "s8"
           starts8 = Get start time of interval: 3, k
           ends8 = Get end time of interval: 3, k
           s8 = 'ends8' - 'starts8'
        endif
    endfor

    ## duration name2 (tier1) ##
    select TextGrid 'name$'
    tier1 = Get number of intervals... 1

    for l from 1 to tier1
        select TextGrid 'name$'
        label1$ = Get label of interval: 1, l

        if label1$ == "name2"
            startn2 = Get start time of interval: 1, l
            endn2 = Get end time of interval: 1, l
            tname = Get starting point: 1, l
            n2 = 'endn2' - 'startn2'
            # duration of rest of name2 (without s8)
			rn2 = 'n2' - 's8'
			s6reln2 = ('s6' * 100) / 'n2'
			s8reln2 = ('s8' * 100) / 'n2'
        endif
    endfor

    ############################################
    ## Calculate values to setup manipulation ##
    ############################################

    ## final lengthening - FL ##
    # min dur s8 - to end up with 1st and 2nd syll having same duration = no lengthening
    s8MinDur = s5 + s6 - s7
    n2Min = s5 + s6 + s7 + s8MinDur
    s8MinFL = ('s8MinDur' * 100) / 'n2Min'
	# s8MinFL = (s6reln2/(100-s6reln2)) * rn2
	# amount of 1ms steps to get from origFL to minFL
    # round to integer - get rid of decimal places
    stepsFL = round((s8-s8MinDur) / 0.001)

    ################
    ## Data Table ##
    ################
    Create Table with column names: "table", stepsFL+1, "stepID filename nameNew s8Orig s8MinDur s8MinFL shortFC s8New diffS8 n2Orig n2Min n2New flOrig flNew diffFL diffSyllDur"

    ##################
    ## Manipulation ##
    ##################

    ## final lengthening - FL continuum ##
    for x from 1 to stepsFL+1

        select Sound 'name$'
        To Manipulation: 0.01, 75, 600
        Edit
        editor Manipulation 'name$'

        # get new factor for shortening of s8 for each step
        s8Manip = s8 - ((x-1) * 0.001)
        s8ManipFac = s8MinDur/s8Manip
        ends8Manip = 'ends8' - ((x-1) * 0.001)

        # duration points at the start and end points of s8
        # and then two additional points with the factor of lengthening or shortening
        # within ten percent of the duration of s8
        # the four points should build a trapezium
        innerstarts8 = starts8 + (s8Manip/100)
        innerends8 = ends8Manip - (s8Manip/100)
        Add duration point at: 'starts8', 1
        Add duration point at: 'ends8Manip', 1
        Add duration point at: 'innerstarts8', 's8ManipFac'
        Add duration point at: 'innerends8', 's8ManipFac'

        Publish resynthesis
        Close

        ## values for table and naming
        # new s8 duration for each step
        n2New = Get duration
        diff = 'n2' - 'n2New'
        s8New = 's8' - 'diff'
        # difference in s8 duration for each step
        diffs8 = 's8' - 's8New'
        # difference in syllable lengths (1st and 2nd)
        # this value will be relevant to find correct stimulus later in JND script
        diffSyllDur = (s8New + s7) - (s5 + s6)
        currDiff$ = fixed$ (diffSyllDur, 3)
        # new relative FL for each step
        flNew = (s8New * 100) / 'n2New'
        # difference in relative FL for each step
        diffFL = 's8reln2' - 'flNew'

        name_new$ = name$ + "_FL_" + currDiff$
        Rename: "'name_new$'"
        Save as WAV file... 'dir$''name_new$'.wav

        select Table table
        Set numeric value: x, "stepID", 'x:1'
        Set string value: x, "filename", name$
        Set string value: x, "nameNew", name_new$
        Set numeric value: x, "s8Orig", 's8:3'
        Set numeric value: x, "s8MinDur", 's8MinDur:3'
        Set numeric value: x, "s8MinFL", 's8MinFL:3'
        Set numeric value: x, "shortFC", 's8ManipFac:3'
        Set numeric value: x, "s8New", 's8New:3'
        Set numeric value: x, "diffS8", 'diffs8:3'
        Set numeric value: x, "n2Orig", 'n2:3'
        Set numeric value: x, "n2Min", 'n2Min:3'
        Set numeric value: x, "n2New", 'n2New:3'
        Set numeric value: x, "flOrig", 's8reln2:3'
        Set numeric value: x, "flNew", 'flNew:3'
        Set numeric value: x, "diffFL", 'diffFL:3'
        Set numeric value: x, "diffSyllDur", 'diffSyllDur:3'
    endfor

    select Table table
    table_name$ = "manipulation_FL_" + name$
    Save as tab-separated file... 'dir$' 'table_name$'.csv

endfor

#########################################
## Generate TextGrid for each wav file ##
#########################################

# opens the wav-files from a file
Create Strings as file list... list 'd$'*.wav

# query number of objects in the stringslist and store in variable n
n = Get number of strings
printline number of strings: 'n'

# for-loop, goes through each object in the list
for i from 1 to n
	select Strings list
	filename$ = Get string... 'i'
	Read from file... 'd$''filename$'
	# store basename in variable name
	name$ = selected$ ("Sound")
	Read from file... 'd$''name$'.TextGrid

#############################################
## Read out information from original file ##
#############################################

    ## duration s8 (tier3) ##
    select TextGrid 'name$'
    tier3 = Get number of intervals... 3

    for k from 1 to tier3
        select TextGrid 'name$'
        label3$ = Get label of interval: 3, k

        if label3$ =="s7"
            # this is the boundary between 1st and 2nd syll used later in new TextGrids
            tsyll = Get starting point: 3, k
        endif
    endfor

    # opens the wav-files from a file
    Create Strings as file list... list 'dir$'*.wav
    # Anzahl der Objekte in der Stringliste erfragen und in Variable q speichern
    q = Get number of strings

    # for-Schleife, die durch jedes Objekt in der Liste geht
    for i from 1 to q
        select Strings list
        filename$ = Get string... 'i'
        Read from file... 'dir$''filename$'
        # store basename in Variable name
        name$ = selected$ ("Sound")
        # query information on condition
        select Sound 'name$'
        # subtract last four elements (.wav)
        length = length (name$)
        partName$ = left$(name$,length)
        # create a TextGrid
        # name all tiers in the first quotation marks
        # repeat those tiers that should be point tiers in the second quotation marks
        # To TextGrid... "Word Syllable", ""
        To TextGrid: "Word Syllable", ""

        Insert boundary: 2, 'tsyll'

        Set interval text: 1, 1, "name2_'partName$'"
        Set interval text: 2, 1, "n2sy1_'partName$'"
        Set interval text: 2, 2, "n2sy2_'partName$'"

        select TextGrid 'name$'
        # Save TextGrid as text file... 'dir$''name$'.TextGrid
        Save as text file... 'dir$''name$'.TextGrid

        select all
        minus Strings list
        Remove
    endfor

endfor

select all
Remove