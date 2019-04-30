def parsingFunc(pathToData):
	reads = []
	with open(pathToData) as seqFile:
		for idx, line in enumerate(seqFile):
			if (idx % 4) == 1:
				reads.append(line.rstrip())
	for readIdx, charRead in enumerate(reads):
		intRead = []
		for char in charRead:
			if(char == 'A'):
				intRead.append(0)
			elif(char == 'C'):
				intRead.append(1)
			elif(char == 'G'):
				intRead.append(2)
			elif(char == 'T'):
				intRead.append(3)
		reads[readIdx] = intRead
	return reads
