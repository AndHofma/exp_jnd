%% Make sure the TandemSTRAIGHT folder is your working directory or it is added to the path

%% Open the MorphingMenu interface
MHandle = MorphingMenu;

%% Load waveform A and choose a wav-file
% e.g. "bak.wav"
% select 'Analyze' to start analyzing the sound file

%%  click on F0/F0 structure extraction to open up the F0 analysis window
% there are three windows
% on the bottom there is the familiar waveform representation of the file
% above that is the F0 trajectory estimation based on periodicity
% the top window shows the level of periodicity detected by the algorithm

% notice how the waveform is encased by a green rectangle
% this rectangle denotes where the algorithm suspects a periodic signal
% this can be manually corrected

% the middle pane will show a smooth curve in the middle, with jagged lines
% where there is no periodic waveform

%% the jagged tracking where no voicing is detected can be corrected by enabling autotracking
% this might also affect the rectangles in the waveform - adjust
% accordingly

%% In the synthesis pane
% the aperiodic and periodic parts can now be played separately

%% Click Finish/upload to move forward and close the F0 extraction window

%% Click on Aperiodicity extraction
% this will not open a new window

%% Then click on STRAIGHT spectrum
% this will not open a different time 

%% Now save the analysis in a so-called STRAIGHT object
% and give it a useful name such as "bak_strObj"

%% Now we can synthesize or manipulate the file: click synthesize
% playing the original versus the synthesized version shows not much
% difference and illustrates the power of this package

% a fun little extra hides in the manipulation GUI
% drawing in your own pitch contours is remarkably easy and convincing

%% Then Finish and Upload again
% the handler closes


%% load two waveforms bak and pak
% by clicking Load waveform A and B respectively

%% if you have saved STRAIGHTObjects before, you can load them here
% if not, you can analyze the files from here and then save a StrObj

%% Once the StrObjs are loaded, you can Open anchoring interface
%% then calculate a distance matrix
% this will show 2D how much distance there is between the data in the
% spectrogram

%% from here, you can set so-called temporal anchors

% these are needed to establish how first and the second file to be morphed
% are related in time
% so you will want anchors near important temporal points such as burst
% onset, onset of voicing etc.
% to do this, click on the white line when the cursor changes to a plus
% sign
% to delete a misplaced anchor, hold shift while clicking on an anchor
% anchors can be dragged in the matrix, but horizontally also in the spectrogram

% these anchors can also be set in the frequency-domain
% hold ALT and when the cursor turns to a pointed index finger click on an 
% anchor to open the frequency anchor interface
% this is a spectrum showing the amplitudes of frequencies at this specific
% time slice
% we can skip this step for now

%% when this is done, 'set up the anchors'
%% and save the morphing substrate before closing the window

%% Back in the morphing menu: Edit Morphing rate
% we want to make a continuum between bak and pak
% for this we need to create one morphing substrate with the morphing rate
% set to one extreme
% and a second to the other

%% pull the slider in the top pane to the bottom (towards A)
% if the Attribute Binding parameter is set to binded attributes,
% then the other sliders should follow

%% then click on set up morphing substrate
%% You will switch back to the MorphingMenu: Save this morphing substrate
% you can check the output by synthesizing the msubstr and replaying it
% in our case it should be the voiced syllable
% save it and name it something like "bak_mSubstr.mat"

%% then go back to the morphingRateGUI: and pull the sliders up to B
%% and save the substrate again (check if it is the voiceless syllable)
%% give it a decriptive name such as "pak_mSubstr.mat"

%% Now you can click on Continuum to create the continuum
% an explorer/finder window will open so you can choose the A-end of the continuum: 
% choose "bak_mSubstr.mat", then choose "pak_mSubstr.mat"

%% You can choose the directory to save to
% what the folder will be called
% what the files will be called
% how many steps there will be

%% While generating the continuum, you will hear the output


