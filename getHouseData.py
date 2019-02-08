
# coding: utf-8

# In[21]:


from bs4 import BeautifulSoup
import re, time
import os
import urllib.request
from io import BytesIO
from PIL import Image
from IPython.display import Image as IMG, display 

import matplotlib.pyplot as plt
import hashlib
import time

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"    
    
def getDataFromLink(link):
    opener = AppURLopener()
    response = opener.open(link).read()
    soup = BeautifulSoup(response, "lxml")
    
    rawList=soup.findAll("li", {"class": "residental"})
    #print(rawList)
    thumbs = [a.find("li") for a in rawList]
    #print(thumbs)
    
    facts = [a.find("a", {"class": "facts"}) for a in rawList]
    
    links = [a.get('href').replace("..","https://www.etuovi.com") for a in facts]
    print(links)
    

    cities = [str(a.find("div", {"class": "address"}).span).replace("<span>","").replace("</span>","") for a in facts]
    #print(cities)
    
    addresses = [str(a.find("div", {"class": "address"}).strong).replace("<strong>","").replace("</strong>","") for a in facts]
    #print(addresses)
    
    house_type = [str(a.find("div", {"class": "type"}).label).replace("<label>","").replace("</label>","") for a in facts]
    #print(house_type)
    
    house_spec = [str(a.find("div", {"class": "type"}).span).replace("<span>","").replace("</span>","") for a in facts]
    #print(house_spec)
    
    sizes = [str(a.find("div", {"class": "size"}).span).replace("<span>","").replace("</span>","") for a in facts]
    #print(sizes)
    
    prices = [str(a.find("div", {"class": "price"}).span).replace("<span>","").replace("</span>","") for a in facts]
    #print(prices)
    
    years = [str(a.find("div", {"class": "year"}).span).replace("<span>","").replace("</span>","") for a in facts]
    #print(years)
    
    #Transpose data
    data=[]
    for i1,i2,i3,i4,i5,i6,i7,i8 in zip(links,cities,addresses,house_type,house_spec,sizes,prices,years):
        data.append([i1,i2,i3,i4,i5,i6,i7,i8])
    return [data,links]


import csv
def writeToCsv(file,data):
    file=os.path.expanduser(file)
    with open(file,'a') as f:
        wr = csv.writer(f, dialect='excel')
        wr.writerows(data)


test=0      
if test==1:    
    data,links,imgs=getDataFromLink('https://www.etuovi.com/myytavat-asunnot')

    dir=os.path.expanduser("~/DataMiner/house data/images")
    if not os.path.exists(dir):
        os.makedirs(dir)
    #saveImgs(links,imgs,dir)

    #for d in data: print(d)
    writeToCsv("~/DataMiner/house data/test data houses.csv", data)
    print("Done")


import datetime

#import progressbar
dir_name=os.path.expanduser("~/DataMiner/house data/")

time=str(datetime.datetime.now().date())
filename=time + " etuovi.csv"
f=open(dir_name+filename,'a')
f.close()

raw_link='https://www.etuovi.com/myytavat-asunnot/?page='
last_page=7000
        
#bar = progressbar.ProgressBar(maxval=last_page, \
#    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
#bar.start()
failed=0
for i in range(1,last_page):
    #Try getting, try saving and try saving seperately?
    try:
        print("Processing page: "+raw_link+str(i))
        data,links=getDataFromLink(raw_link+str(i))
        print("Saving")
        writeToCsv(dir_name+filename, data)
    except:
        print("Round failed ",i)
        failed=failed+1
    finally:
        if i%2==0:
            print("Progress "+str(i/last_page)+" successfull "+str(i-failed)+" failed "+str(failed))
print("Finished")
print("Failed ", failed)
print("Succeeded ", last_page-failed)
#bar.finish()

