from parse import parsingFunc
from align import align

reads = parsingFunc('rand.500.1.fq')
contigs = align(reads,wl=7)
print(contigs)


'''
def stringToList(st):
    l = []
    for c in st:
        if(c == 'A'):
            l.append(0)
        elif(c == 'C'):
            l.append(1)
        elif(c == 'G'):
            l.append(2)
        elif(c == 'T'):
            l.append(3)
    return l
'''
