# # ## ### ##### ########  #############  ##################### 
# Praat Script
# ramp intensity contour
#
# Matthew Winn
# August 2014
##################################
##################### 
############# 
######## 
#####
###
##
#
#
form intensity ramps

	comment Ramp onset?
	boolean ramponset 1 
	comment Enter onset ramp time in ms
	real onramptimems 80
	
	comment Ramp offset?
	boolean rampoffset 1 
	comment Enter onset ramp time in ms
	real offramptimems 80
	
	comment choose linear or cosine ramp
	boolean linear 1
	
	comment type in an additional suffix for the object names
	sentence suffix _ramped

endform

onramptime = onramptimems/1000
offramptime = offramptimems/1000


pause select all sounds that you want to ramp
numberOfSelectedSounds = numberOfSelected ("Sound")

for thisSelectedSound to numberOfSelectedSounds
	sound'thisSelectedSound' = selected("Sound",thisSelectedSound)
endfor

for thisSound from 1 to numberOfSelectedSounds
    select sound'thisSound'
	name$ = selected$("Sound")

Copy... 'name$'_ramped
start1 = Get start time
end1 = Get end time

if ramponset = 1
  if linear = 1
    Formula... if x<start1 + onramptime  
       ...then self * ((x-start1)/onramptime) 
       ...else self endif  
  else
    Formula... if x<(start1 + 'onramptime')  
	...then self * cos((x-('onramptime' + 'start1'))/('onramptime') * pi/2)
	...else self endif  
  endif
endif


if rampoffset = 1  
  if linear = 1
     Formula... if x>('end1' - 'offramptime')  
     	...then self * (1-((x-end1 + 'offramptime')/'offramptime'))
	...else self endif
   
   else
    Formula... if x>('end1' - 'offramptime')  
	...then self * cos((x-(end1 - 'offramptime'))/'offramptime' * pi/2)
	...else self endif
  endif
endif

endfor

#re-select the sounds
select sound1
for thisSound from 2 to numberOfSelectedSounds
    plus sound'thisSound'
endfor