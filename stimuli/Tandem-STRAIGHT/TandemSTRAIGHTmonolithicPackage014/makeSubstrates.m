function makeSubstrates()
  sndpath = 'path/to/sounds/';
  lblpath = 'path/to/labels/';
  sbtpath = 'output/path/';
  sndext = '.wav';
  lblext = '.txt';
  
  pairs = {
    {'sndA_filename1' 'sndB_filename1'}
    {'sndA_filename2' 'sndB_filename2'}
  };

  process(pairs, sndpath, lblpath, sbtpath, sndext, lblext);

function process(pairs, sndpath, lblpath, sbtpath, sndext, lblext)
  for i = 1:size(pairs)
    
    a = pairs{i}{1};
    b = pairs{i}{2};
    
    sndA = [a sndext];
    sndB = [b sndext];
    lblA = [a lblext];
    lblB = [b lblext];

    % The GUI is called only to use some of its internal functions because
    % so far, attampts to use them without the GUI have failed. Eventually,
    % the idea would be to make do without calling the GUI at all, which
    % would make execution be faster and this script compatible with Octave.
    gui = MorphingMenu();
    revisedData = makeCustomMorphingSubstrate([sndpath sndA], [sndpath sndB], [lblpath lblA], [lblpath lblB]);
    data = get(gui, 'userdata');
    revisedData = data.mSubstrate;
    % Once we are done, the GUI can be destroyed so we have a clean slate for
    % for the next one.
    MorphingMenu('QuitButton_Callback', data.currentHandles.QuitButton, [], data.currentHandles);
    
    filename = [sndA '-' sndB];
    save([sbtpath filename], 'revisedData');
  end;
