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

def toFasta(sortedList, filePath):
	print("Starting Fasta")
	count = 1
	store = open(filePath, "w")

	for i in range(len(sortedList)):
		store.write(">" + str(count) + "\n")
		for j in range(len(sortedList[i])):
			if(sortedList[i][j] == 0):
				sortedList[i][j] = "A"
				store.write(str(sortedList[i][j]))
			elif(sortedList[i][j] == 1):
				sortedList[i][j] = "C"
				store.write(str(sortedList[i][j]))
			elif(sortedList[i][j] == 2):
				sortedList[i][j] = "G"
				store.write(str(sortedList[i][j]))
			elif(sortedList[i][j] == 3):
				sortedList[i][j] = "T"
				store.write(str(sortedList[i][j]))

		store.write("\n")
		count += 1
	print("Done...")
