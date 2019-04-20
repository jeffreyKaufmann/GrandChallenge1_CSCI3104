def parsingFunc(pathToData):
	#Create a list of 500 Nones for GENOMES
	seqNumeric = [None] * 500
	#Create a list to store each list of GENOMES
	seqListStore = [] 
	from Bio import SeqIO
	for seq_record in SeqIO.parse(pathToData, "fasta"):
		#Sorting and grabbing list of 500 GENOMES
	    seq = seq_record.seq
	    seqString = str(seq)
	    #Go into string of GENOMES and set A = 0, C = 1, G = 2, T = 3
	    for i, c in enumerate(seqString):

	    	if(c == 'A'):
	    		seqNumeric[i] = 0 
	    	elif(c == 'C'):
	    		seqNumeric[i] = 1
	    	elif(c == 'G'):
	    		seqNumeric[i] = 2
	    	elif(c == 'T'):
	    		seqNumeric[i] = 3
	   	#Store the list into SeqListStore
	    seqListStore.append(seqNumeric)
	return seqListStore



