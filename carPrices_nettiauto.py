
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import re, time

import urllib.request

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

def getDataFromLink(link):
    opener = AppURLopener()
    response = opener.open(link).read()
    soup = BeautifulSoup(response, "lxml")
    dataHtml = soup.findAll("div", {"class": "data_box"})

    #data = dataHtml.find("li", {"class": "bold"})

    #print(dataHtml)
    rawList=soup.find_all("div", {"class": "data_box"})

    linkdataRaw = [a.find_all("div", {"class": "location_info cleafix_nett"}) for a in rawList]
    linkdata = [a[0].find_all("a") for a in linkdataRaw]
    link = [a[0]['href'] for a in linkdata]

    links=[]
    for l in link:
        try:links.append(l.replace("#contact",''))
        except: links.append(None)
            
    nameenginedata = [a.find_all("div", {"class": "make_model_link"}) for a in rawList]
    names=[]
    for n in nameenginedata:
        try:names.append(n[0].text.strip())
        except:names.append(None)
            
    pricedata = [a.find_all("div", {"class": "main_price"}) for a in rawList]
    prices=[]
    for p in pricedata:
        try:prices.append(p[0].string)
        except:prices.append(None)
            
    kmyeardata = [a.find_all("li", {"class": "bold"}) for a in rawList]
    kms=[]
    years=[]
    for pair in kmyeardata:
        try: v1=pair[0].string
        except: v1=None
        try: v2=pair[1].string
        except: v2=None
        kms.append(v1)
        years.append(v2)

    complete_data=[]
    for i in range(0,len(links)):
        complete_data.append((links[i],
        names[i],
        prices[i],
        kms[i],
        years[i]))
    return(complete_data)

import csv
def writeToCsv(file,data):
    with open(file,'a') as f:
        wr = csv.writer(f, dialect='excel')
        wr.writerows(data)

'''link='https://www.nettiauto.com/ford/mustang'
data=getDataFromLink(link)
writeToCsv("carPrices.csv", data)'''


# In[2]:


import datetime

#import progressbar

time=str(datetime.datetime.now().date())
filename=time + " nettiauto.csv"
f=open(filename,'a')
f.close()

raw_link='https://www.nettiauto.com/vaihtoautot?page='
last_page=3087

#bar = progressbar.ProgressBar(maxval=last_page, \
#    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
#bar.start()
failed=0
for i in range(1,last_page):
    try:
        print("Progress "+str(i/last_page))
        link=raw_link+str(i)
        data=getDataFromLink(link)
        writeToCsv(filename, data)
        #bar.update(i+1)
    except:
        print("Round failed ",i)
        failed=failed+1
print("Finished")
print("Failed ", failed)
print("Succeeded ", last_page-failed)
#bar.finish()

