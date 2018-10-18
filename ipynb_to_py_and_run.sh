#transform ipynb notebooks to py if they do not exist yet

if exist carPrices_autotie.ipynb (
    echo "File exists"
) else (
    jupyter nbconvert --to python carPrices_autotie.ipynb 
)

if exist carPrices_nettiauto.ipynb (
    echo "File exists"
) else (
    jupyter nbconvert --to python carPrices_nettiauto.ipynb 
)

if exist carPrices_autotalli.ipynb (
    echo "File exists"
) else (
    jupyter nbconvert --to python carPrices_autotalli.ipynb 
)

#run with python3
python3 carPrices_autotie.py
python3 carPrices_nettiauto.py
python3 carPrices_autotalli.py
