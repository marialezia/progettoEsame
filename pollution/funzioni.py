import pandas as pd
import numpy as np
import classi as cl
import sys, os
from tqdm import tqdm
from scipy import constants, fft
from scipy import optimize
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


"""
Nel file sono vengono definiti i moduli necessari per l'esecuzione dei file di analisi.
"""
#---------------------------------------------------------------#
#           Definizioni moduli per Gestione dati                #
#---------------------------------------------------------------#

def groupSc(df, sc):
    """
    Restituisce una tabella che contiene i dati corrispondenti allo stato con State Code sc. 
    Parametri: 
    df: pandas DataFrame, tabella da cui estrapola la sottotabella, contiene tutti gli stati
    sc: numero intero, State Code corrispondente allo stato di cui si vogliono selezionare i dati
    """
    groups = df.groupby(['State Code'])
    return groups.get_group(sc)

def dropColumns(df):
    """Elimina dalla tabella le colonne relative ai dati che non sono di interesse per l'analisi"""
    df = df.drop(columns=['NO2 1st Max Value', 'NO2 1st Max Hour', 'NO2 AQI', 'O3 1st Max Value', 'O3 1st Max Hour', 'O3 AQI', 'SO2 1st Max Value', 'SO2 1st Max Hour', 'SO2 AQI', 'CO 1st Max Value', 'CO 1st Max Hour', 'CO AQI', 'Unnamed: 29'])
    return df

def stateFromCsv(df, sc, name):
    """
    Salva in un nuovo file csv i dati di uno stato, seleziona solo i dati di interesse.
    Parametri: 
    df: pandas DatFrame, tabella da cui estrae i dati
    sc: numero intero, State Code dello stato di cui si vogliono selezionare i dati
    name: stringa, nome con cui viene salvato il file
    """
    newDf = groupSc(df, sc)
    newDf = dropColumns(newDf)
    newDf.to_csv('~/progettoEsame/fileCSV/'+name)


def meanSameDaySite(df, name):
    """
    Per lo studio delle differenti stazioni all'interno di uno stato. 
    Raggruppa la tabella secondo i parametri data e stazione di monitoraggio, quando sono ripetuti fa la media dei valori degli inquinanti e riordina la tabella in base alla data. 
    Parametri: 
    df: pandas DataFrame, tabella da cui estrae i dati
    name: stringa, nome con cui viene salvato il file
    """ 
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
    """
    Per lo studio degli stati, senza differenziare le stazioni. 
    Raggruppa la tabella secondo la data, fa la media dei valori degli inqunanti in cui la data è la stessa, riordina secondo la data
    Parametri: 
    df: pandas DataFrame, tabella da cui estrae i dati
    name: stringa, nome con cui viene salvato il file
    """ 
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
    """
    Per lo studio degli stati, senza differenziare le stazioni. 
    Raggruppa la tabella secondo la data, fa la media dei valori degli inqunanti in cui la data è la stessa, riordina secondo la data.
    Per ogni mese fa la media dei valori. 
    Parametri: 
    df: pandas DataFrame, tabella da cui estrae i dati
    name: stringa, nome con cui viene salvato il file
    """ 

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

def month(stato, filtro):
    statoFiltratoFft = maskStato(stato, filtro, filtro, filtro, filtro)
    statoFiltrato = sintesiFiltrato2(statoFiltratoFft)
    df = pd.DataFrame()
    df['days'] = statoFiltrato.date
    df['date'] = statoFiltrato.date
    df['no2'] = statoFiltrato.no2
    df['o3'] = statoFiltrato.o3
    df['so2'] = statoFiltrato.so2
    df['co'] = statoFiltrato.co
    df['days'] = pd.to_datetime(df['days'], format = '%Y-%m-%d')
    df['date'] = pd.to_datetime(df['date'], format = '%Y-%m-%d')
    df = df.resample(rule='M', on='days').first()
    #print(df)
    return df
#---------------------------------------------------------------#
#           Definizioni moduli per Analisi Stati                #
#---------------------------------------------------------------#

def createStato2(df):
    """
    Crea una classe stato prendendo i dati dalla tabella. 
    Parametri: 
    df: pandas DataFrame, tabella da cui estrae i dati 
    """
    stato = cl.Stato2()
    dates = pd.to_datetime(df['Date Local'], format = '%d/%m/%Y')
    stato.aggiornaStato(dates, df['no2'].values,  df['o3'].values, df['so2'].values, df['co'].values)
    return stato
    
def createStato2b(df):
    """
    Crea una classe stato prendendo i dati dalla tabella, variante per la tabella con medie mensili. 
    Parametri: 
    df: pandas DataFrame, tabella da cui estrae i dati 
    """
    stato = cl.Stato2()
    stato.aggiornaStato(df['date'], df['no2'].values,  df['o3'].values, df['so2'].values, df['co'].values)
    return stato
       
def mask(freq, soglia):
    return np.absolute(freq) > soglia

def maskStato(statoFft, sogliaNo2, sogliaO3, sogliaSo2, sogliaCo):
    """
    Mette a zero i coefficienti di fourier degli inquinanti dello statoFft che sono superiori alle soglie passate.
    Parametri: 
    statoFft: di tipo classe stato2Fft, stato da filtrare 
    sogliaNo2, sogliaO3, sogliaSo2, sogliaCo: numeri reali, soglie frequenze corrispondenti ai quattro inquinanti
    """
    statoCopia = cl.Stato2Fft(statoFft)
    mascheraNo2 = mask(statoCopia.no2F, sogliaNo2)
    mascheraO3 = mask(statoCopia.o3F, sogliaO3)
    mascheraSo2 = mask(statoCopia.so2F, sogliaSo2)
    mascheraCo = mask(statoCopia.coF, sogliaCo)
    statoCopia.mascheraStato(mascheraNo2, mascheraO3, mascheraSo2, mascheraCo)
    return statoCopia

def sintesiFiltrato2(statoFiltratoFft):
    """
    Risintetizza i coefficienti di Fourier dello statoFft filtrato e restituisce uno stato
    statoFiltratoFft: statoFft filtrato da risintetizzare 
    """
    stato = cl.Stato2()
    stato.sintesi(statoFiltratoFft)
    return stato

def differenza(stato, statoFiltrato):
    """Restituisce uno stato differenza in cui per ogni inquinante è presente la differenza tra i dati originali e quelli filtrati"""
    diff = cl.Stato2()
    diff.date = stato.date
    diff.days = stato.days
    diff.no2 = stato.no2 - statoFiltrato.no2
    diff.o3 = stato.o3 - statoFiltrato.o3
    diff.so2 = stato.so2 - statoFiltrato.so2
    diff.co = stato.co - statoFiltrato.co
    return diff

def massimo(statoFft):
    """ 
    Restituisce i tre array: 
    - maxx: contiene gli indici del massimo valore dello spettro di potenza, per ognuno dei quattro inquinanti
    - fmax: contiente la frequenza in cui si registra il massimo, per ognuno dei quattro inquinanti
    - pmax: contiente il periodo in cui si registra il massimo, per ognuno dei quattro inquinanti
    di quattro elementi, uno per ogni inquinante, in cui sono presenti l'indice in cui 
    """
    maxx = ([np.argmax(statoFft.no2P[1:]), np.argmax(statoFft.o3P[1:]), np.argmax(statoFft.so2P[1:]), np.argmax(statoFft.coP[1:])])
    fmax = ([statoFft.no2F[1:][maxx[0]], statoFft.o3F[1:][maxx[1]], statoFft.so2F[1:][maxx[2]], statoFft.coF[1:][maxx[3]]])
    pmax = ([1/fmax[0], 1/fmax[1], 1/fmax[2], 1/fmax[3]])    
    return maxx, fmax, pmax

def printMax(fmax, pmax, name):
    """ Visualizza sullo schermo una tabella con frequenza e periodo del massimo della potenza, salva la tabella in un file csv. """
    df = pd.DataFrame(index = ['freqMax [1/d]', 'perMax [d]'])
    df['NO2'] = ([round(fmax[0], 5), round(pmax[0], 1)])
    df['O3'] = ([round(fmax[1], 5), round(pmax[1], 1)])
    df['SO2'] = ([round(fmax[2], 5), round(pmax[2], 1)])
    df['CO'] = ([round(fmax[3], 5), round(pmax[3], 1)])
    print(df)
    
    currentDirectory = os.getcwd()
    df.to_csv(currentDirectory + '/datiSalvati/analisiStati/' + name + '/max'+ name +'.csv')
    
def correlazione(stato):
    """Restituisce una tabella con i coefficienti di correlazione tra gli inquinanti di uno stato"""
    df = pd.DataFrame()
    df['no2'] = stato.no2
    df['o3'] = stato.o3
    df['so2'] = stato.so2
    df['co'] = stato.co
    return df.corr()

def visualizzaCorrelazione(stato, name):
    """Visualizza una tabella con le correlazioni tra gli inquinati dello stato e la salva come immagine.
    Parametri: 
    stato: di tipo classe Stato2, stato di cui si vuole vedere la correlazione
    name: di tipo stringa, nome dello stato """
    corr = correlazione(stato)
    fig , ax = plt.subplots( figsize =( 12 , 10 ) )
    plt.title('Correlazione inquinanti stato ' + name)
    cmap = sns.diverging_palette( 220 , 10 , as_cmap = True )
    fig = sns.heatmap(
        corr, 
        cmap = cmap,
        square=True, 
        cbar_kws={ 'shrink' : .9 }, 
        ax=ax, 
        annot = True, 
        annot_kws = { 'fontsize' : 12 }
    )
    currentDirectory = os.getcwd()
    plt.savefig(currentDirectory +'/datiSalvati/analisiStati/' + name + '/correlazione' + name + '.png')
    plt.show()

def figMap(dataframe, maxx, inq):
    """ 
    Fa una mappa animata che mostra l'andamento della concentrazione mensile negli stati seguendo una scala di colori. 
    df   : pandas DataFrame, tabella da cui prende i dati  
    maxx : numero reale, valore massimo dell'inquinante 
    inq  : stringa, nome dell'inquinante
    """
    fig = px.choropleth(dataframe,
                        locations='states', 
                        locationmode="USA-states", 
                        scope="usa",
                        color=inq,
                        color_continuous_scale="Viridis_r",
                        range_color = (0, 100),
                        animation_frame = 'date'
                        )
    fig.update_layout(coloraxis_colorbar=dict(
        title= inq + '% rispetto al massimo = ' + str(maxx) ,
        ticks="outside", 
        dtick=50))
    fig.show()


#---------------------------------------------------------------#
#           Definizioni moduli per analisi rumore               #
#---------------------------------------------------------------#

def rumore(f, N, beta):
    """
    Fit spettro di potenza, restituisce N/f**beta
    parametri:
    f:frequenze
    N: normalizzazione
    beta: esponente frequenza
    """
    return N/f**beta


def fit(stato, mask):
    pNo2, pcovNo2 = optimize.curve_fit(rumore, stato.no2F[mask[0]],stato.no2P[mask[0]], p0=[2, 2])
    pO3, pcovO3 = optimize.curve_fit(rumore, stato.o3F[mask[1]],stato.o3P[mask[1]], p0=[1, 1])
    pSo2, pcovSo2 = optimize.curve_fit(rumore, stato.so2F[mask[2]],stato.so2P[mask[2]], p0=[1, 1])
    pCo, pcovCo = optimize.curve_fit(rumore, stato.coF[mask[3]],stato.coP[mask[3]], p0=[1, 1])
    p = ([pNo2, pO3, pSo2, pCo])
    pcov = ([pcovNo2, pcovO3, pcovSo2, pcovCo])
    return p, pcov


def printParams(p, pcov, f):
    print('Filtro frequenza =' +str(f))
    print('NO2:    beta = ',  round(p[0][1],2) , '+-', round(np.sqrt(np.diag(pcov[0]))[1], 2))
    print('        N = ',  round(p[0][0]), '+-',  round(np.sqrt(np.diag(pcov[0]))[0]))
    print('O3:     beta = ',  round(p[1][1],2),  '+-' ,  round(np.sqrt(np.diag(pcov[1]))[1], 2))
    print('        N = ',  round(p[1][0]), '+-',  round(np.sqrt(np.diag(pcov[1]))[0]))
    print('SO2:    beta = ',  round(p[2][1],2) ,'+-',  round(np.sqrt(np.diag(pcov[2]))[1], 2))
    print('        N = ',  round(p[2][0]), '+-',  round(np.sqrt(np.diag(pcov[2]))[0]))
    print('CO:     beta = ',  round(p[3][1],2) , '+-',  round(np.sqrt(np.diag(pcov[3]))[1], 2))
    print('        N = ',  round(p[3][0]), '+-',  round(np.sqrt(np.diag(pcov[3]))[0]))
    

    
#---------------------------------------------------------------#
#          Definizioni moduli per Analisi Stazioni              #
#---------------------------------------------------------------#

def groupSn(df, sn):
    """Restituisce una tabella corrispondente alla stazione di monitoraggio sn"""
    gp = df.groupby(['Site Num'])
    return gp.get_group(sn)

def chiavi(df):
    """Restituisce in un array l'elenco delle stazioni di monitoraggio"""
    gp = df.groupby(['Site Num'])
    keys = np.empty(0, dtype=int)
    for i in gp.groups.keys():
        keys = np.append(keys, int(i))
    return keys
    
def createSite(df, sn):
    """A partire da una tabella crea una classe di tipo Site. """
    newDf = groupSn(df, sn)
    dates = pd.to_datetime(newDf['Date Local'], format = '%d/%m/%Y')
    s = cl.Site()
    s.aggiornaSite(dates, newDf['Site Num'], newDf['address'], newDf['city'], newDf['no2'].values, newDf['o3'].values, newDf['so2'].values, newDf['co'].values)
    return s

def createStato(df, sitesNum):
    """Crea una classe di tipo stato inserendo le classi site"""
    stato = cl.Stato(sitesNum)
    for i in tqdm(sitesNum, 'creating State: '):
        stato.addSite(createSite(df, i))
    return stato     

def createStatoFft(stato):
    """Calcola le trasformate di Fourier degli inquinanti di uno stato, restituisce lo stato con coefficienti, potenza e frequenze"""
    statoFft = cl.StatoFft()
    statoFft.addSites(stato)
    return statoFft

def sintesiSite(siteFft):
    """ Risintetizza una stazione di monitoraggio filtrata"""
    siteFiltrata = cl.Site()
    siteFiltrata.sintesi(siteFft)
    return siteFiltrata

def maskSite(site, sogliaNo2, sogliaO3, sogliaSo2, sogliaCo):
    """ Mette a zero i coeffienti di Fourier degli inquinanti di una stazione sopra una certa soglia di frequenza"""
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
    """Filtra una classe stato"""
    statoCopia = cl.StatoFft()
    statoCopia.addSites(stato)

    for i in statoCopia.sitesFft:
        i = maskSite(i, sogliaNo2, sogliaO3, sogliaSo2, sogliaCo)
    return statoCopia


def sintesiFiltrato(stato, statoFiltratoFft, siteNum):
    """Risintetizza stato filtrato"""
    sfiltrato = cl.Stato(siteNum)
    sfiltrato.sintesi(statoFiltratoFft)
    return sfiltrato

