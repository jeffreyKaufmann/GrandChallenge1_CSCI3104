from parse import parsingFunc
from align import align

reads = parsingFunc('rand.500.1.fq')
result = align(reads,wl=30)
contigs = result[0]
N50 = result[1]

'''
With rand.500.1.fq:
    wordLength = 7
        n_contigs = 2
        n50       = 1
        time     ~= 540
    wordLength = 10
        n_contigs = 2
        n50       = 1
        time     ~= 360
    wordLength = 15
        n_contigs = 2
        n50       = 1
        time     ~= 345
    wordLength = 25
        n_contigs = 2
        n50       = 1
        time     ~= 335
    wordLength = 30
        n_contigs = 325

'''
