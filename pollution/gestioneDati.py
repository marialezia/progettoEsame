import pandas as pd
import funzioni as fz
from tqdm import tqdm
import sys, os


#-----------------------------------------------------------------------------------#
#                 Prima selezione dati: 5 stati rappresentativi                     #
#-----------------------------------------------------------------------------------#

#importo il file csv con tutti i dati e attraverso una funzione seleziono solo quelli di cinque paesi salvandoli in nuovi file csv, lascio solo le colonne che mi interessano

currentDirectory = os.getcwd()
data = pd.read_csv(currentDirectory+'/fileCSV/pollution_us_2005_2007.csv', low_memory = False)

names = (['texas.csv', 'florida.csv', 'illinois.csv', 'california.csv', 'newyork.csv'])
stateCodes = ([48, 12, 17, 6, 36])

for i in tqdm(range(len(names)), 'progression: '):
    fz.stateFromCsv(data, stateCodes[i], names[i])


#------------------------------------------------------------------------------------#
#      Seconda selezione dati: distinzione tabelle per analisi stati e stazioni      #
#------------------------------------------------------------------------------------#

#creo nuove tabelle per lo studio degli stati e delle stazioni
states = ([pd.read_csv(currentDirectory +'/fileCSV/illinois.csv'), pd.read_csv(currentDirectory +'/fileCSV/texas.csv'), pd.read_csv(currentDirectory +'/fileCSV/florida.csv'), pd.read_csv(currentDirectory +'/fileCSV/newyork.csv'), pd.read_csv(currentDirectory +'/fileCSV/california.csv')])
namesDate = (['illinoisDate.csv', 'texasDate.csv', 'floridaDate.csv', 'newyorkDate.csv', 'californiaDate.csv'])
namesDateSite =  (['illinoisDateSite.csv', 'texasDateSite.csv', 'floridaDateSite.csv', 'newyorkDateSite.csv', 'californiaDateSite.csv'])

for i in tqdm(range(len(namesDate)), 'progression: '):
          fz.meanSameDay(states[i], namesDate[i])
          fz.meanSameDaySite(states[i], namesDateSite[i])


