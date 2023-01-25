import pandas as pd
import numpy as np
import classi as cl
import sys, os
from tqdm import tqdm
from scipy import constants, fft

#---------------------------------------------------------------#
#           Definizioni moduli per Gestione dati                #
#---------------------------------------------------------------#

def groupSc(df, sc):
    #mi resistuisce una tabella corrispondente allo stato di codice sc
    groups = df.groupby(['State Code'])
    return groups.get_group(sc)

def dropColumns(df):
    #per rendere più ordinate le tabelle elimina tutte le colonne che non vado ad analizzare
    df = df.drop(columns=['NO2 1st Max Value', 'NO2 1st Max Hour', 'NO2 AQI', 'O3 1st Max Value', 'O3 1st Max Hour', 'O3 AQI', 'SO2 1st Max Value', 'SO2 1st Max Hour', 'SO2 AQI', 'CO 1st Max Value', 'CO 1st Max Hour', 'CO AQI', 'Unnamed: 29'])
    return df

def stateFromCsv(df, sc, name):
    #dal file CSV generale con tutti gli stati estrae quelli corrispondenti allo State Code inserito (sc) e salva in un nuovo file csv tutti i dati riguardanti quello stato eliminando le colonne di non interesse per lo studio
    newDf = groupSc(df, sc)
    newDf = dropColumns(newDf)
    newDf.to_csv('~/progettoEsame/fileCSV/'+name)


def meanSameDaySite(df, name):
    #Per studio differenti stazioni di monitoraggio: raggruppa la tabella secondo i parametri data e stazione di monitoraggio, quando sono ripetuti fa la media dei valori e riordina la tabella in base alla data 
    groups = df.groupby(['Date Local', 'Site Num'], as_index=False)
    df = groups.agg(
        stateCode = pd.NamedAgg(column = 'State Code', aggfunc = 'first'),
        countryCode = pd.NamedAgg(column = 'County Code', aggfunc = 'first'),
        address = pd.NamedAgg(column = 'Address', aggfunc = 'first'),
        state = pd.NamedAgg(column = 'State', aggfunc = "first"),
        country = pd.NamedAgg(column = 'County', aggfunc = 'first'),
        city = pd.NamedAgg(column = 'City', aggfunc = "first"),
        no2 = pd.NamedAgg(column = 'NO2 Mean', aggfunc = np.mean),
        o3 = pd.NamedAgg(column = 'O3 Mean', aggfunc = np.mean),
        so2 = pd.NamedAgg(column = 'SO2 Mean', aggfunc = np.mean),
        co = pd.NamedAgg(column = 'CO Mean', aggfunc = np.mean),
    )
    df['days'] = pd.to_datetime(df['Date Local'], format = '%d/%m/%Y') 
    df.sort_values(by='days', inplace = True) 
    df.to_csv('~/progettoEsame/fileCSV/' + name)

def meanSameDay(df, name):
    #Per studio stati, senza differenziare stazioni di monitoraggio: raggruppa la tabella secondo solo la data e fa la media dei valori in cui la data è la stessa, riordina secondo la data
    groups = df.groupby('Date Local', as_index=False)
    df = groups.agg(
        no2 = pd.NamedAgg(column = 'NO2 Mean', aggfunc = np.mean),
        o3 = pd.NamedAgg(column = 'O3 Mean', aggfunc = np.mean),
        so2 = pd.NamedAgg(column = 'SO2 Mean', aggfunc = np.mean),
        co = pd.NamedAgg(column = 'CO Mean', aggfunc = np.mean),
    )
    df['days'] = pd.to_datetime(df['Date Local'], format = '%d/%m/%Y') 
    df.sort_values(by='days', inplace = True) 
    df.to_csv('~/progettoEsame/fileCSV/' + name)


#---------------------------------------------------------------#
#           Definizioni moduli per Analisi Stati                #
#---------------------------------------------------------------#

def createStato2(df):
    stato = cl.Stato2()
    dates = pd.to_datetime(df['Date Local'], format = '%d/%m/%Y')
    stato.aggiornaStato(dates, df['no2'].values,  df['o3'].values, df['so2'].values, df['co'].values)
    return stato
       
def mask(freq, soglia):
    return np.absolute(freq) > soglia

def maskStato(stato, sogliaNo2, sogliaO3, sogliaSo2, sogliaCo):
    #soglie = ([sogliaNo2, sogliaO3, sogliaSo2, sogliaCo])
    statoCopia = cl.Stato2Fft(stato)
    mascheraNo2 = mask(statoCopia.no2F, sogliaNo2)
    mascheraO3 = mask(statoCopia.o3F, sogliaO3)
    mascheraSo2 = mask(statoCopia.so2F, sogliaSo2)
    mascheraCo = mask(statoCopia.coF, sogliaCo)
    statoCopia.mascheraStato(mascheraNo2, mascheraO3, mascheraSo2, mascheraCo)
    return statoCopia

def sintesiFiltrato2(statoFiltratoFft):
    stato = cl.Stato2()
    stato.sintesi(statoFiltratoFft)
    return stato

def differenza(stato, statoFiltrato):
    diff = cl.Stato2()
    diff.date = stato.date
    diff.no2 = stato.no2 - statoFiltrato.no2
    diff.o3 = stato.o3 - statoFiltrato.o3
    diff.so2 = stato.so2 - statoFiltrato.so2
    diff.co = stato.co - statoFiltrato.co
    return diff

#---------------------------------------------------------------#
#          Definizioni moduli per Analisi Stazioni              #
#---------------------------------------------------------------#

def groupSn(df, sn):
    #mi resituisce una tabella corrispondente alla stazione di monitoraggio sn
    gp = df.groupby(['Site Num'])
    return gp.get_group(sn)

def chiavi(df):
    gp = df.groupby(['Site Num'])
    keys = np.empty(0, dtype=int)
    for i in gp.groups.keys():
        keys = np.append(keys, int(i))
    return keys
    
def createSite(df, sn):
    newDf = groupSn(df, sn)
    dates = pd.to_datetime(newDf['Date Local'], format = '%d/%m/%Y')
    s = cl.Site()
    s.aggiornaSite(dates, newDf['Site Num'], newDf['address'], newDf['city'], newDf['no2'].values, newDf['o3'].values, newDf['so2'].values, newDf['co'].values)
    return s

def createStato(df, sitesNum):
    stato = cl.Stato(sitesNum)
    for i in tqdm(sitesNum, 'creating State: '):
        stato.addSite(createSite(df, i))
    return stato     

def createStatoFft(stato):
    statoFft = cl.StatoFft()
    statoFft.addSites(stato)
    return statoFft

def sintesiSite(siteFft):
    siteFiltrata = cl.Site()
    siteFiltrata.sintesi(siteFft)
    return siteFiltrata

def maskSite(site, sogliaNo2, sogliaO3, sogliaSo2, sogliaCo):
    maskNo2 = mask(site.no2F, sogliaNo2)
    maskO3 = mask(site.o3F, sogliaO3)
    maskSo2 = mask(site.so2F, sogliaSo2)
    maskCo = mask(site.coF, sogliaCo)
    site.no2Fft[maskNo2] = 0
    site.o3Fft[maskO3] = 0
    site.so2Fft[maskSo2] = 0
    site.coFft[maskCo] = 0

    return site

def maskStato2(stato, sogliaNo2, sogliaO3, sogliaSo2, sogliaCo):
    statoCopia = cl.StatoFft()
    statoCopia.addSites(stato)

    for i in statoCopia.sitesFft:
        i = maskSite(i, sogliaNo2, sogliaO3, sogliaSo2, sogliaCo)
    return statoCopia


def sintesiFiltrato(stato, statoFiltratoFft, siteNum):
    sfiltrato = cl.Stato(siteNum)
    sfiltrato.sintesi(statoFiltratoFft)
    return sfiltrato




#---------------------------------------------------------------#
#           Vecchie definizioni                                 #
#---------------------------------------------------------------#


'''
    
def newDfDateSite(df, name):
    #Per studio differenti stazioni di monitoraggio: raggruppa la tabella secondo i parametri data e stazione di monitoraggio, quando sono ripetuti fa la madia dei valori e riordina la tabella in base alla data 
    df = df.groupby(['Date Local','Site Num'], as_index = False).mean(True)
    df['days'] = pd.to_datetime(df['Date Local'], format = '%d/%m/%Y') 
    df.sort_values(by='days', inplace = True) 
    df.to_csv('~/progettoEsame/fileCSV/' + name)

def newDfDate(df, name):
    #Per studio stati, senza differenziare stazioni di monitoraggio: raggruppa la tabella secondo solo la data e fa la media dei valori in cui la data è la stessa, riordina secondo la data
    df = df.groupby('Date Local', as_index = False).mean(True)
    df['days'] = pd.to_datetime(df['Date Local'], format = '%d/%m/%Y') 
    df.sort_values(by='days', inplace = True) 
    df.to_csv('~/progettoEsame/fileCSV/' + name)
    
def meanSameDays(df):
    groups = df.groupby('Date Local', as_index=False)
    df = groups.agg(
        indice = pd.NamedAgg(column = 'Unnamed: 0', aggfunc = 'first'),
        stateCode = pd.NamedAgg(column = 'State Code', aggfunc = 'first'),
        countryCode = pd.NamedAgg(column = 'County Code', aggfunc = 'first'),
        siteNum = pd.NamedAgg(column = 'Site Num', aggfunc = 'first'),
        address = pd.NamedAgg(column = 'Address', aggfunc = 'first'),
        state = pd.NamedAgg(column = 'State', aggfunc = "first"),
        country = pd.NamedAgg(column = 'County', aggfunc = 'first'),
        city = pd.NamedAgg(column = 'City', aggfunc = "first"),
        no2 = pd.NamedAgg(column = 'NO2 Mean', aggfunc = np.mean),
        no2Err = pd.NamedAgg(column = 'NO2 Mean', aggfunc = np.std),
        o3 = pd.NamedAgg(column = 'O3 Mean', aggfunc = np.mean),
        o3Err = pd.NamedAgg(column = 'O3 Mean', aggfunc = np.std),
        so2 = pd.NamedAgg(column = 'SO2 Mean', aggfunc = np.mean),
        so2Err = pd.NamedAgg(column = 'SO2 Mean', aggfunc = np.std),
        co = pd.NamedAgg(column = 'CO Mean', aggfunc = np.mean),
        coErr = pd.NamedAgg(column = 'CO Mean', aggfunc = np.std),
    )
    return df


    
def newDfMean(df, name):
    df = meanSameDays(df)
    df['days'] = pd.to_datetime(df['Date Local'], format = '%d/%m/%Y') 
    df.sort_values(by='days', inplace = True) 
    df.to_csv('~/progettoEsame/fileCSV/' + name)

def newDfMean2(df, name):
    df = meanSameDays(df)
    df = df.sort_values(by='Starting_dates', inplace = True) 
    df.to_csv(name)


 
'''
