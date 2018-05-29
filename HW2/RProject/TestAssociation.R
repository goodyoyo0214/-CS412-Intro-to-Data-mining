
#用read.csv讀進會變成dataframe
#transaction = read.csv(file="D:/abroad/UIUC/Courses/CS412-Intro to Data Mining/HW2/data.transaction.csv",header = F)

#用arules內建的方法讀成transaction data
transaction = read.transactions("D:/abroad/UIUC/Courses/CS412-Intro to Data Mining/HW3/Result/topicInt/topic-4.txt", sep=" ")

#all pattern minsup=0.01
q3_1a=apriori(transaction,parameter=list(support=0.01, confidence = 0))
inspect(q3_1a)

#lenth == 3, support = 0.2
#q3_1b = apriori(transaction,parameter=list(support=0.2, confidence = 0, maxlen = 3 ,minlen=3))
#inspect(q3_1b)

#max frequent item sup=0.01
q3_1c = apriori(transaction,parameter=list(support=0.01, confidence = 0, target = "maximally frequent itemsets"))
inspect(q3_1c)




#all pattern support = 0.1
q3_2a = apriori(transaction,parameter=list(support=0.1, confidence = 0))
inspect(q3_2a)

#lengh == 3 , support = 0.1
q3_2b = apriori(transaction,parameter=list(support=0.1, confidence = 0, maxlen = 3 ,minlen=3))
inspect(q3_2b)

#max frequent item sup=0.1
q3_2c = apriori(transaction,parameter=list(support=0.1, confidence = 0, target = "maximally frequent itemsets"))
inspect(q3_2c)

q3_2d = apriori(transaction, parameter=list(support=0.1, confidence = 0))
inspect(q3_2d)


