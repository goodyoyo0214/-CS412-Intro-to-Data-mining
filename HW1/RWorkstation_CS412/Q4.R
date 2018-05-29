dist(data.supermarkets , method = "minkowski" , p=1)
dist(data.supermarkets , method = "minkowski" , p=2)
dist(data.supermarkets , method = "maximum")
dist(data.supermarkets[2,],data.supermarkets[1,], js , method ="cosine")


js<- data.supermarkets[1,]
data.supermarkets = data.supermarkets[-"supermarket"]

summary(data.online$V2)
var(data.online$V2)
which.max(table(data.online$V2))
scale(data.online$V2, center = TRUE, scale = TRUE)
scale.data<-scale(data.online$V2, center = TRUE, scale = TRUE)

var(scale.data)
cor(data.online$V2,data.online$V3, method = "pearson")
cov(data.online$V2,data.online$V3)

sumJs <- sum(data.supermarkets[1,])
sumkk <- sum(data.supermarkets[2,])

js<-js/sumJs
kk<-kk/sumkk

js<-as.vector(c(data.supermarket.p[1,]),mode="numeric")
kk<-as.vector(c(data.supermarket.p[2,]),mode="numeric")


z <- c(1,2)

data.supermarket.p <- data.supermarkets
data.supermarket.p[1,]<-data.supermarket.p[1,]/sumJs
data.supermarket.p[2,]<-data.supermarket.p[2,]/sumkk

KLD(js,kk)

y <- c(1346,430)
n <- c(133,32974)
df <- data.frame(y,n)  
names(df)[,1]<-paste("n")
chisq.test(df)