import pandas as pd
import numpy as np
import classi as cl
import sys, os
from tqdm import tqdm
from scipy import constants, fft


def sameDays(days):
    ''' mi restituisce un array in cui ho la sequenza di quante volte la data è ripetuta'''
    conta = 1
    indici = np.empty(0)
    for i in range(len(days)-1):
        if days[i] == days[i+1]:
        	conta = conta +1
        else:
            indici = np.append(indici, int(conta))
            conta = 1
    indici = np.append(indici, int(conta))    
    return indici

def groupSc(df, sc):
    #mi resistuisce una tabella corrispondente allo stato di codice sc
    groups = df.groupby(['State Code'])
    return groups.get_group(sc)


def groupSn(df, sn):
    #mi resituisce una tabella corrispondente alla stazione di monitoraggio sn
    groups = df.groupby(['siteNum'])
    return groups.get_group(sn)

def dropColumns(df):
    df = df.drop(columns=['NO2 1st Max Value', 'NO2 1st Max Hour', 'NO2 AQI', 'O3 1st Max Value', 'O3 1st Max Hour', 'O3 AQI', 'SO2 1st Max Value', 'SO2 1st Max Hour', 'SO2 AQI', 'CO 1st Max Value', 'CO 1st Max Hour', 'CO AQI', 'Unnamed: 29'])
    return df

def stateFromCsv(df, sc, name):
    newDf = groupSc(df, sc)
    newDf = dropColumns(newDf)
    newDf.to_csv('~/progettoEsame/fileCSV/'+name)

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
 
