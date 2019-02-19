
# coding: utf-8

# In[56]:


import os
import csv
import re
import sys
sys.path.insert(0,'/home/m/DataMiner/resources')
from histogram import saveFig
from histogram import makeHist
import matplotlib.pyplot as plt


'''
Part I

# def makeHist(filepath, vals):
    # print("Saving image to "+filepath)
    # # plt.use('GTK')
    # # matplotlib.use('Agg')
    # # Create and generate a word cloud image:
    # #wordcloud = WordCloud().generate(text)
    
    # fig = plt.figure(figsize=(16, 12))
    # plt.hist(vals)
    # # fig.savefig('temp.png')
    
    # # add labels
    # # plt.show()
    
    # # Display the generated image:
    # #plt.imshow(wordcloud, interpolation='bilinear')
    # fig.savefig(filepath)

def getYearPrice(data):
	y=[]
	for d in data:
		#Data is in form [link, region,street,apart.type, rooms, size, price, year]
		y.append(d[-1])
	years=sorted(set(y))

	#Get for each year list of prices
	lop=[]
	for year in years:
		year_data=[]
		for d in data:
			if year == d[-1]:
				year_data.append(int(re.sub(r'[^0-9]','',d[-2])))
		lop.append([year,year_data])
	print(lop)
	return lop



# In[57]:




#Read housedata
path=os.path.expanduser("~/DataMiner/house data/")

link=1
location='Espoo'
address=''
apartment_type=''
rooms=''
size=500
price=500000
year='1900'

count = 0
results=[]
links=[]
for filename in sorted(os.listdir(path),reverse=True):
	if filename.endswith('csv'):
		print(filename)
		#open file
		filepath=os.path.join(path,filename)
		with open(filepath) as f:
			reader = csv.reader(f)
			for row in reader:
				#row=', '.join(row)
				#print(row)
				#Get in espoo
				if location in row[1]:
					#Get smaller apartments than
					if size > int(row[5].split(',')[0]):
						#Get cheaper apartments than
						if price > int(row[6].split('€')[0].replace(" ","").replace(",","")):
							#Get younger apartments than
							if row[7]!=None:
								if year < row[7]:
									#Has sauna
									if 's' in row[4] or 'sauna' in row[4]:
										if not row[0] in links:
											results.append(row)
											links.append(row[0])
											count=count+1
#Keep one with same address
#for r in results:
#	print(r)
lop=getYearPrice(results)

for year,prices in lop:
	if len(prices)>8:
		print(year, prices)
		makeHist(os.path.join(path,"hist",year+"_hist.jpg"),prices)

print("Search produced "+str(count)+" results")

'''

'''
Part II

'''

# In[58]:



#Read housedata
path=os.path.expanduser("~/DataMiner/house data/")

link=1
location='Espoo'
address=''
apartment_type=''
rooms=''
size=500
price=500000
year='1900'

def rankLocation(text):
    if "Tapiola" in text or "Matinkylä" in text:
        return 3
    elif "Niittykumpu" in text or "Piispansilta" in text:
        return 2
    elif "Espoo" in text or "Helsinki" in text:
        return 1
    else:
        return 0
    
def rankHouseType(t):
    if "Kerrostalo" in t:
        return 2
    elif "Omakotitalo" in t:
        return 1
    elif "Paritalo" in t:
        return 1
    elif "Rivitalo" in t:
        return 3
    else:
        return 0
    
def rankSize(size):
    if size == None or size == 'None':
        return 0
		
    if size > 80: return 10
	
    elif size > 70: return 9
    elif size > 60: return 8
    elif size > 50: return 7
    elif size > 40: return 6
    
    elif size > 30: return 4
    elif size > 20: return 3
    elif size > 10: return 1
    else: return 0

def rankPrice(price):
    if price < 50000: return 10
    if price < 100000: return 9
    if price < 150000: return 8
    if price < 200000: return 7
    if price < 250000: return 6
    if price < 300000: return 3
    if price < 350000: return 2
    if price >= 350000: return 1
    else: return 0

def rankYear(year):
    if year > 2020: return 10
    elif year > 2015: return 8
    elif year > 2010: return 6
    elif year > 2005: return 4
    elif year > 2000: return 2
    elif year > 1990: return 1
    else: return 0
        
    
count = 0
results=[]
links=[]
for filename in sorted(os.listdir(path),reverse=True):
    if filename.endswith('csv'):
        print(filename)
        #open file
        filepath=os.path.join(path,filename)
        with open(filepath) as f:
            reader = csv.reader(f)
            for row in reader:
                #Perform multivariable analysis here
                
                try:
                    #print(row[1],row[3],size,price,row[7])
                    r1=rankLocation(row[1])
                    r2=rankHouseType(row[3])

                    size=int(row[5].split(',')[0].replace(" ","").replace(",",""))
                    r3=rankSize(size)

                    price=int(row[6].split('€')[0].replace(" ","").replace(",",""))
                    r5=rankPrice(price)

                    year=row[7]
                    r6=rankYear(int(year))

                    results.append([row[0],r1,r2,r3,r5,r6])
                    
                    for r in results[-1]:
                        if r == "None" or r == None:
                            print("Found None", row)
                            print(["Link","Location","Type","Size","Price","Year"])
                            print(results[-1])
                    
                except ValueError:
                    #print("Skipped: ", row)
                    1+1


# In[60]:


import pandas as pd
#Convert to a data frame
res=pd.DataFrame(results,columns = ["Link","Location","Type","Size","Price","Year"])
print(res)

from sklearn.preprocessing import StandardScaler
#Normalize data
x = res[:][["Location","Type","Size","Price","Year"]]
x = StandardScaler().fit_transform(x)
print(x)

#Make PCA for 5 dimensions
from sklearn.decomposition import PCA

pca = PCA(n_components=2)

principalComponents = pca.fit_transform(x)

principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2'])

#print(principalComponents)
finalDf = pd.concat([principalDf], axis = 1)

#print(finalDf)
#Make Clustering
# fig = plt.figure(figsize = (8,8))
# ax = fig.add_subplot(1,1,1) 
# ax.set_xlabel('Principal Component 1', fontsize = 15)
# ax.set_ylabel('Principal Component 2', fontsize = 15)
# ax.set_title('2 component PCA', fontsize = 20)

# ax.scatter(finalDf['principal component 1']
           # , finalDf['principal component 2']
           # , s = 50)
# #ax.legend(targets,loc=1)
# ax.grid()
# xmin, xmax, ymin, ymax = ax()

# In[64]:


#Get where location, type, size, price or year is optimal
res["Location"]

best=res.index[res['Location'] == 3].tolist()
second=res.index[res['Location'] == 2].tolist()
third=res.index[res['Location'] == 1].tolist()
fourth=res.index[res['Location'] == 0].tolist()

indicesToKeep=[best,second,third,fourth]

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)

targets = ['Tapiola-Matinkylä', 'Niittykumpu-Piispansilta', 'Espoo', 'Muu']
colors = ['r', 'g', 'b', 'y']
val=[0,1,2,3]
for target, color, v in zip(targets,colors,val):
    print(v)
    ind = indicesToKeep[v]
    ax.scatter(finalDf.loc[ind, 'principal component 1']
               , finalDf.loc[ind, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(targets,loc=1)
ax.grid()
xmin, xmax, ymin, ymax = plt.axis()
saveFig("/var/www/html/pca/images/location.png", fig)

# In[64]:


#Get where type is optimal

best=res.index[res['Type'] == 3].tolist()
second=res.index[res['Type'] == 2].tolist()
third=res.index[res['Type'] == 1].tolist()
fourth=res.index[res['Type'] == 0].tolist()

indicesToKeep=[best,second,third,fourth]

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)

targets = ['Rivitalo', 'Omakotitalo-Paritalo', 'Kerrostalo', 'Muu']
colors = ['r', 'g', 'b', 'y']
val=[0,1,2,3]
for target, color, v in zip(targets,colors,val):
    print(v)
    ind = indicesToKeep[v]
    ax.scatter(finalDf.loc[ind, 'principal component 1']
               , finalDf.loc[ind, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(targets,loc=1)
ax.grid()
plt.axis([xmin, xmax, ymin, ymax])
saveFig("/var/www/html/pca/images/type.png", fig)


#Get where size is optimal
res["Size"]

best=res.index[res['Size'] == 10].tolist()
second=res.index[(res['Size'] < 9) & (res['Size'] > 5)].tolist()
third=res.index[(res['Size'] < 5) & (res['Size'] != 0)].tolist()
fourth=res.index[res['Size'] == 0].tolist()

indicesToKeep=[best,second,third,fourth]

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)

targets = ['80<x', '40<x<80', 'x<40', 'Muu']
colors = ['r', 'g', 'b', 'y']
val=[0,1,2,3]
for target, color, v in zip(targets,colors,val):
    print(v)
    ind = indicesToKeep[v]
    ax.scatter(finalDf.loc[ind, 'principal component 1']
               , finalDf.loc[ind, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(targets,loc=1)
ax.grid()
plt.axis([xmin, xmax, ymin, ymax])
saveFig("/var/www/html/pca/images/size.png", fig)

#Get where price is optimal
best=res.index[res['Price'] <= 8].tolist()
second=res.index[(res['Price'] <= 6) & (res['Price'] < 8)].tolist()
third=res.index[(res['Price'] <= 2) & (res['Price'] < 6)].tolist()
fourth=res.index[res['Price'] == 1].tolist()
fifth=res.index[res['Price'] == 0].tolist()

indicesToKeep=[best,second,third,fourth,fifth]

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)

targets = ['x<150000', '150000<x<250000', '250000<x<350000', '35000<=x', 'Muu']
colors = ['r', 'g', 'b', 'y', 'c']
val=[0,1,2,3, 4]
for target, color, v in zip(targets,colors,val):
    print(v)
    ind = indicesToKeep[v]
    ax.scatter(finalDf.loc[ind, 'principal component 1']
               , finalDf.loc[ind, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(targets,loc=1)
ax.grid()
plt.axis([xmin, xmax, ymin, ymax])
saveFig("/var/www/html/pca/images/price.png", fig)


#Get where year is optimal
best=res.index[res['Year'] == 10].tolist()
second=res.index[res['Year'] == 8].tolist()
third=res.index[res['Year'] == 6].tolist()
fourth=res.index[res['Year'] == 4].tolist()
fifth=res.index[res['Year'] == 2].tolist()
sixth=res.index[res['Year'] == 1].tolist()

indicesToKeep=[best,second,third,fourth,fifth,sixth]

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)

targets = ['2020', '2015', '2005', '2000', '1990', 'Muu']
colors = ['r', 'g', 'b', 'y', 'c', 'm']
val=[0,1,2,3,4,5]
for target, color, v in zip(targets,colors,val):
    print(v)
    ind = indicesToKeep[v]
    ax.scatter(finalDf.loc[ind, 'principal component 1']
               , finalDf.loc[ind, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(targets,loc=1)
ax.grid()
plt.axis([xmin, xmax, ymin, ymax])
saveFig("/var/www/html/pca/images/year.png", fig)


#Create html
img_paths=["./images/location.png",
		   "./images/type.png",
		   "./images/size.png",
		   "./images/price.png",
		   "./images/year.png"]
names=["Location","Type","Size","Price","Year"]
html_file_path='/var/www/html/pca/images.html'
html=""
for path, name in zip(img_paths,names):
    #html=html+'<figure><img src="'+path+'" alt="'+name+'"hspace="10" vspace="10" align="middle"><figcaption>'+name+'</figcaption></figure>'
	html=html+'<div class="column">\n<img src="'+path+'" alt="'+name+'" style="width:100%" onclick="myFunction(this);">\n</div>'

#write html to path
print("HTML Code is")
print(html)
f = open(html_file_path, "w")
f.write(html) 
# f.write("Keywords left out: "+",".join(sorted(konjunktiot))) 
f.close()


