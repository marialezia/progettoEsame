import numpy as np
import pandas as pd
import sys, os
import classiStati as clSt
import funzioniStati as fzSt
import matplotlib.pyplot as plt
import graficiStati as grSt

kaDf = pd.read_csv('~/progettoEsame/fileCSV/newKansas.csv')
'''
ilDf = pd.read_csv('~/progettoEsame/fileCSV/newIllinois.csv')
nyDf = pd.read_csv('~/progettoEsame/fileCSV/newNewyork.csv')
meDf = pd.read_csv('~/progettoEsame/fileCSV/newMexico.csv')
clDf = pd.read_csv('~/progettoEsame/fileCSV/newCalifornia.csv')
'''

#creo stato kansas (tutte le stazioni insieme) e faccio il plot delle concentrazioni dei vari inquinanti in funzione del tempo
kansas2 = fzSt.createStato2(kaDf)
#grSt.plotInquinanti2(kansas2)

#calcolo le trasformate di fourier dei vari inquinanti e faccio il plot dello spettro di potenza (modulo quadro dei coefficienti) in funzione delle frequenze

kansasFft2 = clSt.Stato2Fft(kansas2)
grSt.plotFft2(kansasFft2)

#faccio dei filtri che eliminano i coefficienti con frequenze maggiori delle quattro che ho selezionato 
filtri = ([0.1,0.05,0.03,0.01])
kansasFft2Filtrato1 = fzSt.maskStato(kansas2, filtri[0], filtri[0], filtri[0], filtri[0])
kansasFft2Filtrato2 = fzSt.maskStato(kansas2,  filtri[1], filtri[1], filtri[1], filtri[1])
kansasFft2Filtrato3 = fzSt.maskStato(kansas2,  filtri[2], filtri[2], filtri[2], filtri[2])
kansasFft2Filtrato4 = fzSt.maskStato(kansas2,  filtri[3], filtri[3], filtri[3], filtri[3])

#risintetizzo il segnale filtrato
kansas2Filtrato1 = fzSt.sintesiFiltrato(kansasFft2Filtrato1)
#grSt.plotInquinanti2(kansas2Filtrato1)
#grSt.originaleVsFiltrato(kansas2, kansas2Filtrato1, 'Kansas, filtrato f< 0.1')

kansas2Filtrato2 = fzSt.sintesiFiltrato(kansasFft2Filtrato2)
#grSt.plotInquinanti2(kansas2Filtrato2)
#grSt.originaleVsFiltrato(kansas2, kansas2Filtrato2, 'Kansas, filtrato f< 0.05')

kansas2Filtrato3 = fzSt.sintesiFiltrato(kansasFft2Filtrato3)
#grSt.plotInquinanti2(kansas2Filtrato3)
#grSt.originaleVsFiltrato(kansas2, kansas2Filtrato3, 'Kansas, filtrato f< 0.03')

kansas2Filtrato4 = fzSt.sintesiFiltrato(kansasFft2Filtrato4)
#grSt.plotInquinanti2(kansas2Filtrato4)
#grSt.originaleVsFiltrato(kansas2, kansas2Filtrato4, 'Kansas, filtrato f< 0.01')


grSt.subplotfiltri(kansas2, kansas2Filtrato1, kansas2Filtrato2, kansas2Filtrato3, kansas2Filtrato4, filtri)
grSt.plotInquinanti2(kansas2Filtrato4)
