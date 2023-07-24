function mSubstrate = makeCustomMorphingSubstrate(sndA, sndB, lblA, lblB)
%MAKECUSTOMMORPHINGSUBSTRATE Scripted generation of a TandemSTRAIGHT
%   morphing substrate
%
%   MAKECUSTOMMORPHINGSUBSTRATE(SNDA, SNDB) takes two strings SNDA and SNDB
%   holding the full paths to the sound files to be used respectively as
%   samples A and B in the morphing substrate and returns a working morphing
%   substrate based on them.
%
%   The state of the resulting morphing substrate allows for immediate use of
%   the GENERATEMORPHEDSPEECHNEWAP TandemSTRAIGHT function.
%
%   MAKECUSTOMMORPHINGSUBSTRATE(SNDA, SNDB, LBLA, LBLB) takes two additional
%   strings LBLA and LBLB holding the full paths to Audacity label files which
%   are passed to the morphing substrate to set temporal anchors.
%
%   This current version relies on the GUI for the use of some of its internal
%   functions, notably to initialize the morphing axis, without which the
%   morphing substrate is unusable. When ongoing attempts to do this without
%   the GUI are fruitful, the GUI can be abandoned and this script should
%   become compatible with Octave. At this point, _this is not the case_.
%
%   Examples
%       gui = MorphingMenu();
%       revisedData = makeCustomMorphingSubstrate(sndA, sndB, lblA, lblB);
%       data = get(gui, 'userdata');
%       revisedData = data.mSubstrate;
%
%           revisedData now holds a new morphing substrate generated from
%           the sound and label files located at the paths passed to
%           MAKECUSTOMMORPHINGSUBSTRATE
%
%   See also MORPHINGMENU, SETSTEP, SETKNOBS
%
%   Notes: This being the first working version of this script, do not
%   rely on future versions working in the same way.
%
%   Author: Jose Joaquin Atria
%   Version: 1.00 (1 July 2013)
%
%   This script is free software: you can redistribute it and/or modify
%   it under the terms of the GNU General Public License as published by
%   the Free Software Foundation, either version 3 of the License, or
%   (at your option) any later version.
%
%   A copy of the GNU General Public License is available at
%   <a href="http://www.gnu.org/licenses/">http://www.gnu.org/licenses/</a>.

	wd = pwd();

	gui = MorphingMenu;
	menuUserData = get(gui,'userdata');
	mSubstrate = menuUserData.mSubstrate;
	mSubstrate.creator = 'CustomScript';
	mSubstrate.creationDate = datestr(now,30);

	global FILES;
	global LABLS;
	FILES = (nargin >= 2);
	LABLS = (nargin == 4);

	if FILES
		snd = sndA(find(sndA==filesep,1,'last')+1:end);
		sndpath = sndA(1:find(sndA==filesep,1,'last'));
	else
		[snd,sndpath] = uigetfile('*.wav','Select sound file for A.');
	end;
	cd(sndpath);
	if LABLS
		lbl = lblA(find(lblA==filesep,1,'last')+1:end);
		lblpath = lblA(1:find(lblA==filesep,1,'last'));
	else
		[lbl,lblpath] = uigetfile('*.txt', ['Read label file for ' snd]);
	end;
	mSubstrate = LoadSoundFile(mSubstrate, 'A', sndpath, snd, lblpath, lbl);

	if FILES
		snd = sndB(find(sndB==filesep,1,'last')+1:end);
		sndpath = sndB(1:find(sndB==filesep,1,'last'));
	else
		[snd,sndpath] = uigetfile('*.wav','Select sound file for B.');
	end;
	if LABLS
		lbl = lblB(find(lblB==filesep,1,'last')+1:end);
		lblpath = lblB(1:find(lblB==filesep,1,'last'));
	else
		[lbl,lblpath] = uigetfile('*.txt', ['Read label file for ' snd]);
	end;
	mSubstrate = LoadSoundFile(mSubstrate, 'B', sndpath, snd, lblpath, lbl);

	menuUserData.mSubstrate = mSubstrate;
	set(gui,'userdata', menuUserData);
	MorphingMenu('syncGUIStatus', menuUserData.currentHandles)
	MorphingMenu('InitializeMorphingTimeAxis_Callback', menuUserData.currentHandles.InitializeMorphingTimeAxis, [], menuUserData.currentHandles);

	cd(wd);
  
% Local functions

% Load sound
function mSubstrate = LoadSoundFile(mSubstrate, speaker, sndpath, snd, lblpath, lbl)
	[wave,rate] = wavread([sndpath snd]);
	wave = wave(:, 1);
	disp(['Processing ' snd]);
	[obj, spec, apr] = ProcessSound(wave, rate);

	mSubstrate.samplintFrequency = rate;
	mSubstrate.(['dataDirectoryForSpeaker'       speaker]) = sndpath;
	mSubstrate.(['waveformForSpeaker'            speaker]) = wave;
	mSubstrate.(['fileNameForSpeaker'            speaker]) = snd;
	mSubstrate.(['f0TimeBaseOfSpeaker'           speaker]) = obj.temporalPositions;
	mSubstrate.(['spectrogramTimeBaseOfSpeaker'  speaker]) = obj.temporalPositions;
	mSubstrate.(['f0OfSpeaker'                   speaker]) = obj.f0CandidatesMap(1,:)';
	mSubstrate.(['STRAIGHTspectrogramOfSpeaker'  speaker]) = spec.spectrogramSTRAIGHT;
	mSubstrate.(['aperiodicityTimeBaseOfSpeaker' speaker]) = apr.temporalPositions;
	mSubstrate.(['aperiodicityOfSpeaker'         speaker]) = apr;

	mSubstrate = loadLabel(mSubstrate, lblpath, lbl, speaker);

	mSubstrate.(['frequencyAnchorOfSpeaker'      speaker]) = generateDefaultFrequencyAnchorStructure(size(mSubstrate.(['temporaAnchorOfSpeaker' speaker]),1), rate);

function mSubstrate = loadLabel(mSubstrate, path, file, speaker)
%LOADLABEL Local function for loading a label file
%
%   LOADLABEL(MSUBSTRATE, PATH, FILE, SPEAKER) takes an existing morphing
%   substrate object, opens the Audacity label FILE found in PATH and adds
%   it to the speakers specified in the string SPEAKER, returning the modified
%   morphing substrate.
	label = readAudacityLabel([path file]);
	mSubstrate = morphingSubstrateNewAP(mSubstrate, 'set', ['temporaAnchorOfSpeaker' speaker], label.segment(:,1));
  
function [obj, spec, apr] = ProcessSound(wave, rate)
%PROCESSSOUND Wrapper function for STRAIGHTAnalysis and STRAIGHTSpectrum
%
%   PROCESSSOUND(WAVE, RATE) takes a sound and its sampling rate
%   and returns an array with the sound, spectrum and aperiodicity
%   STRAIGHT objects.
%
%   See also MAKECUSTOMMORPHINGSUBSTRATE, STRAIGHTANALYSIS, STRAIGHTSPECTRUM
	obj = STRAIGHTAnalysis(wave, rate);
	disp('Extracting STRAIGHT spectrum');
	[spec, apr] = STRAIGHTSpectrum(wave, obj, rate);

function fa = generateDefaultFrequencyAnchorStructure(ta, rate)
%GENERATEDEFAULTFREQUENCYANCHORSTRUCTURE Generate a default frequency
%   anchor structure.
%
%   GENERATEDEFAULTFREQUENCYANCHORSTRUCTURE(TA, RATE) takes the existing
%   temporal anchor structure TA and the sampling rate RATE of the sound
%   to which this belongs and returns a default frequency anchor structure.
%
%   This code taken from the TandemSTRAIGHT source for ease of use.
%
%   See also MAKECUSTOMMORPHINGSUBSTRATE
	nFrequency = floor((rate/2+500)/100);
	fa.frequency = zeros(ta,nFrequency);
	fa.counts = zeros(ta,1);
	for ii = 1:ta
		fa.frequency(ii,:) = (1:nFrequency)*1000 - 550;
	end

%  function mSubstrate = initializeMorphingRate(mSubstrate)
%    rate = [];
%    fields = {'spectrum' 'frequency' 'aperiodicity' 'F0' 'time'};
%    size = length(mSubstrate.f0OfSpeakerA);
%    for i = 1:length(fields)
%      rate.(fields{i}) = ones(size, 1) * 0.5;
%    end;
%    mSubstrate.temporalMorphingRate = rate;