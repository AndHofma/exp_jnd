# specify the directory from which you want to access the soundfiles
d$ = "C:\Users\Andrea Hofmann\OneDrive\PhD\phd_perception_production_link\dissertation\procedure_all\exp_jnd\Tandem-STRAIGHT\TandemSTRAIGHTmonolithicPackage014\mimi_pitch_flat_rise_continuum\"

# opens the wav-files from a file  (es gibt bereits ein TextGrid dazu)
Create Strings as file list... list 'd$'*.wav

# Anzahl der Objekte in der Stringliste erfragen und in Variable n speichern
n = Get number of strings

# for-Schleife, die durch jedes Objekt in der Liste geht
for i from 1 to n
	select Strings list
	filename$ = Get string... 'i'
	Read from file... 'd$''filename$'
	# Speichern basename in Variable name
	name$ = selected$ ("Sound")
	# extractWord is a very convienient expression
	# it "looks for a word without spaces after the first occurrence" of a word (in this script: SJ101_)
	basename$ = extractWord$(selected$(), " ")
	##this is to get the FIRST 4 characters from the string stored in variable a.
	digits$ = right$("'basename$'",3)

	# create a TextGrid
	# name all tiers in the first quotation marks
	# repeat those tiers that should be point tiers in the second quotation marks
	# To TextGrid... "Word Syllable", ""
	To TextGrid: "Word Syllable", ""

	Insert boundary: 1, 0.00923891849733524
	Insert boundary: 1, 0.47889579020013806
	Insert boundary: 2, 0.00923891849733524
	Insert boundary: 2, 0.1657799367251891
	Insert boundary: 2, 0.47889579020013806

	Set interval text: 1, 2, "name2_mimmi_'digits$'"
	Set interval text: 2, 2, "n2sy1_mimmi_'digits$'"
	Set interval text: 2, 3, "n2sy2_mimmi_'digits$'"

	select TextGrid 'name$'
	# save TextGrid under a new directory
	# enter here the directory in which you want to save your annotated files!
	dir$ = "C:\Users\Andrea Hofmann\OneDrive\PhD\phd_perception_production_link\dissertation\procedure_all\exp_jnd\Tandem-STRAIGHT\TandemSTRAIGHTmonolithicPackage014\mimi_pitch_flat_rise_continuum\annotated\"
	# Save TextGrid as text file... 'dir$''name$'.TextGrid
	Save as text file... 'dir$''name$'.TextGrid
	# save wav file to the same directory
	select Sound 'name$'
	Save as WAV file... 'dir$''name$'.wav

	printline completed file 'name$'

	select all
	minus Strings list
	Remove

endfor

select all
Remove