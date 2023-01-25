import numpy as np
import pandas as pd
import funzioni as fz
from tqdm import tqdm

#creo nuove tabelle per lo studio degli stati e delle stazioni
states = ([pd.read_csv('~/progettoEsame/fileCSV/illinois.csv'), pd.read_csv('~/progettoEsame/fileCSV/mexico.csv'), pd.read_csv('~/progettoEsame/fileCSV/kansas.csv'), pd.read_csv('~/progettoEsame/fileCSV/newyork.csv'), pd.read_csv('~/progettoEsame/fileCSV/california.csv')])
namesDate = (['illinoisDate.csv', 'mexicoDate.csv', 'kansasDate.csv', 'newyorkDate.csv', 'californiaDate.csv'])
namesDateSite =  (['illinoisDateSite.csv', 'mexicoDateSite.csv', 'kansasDateSite.csv', 'newyorkDateSite.csv', 'californiaDateSite.csv'])

for i in tqdm(range(len(namesDate)), 'progression: '):
          fz.meanSameDay(states[i], namesDate[i])
          fz.meanSameDaySite(states[i], namesDateSite[i])



 
