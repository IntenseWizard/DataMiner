install.packages('devtools', dependencies = TRUE)
library(devtools)
install.packages("Hmisc")
library(Hmisc)
install.packages("psych")
library(psych)
install.packages('plotly', dependencies = TRUE)
library(plotly)
install.packages('forecast', dependencies = TRUE)
library(forecast)
install.packages('tseries', dependencies = TRUE)
library(tseries)
install.packages('zoo', dependencies = TRUE)
library(zoo)
remove.packages("quantmod")
remove.packages("TTR")
remove.packages("tseries")

setwd('/home/m/dataminer/stock')
data_dir='/home/m/dataminer/stock/stock_data/'
#Read data
files=list.files(path = data_dir, pattern = NULL, all.files = FALSE,
           full.names = FALSE, recursive = FALSE,
           ignore.case = FALSE, include.dirs = FALSE, no.. = FALSE)
print(files)
file=files[1]
for(file in files){
  data <- read.csv(file=paste(data_dir,file,sep=""), header=TRUE, sep=";")
  colnames(data)=c("Date","Open", "High", "Low", "Close", "Volume")
  
  mod <- lm(data$Open ~ data$Close, data=data)
  ar=auto.arima(data$Open, seasonal = FALSE)
  ar=arima(data$Close, order=c(0,1,0))
  plot(ar$residuals)
  fc=forecast(ar,h=30)
  plot(fc)
  
  #count moving average for 100 data points
  #count moving average for 10 data points
  
  
  }
View(data)
