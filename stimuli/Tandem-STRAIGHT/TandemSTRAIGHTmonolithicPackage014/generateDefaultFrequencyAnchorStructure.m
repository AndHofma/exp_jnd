function frequencyAnchor = generateDefaultFrequencyAnchorStructure(nTime,fs)
  nFrequency = floor((fs/2+500)/100);
  frequencyAnchor.frequency = zeros(nTime,nFrequency);
  frequencyAnchor.counts = zeros(nTime,1);
  for ii = 1:nTime
      frequencyAnchor.frequency(ii,:) = (1:nFrequency)*1000 - 550;
  end;
return;