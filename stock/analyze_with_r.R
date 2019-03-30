install.packages('devtools')
install.packages("Hmisc")
install.packages("psych")
install.packages('plotly')
install.packages('forecast')
install.packages('tseries')
install.packages('zoo')#,dependencies=TRUE
install.packages('smooth')
install.packages('dplyr')
install.packages('readr')
install.packages('zoo')
install.packages('tidyverse',dependencies=TRUE)

library(devtools)
library(Hmisc)
library(psych)
library(plotly)
library(forecast)
library(tseries)
library(zoo)
library(smooth)
library(dplyr)
library(readr)
library(tidyverse)
library(zoo)
setwd('/home/m/DataMiner/stock')
data_dir='./stock_data/'
#Read data
files=list.files(path = data_dir, pattern = '*INTC.csv', all.files = FALSE,
           full.names = TRUE, recursive = FALSE,
           ignore.case = FALSE, include.dirs = FALSE, no.. = FALSE)
print(files)

df= lapply(files,read.csv,header=TRUE, sep=";")

for (i in c(1:length(df))) {
  if (i==1){n=df[[1]]}
  else{
    n = rbind(n,df[[i]])
  }
}
colnames(n)=c("Date","Open", "High", "Low", "Close", "Volume")

raw_data=n[order(n["Date"],deccreasing="TRUE"),]
data=raw_data[duplicated(raw_data)==FALSE,]
ts_data=as.ts(data)
ma_30=rollmean(data[["High"]],300)

plot(data[["High"]])
lines(ma_30)
head(data)

length(data["High",])
length(data[["Open"]])

plot.ts(data[["Date"]],data[["High"]])

data_high=as.ts(data[["High"]])

data_high_sma=sma(data_high, h=3)

plot.ts(data_high)
plot.ts(data_high_sma)



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
