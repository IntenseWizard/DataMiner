
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import re, time

import urllib.request


'''
<a class="carsListItemNameLink" href="https://www.autotalli.com/vaihtoauto/35897954/Renault/Laguna/2000?pos=17&amp;page=5&amp;searchType=usedCar">Renault Laguna BREAK CONFORT 1.6</a>
'''

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

def getDataFromLink(link):
    opener = AppURLopener()
    response = opener.open(link).read()
    soup = BeautifulSoup(response, "lxml")
    dataHtml = soup.findAll("div", {"class": "listContent used"})

    linkdataRaw = [a.find_all("a", {"class": "carsListItemNameLink"}) for a in dataHtml]
    links = [a['href'] for a in linkdataRaw[0]]
    
    #print(dataHtml)
    
    pricedataRaw = [a.find_all("div", {"class": "carsListItemCarDetailBottomContainer"}) for a in dataHtml]
    pricekmyeardata = [a.find_all("div", {"class": "carsListItemCarBottomContainerItem"}) for a in pricedataRaw[0]]
    prices=[]
    years=[]
    kms=[]
    for p in pricekmyeardata:
        prices.append(p[0].string)
        years.append(p[1].string)
        kms.append(p[2].string)

    
    complete_data=[]
    for i in range(0,len(links)):
        complete_data.append((links[i],
        #names[i],
        prices[i],
        kms[i],
        years[i]))
    return(complete_data)

import csv
def writeToCsv(file,data):
    with open(file,'a') as f:
        wr = csv.writer(f, dialect='excel')
        wr.writerows(data)
    
link='https://www.autotalli.com/vaihtoautot/listaa/sivu/5'
data=getDataFromLink(link)
#writeToCsv("carPrices.csv", data)

for d in data:
    print(d)


# In[2]:


import datetime
import psutil
import os

time=str(datetime.datetime.now().date())
print(time)
filename=time + " autotalli.csv"
f=open(filename,'a')
f.close()

raw_link='https://www.autotalli.com/vaihtoautot/listaa/sivu/'
last_page=2400

failed=0
for i in range(1,last_page):
    try:
        print("Progress "+str(i/last_page))
        link=raw_link+str(i)
        data=getDataFromLink(link)
        writeToCsv(filename, data)
    except KeyboardInterrupt:
        break
    except:
        print("Round failed ",i)
        failed=failed+1
print("Finished")
print("Failed ", failed)
print("Succeeded ", last_page-failed)

