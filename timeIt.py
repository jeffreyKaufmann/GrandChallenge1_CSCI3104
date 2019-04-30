import timeit

print("getWords:")

npSetup = '''
import numpy as np
toWord = np.array([1,4,16,64,256,1024,4096])
test = np.array([1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0])
wordLen = len(toWord)
testLen = len(test)
'''
npCode = '''
for i in range(testLen - wordLen):
    a = np.matmul(toWord, test[i:i+wordLen])
'''
print( timeit.timeit(setup=npSetup, stmt=npCode, number=100000))

listSetup = '''
import numpy as np
toWord = [1,4,16,64,256,1024,4096]
test = [1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0]
wordLen = len(toWord)
testLen = len(test)
'''
listCode = '''
for i in range(testLen - wordLen):
    a = 0
    for j in range(wordLen):
        a += ( test[i+j] * (4**j) )
'''
print( timeit.timeit(setup=listSetup, stmt=listCode, number=100000))




print("wordHits:")

npSetup = '''
import numpy as np
toWord = np.array([1,4,16,64,256,1024,4096])
test = np.array([1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0])
wordLen = len(toWord)
testLen = len(test)
'''
npCode = '''
a = np.where(test == 1)
'''
print( timeit.timeit(setup=npSetup, stmt=npCode, number=100000))

listSetup = '''
import numpy as np
toWord = [1,4,16,64,256,1024,4096]
test = [1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0]
wordLen = len(toWord)
testLen = len(test)
'''
listCode = '''
[ i==1 for i in test]
'''
print( timeit.timeit(setup=listSetup, stmt=listCode, number=100000))




print("hitIsMatch:")

npSetup = '''
import numpy as np
toWord = np.array([1,4,16,64,256,1024,4096])
test1 = np.array([1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0])
test2 = np.array([1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0])
test3 = np.array([1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3])
'''
npCode = '''
a = np.array_equal(test1,test2)
a = np.array_equal(test2,test3)
'''
print( timeit.timeit(setup=npSetup, stmt=npCode, number=100000))

listSetup = '''
import numpy as np
toWord = [1,4,16,64,256,1024,4096]
test1 = [1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0]
test2 = [1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0]
test3 = [1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3]
'''
listCode = '''
a = test1 == test2
a = test2 == test3
'''
print( timeit.timeit(setup=listSetup, stmt=listCode, number=100000))




print("slice:")

npSetup = '''
import numpy as np
test1 = np.array([1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0])
'''
npCode = '''
a = test1[0:10]
'''
print( timeit.timeit(setup=npSetup, stmt=npCode, number=100000))

listSetup = '''
test1 = [1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0]
'''
listCode = '''
a = test1[0:10]
'''
print( timeit.timeit(setup=listSetup, stmt=listCode, number=100000))




print("combine:")

npSetup = '''
import numpy as np
toWord = np.array([1,4,16,64,256,1024,4096])
test1 = np.array([1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0])
test2 = np.array([1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0])
test3 = np.array([1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3])
'''
npCode = '''
a = np.append(test2,test3)
'''
print( timeit.timeit(setup=npSetup, stmt=npCode, number=100000))

listSetup = '''
import numpy as np
toWord = [1,4,16,64,256,1024,4096]
test1 = [1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0]
test2 = [1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0]
test3 = [1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3]
'''
listCode = '''
a = test2 + test3
'''
print( timeit.timeit(setup=listSetup, stmt=listCode, number=100000))




print("Accessing Tuples vs Lists:")

tupleSetup = '''
import numpy as np
test1 = np.array([1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0])
test2 = np.array([1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0])
test3 = np.array([1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3])
t = ( test1, test2, test3 )
'''
tupleCode = '''
a = t[0][3]
a = t[1][10]
a = t[2][15]
'''
print( timeit.timeit(setup=tupleSetup, stmt=tupleCode, number=100000))

listSetup = '''
import numpy as np
test1 = np.array([1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0])
test2 = np.array([1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,0])
test3 = np.array([1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3,0,2,1,3,1,3,0,1,3,2,0,3,2,1,3,2,0,0,2,3,1,3])
t = [ test1, test2, test3 ]
'''
listCode = '''
a = t[0][3]
a = t[1][10]
a = t[2][15]
'''
print( timeit.timeit(setup=listSetup, stmt=listCode, number=100000))
