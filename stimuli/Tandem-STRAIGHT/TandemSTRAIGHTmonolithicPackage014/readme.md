Readme
======

This set of scripts have been written to ease the generation of sound continua
using [TandemSTRAIGHT][1].

The first function to call is `makeSubstrates()`, which will process the files
in its `files` variable to generate custom Morphing Substrates for each sound
pair specified therein. This function needs to be run from Matlab, since it
still requires the GUI for processing. Hopefully, this will change in future
versions of these scripts, if there is a future version.

Once this is done, `processFilesForContinuum()` can be called on the generated
custom substrates. Since the specific needs for specific continua will probably
change, this script is mostly there as an example. Once called (after the
proper modifications are made) this function will process all the substrates
specified in its `files` variable, and make a call to `makeContinuum()` for
each one. This script can be calle from Matlab or Octave, since it does not
require the TandemSTRAIGHT GUI.

`makeContinuum()` is the final function, serves as a wrapper for the rest of
the synthesis. This function will take a specified morphing substrate, apply
the specific changes, and output a synthesized sound to the specified output
directory.

The rest of the functions in this bundle are there as helper functions for
these main three. Please refer to their documentation for instructions on how
to use them.

A script to convert Praat TextGrid files to Audacity labels (which
TandemSTRAIGHT uses) is available in my [Praat plugin repository][2].

Please send observations and comments to José Joaquín Atria at
jjatria@gmail.com

[1]: http://www.wakayama-u.ac.jp/~kawahara/STRAIGHTadv/index_e.html
[2]: https://github.com/jjatria/plugin_jjatools
