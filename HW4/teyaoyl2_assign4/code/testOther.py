from collections import Counter
import sys
import random

#inFile = sys.argv[1]
#outFile = sys.argv[2]

#print 1.0+0.5**2
#print 2.0*(0.5**2)+1.0
testList = [1,'a',4]
print(testList)

'''
print [1,2,3,4] == [1,2,4,3]

a= [2,1,3,4,5]
print a.index(min(a))


#print 'infile=',inFile,'outfile=',outFile
testApist = []
testApist.append(1)
testApist.append([])


# print testApist
'''
'''
testList = [1,2,3,4,5,6]
print len(testList)/2
result = random.sample(testList,len(testList)/3)
print result
attNameindex = [testList.index(value) for value in  result]
print attNameindex

print int(2/1.5)

def countVal(orgDic,countDic):
    for val in orgDic.values():
        if type(val) == type({}):
            countDic = countVal(val,countDic)
        else:
            if val not in countDic:
                countDic[val] = 0
            countDic[val] += 1
    return countDic



#print  Counter({'red': 4, 'blue': 2})
'''

dic = {7:7,1:1,2:2,4:3,3:3}
#print max(dic.keys())

testCpountList = [2,1,1,1,1,1,2,1,3,5,7,3,7,7,7,7,7]
# print Counter(testCpountList).most_common()
# print Counter(testCpountList).most_common()[0][0]

'''
infile = open('./train_file/balance-scale.train.test', 'r')
outfile = open('./train_file/R_balance-scale.train.test', 'w')

for line in infile:

    for col in line.strip().split(' ')[1:]:
        data = col.strip().split(':')[1]
        outfile.write(str(data)+' ')
    outfile.write(str(line.strip().split(' ')[0])+'\n')

outfile.close()
'''








