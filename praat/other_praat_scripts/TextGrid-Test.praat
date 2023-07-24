################
## Setup data ##
################

## directories ##
# specify the directory from which you want to access the wav and textgrid files
d$ = "C:\Users\Andrea Hofmann\OneDrive\PhD\phd_perception_production_link\dissertation\procedure_all\exp_jnd\stimuli_to-be-manipulated\pause\cut_name2_name3\03\"
# directory for saving the manipulated files
dir$ = "C:\Users\Andrea Hofmann\OneDrive\PhD\phd_perception_production_link\dissertation\procedure_all\exp_jnd\stimuli_manipulated\audio-pause\"

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
            # this is the boundary between 1st and 2nd syll of name2
            tsyll1n2 = Get starting point: 3, k
        elsif label3$ =="s8"
            # this is the boundary at the end of name2
            tn2 = Get end point: 3, k
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

    # opens the wav-files from a file
    Create Strings as file list... list 'dir$'*.wav
    # Anzahl der Objekte in der Stringliste erfragen und in Variable q speichern
    q = Get number of strings

    Create Table with column names: "table", q, "nrFiles name length partName durSound n3Start c2Start syll1n3End p3"

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
        durSound = Get duration

        # boundaries dependent on pause duration manipulation
        n3Start = 'durSound' - 'syll1n3' - 'syll2n3'
        c2Start = 'n3Start' - 'c2'
        syll1n3End = 'durSound' - 'syll2n3'
        p3 = 'c2Start' - 'tn2'

        select Table table
        Set numeric value: i, "nrFiles", 'q:1'
        Set string value: i, "name", name$
        Set numeric value: i, "length", 'length:4'
        Set string value: i, "partName", partName$
        Set numeric value: i, "durSound", 'durSound:4'
        Set numeric value: i, "n3Start", 'n3Start:4'
        Set numeric value: i, "c2Start", 'c2Start:4'
        Set numeric value: i, "syll1n3End", 'syll1n3End:4'
        Set numeric value: i, "p3", 'p3:4'
    endfor

    select Table table
    table_name$ = "output_test_" + name$
    Save as tab-separated file... 'dir$' 'table_name$'.csv
endfor

select all
Remove