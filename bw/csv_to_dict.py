import pandas as pd

strains = pd.read_csv('https://raw.githubusercontent.com/Build-Week-Med-Cabinet-2-MP/bw-med-cabinet-2-ml/data-generation/data/CLEAN_WMS_2020_05_24.csv')

strains_json = strains.to_json(orient='index')

print(strains_json)