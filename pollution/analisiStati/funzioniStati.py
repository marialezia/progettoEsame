import pandas as pd
import numpy as np
import classiStati as clSt
import sys, os
from tqdm import tqdm
from scipy import constants, fft


def createStato2(df):
    stato = clSt.Stato2()
    dates = pd.to_datetime(df['Date Local'], format = '%d/%m/%Y')
    stato.aggiornaStato(dates, df['siteNum'], df['address'], df['no2'].values,  df['o3'].values, df['so2'].values, df['co'].values)
    return stato
       
def mask(freq, soglia):
    return np.absolute(freq) > soglia

def maskStato(stato, sogliaNo2, sogliaO3, sogliaSo2, sogliaCo):
    #soglie = ([sogliaNo2, sogliaO3, sogliaSo2, sogliaCo])
    statoCopia = clSt.Stato2Fft(stato)
    mascheraNo2 = mask(statoCopia.no2F, sogliaNo2)
    mascheraO3 = mask(statoCopia.o3F, sogliaO3)
    mascheraSo2 = mask(statoCopia.so2F, sogliaSo2)
    mascheraCo = mask(statoCopia.coF, sogliaCo)
    statoCopia.mascheraStato(mascheraNo2, mascheraO3, mascheraSo2, mascheraCo)
    return statoCopia

def sintesiFiltrato(statoFiltratoFft):
    stato = clSt.Stato2()
    stato.sintesi(statoFiltratoFft)
    return stato


    
