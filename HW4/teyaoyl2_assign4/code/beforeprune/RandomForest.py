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
    #print '----in predict----\ndTree',dTree
    confusionDic = {}
    treeVoteList = []
    for tesTuple in testTuple:
        #print '******tesTuple',tesTuple,'******'
        lable = tesTuple[0] # real lable

        tupleVoleList=[]
        for dTree in forestList:
            firsttupleIndex = dTree.keys()[0]# index for tesTuple
            #print 'lable', lable,'firsttupleIndex',firsttupleIndex
            attValKey = tesTuple[firsttupleIndex] # key for subtree to find the next attNameKey
            subTree = dTree[firsttupleIndex] # tree of key = attVal
            #print 'attValKey',attValKey,'subTree',subTree
            attName, subTree = getAttNameOrLable(attValKey,subTree)
            while type(subTree) == type({}):
                attValKey = tesTuple[attName]
                attName, subTree = getAttNameOrLable(attValKey,subTree)
            predictLable = subTree
            #print '*******predictLable',predictLable,'lable',lable,'******'
            tupleVoleList.append(predictLable)
        finalPredicLable = Counter(tupleVoleList).most_common()[0][0]
        if finalPredicLable not in confusionDic:
            confusionDic[finalPredicLable] = {}
        if lable not in confusionDic[finalPredicLable]:
            confusionDic[finalPredicLable][lable] = 0
        confusionDic[finalPredicLable][lable] += 1
    return confusionDic

def outConfusDic(confusionDic):
    #print 'confusionDic',confusionDic
    maxval = len(confusionDic)
    #print maxval
    for i in range(maxval):
        line = ''
        for k in range(maxval):
            if k+1 not in confusionDic[i+1]:
                line = line + '0 '
            else:
                line = line + str(confusionDic[i+1][k+1])+' '
        line=line.strip()
        print line


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
    #print '----in selectAttGini----'
    rainForest = createRainForestTable(tupleList,attNameIndexList)

    giniResult = [] # {attName:giniVal,..}
    #print rainForest
    for key in sorted(rainForest.keys()): # for loop for each table(index of attName in tuple,attNameIndex(tuple))
        #print 'attName',attName
        giniDiList = [] # giniDi result
        totalNoTuple = float(rainForest[key][1])
        #print "totalNoTuple",totalNoTuple
        gini = 0.0
        for attVal in sorted(rainForest[key][0].keys()): # for loop for each rowKey(attVal)
            #print 'columnID(row)',attVal
            resultDi = 1.0
            totalDiSize = rainForest[key][0][attVal][1] # total no of tuple in Di
            #print 'totalDiSize',totalDiSize
            for lable in sorted(rainForest[key][0][attVal][0].keys()): # for loop for each lable val
                #print 'lable',lable
                #print 'numer',rainForest[attName][0][attVal][0][lable]
                resultDi -= (rainForest[key][0][attVal][0][lable]/totalDiSize)**2
                #print 'resultDi',resultDi
            #print 'giniDi',resultDi*totalDiSize/totalNoTuple
            gini+=resultDi*totalDiSize/totalNoTuple
            #print 'gini',gini
            #print '---------------------------'
        giniResult.append(gini)
        #print '***********************'
    bestAttIndex = giniResult.index(min(giniResult))
    #print 'giniResult',giniResult
    #print '----end selectAttGini----return bestAttIndex',bestAttIndex
    return [tupleAttNameIndex for tupleAttNameIndex in sorted(rainForest.keys())][bestAttIndex] # return the index of attName in tuple

def voteResult(lableList): # vote for lable if all the attribute is used
    #print '----in voteResult----\nlableList',lableList
    lableCountDic = {}
    #print 'lableList',lableList
    for attValList in lableList: # lableList is a list contain list with len=1 list ,  lableList = [[lable1],[lable2]
        attVal = attValList[0]
        #print 'attVal',attVal
        if attVal not in lableCountDic:
            lableCountDic[attVal] = 0
        lableCountDic[attVal] += 1
    #print 'lableCountDic',lableCountDic
    #print '----end of lableList----return',max(lableCountDic, key=lambda key: lableCountDic[key])
    return max(lableCountDic, key=lambda key: lableCountDic[key])


def createTupleList(tupleList,tupleAttNameIndex,attval): # create tuple for  next tree node
    #print '----in createTupleList----,spliteAttIndex',spliteAttIndex,'attval',attval,'tupleList',tupleList
    returnTupleList= []
    for row in tupleList: # org tuple to be divided
        #print 'row',row
        if row[tupleAttNameIndex] == attval: # if row attVal = divided attVal
            #print 'row attVal',row,'==','attval',attval
            if len(row) -1 >= tupleAttNameIndex:
                #print 'return before indexdx',row[:spliteAttIndex],'after',row[spliteAttIndex+1:]
                returnTuple = row[:tupleAttNameIndex]
                returnTuple.extend(row[tupleAttNameIndex+1:])
                returnTupleList.append(returnTuple)
                #print '----returnTupleList',returnTupleList,'-----'
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
    #print '----createTree----\ntupleList',tupleList
    lableList = [line[0] for line in tupleList] #list of lable
    # print 'tupleList[0]',tupleList[0]
    # print 'len(tupleList[0])', len(tupleList[0])
    # print 'lableList', lableList
    # print 'set(lableList)', set(lableList)
    # print 'len(set(lableList))', len(set(lableList))
    # print 'attNameList', attNameList
    if len(set(lableList)) == 1: # if there is only one lable value
        # print 'in only one lable value\nreturn',lableList[0]
        return lableList[0] #return lable value
    if len(tupleList[0]) == 1: # if all the att is used
        # print 'all the att is used'
        return voteResult(tupleList) # vote for the result

    attIndexSplite = randomAttName(tupleList,attNameList) # index splitting attName(attNameList)
    splitTupleIndex = attIndexSplite+1 # index of splite attNameList
    splitAttName = attNameList[attIndexSplite]
    # print 'attIndexSplite',attIndexSplite
    dTree = {splitAttName:{}} # decision tree

    #print 'del attNameList[attIndexSplite]',attNameList[attIndexSplite]
    newAttNameList = attNameList[:]
    del(newAttNameList[attIndexSplite]) # delete the splitting attName from attNameList
    #print 'row attval for next branch',[row[splitTupleIndex] for row in tupleList]

    attValList = set([row[splitTupleIndex] for row in tupleList]) # get the unique attVal of splitting attList
    #print 'attValList',attValList
    #print 'dTree', dTree
    for attval in attValList:
        #print '******in attval=',attval,'******'
        #print 'tupleList before',tupleList
        subTupleList = createTupleList(tupleList,splitTupleIndex,attval)
        #print 'tupleList after',subTupleList
        dTree[splitAttName][attval] = createTree(subTupleList,newAttNameList)
        #print 'dTree',dTree
        #print '******end attval=',attval,'******'
    #print dTree
    return dTree


def createForest(tupleList,attNameList,treeNo):
    forestList = []
    for term in range(treeNo+1):
        forestList.append(createTree(tupleList,attNameList))
    return forestList


#trainFile = sys.argv[1]
#testFile = sys.argv[2]
testList = [] #[[lable,attval1,attval2,..]
trainList = []
attNameList = [] # [attName1,attName2,..]
trainFile = './train_file/balance.scale.train'
testFile = './test_file/balance.scale.test'
inputData(trainFile,testFile)
#print len(trainList)
#print len(testList)

forestList = createForest(trainList,attNameList,60)

# dTree = createTree(trainList,attNameList)
# print dTree
#print predict(forestList,testList)
outConfusDic(predict(forestList,testList))
#rainForest = createRainForestTable()
#print selectAttGini(rainForest)
#createTree()