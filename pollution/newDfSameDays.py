import numpy as np
import pandas as pd
import funzioni as fz
from tqdm import tqdm


#creo nuove tabelle in cui si fa la media dei valori ripetuti ogni giorno associando come errore la deviazione standard
states = ([pd.read_csv('~/progettoEsame/fileCSV/illinois.csv'), pd.read_csv('~/progettoEsame/fileCSV/mexico.csv'), pd.read_csv('~/progettoEsame/fileCSV/kansas.csv'), pd.read_csv('~/progettoEsame/fileCSV/newyork.csv'), pd.read_csv('~/progettoEsame/fileCSV/california.csv')])
names = (['newIllinois.csv', 'newMexico.csv', 'newKansas.csv', 'newNewyork.csv', 'newCalifornia.csv'])
for i in tqdm(range(len(names)), 'progression: '):
          fz.newDfMean(states[i], names[i])

