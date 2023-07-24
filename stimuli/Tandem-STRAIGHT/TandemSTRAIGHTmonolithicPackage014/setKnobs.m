function temporalRate = setKnobs (originalRate, fields, value)
%SETKNOBS Change the position of a knob in the morphing rate of a
%   TandemSTRAIGHT morphing substrate.
%
%   SETKNOBS(ORIGINALRATE, FIELDS, VALUE) takes the temporal rate
%   of an existing morphing substrate and sets the knobs stated in
%   the string cell array FIELDS to the position stated in VALUE,
%   wchich must be between 0 and 1.
%
%   Examples
%       rate = mSubstrate.temporalMorphingRate;
%       rate = SETKNOBS(rate, {'F0', 'aperiodicity'}, 0.33);
%       mSubstrate.temporalMorphingRate = rate;
%
%           the F0 and aperiodicity knobs in the morphing rate in
%           mSubstrate are now set to one third of the way between
%           the A and B samples in mSubstrate.
%
%   See also MORPHINGMENU, MAKECUSTOMMORPHINGSUBSTRATE, SETSTEP
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

  if value > 1 value = 1; elseif value < 0 value = 0; end;
  temporalRate = originalRate;
  for i = 1:length(fields)
    n = length(temporalRate.(fields{i}));
    temporalRate.(fields{i}) = ones(n, 1) * value;
  end;
  