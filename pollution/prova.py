import numpy as np
import pandas as pd
import classi as cl
import funzioni as fz
from tqdm import tqdm

#leggo dati da csv
il = pd.read_csv('illinois.csv')
'''
ks = pd.read_csv('kansas.csv')
mx = pd.read_csv('mexico.csv')
ny = pd.read_csv('newyork.csv')
cl = pd.read_csv('california.csv')
'''
ilNewDf = fz.meanSameDays(il, 'Illinois: ')
ilNewDf.to_csv('illinoisNewDf.csv')
'''
ksNewDf = fz.meanSameDays(ks, 'Kansas: ')
ksNewDf.to_csv('kansasNewDf.csv')
mxNewDf = fz.meanSameDays(mx, 'Mexico: ')
mxNewDf.to_csv('mexicoNewDf.csv')
nyNewDf = fz.meanSameDays(ny, 'New York: ')
nyNewDf.to_csv('newyorkNewDf.csv')
clNewDf = fz.meanSameDays(cl, 'California: ')
clNewDf.to_csv('californiaNewDf.csv')
'''
