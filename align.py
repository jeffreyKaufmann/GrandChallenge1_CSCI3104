from parse import parsingFunc
import numpy as np
import pdb
import time

#print(parsingFunc("FQ/rand.500.fa"))

def listsToArrays(reads):
    for i in reads:
        i = np.array(reads)
    return reads


#converts a list of ints (between 0 and 4) to a single base-4 int, for easy comparison
def intsToWord(ints):
    base = 4
    word = 0
    for i in range(len(ints)):
        word += ints[i]*(base**i)
    return word

def getFirstWord(read, wordLength =7):
    return intsToWord( read[0:wordLength] )

def getLastWord(read, wordLength=7):
    readLength = len(read)
    return intsToWord( read[(readLength - wordLength) : readLength] )

def getWordByIndex(read, index, wordLength=7):
    return intsToWord( read[index : (index + wordLength)] )

def getAllWords_asList(read, wordLength=7):
    readLength = len(read)
    words = []
    for index in range(readLength - wordLength + 1):
        words.append(intsToWord( read[index : (index + wordLength)] ))
    return words

# We want to use arrays because they are much faster to search than lists
def getAllWords_asArray(read, wordLength=7):
    return np.array(getAllWords_asList(read, wordLength))

def getAllWordsList(reads, wordLength=7):
    allWordsList = []
    for read in reads:
        allWordsList.append(getAllWords_asArray(read,wordLength))
    return allWordsList

# This can take reads of varying sizes!!!
# Outputs in format [match_1, match_2, ...]
# Where match_n = [ comp, target, [matchLoc_1, matchLoc_2, ...]]
# Where matchLoc_n is the index in comp that matches the beginning of target
# Note that comp and target in match_n are indicies of allReads
def getWordMatches(allReads, getAllWordsList): ## TODO: rename matches to hits
    n_R = len(allReads)
    wordHits = []

    for compIndex in range(n_R):
        #compRead = allWords[compIndex]
        compWords = getAllWordsList[compIndex]
        #wordHits.append([])
        for targetIndex in range(n_R):
            targetRead = allReads[targetIndex]
            targetWord = getFirstWord(targetRead) #TODO: Should this pull from getAllWordsList ??

            matches = ( np.where(compWords == targetWord)[0] ).tolist()
            if matches != [] and targetIndex != compIndex:
                wordHits.append([ compIndex, targetIndex, matches])

    return wordHits

#This can take reads of varying sizes!!
def isMatch(comp, target, startIndex):
    compLen = len(comp)
    targetLen = len(target)
    searchLen = min(targetLen, compLen - startIndex)
    searchTo = startIndex + searchLen
    #match = all( [ comp[j] == target[j-startIndex] for j in range(startIndex,searchTo)] ) ## TODO: speed this up
    match = True
    for j in range(startIndex,searchTo):
        if comp[j] != target[j-startIndex]:
            match = False
            break
    return ( match, searchLen )

def isMatch_list(comp, target, startIndex): ## TODO: Convert all isMatch to list (?)
    compLen = len(comp)
    targetLen = len(target)
    searchLen = min(targetLen, compLen - startIndex)
    searchTo = startIndex + searchLen
    match = all( [ comp[j] == target[j-startIndex] for j in range(startIndex,searchTo)] )
    return [ match, searchLen ]


# This can take reads of varying sizes!!
# This returns matches = [match_1, match_2, ...]
# Where match_n = [compIndex, targetIndex, matchIndex, matchLength]
def getMatchesFromHits(allReads, allWordHits):
    matches = []
    for wordHits in allWordHits:
        comp = allReads[wordHits[0]]
        target = allReads[wordHits[1]]
        for hit in wordHits[2]:
            matchResult = isMatch(comp,target, hit)
            if matchResult[0]:
                matches.append([ wordHits[0], wordHits[1], hit, matchResult[1] ])
                break
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
            [ isMatch, addLen ] = isMatch_list(compRead,contig['contig'],matchLoc)
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
                isMatch = isMatch_list(contig['contig'],compRead,compLocInContig)[0]

                #if comp isn't not a match, we ignore it
                if isMatch:
                    contig['locations'][comp] = compLocInContig
                    contig['contig'] = contig['contig'][0:compLocInContig] + compRead
                    readLocations[comp] = contigIndex
            else:
                isMatch = isMatch_list(contig['contig'],compRead,compLocInContig)[0]
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
        isMatch = isMatch_list(contig['contig'], targetRead, targetLocInContig)
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
            [ isMatch, matchLen ] = isMatch_list(compContig['contig'],
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
            [ isMatch, matchLen ] = isMatch_list(targetContig['contig'],
                                                 compContig['contig'],
                                                 contigStartDiff)
            if isMatch:
                for read in compContig['locations']:
                    targetContig['locations'][read] = compContig['locations'][read] + contigStartDiff
                    readLocations[read] = targetContigIndex
                if targetContigEndFromMatch < compContigEndFromMatch:
                    targetContig['contig'] = targetContig['contig'][0:targetLocInTargetContig] + compContig['contig']
                contigs[compContigIndex] = None


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

    return contigs

def contigFilter(contigs):
    return list(filter(lambda x: x != None, contigs))


def align(allReads,wl=7):
    pdb.set_trace()

    start = time.time()
    print("Getting words from reads...")
    allWords = getAllWordsList(allReads,wordLength=wl)
    print(time.time() - start)
    print("len(allWords):\t" + str(len(allWords)))
    pdb.set_trace()

    start = time.time()
    print("Getting hits from words...")
    allWordHits = getWordMatches(allReads, allWords)
    print(time.time() - start)
    print("len(allWordHits):\t" + str(len(allWordHits)))

    start = time.time()
    print("Getting matches from hits...")
    allMatches = getMatchesFromHits(allReads, allWordHits)
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
    print(contigs)

    print("Finishing up...")
    contigs = contigFilter(contigs)
    return contigs



'''
reads = parsingFunc("FQ/rand.500.fa")
print( reads[0] )

for i in range(500):
    parentWords = []
    for
'''
