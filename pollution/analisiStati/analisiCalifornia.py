import numpy as np
import pandas as pd
import sys, os
import classiStati as clSt
import funzioniStati as fzSt
import matplotlib.pyplot as plt
import graficiStati as grSt

nyDf = pd.read_csv('~/progettoEsame/fileCSV/newCalifornia.csv')


#creo stato kansas (tutte le stazioni insieme) e faccio il plot delle concentrazioni dei vari inquinanti in funzione del tempo
california2 = fzSt.createStato2(nyDf)
grSt.plotInquinanti2(california2)

#calcolo le trasformate di fourier dei vari inquinanti e faccio il plot dello spettro di potenza (modulo quadro dei coefficienti) in funzione delle frequenze

californiaFft2 = clSt.Stato2Fft(california2)
grSt.plotFft2(californiaFft2)

#faccio dei filtri che eliminano i coefficienti con frequenze maggiori delle quattro che ho selezionato 
filtri = ([0.1,0.05,0.03,0.01])
californiaFft2Filtrato1 = fzSt.maskStato(california2, filtri[0], filtri[0], filtri[0], filtri[0])
californiaFft2Filtrato2 = fzSt.maskStato(california2,  filtri[1], filtri[1], filtri[1], filtri[1])
californiaFft2Filtrato3 = fzSt.maskStato(california2,  filtri[2], filtri[2], filtri[2], filtri[2])
californiaFft2Filtrato4 = fzSt.maskStato(california2,  filtri[3], filtri[3], filtri[3], filtri[3])

#risintetizzo il segnale filtrato
california2Filtrato1 = fzSt.sintesiFiltrato(californiaFft2Filtrato1)
#grSt.plotInquinanti2(california2Filtrato1)
#grSt.originaleVsFiltrato(kansas2, california2Filtrato1, 'california, filtrato f< 0.1')

california2Filtrato2 = fzSt.sintesiFiltrato(californiaFft2Filtrato2)
#grSt.plotInquinanti2(california2Filtrato2)
#grSt.originaleVsFiltrato(california2, california2Filtrato2, 'california, filtrato f< 0.05')

california2Filtrato3 = fzSt.sintesiFiltrato(californiaFft2Filtrato3)
#grSt.plotInquinanti2(california2Filtrato3)
#grSt.originaleVsFiltrato(california2, california2Filtrato3, 'california, filtrato f< 0.03')

california2Filtrato4 = fzSt.sintesiFiltrato(californiaFft2Filtrato4)
#grSt.plotInquinanti2(california2Filtrato4)
#grSt.originaleVsFiltrato(california2, california2Filtrato4, 'california, filtrato f< 0.01')


grSt.subplotfiltri(california2, california2Filtrato1, california2Filtrato2, california2Filtrato3, california2Filtrato4, filtri)
grSt.plotInquinanti2(california2Filtrato4)
