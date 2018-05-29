#------knn------
# knn test set all
id = c(11,12,13,14)
x1 =c(1.9,2.7,0.6,3.4)
x2 = c(1.0,1.8,2.1,2.4)
y = c(-1,+1,-1,-1)
q2Data.Test = data.frame(x1,x2,y)
q2Data.Test.att = q2Data.Test[,c(1,2,3)]
q2Data.Test.lable = q2Data.Test[,c(4)]

# knn test set one by one
q2DataID11.Test = data.frame(id=11,x1=1.9,x2=1.0,y=-1)
q2DataID11.Test.att = q2DataID11.Test[,c(2,3)]
q2DataID11.Test.lable = q2DataID11.Test[,c(4)]

q2DataID12.Test.att = q2Data.Test[2,c(1,2)]
q2DataID13.Test.att = q2Data.Test[3,c(1,2)]
q2DataID14.Test.att = q2Data.Test[4,c(1,2)]


# knn training set
id = c(1,2,3,4,5,6,7,8,9,10)
x1 =c(1.6,3.7,1.1,2.5,0.4,4.0,3.4,2.6,2,3.7)
x2 = c(1.1,2.2,3.1,3.7,0.6,0.5,2.9,0.5,1,1.4)
y = c(1,-1,1,1,1,-1,1,-1,-1,-1)
q2Data.Train = data.frame(x1,x2,y)
q2Data.Train.att = q2Data.Train[,c(1,2)]
q2Data.Train.lable = q2Data.Train[,c(3)]

# knn result one by one
classSet11 = knn(q2Data.Train.att, q2DataID11.Test.att, q2Data.Train.lable, k = 3)
classSet12 = knn(q2Data.Train.att, q2DataID12.Test.att, q2Data.Train.lable, k = 3)
classSet13 = knn(q2Data.Train.att, q2DataID13.Test.att, q2Data.Train.lable, k = 3)
classSet14 = knn(q2Data.Train.att, q2DataID14.Test.att, q2Data.Train.lable, k = 3)

#-----k-means-----
#k-means test set
id = c(1,2,3,4,5,6,7,8,9)
x = c(8.2,0.1,1.5,2.2,1.6,4.3,2.5,6.2,5.5)
y = c(6.4,6.7,7.8,3.4,3.5,9.7,2.2,3.1,0.3)
q3dataSet = data.frame(id,x,y)
q3data = q3dataSet[,c(2,3)]
#c(2.0, 5.0),c(6.0, 0.5),c(6.0, 5.0)
iniCent = data.frame(c(2.0, 6.0,5.0),c(5.0,0.5,5.0))
iniCent2 = data.frame(c(1.0, 0.2,4.3),c(4.0,6.0,2.0))

test = kmeans(q3data, iniCent)
test2 = kmeans(q3data, iniCent2)

