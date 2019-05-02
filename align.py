from parse import parsingFunc
import numpy as np
import pdb
import time
from itertools import chain

def getToWordArray(wordLength=7):
    toWord = []
    for i in range(wordLength):
        toWord.append(4**i)
    return np.array(toWord)

def getWordByIndex_A(read, idx, toWord, wordLength=7):
    word = np.matmul( toWord, read[idx : idx+wordLength] )
    return word

def getFirstWordByIndex_A(read, toWord, wordLength=7):
    return getWordByIndex_A(read, 0, toWord, wordLength)

def getEveryWord_A(read, toWord, wordLength=7):
    readLength = len(read)
    words = np.full( readLength - wordLength + 1, -1)
    for idx in range(readLength - wordLength + 1):
        words[idx] = np.matmul( toWord, read[idx : idx+wordLength] )
    return words

def getAllWords_A(reads, toWord, wordLength=7):
    n_reads = len(reads)
    allWords = [None] * n_reads
    for i in range(n_reads):
        allWords[i] = getEveryWord_A(reads[i], toWord, wordLength)
    return allWords

def getWordHits_A(allWords):
    hits = []
    n_reads = len(allWords)
    for comp in range(n_reads):
        targetRange = chain( range(comp), range(comp+1,n_reads))
        for target in targetRange:
            hit = np.where(allWords[comp] == allWords[target][0])[0]
            if hit.size:
                hits.append([comp,target,hit.tolist()])
    return hits

#comp and target are indexes
#comp and target must be same size
def isMatch_fromWords(comp, target, idx, allWords, wordLength=7):
    compWords = allWords[comp]
    targetWords = allWords[target]
    n_compWords = len(compWords)
    readLen = n_compWords - idx

    wordsMatch = all([ compWords[idx+i] == targetWords[i] for i in range(0, (readLen), wordLength) ])
    lastWordMatch = compWords[n_compWords-1] == targetWords[readLen-1]
    return wordsMatch and lastWordMatch

#comp and target are objects
#comp and target can be any size
def isMatch_fromChars(comp, target, idx):
    compLen = len(comp)
    targetLen = len(target)
    if compLen - idx < targetLen:
        readlen = compLen - idx
    else:
        readlen = targetLen
    match =  all([target[i] == comp[i+idx] for i in range(readlen)])
    return [ match, readlen ]

def getAllMatches(hits,allWords,wordLength=7):
    matches = []
    for hit in hits:
        comp = hit[0]
        target = hit[1]
        indexes = hit[2]
        for idx in indexes:
            if isMatch_fromWords(comp, target, idx, allWords, wordLength):
                matchLen = len(allWords[comp]) + wordLength - idx - 1
                matches.append([comp, target, idx, matchLen])
    return matches

def sortMatches(matches):
    def getMatchLen(match):
        return match[3]
    matches.sort(reverse=True, key=getMatchLen)
    return matches

def alignReads(allReads, sortedMatches):

    n_reads = len(allReads)
    n_matches = len(allReads)
    readLocations = [None] * n_reads
    contigs = []

    def newContig(comp,target,matchLoc):
        compRead = allReads[comp]
        targetRead = allReads[target]
        newContig = {
                        'locations':{ comp: 0, target: matchLoc },
                        'contig': compRead[0:matchLoc] + targetRead
                    }
        contigIndex = len(contigs)
        contigs.append( newContig )
        readLocations[comp] = contigIndex
        readLocations[target] = contigIndex

    def updateContig_targetExists(comp,target,matchLoc):
        #pdb.set_trace()
        compRead = allReads[comp]
        contigIndex = readLocations[target]
        contig = contigs[contigIndex]
        targetLocInContig = contig['locations'][target]
        if matchLoc > targetLocInContig:
            matchLoc = matchLoc - targetLocInContig
            [ isMatch, addLen ] = isMatch_fromChars(compRead,contig['contig'],matchLoc)
            if isMatch:
                for read in contig['locations']:
                    contig['locations'][read] += addLen
                contig['locations'][comp] = 0
                readLocations[comp] = contigIndex
                contig['contig'] = compRead[0:addLen] + contig['contig']
        else:
            compLocInContig = targetLocInContig - matchLoc

            # If comp wouldn't add any length ot contig, we ignore it
            if ( len(contig['contig']) - compLocInContig ) < len(compRead): #TODO refactor
                isMatch = isMatch_fromChars(contig['contig'],compRead,compLocInContig)[0]

                #if comp isn't not a match, we ignore it
                if isMatch:
                    contig['locations'][comp] = compLocInContig
                    contig['contig'] = contig['contig'][0:compLocInContig] + compRead
                    readLocations[comp] = contigIndex
            else:
                isMatch = isMatch_fromChars(contig['contig'],compRead,compLocInContig)[0]
                if isMatch:
                    contig['locations'][comp] = compLocInContig
                    readLocations[comp] = contigIndex

    def updateContig_compExists(comp,target,matchLoc):
        targetRead = allReads[target]
        contigIndex = readLocations[comp]
        contig = contigs[contigIndex]
        compLocInContig = contig['locations'][comp]
        targetLocInContig = compLocInContig + matchLoc
        contigLen = len(contig['contig'])
        isMatch = isMatch_fromChars(contig['contig'], targetRead, targetLocInContig)
        if isMatch:
            contig['locations'][target] = targetLocInContig
            readLocations[target] = contigIndex
            if targetLocInContig + len(targetRead) > contigLen:
                contig['contig'] = contig['contig'][0:targetLocInContig] + targetRead

    def combineContigs(comp,target,matchLoc):
        compContigIndex = readLocations[comp]
        targetContigIndex = readLocations[target]
        compContig = contigs[compContigIndex]
        targetContig = contigs[targetContigIndex]

        compLocInCompContig = compContig['locations'][comp]
        matchLocInCompContig = compLocInCompContig + matchLoc
        targetLocInTargetContig = targetContig['locations'][target]

        compContigEndFromMatch = len(compContig['contig']) - matchLocInCompContig
        targetContigEndFromMatch = len(targetContig['contig']) - targetLocInTargetContig

        if matchLocInCompContig >= targetLocInTargetContig:
            contigStartDiff = matchLocInCompContig - targetLocInTargetContig
            [ isMatch, matchLen ] = isMatch_fromChars(compContig['contig'],
                                                 targetContig['contig'],
                                                 contigStartDiff)
            if isMatch:
                #contigStartDiff = matchLocInCompContig - targetLocInTargetContig
                for read in targetContig['locations']:
                    compContig['locations'][read] = targetContig['locations'][read] + contigStartDiff
                    readLocations[read] = compContigIndex
                if compContigEndFromMatch < targetContigEndFromMatch:
                    compContig['contig'] = compContig['contig'][0:matchLocInCompContig] + targetContig['contig']
                contigs[targetContigIndex] = None

        else:
            contigStartDiff = targetLocInTargetContig - matchLocInCompContig
            [ isMatch, matchLen ] = isMatch_fromChars(targetContig['contig'],
                                                 compContig['contig'],
                                                 contigStartDiff)
            if isMatch:
                for read in compContig['locations']:
                    targetContig['locations'][read] = compContig['locations'][read] + contigStartDiff
                    readLocations[read] = targetContigIndex
                if targetContigEndFromMatch < compContigEndFromMatch:
                    targetContig['contig'] = targetContig['contig'][0:targetLocInTargetContig] + compContig['contig']
                contigs[compContigIndex] = None

    def newContig_singleRead(readIndex):
        read = allReads[readIndex]
        newContig = {
                        'locations':{ readIndex: 0 },
                        'contig': read
                    }
        contigIndex = len(contigs)
        contigs.append( newContig )
        readLocations[readIndex] = contigIndex


    for match in sortedMatches:
        #pdb.set_trace()
        comp = match[0]
        target = match[1]
        matchLoc = match[2]
        matchLen = match[3]
        if readLocations[comp] == None:
            if readLocations[target] == None:
                newContig(comp,target,matchLoc)
            else:
                updateContig_targetExists(comp,target,matchLoc)
        else:
            if readLocations[target] == None:
                updateContig_compExists(comp,target,matchLoc)
            else:
                if readLocations[target] != readLocations[comp]:
                    combineContigs(comp,target,matchLoc)
    for i in range(n_reads):
        if readLocations[i] == None:
            newContig_singleRead(i)


    return contigs

def contigFilter(contigs):
    return list(filter(lambda x: x != None, contigs))

def getN50(contigs):
    n_contigs = len(contigs)
    lengths = [None]*n_contigs
    for idx, contig in enumerate(contigs):
        lengths[idx] =  len(contig['contig'])
    lengths.sort(reverse=True)

    halfLength = sum(lengths)/2
    n = 0
    i=0
    while n < halfLength:
        n += lengths[i]
        i += 1
    return i

def getRawContigs(contigs):
    n_contigs = len(contigs)
    rawContigs = [None]*n_contigs
    for i in range(n_contigs):
        rawContigs[i] = contigs[i]['contig']
    return rawContigs



def align(allReads,wl=7):
    toWord = getToWordArray(wl)

    start = time.time()
    print("Getting words from reads...")
    allWords = getAllWords_A(allReads,toWord,wordLength=wl)
    print(time.time() - start)
    print("len(allWords):\t" + str(len(allWords)))

    start = time.time()
    print("Getting hits from words...")
    allWordHits = getWordHits_A(allWords)
    print(time.time() - start)
    print("len(allWordHits):\t" + str(len(allWordHits)))

    start = time.time()
    print("Getting matches from hits...")
    allMatches = getAllMatches(allWordHits, allWords, wl)
    print(time.time() - start)

    start = time.time()
    print("Sorting matches...")
    allMatches = sortMatches(allMatches)
    print(time.time() - start)
    print("len(allMatches):\t" + str(len(allMatches)))

    start = time.time()
    print("Aligning reads...")
    contigs = alignReads(allReads, allMatches)
    print(time.time() - start)

    print("Filtering Contigs...")
    contigs = contigFilter(contigs)

    print("Getting N50...")
    n50 = getN50(contigs)

    print("Getting Raw Contigs...")
    rawContigs = getRawContigs(contigs)

    return (rawContigs, n50)
