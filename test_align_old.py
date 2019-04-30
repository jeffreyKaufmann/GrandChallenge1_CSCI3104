import unittest
import align_old as align
import numpy as np

class testAlignMethods(unittest.TestCase):

    def setUp(self):
        #self.maxDiff = None

        self.A = [0,0,0,0,0,0,0]
        self.B = [1,1,1,1,1,1,1]
        self.C = [1,2,3,0,1,0,3]
        self.D = [3,1,2,0,3,3,2]

        self.E = [0] * 500
        self.F = [1] * 500
        self.G = [1, 3, 1, 1, 3, 2, 1, 1, 1, 2, 2, 1, 1, 3, 1, 3, 3, 3, 3, 0, 0, 3, 0, 2, 2, 3, 1, 2, 3, 2, 0, 2, 1, 0, 0, 1, 2, 3, 3, 0, 0, 3, 0, 0, 1, 1, 0, 2, 2, 0, 3, 1, 1, 0, 1, 3, 0, 2, 0, 1, 0, 3, 3, 3, 0, 3, 0, 3, 0, 1, 1, 1, 0, 0, 3, 3, 0, 2, 2, 3, 3, 2, 2, 0, 1, 2, 2, 2, 0, 1, 2, 3, 0, 1, 1, 1, 2, 1, 0, 0, 3, 3, 0, 0, 0, 1, 1, 3, 2, 1, 0, 2, 2, 0, 1, 3, 3, 1, 1, 1, 3, 0, 2, 2, 2, 3, 3, 1, 3, 1, 0, 2, 2, 3, 0, 3, 2, 1, 3, 0, 1, 0, 2, 2, 3, 2, 1, 1, 1, 0, 0, 1, 0, 0, 0, 3, 1, 1, 2, 1, 2, 1, 3, 1, 1, 1, 0, 0, 2, 0, 3, 1, 1, 1, 3, 3, 0, 1, 2, 0, 1, 0, 3, 3, 2, 2, 1, 0, 2, 1, 1, 0, 2, 1, 1, 1, 0, 3, 1, 2, 1, 0, 3, 3, 3, 0, 3, 1, 1, 1, 3, 2, 2, 3, 0, 3, 0, 2, 1, 0, 3, 1, 3, 1, 2, 3, 0, 2, 3, 3, 1, 1, 3, 2, 1, 0, 0, 3, 1, 1, 1, 0, 2, 2, 1, 2, 0, 1, 2, 2, 3, 2, 1, 2, 2, 1, 2, 2, 0, 0, 3, 0, 3, 2, 0, 3, 3, 1, 2, 2, 0, 3, 0, 1, 1, 3, 1, 0, 0, 3, 1, 0, 3, 0, 3, 1, 2, 3, 2, 0, 1, 0, 2, 2, 2, 0, 2, 1, 1, 0, 0, 3, 3, 1, 0, 2, 1, 1, 2, 0, 2, 2, 0, 2, 2, 0, 2, 0, 2, 0, 1, 3, 2, 1, 0, 2, 2, 3, 0, 0, 2, 0, 3, 1, 0, 1, 2, 3, 2, 3, 1, 2, 3, 1, 0, 3, 2, 1, 2, 3, 0, 0, 0, 2, 3, 1, 2, 1, 1, 0, 1, 0, 2, 1, 2, 2, 2, 3, 3, 3, 0, 2, 3, 1, 3, 1, 0, 3, 0, 1, 3, 2, 1, 3, 0, 2, 0, 2, 1, 0, 2, 0, 0, 1, 3, 2, 0, 1, 0, 1, 3, 0, 1, 0, 0, 3, 0, 0, 2, 1, 2, 1, 0, 0, 3, 3, 1, 3, 1, 3, 3, 3, 2, 0, 3, 2, 1, 2, 1, 3, 2, 0, 0, 1, 0, 0, 1, 1, 1, 0, 2, 2, 0, 0, 0, 2, 2, 3, 2, 1, 0, 0, 1, 0, 0, 1, 2, 0, 2, 3, 3, 2, 2, 2, 2, 3, 2, 3, 3, 2, 3, 3, 3, 2, 3, 2, 0, 1, 2, 2, 1, 0, 0, 0, 0, 2, 2, 1, 2, 0, 0, 3, 3, 3, 0, 2, 3, 3, 3, 3]

        self.H = [3,1,2,0,3,3,2,1,2]

        self.I = [1,2,0,1,3,3,1,2,0,3,3,2,1,2]
        self.J =               [2,0,3,3,2,1,2,3,3,3,1,2,3,1,0,0]
        self.K =                     [3,2,1,2,3,3,3,1,2,3,1,0,0,3,2,4,2]
        self.L = [0] * 25

                       #self.I = [1,2,0,1,3,3,1,2,0,3,3,2,1,2]
        self.M = [1,2,3,0,2,0,1,3,1,2,0,1,3,3,1,2]
        self.N =             [1,3,1,2,0,1,3,3,1,2,0,3,3,2,1,2,3,0,2,0,1]
                                               #self.M = [1,2,3,0,2,0,1,3,1,2,0,1,3,3,1,2]
        self.O = [1,2,3,0,0,2,3,1,3,2,0,2,0,3,1,3]
                    # = = = = = = = = = = = = = x
        self.P =     [3,0,0,2,3,1,3,2,0,2,0,3,1,0,0,0]
        self.Q =                 [3,2,0,2,0,3,1,0,0,0,1,2,0,1,3,3,1,2,3,2]
                                                    # = = = = = = = = x x
                                           #self.I = [1,2,0,1,3,3,1,2,0,3,3,2,1,2]
        pass


    def test_listsToArrays(self):
        lists = [self.A, self.B, self.C, self.D]
        arrays = [np.array(self.A), np.array(self.B), np.array(self.C), np.array(self.D)]
        self.assertTrue( all([ (lists[i] == arrays[i]).all() for i in range(len(lists))]) )

        arrays[0] = np.array(self.D)
        self.assertFalse( all([ (lists[i] == arrays[i]).all() for i in range(len(lists))]) )


    def test_intsToWord(self):
        self.assertEqual( align.intsToWord(self.A), 0 )
        self.assertEqual( align.intsToWord(self.B), 5461 )
        self.assertEqual( align.intsToWord(self.C), 12601 )
        self.assertEqual( align.intsToWord(self.D), 12071 )

    def test_getFirstWord(self):
        self.assertEqual( align.getFirstWord(self.A), align.intsToWord(self.A) )
        self.assertEqual( align.getFirstWord(self.D), align.intsToWord(self.D) )

        self.assertEqual( align.getFirstWord(self.E), align.intsToWord(self.A) )
        self.assertEqual( align.getFirstWord(self.F), align.intsToWord(self.B) )
        self.assertEqual( align.getFirstWord(self.G), align.intsToWord([1, 3, 1, 1, 3, 2, 1]) )

    def test_getLastWord(self):
        self.assertEqual( align.getLastWord(self.A), align.intsToWord(self.A) )
        self.assertEqual( align.getLastWord(self.D), align.intsToWord(self.D) )

        self.assertEqual( align.getLastWord(self.E), align.intsToWord(self.A) )
        self.assertEqual( align.getLastWord(self.F), align.intsToWord(self.B) )
        self.assertEqual( align.getLastWord(self.G), align.intsToWord([3, 0, 2, 3, 3, 3, 3]) )

    def test_getWordByIndex(self):
        self.assertEqual( align.getWordByIndex(self.D, 0), align.intsToWord(self.D) )

        self.assertEqual( align.getWordByIndex(self.G, 0), align.getFirstWord(self.G) )
        self.assertEqual( align.getWordByIndex(self.G, 500-7), align.getLastWord(self.G) )
        self.assertEqual( align.getWordByIndex(self.G, 2), align.intsToWord([1, 1, 3, 2, 1, 1, 1]) )

    def test_getAllWords_asList(self):
        self.assertEqual( align.getAllWords_asList(self.A), [align.intsToWord(self.A)] )
        self.assertEqual( align.getAllWords_asList(self.A + [0]), [align.intsToWord(self.A), align.intsToWord(self.A)] )

        h = [ align.intsToWord(self.H[0:7]), align.intsToWord(self.H[1:8]), align.intsToWord(self.H[2:9])]
        self.assertEqual( align.getAllWords_asList(self.H), h)

        g = align.getAllWords_asList(self.G)
        for i in range(len(g)):
            self.assertEqual( g[i], align.getWordByIndex(self.G, i))

    def test_getAllWords_asArray(self):
        pass

    def test_getAllWordsList(self):
        ABCD = [ self.A, self.B, self.C, self.D ]
        abcd = [ align.getAllWords_asArray(self.A),
                 align.getAllWords_asArray(self.B),
                 align.getAllWords_asArray(self.C),
                 align.getAllWords_asArray(self.D) ]
        self.assertEqual( align.getAllWordsList(ABCD), abcd)

    def test_getWordMatches(self):
        IJKL = [self.I,self.J,self.K,self.L]
        IJKL_wl = align.getAllWordsList(IJKL)
        ijkl = [ [0,1,[7]], [1,2,[3]] ]
        self.assertEqual(align.getWordMatches(IJKL, IJKL_wl), ijkl)

        IMN = [self.I,self.M,self.N]
        IMN_wl = align.getAllWordsList(IMN)
        imn = [ [1,0,[8]], [1,2,[6]], [2,0,[2]], [2,1,[14]] ]
        self.assertEqual(align.getWordMatches(IMN, IMN_wl), imn)

    def test_isMatch(self):
        self.assertEqual( align.isMatch(self.J, self.K, 3), (True, 13) )
        self.assertEqual( align.isMatch(self.J, self.K, 2), (False, 14) )
        self.assertEqual( align.isMatch(self.O, self.P, 2), (False, 14) )

    def test_getMatchesFromHits(self):
        OPQI = [ self.O, self.P, self.Q, self.I ]
        OPQI_hits = align.getWordMatches(OPQI, align.getAllWordsList(OPQI))
        opqi = [ [1,2,6,10] ]
        self.assertEqual( align.getMatchesFromHits(OPQI,OPQI_hits), opqi )

        IJKL = [self.I,self.J,self.K,self.L]
        IJKL_hits = align.getWordMatches(IJKL, align.getAllWordsList(IJKL))
        ijkl = [ [0,1,7,7], [1,2,3,13] ]
        self.assertEqual( align.getMatchesFromHits(IJKL,IJKL_hits), ijkl )

    def test_sortMatches(self):
        unsorted_1 = [ [0,1,7,7], [1,2,3,13], [5,1,6,20], [9,2,13,2] ]
        sorted_1 = [ [5,1,6,20], [1,2,3,13], [0,1,7,7], [9,2,13,2] ]
        self.assertEqual( align.sortMatches(unsorted_1), sorted_1)

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
        # contig shouldn't change
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
        contigs = [ contig1 ]
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
        contigs = [ contig1 ]
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
        contigs = [ contig1, contig2 ]
        self.assertEqual( align.alignReads(reads, matches), contigs)

        matches = [ [0,1,6,10], [2,0,9,9], [3,1,4,1], [4,1,3,21], [5,1,3,21],
                    [5,6,3,20], [7,8,13,9], [5,7,18,9]]
        contig1 = {
                    'locations':{ 0:9, 1:15, 2:0, 3:11, 5:12, 6:15, 7:30, 8:43 },
                    'contig': C[0:9] + A[0:6] + B + H[6:13] + I
                  }
        contigs = [ contig1, None]
        self.assertEqual( align.alignReads(reads, matches) , contigs)

        ## TODO: test case for opposite-oriented comp & target - combineContigs
        ## TODO: test case for different word length


    def test_contigFilter(self):
        A = [1,2,3,0,2,0,1,3,1,2,0,1,3,3,1,2]
        B = [1,3,1,2,0,1,3,3,1,2,0,3,3,2,1,2,3,0,2,0,1]
        C = [0,2,3,0,1,2,0,2,3,1,2,3,0,2,0,1,3,1]
        H = [2,3,0,2,0,1,3,1,2,0,0,2,2,3,1,3,2,0,0,1,3,2]
        I = [3,1,3,2,0,0,1,3,2,3,0,0,2,0,1]

        contig1 = {
                    'locations':{ 0:9, 1:15, 2:0, 3:11, 5:12, 6:15, 7:30, 8:43 },
                    'contig': C[0:9] + A[0:6] + B + H[6:13] + I
                  }
        contig2 = {
                    'locations':{ 7:0, 8:13 },
                    'contig': H[0:13] + I
                  }
        contigs = [ contig1, None, None, contig2, contig2, None, None ]
        filtered = [ contig1, contig2, contig2 ]
        self.assertEqual( align.contigFilter(contigs), filtered )


if __name__ == '__main__':
    unittest.main()
