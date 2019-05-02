from parse import parsingFunc, toFasta
from align import align

##### Config variables #####
filePath = 'rand.500.4.fq'
wordLength = 30 # See readme if running on 32-bit machine
writePath = 'output.fasta'
############################


reads = parsingFunc(filePath)
result = align(reads,wl=wordLength)
contigs = result[0]
N50 = result[1]

toFasta(contigs, writePath)
print("Complete. n50: " + str(N50))

'''
rand.500.1.fq:
    wordLength = 7
        n_contigs = 2
        n50       = 1
        time     ~= 540
    wordLength = 15
        n_contigs = 2
        n50       = 1
        time     ~= 345
    wordLength = 30
        n_contigs = 2
        n50       = 1
        time     ~= 325
rand.500.2.fq:
    wordLength = 7
        n_contigs = 2200
        n50       = 605
        time      ~= 340
    wordLength = 15
        n_contigs = 3868
        n50       = 1170
        time     ~= 310
    wordLength = 30
        n_contigs = 4882
        n50       = 1536
        time     ~= 342
rand.500.3.fq:
    wordLength = 7
        n_contigs = 2938
        n50       = 801
        time      ~= 605
    wordLength = 15
        n_contigs = 5997
        n50       = 1861
        time      ~= 275
    wordLength = 30
        n_contigs = 7532
        n50       = 3007
        time      ~= 345
'''
