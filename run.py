from parse import parsingFunc
from align import align

reads = parsingFunc("FQ/rand.500.fa")
contigs = align(reads,wl=7)
print(contigs)
