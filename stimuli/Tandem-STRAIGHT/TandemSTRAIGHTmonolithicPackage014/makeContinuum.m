function makeContinuum(mSubstrate, fields, steps, outpath, nameroot)
%MAKECONTINUUM Synthesize steps of a continuum using TandemSTRAIGHT
%
%   MAKECONTINUUM(MSUBSTRATE, FIELDS, STEPS, OUTPATH, NAMEROOT)
%
%   This function takes a morphing substrate MSUBSTRATE and generates a
%   continuum between its A and B samples by varying the TandemSTRAIGHT
%   parameters specified in the FIELDS string cell array with as many
%   steps as specified in STEPS.
%
%   The function saves the resulting steps as WAV files in the folder
%   specified in OUTPATH, using NAMEROOT as the basis for the generated
%   filenames. The file saving and naming options will probably need to
%   be modified in the future for increased generality. Meanwhile, adjust
%   to suit your own needs.
%
%   Examples
%       makeContinuum(mSubstrate, {'F0', 'time'}, 11, '/home/user/morph/', 'sound')
%
%           Will generate an 11-step continuum varying F0 and segment
%           duration and save the resulting synthesized sounds into the
%           specified folder. Each new file will have a name like
%           'sound.F0-time.01of11.wav'
%
%   See also MORPHINGMENU, SETSTEP
%
%   Notes: This being the first working version of this script, do not
%   rely on future versions working in the same way. Runs in Matlab and Octave.
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

	strfields = strjoin(fields, '-');

	for j = 1:steps
		step = zeropad(j, length(int2str(steps)));
		disp(['In step ' int2str(j) ' of ' int2str(steps)]);
		mSubstrate = setStep(mSubstrate, fields, steps, j);
		morphedSound = generateMorphedSpeechNewAP(mSubstrate);
		filename = [outpath nameroot int2str(j) '.wav'];
		maxAmplitude = max(abs(morphedSound.outputBuffer));
		audiowrite(filename, morphedSound.outputBuffer, mSubstrate.samplintFrequency);

%		wavwrite is deprecated, but audiowrite is not yet in octave
%		audiowrite(filename, morphedSound.outputBuffer, mSubstrate.samplintFrequency);
	end;