import pandas as pd
import funzioni as fz
from tqdm import tqdm

#importo il file csv con tutti i dati e attraverso una funzione seleziono solo quelli di cinque paesi salvandoli in nuovi file csv, lascio solo le colonne che mi interessano
data = pd.read_csv('pollution_us_2005_2007.csv')

names = (['mexico.csv', 'kansas.csv', 'illinois.csv', 'california.csv', 'newyork.csv'])
stateCodes = ([80, 20, 17, 6, 36])

for i in tqdm(range(len(names)), 'progression: '):
    fz.stateFromCsv(data, stateCodes[i], names[i])

