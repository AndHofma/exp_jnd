function mSubstrate = setStep(mSubstrate, fields, totalSteps, thisStep)
%SETSTEP Set a TandemSTRAIGHT morphing substrate to a specific step in
%   a continuum
%
%   SETSTEP(MSUBSTRATE, FIELDS, TOTALSTEPS, THISSTEP) takes an
%   existing morphing substrate object and modifies the fields in the
%   string cell array 'FIELDS' to a position corresponding to that of
%   THISSTEP in a continuum consisting of TOTALSTEPS steps.
%
%   Examples
%       SETSTEP(mSubstrate, {'F0', 'time'}, 11, 11)
%
%           returns a morphing substrate equal to mSubstrate but with
%           the F0 and time parameters in the morphing rate set to the final
%           step in a 11-step continuum from A to B (i.e. they will be set to B)
%
%       steps = 5;
%       for i = 1:steps
%         mSubstrate = SETSTEP(mSubstrate, {'aperiodicity'}, steps, i);
%         morphedSound = generateMorphedSpeechNewAP(mSubstrate);
%         sound(morphedSound.outputBuffer, mSubstrate.samplintFrequency);
%       end
%
%           plays an aperiodicity continuum of five steps between the A and B
%           samples in mSubstrate ("samplintFrequency" is not a typo, at least
%           here).
%   
%   See also MORPHINGMENU, MAKECUSTOMMORPHINGSUBSTRATE, SETKNOBS
%
%   Notes: This being the first working version of this script, do not
%   rely on future versions working in the same way. Runs in Matlab or Octave.
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

  rate = mSubstrate.temporalMorphingRate;

  if ~iscell(fields) && ischar(fields) && fields == 'all'
    fields = {'spectrum' 'time' 'aperiodicity' 'F0' 'frequency'};
  end;
  
  delta = 1 / (totalSteps - 1);
  slider = delta * (thisStep - 1);

  rate = setKnobs(rate, fields, slider);
  mSubstrate.temporalMorphingRate = rate;
  