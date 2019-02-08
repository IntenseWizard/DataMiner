import os
import csv
import re
import sys
sys.path.insert(0,'/home/m/DataMiner/resources')
from histogram import makeHist

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


