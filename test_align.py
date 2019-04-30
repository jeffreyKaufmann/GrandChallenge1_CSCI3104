import unittest
import align
import numpy as np
import pdb

class testAlignMethods(unittest.TestCase):

    def setUp(self):
        self.toWord7 = align.getToWordArray(7)
        self.toWord9 = align.getToWordArray(9)

        self.read1 = np.array([0,1,2,3,0,1,2,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2])
        self.read2 = np.array([0,1,2,3,0,1,2,3,0,1,2,3])
        self.read3 = np.array([0,0,0,0,0,0,0,0,0,0,0,0])
        self.read4 = np.array([0,1,2,3,0,1,2,3,0,1,2,3])
        self.read5 = np.array([1,1,1,1,1,1,1,1,1,1,1,1])
        pass


    def test_getToWordArray(self):
        toWord5 = np.array([1,4,16,64,256])
        toWord7 = np.array([1,4,16,64,256,1024,4096])
        toWord8 = np.array([1,4,16,64,256,1024,4096,16384])

        self.assertTrue(all( align.getToWordArray(5) == toWord5 ))
        self.assertTrue(all( align.getToWordArray(7) == toWord7 ))
        self.assertTrue(all( align.getToWordArray(8) == toWord8 ))

    def test_getWordByIndex_A(self):
        read1 = self.read1
        toWord7 = self.toWord7
        toWord9 = self.toWord9

        word1_a = np.matmul( [0,1,2,3,0,1,2], toWord7 )
        word1_b = np.matmul( [0,1,2,3,0,1,2,3,2], toWord9 )
        word1_c = np.matmul( [0,1,2,3,2,2,2], toWord7 )

        self.assertEqual( align.getWordByIndex_A(read1, 0, toWord7, 7) , word1_a )
        self.assertEqual( align.getWordByIndex_A(read1, 0, toWord9, 9) , word1_b )
        self.assertEqual( align.getWordByIndex_A(read1, 4, toWord7, 7) , word1_c )

    def test_getEveryWord_A(self):
        toWord7 = self.toWord7
        read2 = self.read2

        words = np.array( [ 9444, 14649, 3662, 5011, 9444, 14649 ] )

        self.assertTrue(all( align.getEveryWord_A(read2, toWord7, wordLength=7) == words ))

    def test_getAllWords_A(self):
        reads = [ self.read2, self.read3, self.read4, self.read5 ]
        words2 = np.array( [ 9444, 14649, 3662, 5011, 9444, 14649 ] )
        words3 = np.array( [ 0, 0, 0, 0, 0, 0 ] )
        words4 = np.array( [ 9444, 14649, 3662, 5011, 9444, 14649 ] )
        words5 = np.array( [ 5461, 5461, 5461, 5461, 5461, 5461] )
        toWord7 = self.toWord7

        allWords_calc = [ words2, words3, words4, words5 ]
        allWords_test = align.getAllWords_A(reads,toWord7, 7)

        for i in range(4):
            self.assertTrue(all( allWords_calc[i] == allWords_test[i] ))

    def test_getWordHits_A(self):
        reads = [ self.read1, self.read2, self.read3, self.read4, self.read5 ]
        allWords = align.getAllWords_A(reads, self.toWord7, 7)
        wordHits = [    [0,1,[0]], [0,3,[0]],
                        [1,0,[0,4]], [1,3,[0,4]],
                        [3,0,[0,4]], [3,1,[0,4]]
                   ]

        self.assertEqual( align.getWordHits_A(allWords), wordHits )

    def test_isMatch_fromWords(self):
        read1 = np.array([0,1,2,3,0,1,2,3,2,2,2,2])
        reads = [ read1, self.read2, self.read3, self.read4, self.read5 ]
        allWords = align.getAllWords_A(reads, self.toWord7, 7)

        self.assertFalse(align.isMatch_fromWords(0,1,0,allWords,7))
        self.assertFalse(align.isMatch_fromWords(0,3,0,allWords,7))
        self.assertTrue(align.isMatch_fromWords(1,3,0,allWords,7))
        self.assertTrue(align.isMatch_fromWords(1,3,4,allWords,7))
        self.assertFalse(align.isMatch_fromWords(3,0,0,allWords,7))
        self.assertTrue(align.isMatch_fromWords(3,0,4,allWords,7))
        '''
        allWords2 = [np.array([ 4665, 13454,  7459, 10056,  2514,  4724, 13469, 15655,  8009, 10194]), np.array([13469, 15655,  8009, 10194,  2548, 12925, 15519, 12071,  7113, 9970, 14780,  3695,  9115,  2278,  4665]), np.array([ 2360,  8782, 14483,  7716, 10121, 14818,  3704,  9118,  2279, 4665, 13454,  7459]), np.array([ 7459, 10056,  2514,  4724, 13469, 15655,  8009, 10194,  2548, 12925, 15519]), np.array([10111,  2527,  4727, 13469, 15655,  8009, 10194,  2548, 12925, 15519, 12071,  7113,  9970, 14780, 3695,  9115,  2278,  4665, 13454,  7459, 10056]), np.array([10056,  2514,  4724, 13469, 15655,  8009, 10194,  2548, 12925, 15519, 12071,  7113,  9970, 14780,  3695,  9115,  2278,  4665, 13454,  7459, 10056]), np.array([13469, 15655,  8009, 10194,  2548, 12925, 15519, 12071,  7113, 9970, 14780,  3695,  9115,  2278]), np.array([13454,  7459, 10056,  2514,   628,  8349, 10279, 14857,  7810, 14240, 11752,  2938,   734,  4279, 13357, 11531]), np.array([ 4279, 13357, 11531, 15170,  3792,   948,  8429,  2107,  4622])]

        align.isMatch_fromWords(1,6,0,allWords2,7)
        '''

    '''
    def test_isMatch_fromChars(self):
        read1 = self.read1
        read2 = self.read2
        read3 = self.read3
        read4 = self.read4
        read5 = self.read5

        self.assertFalse(align.isMatch_fromChars(read1,read2,0))
        self.assertFalse(align.isMatch_fromChars(read1,read4,0))
        self.assertTrue(align.isMatch_fromChars(read2,read4,0))
        self.assertTrue(align.isMatch_fromChars(read2,read4,4))
        self.assertFalse(align.isMatch_fromChars(read4,read1,0))
        self.assertTrue(align.isMatch_fromChars(read4,read1,4))
    '''

    def test_getAllMatches(self):
        read1 = np.array([0,1,2,3,0,1,2,3,2,2,2,2])
        reads = [read1, self.read2, self.read3, self.read4, self.read5]
        toWord7 = self.toWord7
        allWords = align.getAllWords_A(reads, toWord7, 7)
        wordHits = [    [0,1,[0]], [0,3,[0]],
                        [1,0,[0,4]], [1,3,[0,4]],
                        [3,0,[0,4]], [3,1,[0,4]]
                   ]
        matches = [     [1,0,4,8],
                        [1,3,0,12], [1,3,4,8],
                        [3,0,4,8],
                        [3,1,0,12], [3,1,4,8]
                  ]

        self.assertEqual( align.getAllMatches(wordHits, allWords, 7), matches )

    def test_sortMatches(self):
        unsorted = [ [0,1,7,7], [1,2,3,13], [5,1,6,20], [9,2,13,2] ]
        sorted = [ [5,1,6,20], [1,2,3,13], [0,1,7,7], [9,2,13,2] ]
        self.assertEqual( align.sortMatches(unsorted), sorted)




    def test_alignReads(self):
        A = [1,2,3,0,2,0,1,3,1,2,0,1,3,3,1,2]
        B =             [1,3,1,2,0,1,3,3,1,2,0,3,3,2,1,2,3,0,2,0,1]
        reads = [ A, B ]
        matches = [ [0,1,6,10] ]
        contig1 = {
                    'locations':{ 0:0, 1:6 },
                    'contig': A[0:6] + B
                  }
        contigs = [ contig1 ]
        self.assertEqual( align.alignReads(reads, matches), contigs )


        C = [0,2,3,0,1,2,0,2,3,1,2,3,0,2,0,1,3,1]
                        # A = [1,2,3,0,2,0,1,3,1,2,0,1,3,3,1,2]
        reads = [ A, B, C ]
        matches = [ [0,1,6,10], [2,0,9,9] ]
        contig1 = {
                    'locations':{ 0:9, 1:15, 2:0 },
                    'contig': C[0:9] + A[0:6] + B
                  }
        contigs = [ contig1 ]
        self.assertEqual( align.alignReads(reads, matches), contigs )


        D =       [3,0,2,0,1,3,1,2,0,1,3,3,1,2,0,3,3]
        # A = [1,2,3,0,2,0,1,3,1,2,0,1,3,3,1,2]
        # B =             [1,3,1,2,0,1,3,3,1,2,0,3,3,2,1...
        reads = [ A, B, C, D ]
        matches = [ [0,1,6,10], [2,0,9,9], [3,1,4,1] ]
        contig1 = {
                    'locations':{ 0:9, 1:15, 2:0, 3:11 },
                    'contig': C[0:9] + A[0:6] + B
                  }
        contigs = [ contig1 ]
        self.assertEqual( align.alignReads(reads, matches), contigs )


        E =         [3,3,3,1,3,1,2,0,1,3,3,1,2,0,3,3,2,1,2,3,0,2,0,1,3,1,2]
        # A = [1,2,3,0,2,0,1,3,1,2,0,1,3,3,1,2]
        # B =             [1,3,1,2,0,1,3,3,1,2,0,3,3,2,1,2,3,0,2,0,1]
        reads = [ A, B, C, D, E ]
        matches = [ [0,1,6,10], [2,0,9,9], [3,1,4,1], [4,1,3,21] ]
        contig1 = {
                    'locations':{ 0:9, 1:15, 2:0, 3:11 },
                    'contig': C[0:9] + A[0:6] + B
                  }
        contig2 = {
                    'locations':{ 4:0 },
                    'contig': E
                  }
        contigs = [ contig1, contig2 ]
        self.assertEqual( align.alignReads(reads, matches), contigs )


        F =         [0,2,0,1,3,1,2,0,1,3,3,1,2,0,3,3,2,1,2,3,0,2,0,1,3,1,2]
        # A = [1,2,3,0,2,0,1,3,1,2,0,1,3,3,1,2]
        # B =             [1,3,1,2,0,1,3,3,1,2,0,3,3,2,1,2,3,0,2,0,1]
        reads = [ A, B, C, D, E, F ]
        matches = [ [0,1,6,10], [2,0,9,9], [3,1,4,1], [4,1,3,21], [5,1,3,21] ]
        contig1 = {
                    'locations':{ 0:9, 1:15, 2:0, 3:11, 5:12  },
                    'contig': C[0:9] + A[0:6] + B + [3,1,2]
                  }
        contig2 = {
                    'locations':{ 4:0 },
                    'contig': E
                  }
        contigs = [ contig1, contig2 ]
        self.assertEqual( align.alignReads(reads, matches), contigs )


        G =        [1,3,1,2,0,1,3,3,1,2,0,3,3,2,1,2,3,0,2,0]
        #F = [0,2,0,1,3,1,2,0,1,3,3,1,2,0,3,3,2,1,2,3,0,2,0,1,3,1,2]
        reads = [ A, B, C, D, E, F, G]
        matches = [ [0,1,6,10], [2,0,9,9], [3,1,4,1], [4,1,3,21], [5,1,3,21],
                    [5,6,3,20], ]
        contig1 = {
                    'locations':{ 0:9, 1:15, 2:0, 3:11, 5:12, 6:15 },
                    'contig': C[0:9] + A[0:6] + B + [3,1,2]
                  }
        contig2 = {
                    'locations':{ 4:0 },
                    'contig': E
                  }
        contigs = [ contig1, contig2 ]
        self.assertEqual( align.alignReads(reads, matches), contigs )


        # F = ... 2,3,0,2,0,1,3,1,2]
        H =      [2,3,0,2,0,1,3,1,2,0,0,2,2,3,1,3,2,0,0,1,3,2] #7
        I =                                [3,1,3,2,0,0,1,3,2,3,0,0,2,0,1]

        reads = [ A, B, C, D, E, F, G, H, I ]
        matches = [ [0,1,6,10], [2,0,9,9], [3,1,4,1], [4,1,3,21], [5,1,3,21],
                    [5,6,3,20], [7,8,13,9]]
        contig2 = {
                    'locations':{ 7:0, 8:13 },
                    'contig': H[0:13] + I
                  }
        contig3 = {
                    'locations':{ 4:0 },
                    'contig': E
                  }
        contigs = [ contig1, contig2, contig3 ]
        self.assertEqual( align.alignReads(reads, matches), contigs)

        matches = [ [0,1,6,10], [2,0,9,9], [3,1,4,1], [4,1,3,21], [5,1,3,21],
                    [5,6,3,20], [7,8,13,9], [5,7,18,9]]
        contig1 = {
                    'locations':{ 0:9, 1:15, 2:0, 3:11, 5:12, 6:15, 7:30, 8:43 },
                    'contig': C[0:9] + A[0:6] + B + H[6:13] + I
                  }
        contigs = [ contig1, None, contig3 ]
        self.assertEqual( align.alignReads(reads, matches) , contigs)

        ## TODO: test case for opposite-oriented comp & target - combineContigs
        ## TODO: test case for different word length


if __name__ == '__main__':
    unittest.main()
