import numpy as np
import pandas as pd
import sys, os
import classi as cl
import funzioni as fz
import matplotlib.pyplot as plt
import grafici as gr
import plotly.express as px
import seaborn as sns

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

    #Grafico della concentrazione degli inquinanti in funzione del tempo e dello spettro di potenza in funzione delle frequenze, sia scala normale che scala logaritmica
    print('\n 1.ANALISI ANDAMENTO TEMPORALE \n')
    risposta = input('Per visualizzare grafici concentrazione degli inquinanti in funzione del tempo digita 1, altrimenti digita 0 \n')
    if risposta == '1':
        gr.subplotInquinantiScale(stato,'Analisi ' + nome + ': grafico concentrazione inquinanti in funzione del tempo', nome , '/inq'+nome+'.png')

    print('\n 2.ANALISI SPETTRO DI FOURIER \n Verranno visualizzati i seguenti grafici: \n - spettro di potenza in funzione delle frequenze, incluso ed escluso il termine corrispondente alla frequenza 0 \n - spettro di potenza in funzione dei periodi, evidenziando la posizione dei punti in cui lo spettro ha ampiezza massima. \n Verrà visualizzato sullo schermo una tabella in cui sono riportati i valori di frequenza e periodo in cui lo spettro assume ampiezza massima, per ogni inquinante. \n')
    risposta = input('Per visualizzare i grafici e la tabella digita 1 altrimenti digita 0 \n')
    if risposta == '1':
        gr.subplotFftScale(statoFft, 'Analisi ' + nome + ': grafico spettro di potenza inquinanti in funzione delle frequenze',nome, True)
        gr.subplotFftScale(statoFft, 'Analisi ' + nome + ': grafico spettro di potenza inquinanti in funzione delle frequenze (termine zero escluso)', nome,  False)
        #trovo il massimo dello spettro di potenza degli inquinanti
        maxx, fmax, pmax = fz.massimo(statoFft)
        #gr.subplotFftScalePeriodo(statoFft, 'Analisi ' + nome + ': grafico spettro di potenza inquinanti in funzione dei periodi', nome, False, maxx)
        gr.subplotFftScalePeriodo(statoFft, 'Analisi ' + nome + ': grafico spettro di potenza inquinanti in funzione dei periodi', nome, True, maxx)
        

        fz.printMax(fmax, pmax, nome)
    print('Per confrontare lo spettro di potenza degli inquinanti si può normalizzare al valore massimo e al coefficiente c(0).\n')
    risposta = input('Per visualizzare i grafici normalizzati digita 1 altrimenti digita 0. \n')
    if risposta == '1':
        maxx, fmax, pmax = fz.massimo(statoFft)
        normC0 = ([statoFft.no2P[0], statoFft.o3P[0], statoFft.so2P[0], statoFft.coP[0]])
        normMax =  ([statoFft.no2P[maxx[0]], statoFft.o3P[maxx[1]], statoFft.so2P[maxx[2]], statoFft.coP[maxx[3]]])
        gr.subplotFftNorm(statoFft, 'Analisi ' + nome + ': grafico spettro di potenza inquinanti in funzione delle frequenze normalizzato a C(0)', nome, normC0)
        gr.subplotFftNorm(statoFft, 'Analisi ' + nome + ': grafico spettro di potenza inquinanti in funzione delle frequenze normalizzato al massimo', nome, normMax)

    #faccio stampare le correlazioni
    print('\n 3.CORRELAZIONE TRA I DATI \n')
    print('Si possono calcolare quali sono i coefficienti di correlazione tra gli inquinanti. \n Verrà visualizzata una tabella con i coefficienti. \n')
    risposta = input('Per visualizzare la tabella digita 1 altrimenti digita 0 \n')
    if risposta == '1':
        fz.visualizzaCorrelazione(stato, nome)

    print('\n 4.FILTRO IN FREQUENZA \n')
    print('Per osservare il comportamento su lungo periodo si può applicare un filtro in frequenza ai dati, mettendo a zero i coefficienti di Fourier corrispondenti a frequenze superiori ad una certa soglia. Di seguito sono state scelti quattro valori di soglia delle frequenze: \n f1 = 0.05 \n f2 = 0.03 \n f3 = 0.01 \n f4 = 0.005 \n dove l unità di misura è 1/giorno. \n Verranno visualizzati i grafici dei dati risintetizzati con i diversi filtri in funzione del tempo. \n ')

    #filtri che eliminano i coefficienti con frequenze maggiori dei quattro valori 
    filtri = ([0.05,0.03,0.01,0.005])
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
    risposta = input('Per visualizzare i grafici digiti 1 altrimenti digita 0 \n')
    if risposta == '1':
        gr.subplotFiltri(statoFiltrato1, statoFiltrato2, statoFiltrato3, statoFiltrato4, nome, filtri)

    risposta = input('Per visualizzare i grafici precedenti con maggior dettaglio digita: \n a) per f1 \n b) per f2 \n c) per f3 \n d) per f4 \n altrimenti digita 0 \n')
    if risposta == 'a':
        gr.plotInquinanti2(statoFiltrato1, 'Analisi ' + nome + ': dati risintetizzati con filtro frequenze f < ' +str(filtri[0])+' $d^-1$', nome)
    elif risposta == 'b':
        gr.plotInquinanti2(statoFiltrato2, 'Analisi ' + nome + ': dati risintetizzati con filtro frequenze f < ' +str(filtri[1])+' $d^-1$', nome)
    elif risposta == 'c':
        gr.plotInquinanti2(statoFiltrato3, 'Analisi ' + nome + ': dati risintetizzati con filtro frequenze f < ' +str(filtri[2])+ ' $d^-1$', nome)
    elif risposta == 'd':
        gr.plotInquinanti2(statoFiltrato4, 'Analisi ' + nome + ': dati risintetizzati con filtro frequenze f < ' +str(filtri[3])+ ' $d^-1$', nome)
        
    '''subplot di quattro grafici della concentrazione in funzione del tempo, in ogni grafico è riportato il dato originale e quello filtratii quattro grafici corrispondono a un tipo di inquinante diverso'''

    print('Verranno visualizzati i grafici dei dati originali e di quelli filtrati. \n')
    
    risp = '1'
    while risp == '1':
        risp = input('Per visualizzare i grafici digita 1 altrimenti digita 0. ')
        if risp == '1':
            risposta = input('Scegli il valore della frequenza di filtro: \n a) f = 0.05  \n b) f = 0.03 \n c) f = 0.01 \n d) f = 0.005 \n e) inserisci tu il valore \n')
            if risposta == 'a':
                gr.originaleVsFiltrato(stato, statoFiltrato1, 'Analisi ' + nome + ':confronto inquinanti dati originali e filtrati con frequenza f<0.1',nome, filtri[0])
            elif risposta == 'b':
                gr.originaleVsFiltrato(stato, statoFiltrato2, 'Analisi ' + nome + ': confronto inquinanti dati originali e filtrati con frequenza f<0.05',nome, filtri[1])
            elif risposta == 'c':
                gr.originaleVsFiltrato(stato, statoFiltrato3, 'Analisi ' + nome + ': confronto inquinanti dati originali e filtrati con frequenza f<0.03',nome, filtri[2])
            elif risposta == 'd':
                gr.originaleVsFiltrato(stato, statoFiltrato4, 'Analisi ' + nome + ': confronto inquinanti dati originali e filtrati con frequenza f<0.01',nome, filtri[3])
            elif risposta == 'e':
                f = float(input('inserisci frequenza [1/d]: '))
                sFiltratoFft = fz.maskStato(stato, f, f, f, f)
                sFiltrato = fz.sintesiFiltrato2(sFiltratoFft)
                gr.originaleVsFiltrato(stato, sFiltrato, 'Analisi ' + nome + ': confronto inquinanti dati originali e filtrati con frequenza f<' + str(f),nome, f)

    print('\n 5.ANALISI RUMORE \n')
    print('Calcolando la differenza tra i dati filtrati e risintetizzati e quelli originale si può analizzare l andamento del rumore, eseguendo un fito con una funzione che varia come N/f^beta. Verranno visualizzati i grafici di spettro di potenza delle differenze e funzione fittata. \n ')
    
    #calcolo differenza originale e filtrato
    diff1 = fz.differenza(stato, statoFiltrato1)
    diff2 = fz.differenza(stato, statoFiltrato2)
    diff3 = fz.differenza(stato, statoFiltrato3)
    diff4 = fz.differenza(stato, statoFiltrato4)

    diff1Fft = cl.Stato2Fft(diff1)
    diff2Fft = cl.Stato2Fft(diff2)
    diff3Fft = cl.Stato2Fft(diff3)
    diff4Fft = cl.Stato2Fft(diff4)

    mask1 = ([fz.mask(diff1Fft.no2F, filtri[0]),fz.mask(diff1Fft.o3F, filtri[0]), fz.mask(diff1Fft.so2F, filtri[0]), fz.mask(diff1Fft.coF, filtri[0])])
    mask2 = ([fz.mask(diff2Fft.no2F, filtri[1]),fz.mask(diff2Fft.o3F, filtri[1]), fz.mask(diff2Fft.so2F, filtri[1]), fz.mask(diff2Fft.coF, filtri[1])])
    mask3 = ([fz.mask(diff3Fft.no2F, filtri[2]),fz.mask(diff3Fft.o3F, filtri[2]), fz.mask(diff3Fft.so2F, filtri[2]), fz.mask(diff3Fft.coF, filtri[2])])
    mask4 = ([fz.mask(diff4Fft.no2F, filtri[3]),fz.mask(diff4Fft.o3F, filtri[3]), fz.mask(diff4Fft.so2F, filtri[3]), fz.mask(diff4Fft.coF, filtri[3])])
    
    p1, pcov1 = fz.fit(diff1Fft, mask1)
    p2, pcov2 = fz.fit(diff2Fft, mask2)
    p3, pcov3 = fz.fit(diff3Fft, mask3)
    p4, pcov4 = fz.fit(diff4Fft, mask4)
    
    
    risp = '1'
    while risp == '1':
        risp = input('Per visualizzare i grafici digita 1 altrimenti digita 0. \n ')
        if risp == '1':
            risposta = input('Scegli il valore della frequenza di filtro: \n a) f = 0.05  \n b) f = 0.03 \n c) f = 0.01 \n d) f = 0.005 \n ')
            if risposta == 'a':
                fz.printParams(p1, pcov1, filtri[0])
                gr.graficoRumore(diff1Fft, p1[0], p1[1], p1[2],p1[3], mask1, 'Rumore e fit, filtro f <'+ str(filtri[0]), filtri[0], nome)
            elif risposta == 'b':
                fz.printParams(p2, pcov2, filtri[1])
                gr.graficoRumore(diff2Fft, p2[0], p2[1], p3[2],p4[3], mask2, 'Rumore e fit, filtro f <'+ str(filtri[1]), filtri[1], nome)
            elif risposta == 'c':
                fz.printParams(p3, pcov3, filtri[2])
                gr.graficoRumore(diff3Fft, p3[0], p2[1], p3[2],p4[3], mask3, 'Rumore e fit, filtro f <'+ str(filtri[2]), filtri[2], nome)
            elif risposta == 'd':
                fz.printParams(p4, pcov4, filtri[3])
                gr.graficoRumore(diff4Fft, p4[0], p2[1], p3[2],p4[3], mask4, 'Rumore e fit, filtro f <'+ str(filtri[3]), filtri[3], nome)
            


    
    return 'Analisi completata \n'

def tuttiInsieme(fl, il, ny, te, ca, flF, ilF, nyF, teF, caF):
    print('Verranno visualizzati i grafici : \n -  concentrazione degli inquinanti in funzione del tempo \n - concentrazione dati filtrati in funzione del tempo\n dei cinque stati. \n') 
    filtro = float(input('Inserisci valore frequenza con cui filtrare i dati \n f = '))
    
    #filtro gli stati
    flFf = fz.maskStato(fl, filtro, filtro, filtro, filtro)
    ilFf = fz.maskStato(il, filtro, filtro, filtro, filtro)
    nyFf = fz.maskStato(ny, filtro, filtro, filtro, filtro)
    teFf = fz.maskStato(te, filtro, filtro, filtro, filtro)
    caFf = fz.maskStato(ca, filtro, filtro, filtro, filtro)
    #risintetizzo
    flFil = fz.sintesiFiltrato2(flFf)
    ilFil = fz.sintesiFiltrato2(ilFf)
    nyFil = fz.sintesiFiltrato2(nyFf)
    teFil = fz.sintesiFiltrato2(teFf)
    caFil = fz.sintesiFiltrato2(caFf)
    gr.graficoTuttiStati(fl, 'Florida', il, 'Illinois', ny, 'New York', te, 'Texas', ca, 'California', 'confronto inquinanti in tutti gli stati', '')
    gr.graficoTuttiStati(flFil, 'Florida', ilFil, 'Illinois', nyFil, 'New York', teFil, 'Texas', caFil, 'California', 'confronto inquinanti in tutti gli stati filtrati con filtro f < '+ str(filtro) + '$d^{-1}$', str(filtro))

def mappa(fl, il, ny, te, ca):
    #funzione che fa visualizzare in una mappa l'andamento degli inquinanti filtrati con cadenza mensile
    
    print('Può essere visualizzata una mappa che mostra come varia la concentrazione di un inquinante mensilmente a partire dai dati filtrati con una frequenza a piacere. \n ') 
    filtro = float(input('Inserisci valore frequenza con cui filtrare i dati \n f = '))
    
    flDf = fz.month(fl, filtro)
    ilDf = fz.month(il, filtro)
    nyDf = fz.month(ny, filtro)
    teDf = fz.month(te, filtro)
    caDf = fz.month(ca, filtro)
    
    fl = fz.createStato2b(flDf)
    il = fz.createStato2b(ilDf)
    ny = fz.createStato2b(nyDf)
    te = fz.createStato2b(teDf)
    ca = fz.createStato2b(caDf)

    gr.graficoTuttiStati(fl, 'Florida', il, 'Illinois', ny, 'New York', te, 'Texas', ca, 'California', 'inquinanti filtrati valori mensili filtrati con filtro f < '+ str(filtro) + '$d^{-1}$', str(filtro)+'mensile')

    florida = np.full(len(fl.no2), 'FL')
    illinois = np.full(len(il.no2), 'IL')
    newyork = np.full(len(ny.no2), 'NY')
    texas = np.full(len(te.no2), 'TX')
    california = np.full(len(ca.no2), 'CA')
    
    dates = np.concatenate((fl.date, il.date, ny.date, te.date, ca.date))
    states = np.concatenate((florida, illinois, newyork, texas, california))
    no2 = np.concatenate((fl.no2, il.no2, ny.no2, te.no2, ca.no2))
    o3 = np.concatenate((fl.o3, il.o3, ny.o3, te.o3, ca.o3))
    so2 = np.concatenate((fl.so2, il.so2, ny.no2, te.so2, ca.so2))
    co = np.concatenate((fl.co, il.co, ny.co, te.co, ca.co))

    maxno2 = max(no2)
    maxo3 = max(o3)
    maxso2 = max(so2)
    maxco = max(co)
    
    dataframe = pd.DataFrame()
    dataframe['date'] = dates
    dataframe['states'] = states
    dataframe['no2'] = no2*100/maxno2
    dataframe['o3'] = o3*100/maxo3
    dataframe['so2'] = so2*100/maxso2
    dataframe['co'] = co*100/maxco
    dataframe['date'] = pd.to_datetime(dataframe['date']).dt.date.astype(str)
    dataframe = dataframe.sort_values('date')

    risp = '1'
    while risp == '1':
        risp = input('Per visualizzare le mappe digita 1 altrimenti digita 0. \n ')
        if risp == '1':
            risposta = input('Scegli l inquinante da visualizzare: \n a) NO2  \n b) O3 \n c) SO2 \n d) CO \n ')
            if risposta == 'a':
                fz.figMap(dataframe, maxno2, 'no2')
            elif risposta == 'b':
                fz.figMap(dataframe, maxo3, 'o3')
            elif risposta == 'c':
                fz.figMap(dataframe, maxso2, 'so2')
            elif risposta == 'd':
                fz.figMap(dataframe, maxco, 'co')
        


#---------------------------------------------------------------#
#      Lettura file di dati: medie giornaliere                  #
#---------------------------------------------------------------#
currentDirectory = os.getcwd()

flDf = pd.read_csv(currentDirectory+'/fileCSV/floridaDate.csv')
ilDf = pd.read_csv(currentDirectory+'/fileCSV/illinoisDate.csv')
nyDf = pd.read_csv(currentDirectory+'/fileCSV/newyorkDate.csv')
teDf = pd.read_csv(currentDirectory+'/fileCSV/texasDate.csv')
caDf = pd.read_csv(currentDirectory+'/fileCSV/californiaDate.csv')

#---------------------------------------------------------------#
#              Creazione classi stato                           #
#---------------------------------------------------------------#

Florida = fz.createStato2(flDf)
Illinois = fz.createStato2(ilDf)
Newyork = fz.createStato2(nyDf)
Texas = fz.createStato2(teDf)
California = fz.createStato2(caDf)

#---------------------------------------------------------------#
#      Calcolo trasformate di Fourier per ogni stato            #
#---------------------------------------------------------------#

FloridaFft = cl.Stato2Fft(Florida)
IllinoisFft = cl.Stato2Fft(Illinois)
NewyorkFft = cl.Stato2Fft(Newyork)
TexasFft = cl.Stato2Fft(Texas)
CaliforniaFft = cl.Stato2Fft(California)

#---------------------------------------------------------------#
#              Scelta stato da analizzare                       #
#---------------------------------------------------------------#
scelta = '1'
while scelta != '0':
    scelta = input('Seleziona lo stato da analizzare inserendo il numero corrispondente tra i seguenti: \n 1-Florida \n 2-Illinois \n 3-Newyork \n 4-Texas \n 5-California \n 6-Confronto tutti gli stati \n 7-visualizza mappa \n oppure digita 0 per terminare esecuzione \n ')
    if scelta == '1':
        risposta = analisiStato(Florida, FloridaFft, 'Florida')
        print(risposta)
    elif scelta == '2':
        risposta = analisiStato(Illinois, IllinoisFft, 'Illinois')
        print(risposta)
    elif scelta == '3':
        risposta = analisiStato(Newyork, NewyorkFft, 'NewYork')
        print(risposta)
    elif scelta == '4':
        risposta = analisiStato(Texas, TexasFft, 'Texas')
        print(risposta)
    elif scelta == '5':
        risposta = analisiStato(California, CaliforniaFft, 'California')
        print(risposta)
    elif scelta == '6':
        tuttiInsieme(Florida, Illinois,  Newyork, Texas, California, FloridaFft, IllinoisFft,NewyorkFft, TexasFft, CaliforniaFft)
    elif scelta == '7':
        mappa(Florida, Illinois,  Newyork, Texas, California)
    elif scelta == '0':
        print('esecuzione terminata')
    else:
        print('Non hai selezionato una scelta valida \n')

