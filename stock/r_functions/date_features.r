library(zoo)
#install.packages('lubridate')
library(lubridate)
#To call this function, use
#source("./r_functions/date_features.r")

#sessionInfo()
#Sys.setenv("LANGUAGE"="En")
#Sys.setlocale("LC_TIME", "en_US.UTF-8")
#Sys.setlocale("LC_MONETARY", "en_US.UTF-8")
#Sys.setlocale("LC_MEASUREMENT", "en_US.UTF-8")
#Sys.setlocale("LC_PAPER", "en_US.UTF-8")

date_features<-function(dates) {
  #dates=as.ts(dates)
  #w=weekdays(as.Date(dates))
  #m=months(as.Date(dates))
  hs=hour(dates)
  ms=minute(dates)
  res=matrix(c(#w,m,
               hs,ms),#ncol=4
                      ncol=2)
  return(res)
}
#file_path="./stock_data//2019-03-18 23-32-23 INTC.csv"
#example_data=read.csv(file_path,header=TRUE, sep=";")
#dates=as.ts(example_data$date, frequency=280)
##h=holidayNYSE(as.Date(dates))

#date_features(dates)
