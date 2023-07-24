function obj = STRAIGHTAnalysis(wave, rate)
%STRAIGHTANALYSIS Scripted extraction of STRAIGHT F0 and F0 structure
%
%   STRAIGHTANALYSIS(WAVE, RATE) takes a sound wave (such as that
%   returned by WAVREAD), and the sampling rate of the WAVE and returns
%   a STRAIGHT sound object.
%
%   Examples
%       [wave, rate] = WAVREAD(filename);
%       obj = STRAIGHTANALYSIS(wave, rate);
%       [spec, apr] = STRAIGHTSPECTRUM(wave, obj, rate);
%
%           This is the equivalent of using the "F0/F0 structure extraction",
%           "Aperiodicity extraction" and "STRAIGHT spectrum" buttons in the
%           TandemSTRAIGHTHandler GUI.
%
%   See also MAKECUSTOMMORPHINGSUBSTRATE, STRAIGHTSPECTRUM
%
%   Notes: This being the first working version of this script, do not
%   rely on future versions working in the same way. Running in Octave generates
%   unexpected results.
%
%   Author: Jose Joaquin Atria
%   Version: 1.00 (1 July 2013)

	obj = exF0candidatesTSTRAIGHTGB(wave,rate);              % Calculate
	wave = removeLF(wave,rate,obj.f0,obj.periodicityLevel);  % Clean LF noise
	obj = exF0candidatesTSTRAIGHTGB(wave,rate);              % Calculate
	obj = autoF0Tracking(obj,wave);                          % Auto tracking
	obj.vuv = refineVoicingDecision(wave,obj);