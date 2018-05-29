# coding=utf-8
import sys
import random
from collections import Counter

#input data
def inputData(trainFileDir,testFileDir): # input raw data as list
    trainFile = open(trainFileDir,'r')
    testFile = open(testFileDir, 'r')
    count = 1
    for line in trainFile:
        tupleList = []
        line = line.strip().split(' ')
        #print line[0]
        lable = int(line[0])
        tupleList.append(lable)
        for att in line[1:]:
            tupleList.append(int(att.strip().split(':')[1]))
            if count ==1:
                attNameList.append(int(att.strip().split(':')[0]))
        count += 1
        #print 'count',count
        #print tupleList
        trainList.append(tupleList)
    for line in testFile:
        tupleList = []
        line = line.strip().split(' ')
        # print line[0]
        lable = int(line[0])
        tupleList.append(lable)
        for att in line[1:]:
            tupleList.append(int(att.strip().split(':')[1]))
            if count == 1:
                attNameList.append(int(att.strip().split(':')[0]))
        count += 1
        # print 'count',count
        # print tupleList
        testList.append(tupleList)
    #print testList


# test tree
def voteLable(subTree): # vote the lable of the test result
    #print '----in voteLable----'
    keyList = subTree.keys() # get the keys(attValKey)
    countDic = {}
    for key in keyList:
        value = subTree[key] # get the lable of each attValKey
        if type(value) == type({}):
            countDic = countVal(value,countDic)
        else:
            if value not in countDic:
                countDic[value] = 0
            countDic[value] += 1
    #print '----end vote Lable lable =',max(countDic, key=lambda key: countDic[key]),'----'
    return max(countDic, key=lambda key: countDic[key]) # return the majority of lable

def getAttNameOrLable(attValKey,subTree): # return the subtree or final lable
    #print '----in get attName----\nattValKey',attValKey,'\nsubTree',subTree
    if attValKey in subTree.keys():
        if type(subTree[attValKey]) == type({}):
            attName = subTree[attValKey].keys()[0]
            reSubtree = subTree[attValKey][attName]
        else:
            attName = 'final'
            reSubtree = subTree[attValKey]
        #print 'attName', attName, 'subTree',subTree
    else:
        reSubtree = voteLable(subTree)
        attName = 'final'
    return  attName, reSubtree

def predict(forestList,testTuple): # use Dtree to predict test Data
    confusionDic = {}
    treeVoteList = []
    for tesTuple in testTuple:
        lable = tesTuple[0] # real lable

        tupleVoleList=[]
        for dTree in forestList:
            firsttupleIndex = dTree.keys()[0]# index for tesTuple
            attValKey = tesTuple[firsttupleIndex] # key for subtree to find the next attNameKey
            subTree = dTree[firsttupleIndex] # tree of key = attVal
            attName, subTree = getAttNameOrLable(attValKey,subTree)
            while type(subTree) == type({}):
                attValKey = tesTuple[attName]
                attName, subTree = getAttNameOrLable(attValKey,subTree)
            predictLable = subTree
            tupleVoleList.append(predictLable)
        finalPredicLable = Counter(tupleVoleList).most_common()[0][0]
        if finalPredicLable not in confusionDic:
            confusionDic[finalPredicLable] = {}
        if lable not in confusionDic[finalPredicLable]:
            confusionDic[finalPredicLable][lable] = 0
        confusionDic[finalPredicLable][lable] += 1
    return confusionDic

def outConfusDic(confusionDic,testtupleLen):
    confusionList = []
    maxval = len(confusionDic)
    lineOut = ''
    for i in range(maxval):
        line = ''
        rowList = []
        for k in range(maxval):
            if k+1 not in confusionDic[i+1]:
                rowList.append(0)
                line = line + '0 '
            else:
                rowList.append(confusionDic[i+1][k+1])
                line = line + str(confusionDic[i+1][k+1])+' '
        line=line.strip()
        confusionList.append(rowList)
        lineOut += line + '\n'
    print   lineOut
    evalu(confusionList,testtupleLen)


def evalu(confusionList,testtupleLen):
    evaluDic = {}
    acuracyList = [0.0, 0.0]
    for row in range(len(confusionList)):
        if row not in evaluDic:
            evaluDic[row] = {'tp':0,'fn':0,'fp':0,'tn':0}
        for col in range(len(confusionList)):
            if row not in evaluDic:
                evaluDic[col] = {'tp':0,'fn':0,'fp':0,'tn':0}
            if row == col:
                evaluDic[row]['tp'] = confusionList[row][col]
                acuracyList[0] += confusionList[row][col]
            else:
                evaluDic[row]['fn'] += confusionList[col][row]
                evaluDic[row]['fp'] += confusionList[row][col]
                acuracyList[1] += confusionList[row][col]




    for row in range(len(confusionList)):
        evaluDic[row]['tn'] = testtupleLen - evaluDic[row]['tp']-evaluDic[row]['fn']-evaluDic[row]['fp']
        tp = evaluDic[row]['tp']
        tn = evaluDic[row]['tn']
        fp = evaluDic[row]['fp']
        fn = evaluDic[row]['fn']
        if tp+fn == 0:
            sensitivity = 0
        else:
            sensitivity= float(tp)/float(tp+fn)
        recall = sensitivity
        f1score = float(2*tp)/float(2*tp+fp+fn)
        precision = float(tp)/float(tp+fp)
        if precision+recall == 0:
            f1beta5 = 0
            f1beta2 = 0
        else:
            f1beta5 = (1.0+0.5**2)*precision*recall/(precision*(0.5**2)+recall)
            f1beta2  =(1.0+2**2)*precision*recall/(precision*(2**2)+recall)



# create tree

def randomAttName(tupleList,attNameList): #randomly select attName, return the final index of attNameList
    #print '-----in randomAttName-----'
    #print 'attNameList',attNameList
    if len(attNameList)>=5:
        randomList = sorted(random.sample(attNameList, int(len(attNameList) / 2)))  # result of selection , [1,2,3,4] -> [1,3]
        #print 'randomList', randomList
        randomAttNIndexList = [attNameList.index(value) + 1 for value in randomList]  # index of the tupleList on tuple[lable,1,2,3,4] , [1,3]
        #print 'randomAttNIndexList', randomAttNIndexList
        tupleAttNameIndex = selectAttByGini(tupleList, randomAttNIndexList)
        #print '-----end of randomAttName-----return tupleAttNameIndex', tupleAttNameIndex
    elif len(attNameList)>=2: # if canditate attribute >=2, do random
        randomList = sorted(random.sample(attNameList,int(len(attNameList)/1.5))) # result of selection , [1,2,3,4] -> [1,3]
        #print 'randomList',randomList
        randomAttNIndexList = [attNameList.index(value)+1 for value in randomList] # index of the tupleList on tuple[lable,1,2,3,4] , [1,3]
        #print 'randomAttNIndexList',randomAttNIndexList
        tupleAttNameIndex = selectAttByGini(tupleList,randomAttNIndexList)
        #print '-----end of randomAttName-----return tupleAttNameIndex',tupleAttNameIndex
    else: # just input
        randomAttNIndexList = [attNameList.index(value) + 1 for value in attNameList]
        tupleAttNameIndex = selectAttByGini(tupleList, randomAttNIndexList)
    return tupleAttNameIndex-1 # return attNameIndex


def createRainForestTable(tupleList,randomAttNIndexList):
    #print '---- in createRainForestTable----\nrandomAttNIndexList',randomAttNIndexList
    rainForest = {} # {attNameIndex(tuple):[{attVal:[{lable:count,lable2:count,..},total tuple of attVal],attVal2:[],..},total no tuple in attNameIndex],attNameIndex2(tuple):[],...}
    for tuple in tupleList:
        lable = tuple[0] # tuple =[lable,attVal1,attVal2,...]
        #print 'tuple',tuple
        #print 'len(tuple)',len(tupleList[0])
        for attNameIndex in randomAttNIndexList : # attNameIndex of tuple
            #print 'attNameIndex',attNameIndex

            if attNameIndex not in rainForest: # create each rainForest table
                rainForest[attNameIndex]=[{},0.0] # [{attVal:[{lable:count,..},totalDiSize],..},totalNoTuple in tupleList]
            intAttVal = int(tuple[attNameIndex])
            if intAttVal not in rainForest[attNameIndex][0]: # create row of each table
                rainForest[attNameIndex][0][intAttVal] = [{},0.0] # [{lable:count,..},totalDiSize]
            if lable not in rainForest[attNameIndex][0][intAttVal][0]: # create col of each row
                rainForest[attNameIndex][0][intAttVal][0][lable] = 0.0 # {lable:count,..}
            rainForest[attNameIndex][0][intAttVal][0][lable] += 1.0
            rainForest[attNameIndex][0][intAttVal][1] +=1.0
            rainForest[attNameIndex][1] = len(tupleList)
    #print 'rainForest',rainForest
    #print '----end createRainForestTable----'
    return rainForest

def selectAttByGini(tupleList,attNameIndexList):
    rainForest = createRainForestTable(tupleList,attNameIndexList)

    giniResult = [] # {attName:giniVal,..}
    for key in sorted(rainForest.keys()): # for loop for each table(index of attName in tuple,attNameIndex(tuple))
        giniDiList = [] # giniDi result
        totalNoTuple = float(rainForest[key][1])
        gini = 0.0
        for attVal in sorted(rainForest[key][0].keys()): # for loop for each rowKey(attVal)
            resultDi = 1.0
            totalDiSize = rainForest[key][0][attVal][1] # total no of tuple in Di
            for lable in sorted(rainForest[key][0][attVal][0].keys()): # for loop for each lable val
                resultDi -= (rainForest[key][0][attVal][0][lable]/totalDiSize)**2
            gini+=resultDi*totalDiSize/totalNoTuple
        giniResult.append(gini)
    bestAttIndex = giniResult.index(min(giniResult))
    return [tupleAttNameIndex for tupleAttNameIndex in sorted(rainForest.keys())][bestAttIndex] # return the index of attName in tuple

def voteResult(lableList): # vote for lable if all the attribute is used
    lableCountDic = {}
    for attValList in lableList: # lableList is a list contain list with len=1 list ,  lableList = [[lable1],[lable2]
        attVal = attValList[0]
        #print 'attVal',attVal
        if attVal not in lableCountDic:
            lableCountDic[attVal] = 0
        lableCountDic[attVal] += 1
    return max(lableCountDic, key=lambda key: lableCountDic[key])


def createTupleList(tupleList,tupleAttNameIndex,attval): # create tuple for  next tree node
    #print '----in createTupleList----,spliteAttIndex',spliteAttIndex,'attval',attval,'tupleList',tupleList
    returnTupleList= []
    for row in tupleList: # org tuple to be divided
        #print 'row',row
        if row[tupleAttNameIndex] == attval: # if row attVal = divided attVal
            #print 'row attVal',row,'==','attval',attval
            if len(row) -1 >= tupleAttNameIndex:
                returnTuple = row[:tupleAttNameIndex]
                returnTuple.extend(row[tupleAttNameIndex+1:])
                returnTupleList.append(returnTuple)
    return  returnTupleList

def countVal(subTree,countDic):  # count the number of each lable if value is a nested dictionary
    for val in subTree.values():
        if type(val) == type({}):
            countDic = countVal(val,countDic)
        else:
            if val not in countDic:
                countDic[val] = 0
            countDic[val] += 1
    return countDic

def createTree(tupleList,attNameList):
    lableList = [line[0] for line in tupleList] #list of lable
    if len(set(lableList)) == 1: # if there is only one lable value
        # print 'in only one lable value\nreturn',lableList[0]
        return lableList[0] #return lable value
    if len(tupleList[0]) == 2: # if all the att is used
        # print 'all the att is used'
        return voteResult(tupleList) # vote for the result

    attIndexSplite = randomAttName(tupleList,attNameList) # index splitting attName(attNameList)
    splitTupleIndex = attIndexSplite+1 # index of splite attNameList
    splitAttName = attNameList[attIndexSplite]
    dTree = {splitAttName:{}} # decision tree

    newAttNameList = attNameList[:]
    del(newAttNameList[attIndexSplite]) # delete the splitting attName from attNameList

    attValList = set([row[splitTupleIndex] for row in tupleList]) # get the unique attVal of splitting attList
    for attval in attValList:
        subTupleList = createTupleList(tupleList,splitTupleIndex,attval)
        dTree[splitAttName][attval] = createTree(subTupleList,newAttNameList)
    return dTree


def createForest(tupleList,attNameList,treeNo):
    forestList = []
    for term in range(treeNo+1):
        forestList.append(createTree(tupleList,attNameList))
    return forestList


trainFile = sys.argv[1]
testFile = sys.argv[2]
testList = [] #[[lable,attval1,attval2,..]
trainList = []
attNameList = [] # [attName1,attName2,..]

#trainFile = './train_file/poker.train'
#testFile = './test_file/poker.test'
inputData(trainFile,testFile)
#print len(testList)
#print len(trainList)
#print len(testList)

forestList = createForest(trainList,attNameList,60)

# dTree = createTree(trainList,attNameList)
# print dTree
#print predict(forestList,testList)
outConfusDic(predict(forestList,testList),len(testList))
#rainForest = createRainForestTable()
#print selectAttGini(rainForest)
#createTree()