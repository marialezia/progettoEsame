import numpy as np
import pandas as pd
import sys, os
import classiStati as clSt
import funzioniStati as fzSt
import matplotlib.pyplot as plt
import graficiStati as grSt

nyDf = pd.read_csv('~/progettoEsame/fileCSV/newMexico.csv')


#creo stato kansas (tutte le stazioni insieme) e faccio il plot delle concentrazioni dei vari inquinanti in funzione del tempo
mexico2 = fzSt.createStato2(nyDf)
grSt.plotInquinanti2(mexico2)

#calcolo le trasformate di fourier dei vari inquinanti e faccio il plot dello spettro di potenza (modulo quadro dei coefficienti) in funzione delle frequenze

mexicoFft2 = clSt.Stato2Fft(mexico2)
grSt.plotFft2(mexicoFft2)

#faccio dei filtri che eliminano i coefficienti con frequenze maggiori delle quattro che ho selezionato 
filtri = ([0.1,0.05,0.03,0.01])
mexicoFft2Filtrato1 = fzSt.maskStato(mexico2, filtri[0], filtri[0], filtri[0], filtri[0])
mexicoFft2Filtrato2 = fzSt.maskStato(mexico2,  filtri[1], filtri[1], filtri[1], filtri[1])
mexicoFft2Filtrato3 = fzSt.maskStato(mexico2,  filtri[2], filtri[2], filtri[2], filtri[2])
mexicoFft2Filtrato4 = fzSt.maskStato(mexico2,  filtri[3], filtri[3], filtri[3], filtri[3])

#risintetizzo il segnale filtrato
mexico2Filtrato1 = fzSt.sintesiFiltrato(mexicoFft2Filtrato1)
#grSt.plotInquinanti2(mexico2Filtrato1)
#grSt.originaleVsFiltrato(kansas2, mexico2Filtrato1, 'mexico, filtrato f< 0.1')

mexico2Filtrato2 = fzSt.sintesiFiltrato(mexicoFft2Filtrato2)
#grSt.plotInquinanti2(mexico2Filtrato2)
#grSt.originaleVsFiltrato(mexico2, mexico2Filtrato2, 'mexico, filtrato f< 0.05')

mexico2Filtrato3 = fzSt.sintesiFiltrato(mexicoFft2Filtrato3)
#grSt.plotInquinanti2(mexico2Filtrato3)
#grSt.originaleVsFiltrato(mexico2, mexico2Filtrato3, 'mexico, filtrato f< 0.03')

mexico2Filtrato4 = fzSt.sintesiFiltrato(mexicoFft2Filtrato4)
#grSt.plotInquinanti2(mexico2Filtrato4)
#grSt.originaleVsFiltrato(mexico2, mexico2Filtrato4, 'mexico, filtrato f< 0.01')


grSt.subplotfiltri(mexico2, mexico2Filtrato1, mexico2Filtrato2, mexico2Filtrato3, mexico2Filtrato4, filtri)
grSt.plotInquinanti2(mexico2Filtrato4)
