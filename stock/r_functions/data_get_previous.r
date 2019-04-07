
#For each given point in vector, return 30 previous points

#To call this function, use
#source("./r_functions/data_get_previous.r")

data_get_previous<-function(data_vec) {
  #initialize vector
  len=length(data_vec)
  res=matrix(numeric(len*30),ncol=30)
  for(i in c(1:len)){
    if(i-30>0){
      res[i,]=data_vec[(i-30):(i-1)]
    }
    else if(i!=1){
      res[i,(32-i):30]=data_vec[0:(i-1)]
    }
    
  }
  return(res)
}


#data_vec=c(1:100)
#data_get_previous(data_vec)


