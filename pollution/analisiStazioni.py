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
    '''
    Funzione che: 
    - genera i grafici: concentrazione inquinanti su tempo, spettro di potenza su frequenza, spettro di potenza su periodo visualizzando il punto in cui è presente il massimo dello spettro di potenza. I grafici sono sia in scala logaritmica che in scala normale.
    - visualizza nello schermo il periodo e la frequenza in cui si ha il massimo
    - filtra i coefficienti di fourier degli inquinanti mettendo a zero quelli corrispondenti a frequenze più alte di quattro valori
    - risintetizza i coefficienti e genera i grafici di confronto tra dati originali e risintetizzati per ognuno degli inquinanti e filtri
    - calcola la differenza tra segnale originale e filtrato e la grafica, insieme al segnale risintetizzato
    - calcola la correlazione tra gli inquinanti e visualizza nello schermo i valori
    '''

    #Grafico della concentrazione degli inquinanti in funzione del tempo e dello spettro di potenza in funzione delle frequenze, sia scala normale che scala logaritmica
    print('\n 1.ANALISI ANDAMENTO TEMPORALE \n')
    risposta = input('Per visualizzare grafici concentrazione degli inquinanti in funzione del tempo digita 1, altrimenti digita 0 \n')
    if risposta == '1':
        gr.subplotInquinanti(stato, 'Analisi ' + name + ': concentrazione inquinanti in funzione del tempo ', name)

    print('\n 2.ANALISI SPETTRO DI FOURIER \n Verranno visualizzati i seguenti grafici: \n - spettro di potenza in funzione delle frequenze \n - spettro di potenza in funzione dei periodi \n dove è stato escluso il termine corrispondente alla frequenza 0')   
    risposta = input('Per visualizzare i grafici in scala logaritmica digita 1, per visualizzarli in scala normale digita 2  altrimenti digita 0 \n')
    if risposta == '2':
        gr.subplotInquinantiFft(statoFft, 'Analisi ' + name + ': spettro di potenza in funzione delle frequenze', '', name)
        gr.subplotInquinantiFftPeriodo(statoFft, 'Analisi ' + name + ': spettro di potenza in funzione dei periodo', '', name)
    elif risposta == '1':
        gr.subplotInquinantiFft(statoFft, 'Analisi ' + name + ': spettro di potenza in funzione delle frequenze', 'log', name)
        gr.subplotInquinantiFftPeriodo(statoFft, 'Analisi ' + name + ': spettro di potenza in funzione dei periodo', 'log', name)



    #faccio stampare le correlazioni
    print('\n 3.CORRELAZIONE TRA I DATI \n')
    print('Si possono calcolare quali sono i coefficienti di correlazione tra: \n - gli inquinanti diversi nella stessa stazione \n - lo stesso inquinante in stazioni diverse dello stesso stato. \n Verrà visualizzata una tabella con i coefficienti. \n')
    risposta = input('Per visualizzare le tabelle digita 1 altrimenti digita 0 \n')
    #if risposta == '1':
        #fz.visualizzaCorrelazione(stato, nome)
        #fz.visualizzaCorrelazione2(stato, nome)

    no2Corr, o3Corr, so2Corr, coCorr = fz.statoCorr(stato)
    print(no2Corr, o3Corr, so2Corr, coCorr)
    
    print('\n 4.FILTRO IN FREQUENZA \n')
    print('Per osservare il comportamento su lungo periodo si può applicare un filtro in frequenza ai dati, mettendo a zero i coefficienti di Fourier corrispondenti a frequenze superiori ad una certa soglia. Di seguito sono state scelti quattro valori di soglia delle frequenze: \n f1 = 0.1 \n f2 = 0.05 \n f3 = 0.03 \n f4 = 0.01 \n dove l unità di misura è 1/giorno. In seguito sarà possibile inserire una frequenza di soglia a scelta. \n Verranno visualizzati i grafici dei dati risintetizzati con i diversi filtri in funzione del tempo. \n ')
    
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

    #grafici dati risintetizzati 
    risposta = input('Per visualizzare i grafici dei segnali risintetizzati con le diverse frequenza digita: \n a) per f1 \n b) per f2 \n c) per f3 \n d)per f4 \n altrimenti digita 0 \n')
    if risposta == 'a':
        gr.subplotInquinanti(statoFiltrato1, 'Analisi ' + name + ': concentrazione inquinanti in funzione del tempo ', name)
    elif risposta == 'b':
        gr.subplotInquinanti(statoFiltrato2, 'Analisi ' + name + ': concentrazione inquinanti in funzione del tempo ', name)
    elif risposta == 'c':
        gr.subplotInquinanti(statoFiltrato3, 'Analisi ' + name + ': concentrazione inquinanti in funzione del tempo ', name)
    elif risposta == 'd':
        gr.subplotInquinanti(statoFiltrato4, 'Analisi ' + name + ': concentrazione inquinanti in funzione del tempo ', name)

        
    '''subplot di quattro grafici della concentrazione in funzione del tempo, in ogni grafico è riportato il dato originale e quello filtratii quattro grafici corrispondono a un tipo di inquinante diverso'''

    print('Verranno visualizzati i grafici dei dati originali e di quelli filtrati. \n')

#---------------------------------------------------------------#
#              Lettura file di dati                             #
#---------------------------------------------------------------#

flDf = pd.read_csv('~/progettoEsame/fileCSV/floridaDateSite.csv')
ilDf = pd.read_csv('~/progettoEsame/fileCSV/illinoisDateSite.csv')
nyDf = pd.read_csv('~/progettoEsame/fileCSV/newyorkDateSite.csv')
teDf = pd.read_csv('~/progettoEsame/fileCSV/texasDateSite.csv')
caDf = pd.read_csv('~/progettoEsame/fileCSV/californiaDateSite.csv')

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

scelta = '1'
while scelta != '0':
    scelta = input('Seleziona lo stato da analizzare inserendo il numero corrispondente tra i seguenti: \n 1-Florida \n 2-Illinois \n 3-Newyork \n 4-Texas \n 5-California \n oppure digita 0 per terminare esecuzione \n ')
    if scelta == '1':
        analisiStazioni(florida, floridaFft, flSn, 'Florida')
    elif scelta == '2':
        analisiStazioni(illinois, illinoisFft, ilSn, 'Illinois')
    elif scelta == '3':
        analisiStazioni(newyork, newyorkFft, nySn, 'New York')
    elif scelta == '4':
        analisiStazioni(texas, texasFft, teSn, 'Texas')
    elif scelta == '5':
        analisiStazioni(california, californiaFft, caSn, 'California')
    elif scelta == '0':
        print('esecuzione terminata')
    else:
        print('Non hai selezionato una scelta valida \n')

#creo lo stato in cui sono presenti la sottocategoria siteNum che corrisponde alle stazioni di monitoraggio, ogni stazione di monitoraggio ha i suoi dati sugli inquinanti distinti. faccio grafico degli inquinanti in funzione del tempo per ogni stazione di riferimento sia in grafici distinti (sublots) che nello stesso (plot)
'''
florida = fzSz.createStato(flDf, sitesNum)
#grSz.subplots(florida)
#grSz.plot(florida)

#calcolo trasformata di fourier degli inuinanti per ogni stazione di monitoraggio e faccio grafico spettro di potenza in funzione del tempo 

floridaFft = fzSz.createStatoFft(florida)
#print(floridaFft.sitesFft[0].no2F)
#print(floridaFft.sitesFft[0].no2Fft)
#print(floridaFft.sitesFft[0].no2P)

grSz.subplotsFft(floridaFft)
grSz.subplotStazioni(florida, 'florida')
'''
