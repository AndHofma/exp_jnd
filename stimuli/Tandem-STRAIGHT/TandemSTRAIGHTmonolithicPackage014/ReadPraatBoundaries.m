function [boundaries] = ReadPraatBoundaries(file, tier)

if nargin == 0
  [file, path] = uigetfile('*TextGrid', 'Read TextGrid files');
  file = [path file];
  tier = 1;
end;

fid         = fopen(file);
tline       = fgetl(fid);
counter     = 1;
found       = 0;
get_line    = 0;
boundaries  = [];
line_length = 0;
line_ending = '';
this_tier   = 0;
tier_name   = '';

while ischar(tline)
  counter = counter + 1;

  if (get_line)
    boundaries = [boundaries; str2num(tline)];
    get_line = 0;
  end
    
  if (this_tier == tier)
    if (strcmp(tline(1),'"'))
      if (strcmp(tier_name,''))
        tier_name = fgetl(fid);
        counter = counter + 1;
      else
        get_line = 1;
      end
    end
  end

  line_length = length(tline);
  if line_length > 4
    line_ending = tline(line_length-4:line_length-1);
    if (strcmp(line_ending,'Tier'))
      this_tier = this_tier + 1;
    end
  end
  
  tline = fgetl(fid);
end
fclose(fid);