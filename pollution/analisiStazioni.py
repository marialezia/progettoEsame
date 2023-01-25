import numpy as np
import pandas as pd
import sys, os
import classi as cl
import funzioni as fz
import matplotlib.pyplot as plt
import grafici as gr
from scipy import constants, fft

#---------------------------------------------------------------#
#              Definizione funzione generale                    #
#---------------------------------------------------------------#

def analisiStazioni(stato, statoFft, siteNum, name):
    #gr.subplotInquinanti(stato, 'Analisi ' + name + ': concentrazione inquinanti in funzione del tempo ')
    #gr.subplotInquinantiFft(statoFft, 'Analisi ' + name + ': spettro di potenza in funzione delle frequenze')

    #gr.subplotsFft(statoFft)
    #gr.subplotStazioni(stato, 'kansas')
    
    #faccio dei filtri che eliminano i coefficienti con frequenze maggiori delle quattro che ho selezionato 
    filtri = ([0.1,0.05,0.03,0.01])
    statoFftFiltrato1 = fz.maskStato2(stato, filtri[0], filtri[0], filtri[0], filtri[0])
    statoFftFiltrato2 = fz.maskStato2(stato, filtri[1], filtri[1], filtri[1], filtri[1])
    statoFftFiltrato3 = fz.maskStato2(stato, filtri[2], filtri[2], filtri[2], filtri[2])
    statoFftFiltrato4 = fz.maskStato2(stato, filtri[3], filtri[3], filtri[3], filtri[3])
    
    #risintetizzo il segnale filtrato
    statoFiltrato1 = fz.sintesiFiltrato(stato, statoFftFiltrato1, siteNum)
    statoFiltrato2 = fz.sintesiFiltrato(stato, statoFftFiltrato2, siteNum)
    statoFiltrato3 = fz.sintesiFiltrato(stato, statoFftFiltrato3, siteNum)
    statoFiltrato4 = fz.sintesiFiltrato(stato, statoFftFiltrato4, siteNum)

    #gr.subplotInquinanti(statoFiltrato1, 'Analisi ' + name + ': concentrazione inquinanti in funzione del tempo ')
    #gr.subplotInquinanti(statoFiltrato2, 'Analisi ' + name + ': concentrazione inquinanti in funzione del tempo ')
    #gr.subplotInquinanti(statoFiltrato3, 'Analisi ' + name + ': concentrazione inquinanti in funzione del tempo ')
    gr.subplotInquinanti(statoFiltrato4, 'Analisi ' + name + ': concentrazione inquinanti in funzione del tempo ')
    

#---------------------------------------------------------------#
#              Lettura file di dati                             #
#---------------------------------------------------------------#

kaDf = pd.read_csv('~/progettoEsame/fileCSV/kansasDateSite.csv')
ilDf = pd.read_csv('~/progettoEsame/fileCSV/illinoisDateSite.csv')
nyDf = pd.read_csv('~/progettoEsame/fileCSV/newyorkDateSite.csv')
meDf = pd.read_csv('~/progettoEsame/fileCSV/mexicoDateSite.csv')
caDf = pd.read_csv('~/progettoEsame/fileCSV/californiaDateSite.csv')

#---------------------------------------------------------------#
#        Estrapolazione elenco Stazioni di Monitoraggio         #
#---------------------------------------------------------------#

kaSn = fz.chiavi(kaDf)
ilSn = fz.chiavi(ilDf)
nySn = fz.chiavi(nyDf)
meSn = fz.chiavi(meDf)
caSn = fz.chiavi(caDf)

#---------------------------------------------------------------#
#                       Creazione Stati                         #
#---------------------------------------------------------------#

kansas = fz.createStato(kaDf, kaSn)
illinois = fz.createStato(ilDf, ilSn)
newyork = fz.createStato(nyDf, nySn)
mexico = fz.createStato(meDf, meSn)
california = fz.createStato(caDf, caSn)


#---------------------------------------------------------------#
#          Calcolo traformate di Fourier stati                  #
#---------------------------------------------------------------#

kansasFft = fz.createStatoFft(kansas)
illinoisFft = fz.createStatoFft(illinois)
newyorkFft = fz.createStatoFft(newyork)
mexicoFft = fz.createStatoFft(mexico)
californiaFft = fz.createStatoFft(california)

#---------------------------------------------------------------#
#              Scelta stato da analizzare                       #
#---------------------------------------------------------------#

scelta = '1'
while scelta != '0':
    scelta = input('Seleziona lo stato da analizzare inserendo il numero corrispondente tra i seguenti: \n 1-Kansas \n 2-Illinois \n 3-Newyork \n 4-Mexico \n 5-California \n oppure digita 0 per terminare esecuzione \n ')
    if scelta == '1':
        analisiStazioni(kansas, kansasFft, kaSn, 'Kansas')
    elif scelta == '2':
        analisiStazioni(illinois, illinoisFft, ilSn, 'Illinois')
    elif scelta == '3':
        analisiStazioni(newyork, newyorkFft, nySn, 'New York')
    elif scelta == '4':
        analisiStazioni(mexico, mexicoFft, meSn, 'Mexico')
    elif scelta == '5':
        analisiStazioni(california, californiaFft, caSn, 'California')
    elif scelta == '0':
        print('esecuzione terminata')
    else:
        print('Non hai selezionato una scelta valida \n')

#creo lo stato in cui sono presenti la sottocategoria siteNum che corrisponde alle stazioni di monitoraggio, ogni stazione di monitoraggio ha i suoi dati sugli inquinanti distinti. faccio grafico degli inquinanti in funzione del tempo per ogni stazione di riferimento sia in grafici distinti (sublots) che nello stesso (plot)
'''
kansas = fzSz.createStato(kaDf, sitesNum)
#grSz.subplots(kansas)
#grSz.plot(kansas)

#calcolo trasformata di fourier degli inuinanti per ogni stazione di monitoraggio e faccio grafico spettro di potenza in funzione del tempo 

kansasFft = fzSz.createStatoFft(kansas)
#print(kansasFft.sitesFft[0].no2F)
#print(kansasFft.sitesFft[0].no2Fft)
#print(kansasFft.sitesFft[0].no2P)

grSz.subplotsFft(kansasFft)
grSz.subplotStazioni(kansas, 'kansas')
'''
