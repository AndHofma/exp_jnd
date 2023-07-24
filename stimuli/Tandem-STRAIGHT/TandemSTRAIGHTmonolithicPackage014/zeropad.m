function x = zeropad(x, n)

	if n>length(int2str(x))
		pad = strjoin(repmat(0, 1, n), '');
		x = [pad int2str(x)];
		x = x(length(x)-n+1:end);
	end;
