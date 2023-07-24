function [spec,apr] = STRAIGHTSpectrum(wave, obj, rate)
%STRAIGHTSPECTRUM Scripted extraction of the TandemSTRAIGHT spectrum
%   object.
%
%   STRAIGHTSPECTRUM(WAVE, OBJ, RATE) takes a sound wave (such as that
%   returned by WAVREAD), an existing sound object OBJ (such as that
%   resulting from the F0 and F0 structure extraction process in TandemSTRAIGHT)
%   and the sampling rate of the WAVE. It returns an array with the
%   STRAIGHT spectrum and aperiodicity objects.
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
%   See also MAKECUSTOMMORPHINGSUBSTRATE, STRAIGHTANALYSIS
%
%   Notes: This being the first working version of this script, do not
%   rely on future versions working in the same way. Running in Octave generates
%   unexpected results.
%
%   Author: Jose Joaquin Atria
%   Version: 1.00 (1 July 2013)

	% Aperiodicity extraction 
	apr  = aperiodicityRatioSigmoid(wave,obj,1,2,0);
	% STRAIGHT Spectrum
	spec = exSpectrumTSTRAIGHTGB(wave,rate,apr);
	o.waveform = wave;
	o.samplingFrequency = rate;
	o.refinedF0Structure.temporalPositions = obj.temporalPositions;
	o.SpectrumStructure.spectrogramSTRAIGHT = spec.spectrogramSTRAIGHT;
	o.refinedF0Structure.vuv = obj.vuv;
	spec.spectrogramSTRAIGHT = unvoicedProcessing(o);