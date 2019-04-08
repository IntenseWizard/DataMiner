#This script runs in the DataMiner folder and creates images by date of the csv files in house data folder
#Each day gets an own figure of three histograms describing the price of the house, year they were built and size in square meters


setwd('/home/m/DataMiner/')
data_dir='./house data/'
#Read data
files=list.files(path = data_dir, pattern = '*.csv', all.files = FALSE,
                 full.names = TRUE, recursive = FALSE,
                 ignore.case = FALSE, include.dirs = FALSE, no.. = FALSE)
print(files)

#df = lapply(files,read.csv,header=FALSE, sep=",")
counter=1

result = tryCatch({
  for (file in files){
    print("Reading file")
    n=read.csv(file,header=FALSE, sep=",")
    # for (i in c(1:length(df))) {
    #   if (i==1){n=df[[1]]}
    #   else{
    #     n = rbind(n,df[[i]])
    #   }
    # }
    #rm(df)
    labels=c("Link","Location", "Address", "Type", "Rooms", "Size", "Price", "Year")
    colnames(n)=labels
    
    data=n
    
    #data=raw_data[duplicated(raw_data["Date"])==FALSE,]
    #data=data[is.null(data["Close"])==0,]
    #data=data[order(data["Date"]),]
    print("Formatting Size, Price and Year")
    
    data$Size=gsub("m²", "", data$Size) 
    data$Size=gsub(",", ".", data$Size) 
    data$Size=round(as.integer(data$Size,na.rm=TRUE))
    
    data$Price=gsub("€", "", data$Price)
    data$Price=gsub(" ", "", data$Price) 
    data$Price=gsub(",", ".", data$Price) 
    data$Price=round(as.integer(data$Price,na.rm=TRUE))
    
    data$Year=as.integer(as.character(data$Year,na.rm=TRUE))
    
    n_n <- 5
    n_size=10
    brp=quantile(data$Price,prob=1-n_n/100,na.rm=TRUE)
    brs=quantile(data$Size,prob=1-n_size/100,na.rm=TRUE)
    sty=quantile(data$Year,prob=n_n/100,na.rm=TRUE)
    bry=quantile(data$Year,prob=1-n_n/100,na.rm=TRUE)
    d=data[data["Price"]<brp,]
    d=d[d["Size"]<brs,]
    d=d[d["Year"]<bry && d["Year"]>sty,]
    
    mean_price=round(mean(d$Price,na.rm=TRUE))
    png_name=gsub(".csv",".png",gsub("./house data//","",files[counter]))
    target_dir="/var/www/html/house_prices/"
    png(filename=paste(target_dir,png_name,sep=""))
    par(mfrow=c(1,3))
    hist(d$Year, main = png_name)
    hist(d$Size)
    hist(d$Price, main = mean_price)
    dev.off()
    counter=counter+1
    print(paste("Image saved at ",png_name, sep=""))
  }
#}, warning = function(w) {
  #warning-handler-code
}, error = function(e) {
  #error-handler-code
}, finally = {
  #cleanup-code
})



rcon<-file(paste(target_dir,"testR2.html",sep=""),"w")
for (f in files){
  png_name=gsub(".csv",".png",gsub("./house data//","",f))
  target_dir="/var/www/html/house_prices/"
  filename=paste("./",png_name,sep="")
  cat(paste('<img src="',filename,'">\n', sep=""),
      file=rcon)
}

close(rcon)
