import numpy as np
import pandas as pd
import sys, os
import classiStati as clSt
import funzioniStati as fzSt
import matplotlib.pyplot as plt
import graficiStati as grSt

nyDf = pd.read_csv('~/progettoEsame/fileCSV/newNewyork.csv')


#creo stato kansas (tutte le stazioni insieme) e faccio il plot delle concentrazioni dei vari inquinanti in funzione del tempo
newyork2 = fzSt.createStato2(nyDf)
grSt.plotInquinanti2(newyork2)

#calcolo le trasformate di fourier dei vari inquinanti e faccio il plot dello spettro di potenza (modulo quadro dei coefficienti) in funzione delle frequenze

newyorkFft2 = clSt.Stato2Fft(newyork2)
grSt.plotFft2(newyorkFft2)

#faccio dei filtri che eliminano i coefficienti con frequenze maggiori delle quattro che ho selezionato 
filtri = ([0.1,0.05,0.03,0.01])
newyorkFft2Filtrato1 = fzSt.maskStato(newyork2, filtri[0], filtri[0], filtri[0], filtri[0])
newyorkFft2Filtrato2 = fzSt.maskStato(newyork2,  filtri[1], filtri[1], filtri[1], filtri[1])
newyorkFft2Filtrato3 = fzSt.maskStato(newyork2,  filtri[2], filtri[2], filtri[2], filtri[2])
newyorkFft2Filtrato4 = fzSt.maskStato(newyork2,  filtri[3], filtri[3], filtri[3], filtri[3])

#risintetizzo il segnale filtrato
newyork2Filtrato1 = fzSt.sintesiFiltrato(newyorkFft2Filtrato1)
#grSt.plotInquinanti2(newyork2Filtrato1)
#grSt.originaleVsFiltrato(kansas2, newyork2Filtrato1, 'Newyork, filtrato f< 0.1')

newyork2Filtrato2 = fzSt.sintesiFiltrato(newyorkFft2Filtrato2)
#grSt.plotInquinanti2(newyork2Filtrato2)
#grSt.originaleVsFiltrato(newyork2, newyork2Filtrato2, 'Newyork, filtrato f< 0.05')

newyork2Filtrato3 = fzSt.sintesiFiltrato(newyorkFft2Filtrato3)
#grSt.plotInquinanti2(newyork2Filtrato3)
#grSt.originaleVsFiltrato(newyork2, newyork2Filtrato3, 'Newyork, filtrato f< 0.03')

newyork2Filtrato4 = fzSt.sintesiFiltrato(newyorkFft2Filtrato4)
#grSt.plotInquinanti2(newyork2Filtrato4)
#grSt.originaleVsFiltrato(newyork2, newyork2Filtrato4, 'Newyork, filtrato f< 0.01')


#grSt.subplotfiltri(newyork2, newyork2Filtrato1, newyork2Filtrato2, newyork2Filtrato3, newyork2Filtrato4, filtri)
grSt.plotInquinanti2(newyork2Filtrato4)
