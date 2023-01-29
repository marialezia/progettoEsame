import numpy as np
import pandas as pd
import sys, os
import classi as cl
import funzioni as fz
import matplotlib.pyplot as plt
import grafici as gr
from scipy import constants, fft


#---------------------------------------------------------------#
#              Lettura file di dati                             #
#---------------------------------------------------------------#


currentDirectory = os.getcwd()


flDf = pd.read_csv(currentDirectory+'/fileCSV/floridaDateSite.csv')
ilDf = pd.read_csv(currentDirectory+'/fileCSV/illinoisDateSite.csv')
nyDf = pd.read_csv(currentDirectory+'/fileCSV/newyorkDateSite.csv')
teDf = pd.read_csv(currentDirectory+'/fileCSV/texasDateSite.csv')
caDf = pd.read_csv(currentDirectory+'/fileCSV/californiaDateSite.csv')

#---------------------------------------------------------------#
#        Estrapolazione elenco Stazioni di Monitoraggio         #
#---------------------------------------------------------------#

flSn = fz.chiavi(flDf)
ilSn = fz.chiavi(ilDf)
nySn = fz.chiavi(nyDf)
teSn = fz.chiavi(teDf)
caSn = fz.chiavi(caDf)

#---------------------------------------------------------------#
#                       Creazione Stati                         #
#---------------------------------------------------------------#

florida = fz.createStato(flDf, flSn)
illinois = fz.createStato(ilDf, ilSn)
newyork = fz.createStato(nyDf, nySn)
texas = fz.createStato(teDf, teSn)
california = fz.createStato(caDf, caSn)


#---------------------------------------------------------------#
#          Calcolo traformate di Fourier stati                  #
#---------------------------------------------------------------#

floridaFft = fz.createStatoFft(florida)
illinoisFft = fz.createStatoFft(illinois)
newyorkFft = fz.createStatoFft(newyork)
texasFft = fz.createStatoFft(texas)
californiaFft = fz.createStatoFft(california)

#---------------------------------------------------------------#
#              Scelta stato da analizzare                       #
#---------------------------------------------------------------#

fz.corrStato(florida)
