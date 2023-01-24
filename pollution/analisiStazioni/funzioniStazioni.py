import pandas as pd
import numpy as np
import classiStazioni as clSz
import graficiStazioni as grSz
import sys, os
from tqdm import tqdm
from scipy import constants, fft


def groupSn(df, sn):
    #mi resituisce una tabella corrispondente alla stazione di monitoraggio sn
    groups = df.groupby(['siteNum'])
    return groups.get_group(sn)
    
def createSite(df, sn):
    newDf = groupSn(df, sn)
    dates = pd.to_datetime(newDf['Date Local'], format = '%d/%m/%Y')
    return clSz.Site(dates, newDf['stateCode'], newDf['countryCode'], newDf['siteNum'], newDf['address'], newDf['state'], newDf['country'], newDf['city'], newDf['no2'].values, newDf['no2Err'], newDf['o3'].values, newDf['o3Err'], newDf['so2'].values, newDf['so2Err'], newDf['co'].values, newDf['coErr'])

def createStato(df, sitesNum):
    stato = clSz.Stato(sitesNum)
    for i in tqdm(sitesNum, 'creating State: '):
        stato.addSite(createSite(df, i))
    return stato     

def createStatoFft(stato):
    statoFft = clSz.StatoFft()
    statoFft.addSites(stato)
    return statoFft

