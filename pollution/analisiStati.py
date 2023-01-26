import numpy as np
import pandas as pd
import sys, os
import classi as cl
import funzioni as fz
import matplotlib.pyplot as plt
import grafici as gr
import plotly.express as px

#---------------------------------------------------------------#
#              Definizione funzioni generali                    #
#---------------------------------------------------------------#

def analisiStato(stato, statoFft, nome):
    '''
    Funzione che: 
    - genera i grafici: concentrazione inquinanti su tempo, spettro di potenza su frequenza, spettro di potenza su periodo visualizzando il punto in cui è presente il massimo dello spettro di potenza. I grafici sono sia in scala logaritmica che in scala normale.
    - visualizza nello schermo il periodo e la frequenza in cui si ha il massimo
    - filtra i coefficienti di fourier degli inquinanti mettendo a zero quelli corrispondenti a frequenze più alte di quattro valori
    - risintetizza i coefficienti e genera i grafici di confronto tra dati originali e risintetizzati per ognuno degli inquinanti e filtri
    - calcola la differenza tra segnale originale e filtrato e la grafica, insieme al segnale risintetizzato
    - calcola la correlazione tra gli inquinanti e visualizza nello schermo i valori
    '''
    #Faccio il grafico della concentrazione degli inquinanti in funzione del tempo e dello spettro di potenza in funzione delle frequenze, sia scala normale che scala logaritmica
    
    gr.subplotInquinantiScale(stato, 'Analisi ' + nome + ': grafico concentrazione inquinanti in funzione del tempo')
    gr.subplotFftScale(statoFft, 'Analisi ' + nome + ': grafico spettro di potenza inquinanti in funzione delle frequenze', True)
    #gr.subplotFftScale(statoFft, 'Analisi ' + nome + ': grafico spettro di potenza inquinanti in funzione delle frequenze (termine zero escluso)', False)
    
    #trovo il massimo dello spettro di potenza degli inquinanti
    maxx, fmax, pmax = fz.massimo(statoFft)
    #gr.subplotFftScalePeriodo(statoFft, 'Analisi ' + nome + ': grafico spettro di potenza inquinanti in funzione dei periodi', False, maxx)
    #gr.subplotFftScalePeriodo(statoFft, 'Analisi ' + nome + ': grafico spettro di potenza inquinanti in funzione dei periodi', True, maxx)

    #trovo il massimo dello spettro di potenza degli inquinanti
    maxx, fmax, pmax = fz.massimo(statoFft)
    print(fmax, pmax)
    fz.printMax(fmax, pmax, nome)
    
    
    #faccio dei filtri che eliminano i coefficienti con frequenze maggiori delle quattro che ho selezionato 
    filtri = ([0.1,0.05,0.03,0.01])
    statoFftFiltrato1 = fz.maskStato(stato, filtri[0], filtri[0], filtri[0], filtri[0])
    statoFftFiltrato2 = fz.maskStato(stato, filtri[1], filtri[1], filtri[1], filtri[1])
    statoFftFiltrato3 = fz.maskStato(stato, filtri[2], filtri[2], filtri[2], filtri[2])
    statoFftFiltrato4 = fz.maskStato(stato, filtri[3], filtri[3], filtri[3], filtri[3])

    #risintetizzo il segnale filtrato
    statoFiltrato1 = fz.sintesiFiltrato2(statoFftFiltrato1)
    statoFiltrato2 = fz.sintesiFiltrato2(statoFftFiltrato2)
    statoFiltrato3 = fz.sintesiFiltrato2(statoFftFiltrato3)
    statoFiltrato4 = fz.sintesiFiltrato2(statoFftFiltrato4)

    #grafici confronto inquinanti originali e risintetizzati  
    #gr.plotInquinanti2(statoFiltrato1, 'Analisi ' + nome + ': dati risintetizzati con filtro frequenze f < ' +str(filtri[0]), '')
    #gr.plotInquinanti2(statoFiltrato2, 'Analisi ' + nome + ': dati risintetizzati con filtro frequenze f < ' +str(filtri[1]), '')
    #gr.plotInquinanti2(statoFiltrato3, 'Analisi ' + nome + ': dati risintetizzati con filtro frequenze f < ' +str(filtri[2]), '')
    #gr.plotInquinanti2(statoFiltrato4, 'Analisi ' + nome + ': dati risintetizzati con filtro frequenze f < ' +str(filtri[3]), '')

    '''subplot di quattro grafici della concentrazione in funzione del tempo, in ogni grafico è riportato il dato originale e quello filtratii quattro grafici corrispondono a un tipo di inquinante diverso'''
    #gr.originaleVsFiltrato(stato, statoFiltrato1, 'Analisi ' + nome + ':confronto inquinanti dati originali e filtrati con frequenza f<0.1')
    #gr.originaleVsFiltrato(stato, statoFiltrato2, 'Analisi ' + nome + ': confronto inquinanti dati originali e filtrati con frequenza f<0.05')
    #gr.originaleVsFiltrato(stato, statoFiltrato3, 'Analisi ' + nome + ': confronto inquinanti dati originali e filtrati con frequenza f<0.03')
    #gr.originaleVsFiltrato(stato, statoFiltrato4, 'Analisi ' + nome + ': confronto inquinanti dati originali e filtrati con frequenza f<0.01', '')

    
    #gr.subplotfiltri(stato, statoFiltrato1, statoFiltrato2, statoFiltrato3, statoFiltrato4, filtri)
    #gr.plotInquinanti2(statoFiltrato4, '')

    #calcolo differenza originale e filtrato
    diff1 = fz.differenza(stato, statoFiltrato1)
    diff2 = fz.differenza(stato, statoFiltrato2)
    diff3 = fz.differenza(stato, statoFiltrato3)
    diff4 = fz.differenza(stato, statoFiltrato4)
    '''
    gr.plotInquinanti2(diff1, 'Analisi ' + nome + ': differenza originale e filtrato con f < ' + str(filtri[0]), '')
    gr.plotInquinanti2(diff2, 'Analisi ' + nome + ': differenza originale e filtrato con f < ' + str(filtri[1]), '')
    gr.plotInquinanti2(diff3, 'Analisi ' + nome + ': differenza originale e filtrato con f < ' + str(filtri[2]), '')
    gr.plotInquinanti2(diff4, 'Analisi ' + nome + ': differenza originale e filtrato con f < ' + str(filtri[3]), '')

    
    '''
    #faccio stampare le correlazioni
    
    corr = fz.correlazione(stato)
    print(corr)
    
    return 'Analisi completata \n'

def tuttiInsieme(ka, il, ny, te, ca, kaF, ilF, nyF, teF, caF):
    filtro = 0.001
    #filtro gli stati
    kaFf = fz.maskStato(ka, filtro, filtro, filtro, filtro)
    ilFf = fz.maskStato(il, filtro, filtro, filtro, filtro)
    nyFf = fz.maskStato(ny, filtro, filtro, filtro, filtro)
    teFf = fz.maskStato(te, filtro, filtro, filtro, filtro)
    caFf = fz.maskStato(ca, filtro, filtro, filtro, filtro)
    #risintetizzo
    kaFil = fz.sintesiFiltrato2(kaFf)
    ilFil = fz.sintesiFiltrato2(ilFf)
    nyFil = fz.sintesiFiltrato2(nyFf)
    teFil = fz.sintesiFiltrato2(teFf)
    caFil = fz.sintesiFiltrato2(caFf)
    #gr.graficoTuttiStati(ka, 'Kansas', il, 'Illinois', ny, 'New York', te, 'Texas', ca, 'California', 'confronto inquinanti in tutti gli stati')
    #gr.graficoTuttiStati(kaFil, 'Kansas', ilFil, 'Illinois', nyFil, 'New York', teFil, 'Texas', caFil, 'California', 'confronto inquinanti in tutti gli stati filtrati')

    #correlazioni
    #corrNo2, corrO3, corrSo2, corrCo = fz.correlazioneStati(ka, il, ny, te, ca, 'kansas', 'illinois', 'newyork', 'texas', 'california')
    #print(corrNo2, corrO3, corrSo2, corrCo)

def mappa(ka, il, ny, te, ca):
    #funzione che fa visualizzare in una mappa l'andamento delle medie mensili nel periodo di campionamento in base a una scala di colori
    kansas = np.full(len(ka.no2), 'KS')
    illinois = np.full(len(il.no2), 'IL')
    newyork = np.full(len(ny.no2), 'NY')
    texas = np.full(len(te.no2), 'TX')
    california = np.full(len(ca.no2), 'CA')
    
    dates = np.concatenate((ka.date, il.date, ny.date, te.date, ca.date))
    states = np.concatenate((kansas, illinois, newyork, texas, california))
    no2 = np.concatenate((ka.no2, il.no2, ny.no2, te.no2, ca.no2))
    o3 = np.concatenate((ka.o3, il.o3, ny.o3, te.o3, ca.o3))
    so2 = np.concatenate((ka.so2, il.so2, ny.no2, te.so2, ca.so2))
    co = np.concatenate((ka.co, il.co, ny.co, te.co, ca.co))

    dataframe = pd.DataFrame()
    dataframe['date'] = dates
    dataframe['states'] = states
    dataframe['no2'] = no2
    dataframe['o3'] = o3
    dataframe['so2'] = so2
    dataframe['co'] = co
    dataframe['date'] = pd.to_datetime(dataframe['date']).dt.date.astype(str)
    dataframe = dataframe.sort_values('date')


    figNo2 = px.choropleth(dataframe,
                    locations='states', 
                    locationmode="USA-states", 
                    scope="usa",
                    color='no2',
                    color_continuous_scale="Viridis_r",
                    animation_frame = 'date'
                    )
    figNo2.update_layout(coloraxis_colorbar=dict(
        title="Valore medio NO2",
        ticks="outside", 
        dtick=50))
    figNo2.show()

    figO3 = px.choropleth(dataframe,
                    locations='states', 
                    locationmode="USA-states", 
                    scope="usa",
                    color='o3',
                    color_continuous_scale="Viridis_r",
                    animation_frame = 'date'
                    )
    figO3.update_layout(coloraxis_colorbar=dict(
        title="Valore medio O3",
        ticks="outside", 
        dtick=50))
    figO3.show()

    figSo2 = px.choropleth(dataframe,
                    locations='states', 
                    locationmode="USA-states", 
                    scope="usa",
                    color='so2',
                    color_continuous_scale="Viridis_r",
                    animation_frame = 'date'
                    )
    figNo2.update_layout(coloraxis_colorbar=dict(
        title="Valore medio SO2",
        ticks="outside", 
        dtick=50))
    figSo2.show()

    figCo = px.choropleth(dataframe,
                    locations='states', 
                    locationmode="USA-states", 
                    scope="usa",
                    color='co',
                    color_continuous_scale="Viridis_r",
                    animation_frame = 'date'
                    )
    figNo2.update_layout(coloraxis_colorbar=dict(
        title="Valore medio CO",
        ticks="outside", 
        dtick=50))
    figCo.show()
    
#---------------------------------------------------------------#
#      Lettura file di dati: medie giornaliere                  #
#---------------------------------------------------------------#

kaDf = pd.read_csv('~/progettoEsame/fileCSV/kansasDate.csv')
ilDf = pd.read_csv('~/progettoEsame/fileCSV/illinoisDate.csv')
nyDf = pd.read_csv('~/progettoEsame/fileCSV/newyorkDate.csv')
teDf = pd.read_csv('~/progettoEsame/fileCSV/texasDate.csv')
caDf = pd.read_csv('~/progettoEsame/fileCSV/californiaDate.csv')

#---------------------------------------------------------------#
#         Lettura file di dati : medie mensili                  #
#---------------------------------------------------------------#

kaDfM = pd.read_csv('~/progettoEsame/fileCSV/kansasMonth.csv')
ilDfM = pd.read_csv('~/progettoEsame/fileCSV/illinoisMonth.csv')
nyDfM = pd.read_csv('~/progettoEsame/fileCSV/newyorkMonth.csv')
teDfM = pd.read_csv('~/progettoEsame/fileCSV/texasMonth.csv')
caDfM = pd.read_csv('~/progettoEsame/fileCSV/californiaMonth.csv')
        
#---------------------------------------------------------------#
#              Creazione classi stato                           #
#---------------------------------------------------------------#

Kansas = fz.createStato2(kaDf)
Illinois = fz.createStato2(ilDf)
Newyork = fz.createStato2(nyDf)
Texas = fz.createStato2(teDf)
California = fz.createStato2(caDf)

KansasM = fz.createStato2b(kaDfM)
IllinoisM = fz.createStato2b(ilDfM)
NewyorkM = fz.createStato2b(nyDfM)
TexasM = fz.createStato2b(teDfM)
CaliforniaM = fz.createStato2b(caDfM)

#---------------------------------------------------------------#
#      Calcolo trasformate di Fourier per ogni stato            #
#---------------------------------------------------------------#

KansasFft = cl.Stato2Fft(Kansas)
IllinoisFft = cl.Stato2Fft(Illinois)
NewyorkFft = cl.Stato2Fft(Newyork)
TexasFft = cl.Stato2Fft(Texas)
CaliforniaFft = cl.Stato2Fft(California)


#---------------------------------------------------------------#
#              Scelta stato da analizzare                       #
#---------------------------------------------------------------#
scelta = '1'
while scelta != '0':
    scelta = input('Seleziona lo stato da analizzare inserendo il numero corrispondente tra i seguenti: \n 1-Kansas \n 2-Illinois \n 3-Newyork \n 4-Texas \n 5-California \n 6-Confronto tutti gli stati \n 7-visualizza mappa \n oppure digita 0 per terminare esecuzione \n ')
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
        risposta = analisiStato(Texas, TexasFft, 'Texas')
        print(risposta)
    elif scelta == '5':
        risposta = analisiStato(California, CaliforniaFft, 'California')
        print(risposta)
    elif scelta == '6':
        tuttiInsieme(Kansas, Illinois,  Newyork, Texas, California, KansasFft, IllinoisFft,NewyorkFft, TexasFft, CaliforniaFft)
    elif scelta == '7':
        mappa(KansasM, IllinoisM,  NewyorkM, TexasM, CaliforniaM)
    elif scelta == '0':
        print('esecuzione terminata')
    else:
        print('Non hai selezionato una scelta valida \n')

