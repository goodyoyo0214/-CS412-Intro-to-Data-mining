import math

sample = [[8.2,6.4],[0.1,6.7],[1.5,7.8],[2.2,3.4],[1.6,3.5],[4.3,9.7],[2.5,2.2],[6.2,3.1],[5.5,0.3]]
centroids = [[2.0, 5.0],[6.0, 0.5],[6.0, 5.0]]
#centroids = [[1.0, 4.0],[0.2, 6.0],[4.3, 2.0]]
def getCluster(centroids,sample,getClusterCount):  # get the index of samples group
       print 'round',getClusterCount
       #print '-----in getCluster-----'
       clusterList = []
       getClusterCount += 1
       #print 'round',getClusterCount
       for point in sample:
              compareList = []
              for centro in centroids:
                     distance = math.sqrt((point[0]-centro[0])**2+(point[1]-centro[1])**2)
                     #print distance
                     compareList.append(distance)
              index = compareList.index(min(compareList))
              clusterList.append(index)
       print 'clusterList',clusterList
       return clusterList, getClusterCount

def getNewCentroid(centroids,sample,clusterList):
       #print '-----in getNewCentroid----- centroids old',centroids,'sample',sample,'clusterList',clusterList
       cenroidXYList = [[0.0,0.0],[0.0,0.0],[0.0,0.0]]
       cenroidXYCount = [0.0,0.0,0.0]
       for i in range(len(clusterList)):
              #print i
              #print 'cenroidXYList[clusterList[i]]',cenroidXYList[clusterList[i]]
              cenroidXYList[clusterList[i]][0] += sample[i][0]
              cenroidXYList[clusterList[i]][1] += sample[i][1]
              cenroidXYCount[clusterList[i]] += 1.0
       for indexCen in range(len(cenroidXYCount)):
              centroids[indexCen][0] =  cenroidXYList[indexCen][0]/cenroidXYCount[indexCen]
              centroids[indexCen][1] = cenroidXYList[indexCen][1]/cenroidXYCount[indexCen]
       #print '------ end of getNewCentroid----- centroids new',centroids,'------'
       print 'centroids',centroids
       return centroids


def kmean(centroids,sample,clusterList,getClusterCount):
       #print 'round',getClusterCount
       nClusterList,NgetClusterCount = getCluster(centroids,sample,getClusterCount)
       #print "!!!", NgetClusterCount
       Ncentroids = getNewCentroid(centroids, sample, nClusterList)
       print 'result', Ncentroids,nClusterList
       return Ncentroids,sample,nClusterList,NgetClusterCount





clusterList,getClusterCount = getCluster(centroids,sample,0)
centroids = getNewCentroid(centroids, sample, clusterList)
Ncentroids,sample,nClusterList,NgetClusterCount = kmean(centroids,sample,clusterList,getClusterCount)

while clusterList != nClusterList:
       clusterList = nClusterList
       centroids = Ncentroids
       getClusterCount = NgetClusterCount
       Ncentroids, sample, nClusterList, NgetClusterCount = kmean(Ncentroids,sample,clusterList,NgetClusterCount)




#getCluster([[2.1, 3.0333333333333337], [1.9666666666666668, 8.066666666666666], [6.633333333333333, 3.266666666666667]],sample,0)





