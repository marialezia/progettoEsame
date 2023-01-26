import pandas as pd
import numpy as np
import classi as cl
import sys, os
from tqdm import tqdm
from scipy import constants, fft

'''
Nel file sono vengono definite i moduli necessari per l'esecuzione dei file di analisi.
'''
#---------------------------------------------------------------#
#           Definizioni moduli per Gestione dati                #
#---------------------------------------------------------------#

def groupSc(df, sc):
    '''
    Restituisce una tabella che contiene i dati corrispondenti allo stato con State Code sc. 
    Parametri: 
    df: tabella da cui estrapola la sottotabella, contiene tutti gli stati
    sc: State Code corrispondente allo stato di cui si vogliono selezionare i dati
    '''
    groups = df.groupby(['State Code'])
    return groups.get_group(sc)

def dropColumns(df):
    '''Elimina dalla tabella le colonne relative ai dati che non sono di interesse per l'analisi'''
    df = df.drop(columns=['NO2 1st Max Value', 'NO2 1st Max Hour', 'NO2 AQI', 'O3 1st Max Value', 'O3 1st Max Hour', 'O3 AQI', 'SO2 1st Max Value', 'SO2 1st Max Hour', 'SO2 AQI', 'CO 1st Max Value', 'CO 1st Max Hour', 'CO AQI', 'Unnamed: 29'])
    return df

def stateFromCsv(df, sc, name):
    '''
    Salva in un nuovo file csv i dati di uno stato, seleziona solo i dati di interesse.
    Parametri: 
    df: tabella da cui estrae i dati
    sc: State Code dello stato di cui si vogliono selezionare i dati
    name: nome con cui viene salvato il file
    '''
    newDf = groupSc(df, sc)
    newDf = dropColumns(newDf)
    newDf.to_csv('~/progettoEsame/fileCSV/'+name)


def meanSameDaySite(df, name):
    '''
    Per lo studio delle differenti stazioni all'interno di uno stato. 
    Raggruppa la tabella secondo i parametri data e stazione di monitoraggio, quando sono ripetuti fa la media dei valori degli inquinanti e riordina la tabella in base alla data. 
    Parametri: 
    df: tabella da cui estrae i dati
    name: nome con cui viene salvato il file
    ''' 
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
    '''
    Per lo studio degli stati, senza differenziare le stazioni. 
    Raggruppa la tabella secondo la data, fa la media dei valori degli inqunanti in cui la data è la stessa, riordina secondo la data
    Parametri: 
    df: tabella da cui estrae i dati
    name: nome con cui viene salvato il file
    ''' 
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

def meanSameDayMonth(df, name):
    '''
    Per lo studio degli stati, senza differenziare le stazioni. 
    Raggruppa la tabella secondo la data, fa la media dei valori degli inqunanti in cui la data è la stessa, riordina secondo la data.
    Per ogni mese fa la media dei valori. 
    Parametri: 
    df: tabella da cui estrae i dati
    name: nome con cui viene salvato il file
    ''' 
    df['Date Local'] = pd.to_datetime(df['Date Local'], format = '%d/%m/%Y') 
    groups = df.groupby('Date Local', as_index=False)
    df = groups.agg(
        no2 = pd.NamedAgg(column = 'NO2 Mean', aggfunc = np.mean),
        o3 = pd.NamedAgg(column = 'O3 Mean', aggfunc = np.mean),
        so2 = pd.NamedAgg(column = 'SO2 Mean', aggfunc = np.mean),
        co = pd.NamedAgg(column = 'CO Mean', aggfunc = np.mean),
    )
    df['Date Local'] = pd.to_datetime(df['Date Local'], format = '%d/%m/%Y') 
    df = df.resample(rule='M', on='Date Local').mean()
    df.to_csv('~/progettoEsame/fileCSV/' + name)

#---------------------------------------------------------------#
#           Definizioni moduli per Analisi Stati                #
#---------------------------------------------------------------#

def createStato2(df):
    '''
    Crea una classe stato prendendo i dati dalla tabella. 
    Parametri: 
    df: tabella da cui estrae i dati 
    '''
    stato = cl.Stato2()
    dates = pd.to_datetime(df['Date Local'], format = '%d/%m/%Y')
    stato.aggiornaStato(dates, df['no2'].values,  df['o3'].values, df['so2'].values, df['co'].values)
    return stato
    
def createStato2b(df):
    '''
    Crea una classe stato prendendo i dati dalla tabella, variante per la tabella con medie mensili. 
    Parametri: 
    df: tabella da cui estrae i dati 
    '''
    stato = cl.Stato2()
    stato.aggiornaStato(df['Date Local'], df['no2'].values,  df['o3'].values, df['so2'].values, df['co'].values)
    return stato
       
def mask(freq, soglia):
    return np.absolute(freq) > soglia

def maskStato(statoFft, sogliaNo2, sogliaO3, sogliaSo2, sogliaCo):
    '''
    Mette a zero i coefficienti di fourier degli inquinanti dello statoFft che sono superiori alle soglie passate.
    Parametri: 
    statoFft: statoFft* da filtrare 
    sogliaNo2, sogliaO3, sogliaSo2, sogliaCo: soglie frequenze corrispondenti ai quattro inquinanti
    '''
    statoCopia = cl.Stato2Fft(statoFft)
    mascheraNo2 = mask(statoCopia.no2F, sogliaNo2)
    mascheraO3 = mask(statoCopia.o3F, sogliaO3)
    mascheraSo2 = mask(statoCopia.so2F, sogliaSo2)
    mascheraCo = mask(statoCopia.coF, sogliaCo)
    statoCopia.mascheraStato(mascheraNo2, mascheraO3, mascheraSo2, mascheraCo)
    return statoCopia

def sintesiFiltrato2(statoFiltratoFft):
    '''
    Risintetizza i coefficienti di Fourier dello statoFft filtrato e restituisce uno stato
    statoFiltratoFft: statoFft filtrato da risintetizzare 
    '''
    stato = cl.Stato2()
    stato.sintesi(statoFiltratoFft)
    return stato

def differenza(stato, statoFiltrato):
    '''Restituisce uno stato differenza in cui per ogni inquinante è presente la differenza tra i dati originali e quelli filtrati'''
    diff = cl.Stato2()
    diff.date = stato.date
    diff.days = stato.days
    diff.no2 = stato.no2 - statoFiltrato.no2
    diff.o3 = stato.o3 - statoFiltrato.o3
    diff.so2 = stato.so2 - statoFiltrato.so2
    diff.co = stato.co - statoFiltrato.co
    return diff

def massimo(statoFft):
    ''' 
    Restituisce i tre array: 
    - maxx: contiene gli indici del massimo valore dello spettro di potenza, per ognuno dei quattro inquinanti
    - fmax: contiente la frequenza in cui si registra il massimo, per ognuno dei quattro inquinanti
    - pmax: contiente il periodo in cui si registra il massimo, per ognuno dei quattro inquinanti
    di quattro elementi, uno per ogni inquinante, in cui sono presenti l'indice in cui 
    '''
    maxx = ([np.argmax(statoFft.no2P[1:]), np.argmax(statoFft.o3P[1:]), np.argmax(statoFft.so2P[1:]), np.argmax(statoFft.coP[1:])])
    fmax = ([statoFft.no2F[maxx[0]], statoFft.o3F[maxx[1]], statoFft.so2F[maxx[2]], statoFft.coF[maxx[3]]])
    pmax = ([1/fmax[0], 1/fmax[1], 1/fmax[2], 1/fmax[3]])    
    return maxx, fmax, pmax

def printMax(fmax, pmax, name):
    '''Visualizza sullo schermo le frequenze e il periodo in cui si ha il massimo, per ogni inquinante'''
    print('Valori corripondenti allo stato' + name + '\n')
    print('-------------------------------------------------------------')
    print('|           |    NO2    |    O3     |    SO2    |    CO     |')
    print('| freq max  |  '+str(round(fmax[0], 5))+'  |  '+str(round(fmax[1], 5))+'  |  '+ str(round(fmax[2], 5))+'  |  '+str(round(fmax[3], 5))+'  |')
    print('| per  max  |  '+str(round(pmax[0], 5))+'  |  '+str(round(pmax[1], 5))+'  |  '+ str(round(pmax[2], 5))+'  |  '+str(round(pmax[3], 5))+'  |')
    print('-------------------------------------------------------------')

def correlazione(stato):
    '''Restituisce una tabella con i coefficienti di correlazione tra gli inquinanti di uno stato'''
    df = pd.DataFrame()
    df['no2'] = stato.no2
    df['o3'] = stato.o3
    df['so2'] = stato.so2
    df['co'] = stato.co
    return df.corr()



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


def correlazioneStati(s1, s2, s3, s4, s5, name1, name2, name3, name4, name5):
    dfno2 = pd.DataFrame()
    dfo3 = pd.DataFrame()
    dfso2 = pd.DataFrame()
    dfco = pd.DataFrame()

    dfno2[name1] = s1.no2
    dfno2[name2] = s2.no2
    dfno2[name3] = s3.no2
    dfno2[name4] = s4.no2
    dfno2[name5] = s5.no2

    dfo3[name1] = s1.o3
    dfo3[name2] = s2.o3
    dfo3[name3] = s3.o3
    dfo3[name4] = s4.o3
    dfo3[name5] = s5.o3
    
    dfso2[name1] = s1.so2
    dfso2[name2] = s2.so2
    dfso2[name3] = s3.so2
    dfso2[name4] = s4.so2
    dfso2[name5] = s5.so2

    dfco[name1] = s1.co
    dfco[name2] = s2.co
    dfco[name3] = s3.co
    dfco[name4] = s4.co
    dfco[name5] = s5.co
    return dfno2.corr(), dfo3.corr(), dfso2.corr(), dfco.corr()
 
'''
