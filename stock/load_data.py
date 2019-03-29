
# coding: utf-8

# In[10]:


from alpha_vantage.timeseries import TimeSeries
import datetime
import os

def getData(stock):
    ts = TimeSeries(key='EJ69MPM068NGTJ30', output_format='pandas')
    # data, meta_data = ts.get_intraday(symbol=stock,interval='1min', outputsize='compact')
    data, meta_data = ts.get_intraday(symbol=stock,interval='1min', outputsize='full')
    return data, meta_data

stocks = ["INTC","NVDA","AMD"]
#today = datetime.date.today()
today=str(str(datetime.datetime.now()).split('.')[0].replace(":","-"))
folder="/home/m/DataMiner/stock/stock_data/"

if not os.path.exists(folder):
    os.makedirs(folder)
    
for s in stocks:
    data, metadata = getData(s)
    data.to_csv(folder+str(today)+" "+s+".csv",sep=";")
    '''    with open(s+".csv","w") as f:
        for d in data:
            f.write(d)
        for m in metadata:
            f.write(m)
        f.flush()'''
    print("Done: ",folder+str(today)+" "+s+".csv")
print("Ready")

