#transform ipynb notebooks to py if they do not exist yet

jupyter nbconvert --to python carPrices_autotie.ipynb
jupyter nbconvert --to python carPrices_nettiauto.ipynb
jupyter nbconvert --to python carPrices_autotalli.ipynb
jupyter nbconvert --to python carPrices_insert.ipynb
jupyter nbconvert --to python carPrices_analysis.ipynb

#run with python3
# python3 carPrices_autotie.py
# python3 carPrices_nettiauto.py
# python3 carPrices_autotalli.py

 #pip3 install requests
 #sudo apt install python3-bs4
 #sudo apt install python3-psutil
