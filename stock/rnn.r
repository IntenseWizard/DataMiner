

source("./r_functions/date_features.r")
source("./r_functions/data_get_previous.r")

files=list.files(path = data_dir, pattern = '*INTC.csv', all.files = FALSE,
                 full.names = TRUE, recursive = FALSE,
                 ignore.case = FALSE, include.dirs = FALSE, no.. = FALSE)
#print(files)

df= lapply(files,read.csv,header=TRUE, sep=";")

for (i in c(1:length(df))) {
  if (i==1){n=df[[1]]}
  else{
    n = rbind(n,df[[i]])
  }
}
labels=c("Date","Open", "High", "Low", "Close", "Volume")
colnames(n)=labels

raw_data=n[order(n["Date"],decreasing="TRUE"),]
data=raw_data[duplicated(raw_data["Date"])==FALSE,]
data=data[is.null(data["Close"])==0,]
data=data[order(data["Date"]),]
#plot(data)
#ts_data=as.ts(data,frequency=380,start=min(data[["Date"]]),end=max(data[["Date"]]))

#minute(data$Date)
dates=date_features(data$Date)
close_history=data_get_previous(data$Close)

x=cbind(close_history,dates)
y=data$Close

split=round(dim(x)[1]*0.8)
x_train=x[0:split,]
y_train=y[0:split]

end=dim(x)[1]
x_test=x[split:end,]
y_test=y[split:end]

#Now make the analysis
library(keras)
#COPYPASTE STARTS

# Setup input

model <- keras_model_sequential()  %>% 
  layer_dense(units = 64, activation = 'relu', input_shape = c(32), dtype = 'float32') %>%
  layer_dropout(rate = 0.4) %>% 
  layer_lstm(units = 128, activation = "tanh") %>%
  #layer_dense(units = 500, activation = 'relu', input_shape = c(32)) %>% 
  #layer_dropout(rate = 0.4) %>% 
  #layer_dense(units = 128, activation = 'relu') %>%
  layer_dropout(rate = 0.3) %>%
  layer_dense(units = 1, activation = 'softmax') %>% compile(
    optimizer = rms,
    loss = "mean_squared_error",
    metrics = "mean_squared_error"
  )%>% fit(
    x_train,
    y_train,
    validation_data = list(x_test, y_test),
    epochs = 10,
    view_metrics = TRUE,
    verbose = 1
  )



# Bring model togethe
# Freeze the embedding weights initially to prevent updates propgating back through and ruining our embedding

#get_layer(model, name = "embedding") %>% 
#  set_weights(list(fastwiki_embedding_matrix)) %>% 
#  freeze_weights()


# Compile

sgd=optimizer_sgd(lr = 10, momentum = 0, decay = 0.1, nesterov = FALSE,
                  clipnorm = NULL, clipvalue = NULL)
rms=optimizer_rmsprop(lr = 0.7, rho = 0.9, epsilon = NULL, decay = 0.05,
                  clipnorm = NULL, clipvalue = NULL)
model %>% compile(
  optimizer = rms,
  loss = "mean_squared_error",
  metrics = "mean_squared_error"
)


# Print architecture (plot_model isn't implemented in the R package yet)

print(model)

# Train model 

history <- model %>% fit(
  x_train,
  y_train,
  validation_data = list(x_test, y_test),
  epochs = 10,
  view_metrics = TRUE,
  verbose = 1
)

# Look at training results
print(history)
plot(history)


#COPYPASTE ENDS


forest=randomForest(x=x_train,
                    y=y_train,
                    xtest=x_test,
                    ytest=y_test, 
                    ntree=1000,
                    keep.forest=TRUE)





#Make stupid prediction
pred=predict(forest,x_test)

plot(y_train,
     xlim=c(2500,3500),
     ylim=c(52.5,53.6))
lines(c((length(y_train)+1):(length(y_train)+length(y_test))),pred, col='red')
lines(c((length(y_train)+1):(length(y_train)+length(y_test))),y_test, col='green')
length(y_test)

#Make better prediction
n_pred=800
pred_input=matrix(x_test[1,],ncol=32)
preds=numeric(n_pred)
#predict next data point
for(i in c(1:n_pred)){
  #Make prediction
  dp=predict(forest,pred_input)
  #Save prediction
  preds[i]=dp
  #Move input one block to left
  pred_input[1,1:29]=pred_input[1,2:30]
  #Update the prediction to input
  pred_input[1,30]=dp
  #Update time
  if(pred_input[1,32]==59){
    pred_input[1,32]=0
    pred_input[1,31]=pred_input[1,31]+1
  }
  else{
    pred_input[1,32]=pred_input[1,32]+1
  }
  
  if((pred_input[1,31]==16) && (pred_input[1,32]==1)){pred_input[1,31]=9;pred_input[1,32]=31}
}

preds

plot(y_train,
     xlim=c(2500,3500),
     ylim=c(52.5,53.6))
lines(c((length(y_train)+1):(length(y_train)+length(y_test))),pred, col='red')
lines(c((length(y_train)+1):(length(y_train)+length(y_test))),y_test, col='green')
lines(c((length(y_train)+1):(length(y_train)+length(preds))),preds, col='blue')
