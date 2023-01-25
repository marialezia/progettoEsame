import pandas as pd
import numpy as np
import classiStazioni as cl
import graficiStazioni as gr
import sys, os
from tqdm import tqdm
from scipy import constants, fft


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

def mask(freq, soglia):
    return np.absolute(freq) > soglia

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

def maskStato(stato, sogliaNo2, sogliaO3, sogliaSo2, sogliaCo):
    statoCopia = cl.StatoFft()
    statoCopia.addSites(stato)
    
    mascheraNo2 = ([mask(statoCopia.sitesFft[0].no2F, sogliaNo2)])
    mascheraO3 = ([mask(statoCopia.sitesFft[0].o3F, sogliaO3)])
    mascheraSo2 = ([mask(statoCopia.sitesFft[0].so2F, sogliaSo2)])
    mascheraCo = ([mask(statoCopia.sitesFft[0].coF, sogliaCo)])

    print(mascheraNo2)
    print(statoCopia.sitesFft[0].no2Fft)
    for i in np.arange(1,len(stato.siteNum)):
        mascheraNo2 = np.append(mascheraNo2, mask(statoCopia.sitesFft[i].no2F, sogliaNo2))
        mascheraO3 = np.append(mascheraO3, mask(statoCopia.sitesFft[i].o3F, sogliaO3))
        mascheraSo2 = np.append(mascheraSo2, mask(statoCopia.sitesFft[i].so2F, sogliaSo2))
        mascheraCo = np.append(mascheraCo, mask(statoCopia.sitesFft[i].coF, sogliaCo))
    
    statoCopia.mascheraStato(mascheraNo2, mascheraO3, mascheraSo2, mascheraCo)
    
    print(statoCopia.sitesFft[0].no2Fft)
    return statoCopia

def sintesiFiltrato(stato, statoFiltratoFft, siteNum):
    sfiltrato = cl.Stato(siteNum)
    sfiltrato.sintesi(statoFiltratoFft)
    return sfiltrato

