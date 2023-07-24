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
d$ = "C:\Users\Andrea Hofmann\OneDrive\PhD\phd_perception_production_link\dissertation\procedure_all\exp_jnd\stimuli_to-be-manipulated\pause\cut_name2_name3\ch\"

# directory for saving the manipulated files
dir$ = "C:\Users\Andrea Hofmann\OneDrive\PhD\phd_perception_production_link\dissertation\procedure_all\exp_jnd\stimuli_manipulated\audio-pause\wav_plus_textgrid\ch\"

# opens the wav-files from a file
Create Strings as file list... list1 'd$'*.wav

# query number of objects in the stringslist and store in variable n
n = Get number of strings

# for-loop, goes through each object in the list
for i from 1 to n
	select Strings list1
	filename$ = Get string... 'i'
	Read from file... 'd$''filename$'
	# store basename in variable name
	name$ = selected$ ("Sound")
	Read from file... 'd$''name$'.TextGrid

    #############################################
    ## Read out information from original file ##
    #############################################

    ## duration name sequence - name2 und2 pause3 name3 (tier1) ##
    select TextGrid 'name$'
    uttDur = Get duration
    tier1 = Get number of intervals... 1

    for l from 1 to tier1
        select TextGrid 'name$'
        label1$ = Get label of interval: 1, l

        if label1$ == "name2"
            startn2 = Get start time of interval: 1, l
        elsif label1$ == "name3"
            endn3 = Get end time of interval: 1, l
        endif
    endfor

    ## duration p3 (tier3) ##
    select TextGrid 'name$'
    tier3 = Get number of intervals... 3

    for k from 1 to tier3
        select TextGrid 'name$'
        label3$ = Get label of interval: 3, k

        if label3$ =="s7"
            # this is the boundary between 1st and 2nd syll of name2
            tsyll1n2 = Get starting point: 3, k
        elsif label3$ =="s8"
            # this is the boundary at the end of name2
            tn2 = Get end point: 3, k
        elsif label3$ == "p3"
            startp3 = Get start time of interval: 3, k
            endp3 = Get end time of interval: 3, k
            p3 = 'endp3' - 'startp3'
        elsif label3$ =="c2"
            # this is the boundary at the beginning of und2
            tc2start = Get starting point: 3, k
            # this is the boundary at the end of und2 / beginning of name3
            tc2end = Get end point: 3, k
            # calculate duration of c2
            c2 = 'tc2end' - 'tc2start'
        elsif label3$ =="s9"
            # this is the beginning of name3
            tn3start = Get starting point: 3, k
        elsif label3$ =="s11"
            # this is the boundary between 1st and 2nd syll of name3
            tsyll1n3 = Get starting point: 3, k
            # calculate duration of 1st syll of name3
            syll1n3 = 'tsyll1n3' - 'tc2end'
        elsif label3$ =="s12"
            # this is the end of name3
            tn3end = Get end point: 3, k
            # calculate duration of 2nd syll of name3
            syll2n3 = 'tn3end' - 'tsyll1n3'
        endif
    endfor

    ############################################
    ## Calculate values to setup manipulation ##
    ############################################

    ## pause ##
    # min pause dur = 0.005 bc 0 would not work well
    p3Min = 0.005
	# amount of 5ms steps to get from p3 to p3Min
    # round to integer - get rid of decimal places
    stepsPause = round(p3 / 0.005)

    ################
    ## Data Table ##
    ################
    Create Table with column names: "table", stepsPause, "stepID filename nameNew p3Orig p3Min shortFC p3New diffp3 uttDurOrig uttDurMin uttDurNew"

    ##################
    ## Manipulation ##
    ##################

    ## pause continuum ##
    for x from 1 to stepsPause

        select Sound 'name$'
        To Manipulation: 0.01, 75, 600
        Edit
        editor Manipulation 'name$'

        # get new factor for shortening of pause for each step
        p3Manip = p3 - ((x-1) * 0.005)
        p3ManipFac = p3Min / p3Manip
        endp3Manip = 'endp3' - ((x-1) * 0.005)

        # duration points at the start and end points of s8
        # and then two additional points with the factor of lengthening or shortening
        # within ten percent of the duration of s8
        # the four points should build a trapezium
        innerstartp3 = startp3 + 0.000001
        innerendp3 = endp3Manip - 0.000001
        Add duration point at: 'startp3', 1
        Add duration point at: 'endp3Manip', 1
        Add duration point at: 'innerstartp3', 'p3ManipFac'
        Add duration point at: 'innerendp3', 'p3ManipFac'

        # min utterance duration
        uttDurMin = 'uttDur' - 'p3'

        Publish resynthesis
        Close

        ## values for table and naming
        # new p3 duration for each step
        durSound = Get duration
        diffp3 = 'uttDur' - 'durSound'
        p3New = 'p3Min' + ((x-1) * 0.005)
        currp3$ = fixed$ (p3New, 3)

        name_new$ = name$ + "_pause_" + currp3$
        Rename: "'name_new$'"
        Save as WAV file... 'dir$''name_new$'.wav

        select Table table
        Set numeric value: x, "stepID", 'x:1'
        Set string value: x, "filename", name$
        Set string value: x, "nameNew", name_new$
        Set numeric value: x, "p3Orig", 'p3:4'
        Set numeric value: x, "p3Min", 'p3Min:4'
        Set numeric value: x, "shortFC", 'p3ManipFac:4'
        Set numeric value: x, "p3New", 'p3New:3'
        Set numeric value: x, "diffp3", 'diffp3:3'
        Set numeric value: x, "uttDurOrig", 'uttDur:4'
        Set numeric value: x, "uttDurMin", 'uttDurMin:4'
        Set numeric value: x, "uttDurNew", 'durSound:4'
    endfor

    select Table table
    table_name$ = "manipulation_pause_" + name$
    Save as tab-separated file... 'dir$' 'table_name$'.csv

    #########################################
    ## Generate TextGrid for each wav file ##
    #########################################

    # opens the wav-files from a file
    Create Strings as file list... list 'dir$'*.wav
    # Anzahl der Objekte in der Stringliste erfragen und in Variable q speichern
    q = Get number of strings

    # for-Schleife, die durch jedes Objekt in der Liste geht
    for t from 1 to q
        select Strings list
        filename1$ = Get string... 't'
        Read from file... 'dir$''filename1$'
        # store basename in Variable name
        name1$ = selected$ ("Sound")
        # query information on condition
        select Sound 'name1$'
        # subtract last four elements (.wav)
        length = length (name1$)
        partName$ = left$(name1$,length)
        durSound = Get duration

        # boundaries dependent on pause duration manipulation
        n3Start = 'durSound' - 'syll1n3' - 'syll2n3'
        c2Start = 'n3Start' - 'c2'
        syll1n3End = 'durSound' - 'syll2n3'

        # create a TextGrid
        # name all tiers in the first quotation marks
        # repeat those tiers that should be point tiers in the second quotation marks
        To TextGrid: "Word Syllable", ""

        Insert boundary: 1, 'tn2'
        Insert boundary: 1, 'c2Start'
        Insert boundary: 1, 'n3Start'
        Insert boundary: 2, 'tsyll1n2'
        Insert boundary: 2, 'tn2'
        Insert boundary: 2, 'c2Start'
        Insert boundary: 2, 'n3Start'
        Insert boundary: 2, 'syll1n3End'
        Set interval text: 1, 1, "name2_'partName$'"
        Set interval text: 1, 2, "pause3_'partName$'"
        Set interval text: 1, 3, "und2_'partName$'"
        Set interval text: 1, 4, "name3_'partName$'"
        Set interval text: 2, 1, "n2sy1_'partName$'"
        Set interval text: 2, 2, "n2sy2_'partName$'"
        Set interval text: 2, 3, "p3_'partName$'"
        Set interval text: 2, 4, "c2_'partName$'"
        Set interval text: 2, 5, "n3sy1_'partName$'"
        Set interval text: 2, 6, "n3sy2_'partName$'"

        select TextGrid 'name1$'
        Save as text file... 'dir$''name1$'.TextGrid
    endfor

endfor

select all
Remove