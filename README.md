# progettoEsame
**librerie necessarie:** numpy, pandas, scipy, sys, os, tqdm, plotly.express, seaborn
### Passi: 
**1**- copiare file con i dati pollution_us_2005_2007.csv nella cartella fileCSV presente all'interno della cartella pollution della repository \
**2**- eseguire con python il file gestioneDati.py presente all'interno della cartella pollution, questo file seleziona dal csv con tutti i dati solo quelli necessari per l'analisi, in particolare: \
	- in primo luogo estrapola cinque stati rappresentativi (California, New york, Illinois, Florida, Texas) e crea nuovi file csv per ogni stato e lasciando solo i dati di interesse \
	- per ognuno dei cinque stati crea due diverse tabelle mediando i valori degli inquinanti, una per l'analisi stati (no distinzione stazioni monitoraggio) e una per l'analisi delle stazioni (dati stazioni vengono mantenuute separate \
**3**- Eseguire i file analisiStati.py o analisiStazioni.py, l'ordine non è vincolante. \
Il file analisiStati.py esegue un'analisi più dettagliata per i cinque stati metre il file analisiStazioni.py ripete alcuni passaggi dell'analisi, osservando separatamente i dati presi dalle diverse stazioni di monitoraggio degli stati. \
La maggior parte dei grafici e delle tabelle che sono generati nell'esecuzione vengono salvati all'interno della cartella datiSalvati. \

