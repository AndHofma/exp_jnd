## Skript zum Skalieren aller Files aus einem Ordner

form scaling pitch
comment directory to unscaled sound files
sentence dir_in /Users/before_scaling/

comment directory to save scaled sound files
sentence dir_out /Users/scaled/

comment scale pitch to ... dB
integer int 70

comment add to sound name
word add_to_name _scaled

endform

## Files einlesen und Stringlist erstellen
#wav-files einlesen
Create Strings as file list... list 'dir_in$'*.wav
	n = Get number of strings
	clearinfo

#For-Schleife, die ein File nach dem anderen einliest und skaliert
for i from 1 to n
	# Stringliste auswählen
	select Strings list
	#Erstellung Variable, die das erste File aus Liste auswählt
	filename$ = Get string... 'i'
	Read from file... 'dir_in$''filename$'
	name$ = selected$ ("Sound")

	# Soundfile auf dB skalieren, die in Variable int gespeichert ist
	select Sound 'name$'
	Scale pitch... 'int'

	# Ergebnis der Manipulation auswählen, umbenennen und speichern
	select Sound 'name$'

	Save as WAV file... 'dir_out$''name$''add_to_name$'.wav

	printline scaled file 'name$'

endfor

select all
Remove