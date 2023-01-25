import numpy as np
import pandas as pd
import sys, os
import classi as cl
import funzioni as fz
import matplotlib.pyplot as plt
import grafici as gr

#---------------------------------------------------------------#
#              Definizione funzione generale                    #
#---------------------------------------------------------------#

def analisiStato(stato, statoFft, nome):
    #Faccio il grafico della concentrazione degli inquinanti in funzione del tempo e dello spettro di potenza in funzione delle frequenze

    gr.plotInquinanti2(stato, 'Analisi ' + nome + ': grafico concentrazione inquinanti in funzione del tempo')
    gr.plotFft2(statoFft, 'Analisi ' + nome + ': grafico spettro di potenza inquinanti in funzione delle frequenze')

    #faccio dei filtri che eliminano i coefficienti con frequenze maggiori delle quattro che ho selezionato 
    filtri = ([0.1,0.05,0.03,0.01])
    statoFftFiltrato1 = fz.maskStato(stato, filtri[0], filtri[0], filtri[0], filtri[0])
    statoFftFiltrato2 = fz.maskStato(stato, filtri[1], filtri[1], filtri[1], filtri[1])
    statoFftFiltrato3 = fz.maskStato(stato, filtri[2], filtri[2], filtri[2], filtri[2])
    statoFftFiltrato4 = fz.maskStato(stato, filtri[3], filtri[3], filtri[3], filtri[3])

    #risintetizzo il segnale filtrato
    statoFiltrato1 = fz.sintesiFiltrato(statoFftFiltrato1)
    statoFiltrato2 = fz.sintesiFiltrato(statoFftFiltrato2)
    statoFiltrato3 = fz.sintesiFiltrato(statoFftFiltrato3)
    statoFiltrato4 = fz.sintesiFiltrato(statoFftFiltrato4)

    #grafici confronto inquinanti originali e risintetizzati  
    #gr.plotInquinanti2(statoFiltrato1, 'Analisi ' + nome + ': dati risintetizzati con filtro frequenze f < ' +str(filtri[0]))
    #gr.plotInquinanti2(statoFiltrato2, 'Analisi ' + nome + ': dati risintetizzati con filtro frequenze f < ' +str(filtri[1]))
    #gr.plotInquinanti2(statoFiltrato3, 'Analisi ' + nome + ': dati risintetizzati con filtro frequenze f < ' +str(filtri[2]))
    #gr.plotInquinanti2(statoFiltrato4, 'Analisi ' + nome + ': dati risintetizzati con filtro frequenze f < ' +str(filtri[3]))

    '''subplot di quattro grafici della concentrazione in funzione del tempo, in ogni grafico è riportato il dato originale e quello filtratii quattro grafici corrispondono a un tipo di inquinante diverso'''
    gr.originaleVsFiltrato(stato, statoFiltrato1, 'Analisi ' + nome + ':confronto inquinanti dati originali e filtrati con frequenza f<0.1')
    #gr.originaleVsFiltrato(stato, statoFiltrato2, 'Analisi ' + nome + ': confronto inquinanti dati originali e filtrati con frequenza f<0.05')
    #gr.originaleVsFiltrato(stato, statoFiltrato3, 'Analisi ' + nome + ': confronto inquinanti dati originali e filtrati con frequenza f<0.03')
    #gr.originaleVsFiltrato(stato, statoFiltrato4, 'Analisi ' + nome + ': confronto inquinanti dati originali e filtrati con frequenza f<0.01')

    
    #gr.subplotfiltri(stato, statoFiltrato1, statoFiltrato2, statoFiltrato3, statoFiltrato4, filtri)
    #gr.plotInquinanti2(statoFiltrato4, '')
    return 'Analisi completata \n'


#---------------------------------------------------------------#
#              Lettura file di dati                             #
#---------------------------------------------------------------#

kaDf = pd.read_csv('~/progettoEsame/fileCSV/kansasDate.csv')
ilDf = pd.read_csv('~/progettoEsame/fileCSV/illinoisDate.csv')
nyDf = pd.read_csv('~/progettoEsame/fileCSV/newyorkDate.csv')
meDf = pd.read_csv('~/progettoEsame/fileCSV/mexicoDate.csv')
caDf = pd.read_csv('~/progettoEsame/fileCSV/californiaDate.csv')

#---------------------------------------------------------------#
#              Creazione classi stato                           #
#---------------------------------------------------------------#

Kansas = fz.createStato2(kaDf)
Illinois = fz.createStato2(ilDf)
Newyork = fz.createStato2(nyDf)
Mexico = fz.createStato2(meDf)
California = fz.createStato2(caDf)

#---------------------------------------------------------------#
#      Calcolo trasformate di Fourier per ogni stato            #
#---------------------------------------------------------------#

KansasFft = cl.Stato2Fft(Kansas)
IllinoisFft = cl.Stato2Fft(Illinois)
NewyorkFft = cl.Stato2Fft(Newyork)
MexicoFft = cl.Stato2Fft(Mexico)
CaliforniaFft = cl.Stato2Fft(California)

#---------------------------------------------------------------#
#              Scelta stato da analizzare                       #
#---------------------------------------------------------------#
scelta = '1'
while scelta != '0':
    scelta = input('Seleziona lo stato da analizzare inserendo il numero corrispondente tra i seguenti: \n 1-Kansas \n 2-Illinois \n 3-Newyork \n 4-Mexico \n 5-California \n oppure digita 0 per terminare esecuzione \n ')
    if scelta == '1':
        risposta = analisiStato(Kansas, KansasFft, 'Kansas')
        print(risposta)
    elif scelta == '2':
        risposta = analisiStato(Illinois, IllinoisFft, 'Illinois')
        print(risposta)
    elif scelta == '3':
        risposta = analisiStato(Newyork, NewyorkFft, 'New York')
        print(risposta)
    elif scelta == '4':
        risposta = analisiStato(Mexico, MexicoFft, 'Mexico')
        print(risposta)
    elif scelta == '5':
        risposta = analisiStato(California, CaliforniaFft, 'California')
        print(risposta)
    elif scelta == '0':
        print('esecuzione terminata')
    else:
        print('Non hai selezionato una scelta valida \n')

