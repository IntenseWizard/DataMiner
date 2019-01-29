
# coding: utf-8

# In[ ]:


import os
import csv
import re
dir_path=os.path.expanduser("~/DataMiner/hs_data")
all_text=[]
names=[]
for file in sorted(os.listdir(dir_path),reverse=True):
    print(file)
    with open(os.path.join(dir_path,file)) as csvfile:
        day=[]
        names.append(file)
        reader=csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            rawrow=', '.join(row)
            print(rawrow)
            if "https" not in rawrow and len(rawrow)>5:
                #regex = re.compile('[^a-zA-Z]')
                regex = re.compile('[,\.!?–]')
                text = regex.sub('', rawrow)
                day.append(text)
        all_text.append(day)


# In[22]:


import numpy as np
#import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import subprocess, sys

def makeWordmap(text):
    get_ipython().magic('matplotlib inline')
    
    # Create and generate a word cloud image:
    wordcloud = WordCloud().generate(text)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

def makeWordmapImg(text,filepath):
    print("Saving image to "+filepath)
    # plt.use('GTK')
    # matplotlib.use('Agg')
    # Create and generate a word cloud image:
    wordcloud = WordCloud().generate(text)
    
    # Display the generated image:
    #plt.imshow(wordcloud, interpolation='bilinear')
    plt.imsave(filepath, wordcloud)

#Check sudo
# if os.geteuid() == 0:
    # print("We're root!")
# else:
    # print("We're not root.")
    # subprocess.call(['sudo', 'python3', *sys.argv])
    

#Check writepath
writePath='/var/www/html/images/hs/'
if not os.path.exists(writePath):
    os.mkdir(writePath)

html_img_path='./images/hs/'
html_file_path='/var/www/html/images.html'
html=""
#Do the magic
konjunktiot=['ei','nyt','oli','jo','se','ovat','on','ja','mutta','ole','se','vain', 'joka','sen','myös','ettei','sanoo','näyttää','vuosi','vuonna','vuotias','viime','puoli','eivät','sitten','aikaan','niin','saa','sai','saatu','jälkeen']
for day,name in zip(all_text,names):
    pure_text=day
    print(name)
    for k in konjunktiot:
        #pure_text= [a.replace(k,"") for a in pure_text]
        pure_text= [re.sub(r"\b%s\b" % k, "", a) for a in pure_text]
    #makeWordmap(str(pure_text))
    n=name.replace("csv","jpg")
    makeWordmapImg(str(pure_text), os.path.join(writePath,n))
    #Generate HTML
    html_filepath=html_img_path+n
    html=html+'<div class="column"><img src="'+html_filepath+'" alt="'+name+'"></div>'
    
#write html to path
print("HTML Code is")
print(html)
f = open(html_file_path, "w")
f.write(html) 
# f.write("Keywords left out: "+",".join(sorted(konjunktiot))) 
f.close()