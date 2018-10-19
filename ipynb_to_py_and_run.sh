#transform ipynb notebooks to py if they do not exist yet

jupyter nbconvert --to python carPrices_autotie.ipynb
jupyter nbconvert --to python carPrices_nettiauto.ipynb
jupyter nbconvert --to python carPrices_autotalli.ipynb

#run with python3
python3 carPrices_autotie.py
python3 carPrices_nettiauto.py
python3 carPrices_autotalli.py
