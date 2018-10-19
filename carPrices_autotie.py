
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import re, time

import urllib.request

class AppURLopener2(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

import csv
def writeToCsv(file,data):
    with open(file,'a') as f:
        wr = csv.writer(f, dialect='excel')
        wr.writerows(data)
    
def getDataFromAutotieLink(link):
    
    opener = AppURLopener2()
    response = opener.open(link).read()
    soup = BeautifulSoup(response, "lxml")
    dataHtml = soup.findAll("div", {"data-robot-layout": "hakutuloslista"})
    

    #print(data)
    #rawList=soup.find_all("div", {"class": "linkki-autoilmoitukseen"})
    
    linkdataRaw = [a.find_all("li", {"class": "auto-ilmoitus"}) for a in dataHtml]
    #print(linkdataRaw)
    linkdata = [a.find_all("a") for a in linkdataRaw[0]]
    link = [a[0]['href'] for a in linkdata]
    
    links=[]
    names=[]
    for l in link:
        links.append(l)
        names.append(re.sub("%20", " ", " ".join(l.split("/")[2:4])))
        
    pricedataRaw = [a.find_all("span", {"data-robot": "autokortti-hinta"}) for a in dataHtml]
    price=[]
    for p in pricedataRaw[0]:
        price.append(p.string)
        
    yeardataRaw = [a.find_all("div", {"data-robot": "autokortti-vuosimalli"}) for a in dataHtml]
    years=[]
    for y in yeardataRaw[0]:
        years.append(y.string)
        
    labeldataRaw = [a.find_all("div", {"class": "tietoLabel"}) for a in dataHtml]
    faktadataRaw = [a.find_all("div", {"class": "tietoFakta"}) for a in dataHtml]
    #print(kmsdataRaw)
    kms=[]
    for l,f in zip(labeldataRaw[0], faktadataRaw[0]):
        if l.string == "Mittarilukema":
            #kms.append(f.string.replace(r"\xa",'').replace(" km",''))
            #print(f.string)
            #print(re.sub(f.string, "", ""))
            kms.append(re.sub("[^0-9.]", "", f.string))
    #print(kms)
    
    complete_data=[]
    for i in range(0,len(links)):
        complete_data.append((links[i],
        names[i],
        price[i],
        kms[i],
        years[i]))
    return(complete_data)

import datetime

time=str(datetime.datetime.now().date())
filename=time + " autotie.csv"
f=open(filename,'a')
f.close()

raw_link='https://www.autotie.fi/vaihtoautot/hakutulos/hae?Lajittelu=0&Sivu='
last_page=1600

failed=0
for i in range(1,last_page):
    #try:
    print("Progress "+str(i/last_page))
    link=raw_link+str(i)
    data = getDataFromAutotieLink(link)
    writeToCsv(filename, data)
    #bar.update(i+1)
    #except:
    #print("Round failed ",i)
    #failed=failed+1
print("Finished")
print("Failed ", failed)
print("Succeeded ", last_page-failed)

