install.packages('devtools')
library(devtools)
install.packages("Hmisc")
library(Hmisc)
install.packages("psych")
library(psych)
install.packages('plotly')
library(plotly)
install.packages('forecast')
library(forecast)
install.packages('tseries')
library(tseries)
install.packages('zoo', dependencies = TRUE)
library(zoo)
# remove.packages("quantmod")
# remove.packages("TTR")
# remove.packages("tseries")

#setwd('/home/m/DataMiner/stock')
data_dir='./stock_data/'
#Read data
files=list.files(path = data_dir, pattern = NULL, all.files = FALSE,
           full.names = FALSE, recursive = FALSE,
           ignore.case = FALSE, include.dirs = FALSE, no.. = FALSE)
print(files)
file=files[1]

data <- read.csv(file=paste(data_dir,files,sep=""), header=TRUE, sep=";")

#install.packages('dplyr')
#install.packages('readr')
library(dplyr)
library(readr)
files = list.files(path = data_dir, full.names = TRUE)
df= lapply(files,read.csv,header=TRUE, sep=";")

for (i in c(1:length(df))) {
  if (i==1){n=df[[1]]}
  else{
    n = rbind(n,df[[i]])
  }
}
colnames(n)=c("Date","Open", "High", "Low", "Close", "Volume")

data=n[order(n["Date"]),]

length(data["High",])
length(data[["Open"]])

plot(data[["Date"]],data[["High"]])


install.packages('smooth')
library(smooth)
data_high=as.ts(data[["High"]])

data_high_sma=sma(data_high, h=3)

plot.ts(data_high)
plot.ts(data_high_sma)

movavg(x, n, type=c("s"))
rollMonthlyWindows(data["Open"], period = "12m", by = "1m")

# for(file in files){
  # print(file)
  # colnames(data)=c("Date","Open", "High", "Low", "Close", "Volume")
  
  # mod <- lm(data$Open ~ data$Close, data=data)
  # ar=auto.arima(data$Open, seasonal = FALSE)
  # ar=arima(data$Close, order=c(0,1,0))
  # plot(ar$residuals)
  # fc=forecast(ar,h=30)
  # plot(fc)
  
  #count moving average for 100 data points
  #count moving average for 10 data points
  
  
  # }
# View(data)
