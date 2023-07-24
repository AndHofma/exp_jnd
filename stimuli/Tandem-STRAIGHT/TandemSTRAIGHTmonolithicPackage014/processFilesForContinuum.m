function processFilesForContinuum()
	outpath = 'C:\Users\Andrea Hofmann\OneDrive\PhD\phd_perception_production_link\dissertation\procedure_all\exp_jnd\Tandem-STRAIGHT\TandemSTRAIGHTmonolithicPackage014\continuum\';
	sbtpath = 'C:\Users\Andrea Hofmann\OneDrive\PhD\phd_perception_production_link\dissertation\procedure_all\exp_jnd\Tandem-STRAIGHT\TandemSTRAIGHTmonolithicPackage014\';
	files = {
		'mSubstr-mimmi-anchor-A'
		'mSubstr-mimmi-anchor-B'
	};

	process(files, sbtpath, outpath);

	function process(files, sbtpath, outpath)
		% sbtext holds the extension for the morphing substrate object
		sbtext = '.mat';
		steps = 150;

		for i = 1:size(files)
			disp(['Processing ' files{i}]);
			sbtname = [sbtpath files{i} sbtext];
			load(sbtname);
			mSubstrate = revisedData;

			% Modify this cell array to contain the names of whatever
			% fields you want to change along the continuum. If you want
			% to vary all five parameters at once, you can enter 'all' as its
			% only string as shorthand.
			fields = {'F0'};

			% As an example, all stepts in this F0 continuum will have the duration
			% fixed at A (the A-B continuum is represented as a range from 0 to 1)
			mSubstrate.temporalMorphingRate = setKnobs(mSubstrate.temporalMorphingRate, {'time'}, 0);
			nameroot = files{i};
			disp(['Duration set to A']);
			makeContinuum(mSubstrate, fields, steps, outpath, nameroot)

		end;
