import pandas as pd
import funzioni as fz
from tqdm import tqdm


#-----------------------------------------------------------------------------------#
#                 Prima selezione dati: 5 stati rappresentativi                     #
#-----------------------------------------------------------------------------------#

#importo il file csv con tutti i dati e attraverso una funzione seleziono solo quelli di cinque paesi salvandoli in nuovi file csv, lascio solo le colonne che mi interessano

data = pd.read_csv('~/progettoEsame/fileCSV/pollution_us_2005_2007.csv')

names = (['texas.csv', 'kansas.csv', 'illinois.csv', 'california.csv', 'newyork.csv'])
stateCodes = ([48, 20, 17, 6, 36])

for i in tqdm(range(len(names)), 'progression: '):
    fz.stateFromCsv(data, stateCodes[i], names[i])


#------------------------------------------------------------------------------------#
#      Seconda selezione dati: distinzione tabelle per analisi stati e stazioni      #
#------------------------------------------------------------------------------------#

#creo nuove tabelle per lo studio degli stati e delle stazioni
states = ([pd.read_csv('~/progettoEsame/fileCSV/illinois.csv'), pd.read_csv('~/progettoEsame/fileCSV/texas.csv'), pd.read_csv('~/progettoEsame/fileCSV/kansas.csv'), pd.read_csv('~/progettoEsame/fileCSV/newyork.csv'), pd.read_csv('~/progettoEsame/fileCSV/california.csv')])
namesDate = (['illinoisDate.csv', 'texasDate.csv', 'kansasDate.csv', 'newyorkDate.csv', 'californiaDate.csv'])
namesDateSite =  (['illinoisDateSite.csv', 'texasDateSite.csv', 'kansasDateSite.csv', 'newyorkDateSite.csv', 'californiaDateSite.csv'])
namesMonth = (['illinoisMonth.csv', 'texasMonth.csv', 'kansasMonth.csv', 'newyorkMonth.csv', 'californiaMonth.csv'])
for i in tqdm(range(len(namesDate)), 'progression: '):
          fz.meanSameDay(states[i], namesDate[i])
          fz.meanSameDaySite(states[i], namesDateSite[i])
          fz.meanSameDayMonth(states[i], namesMonth[i])

