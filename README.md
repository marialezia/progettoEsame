# progettoEsame
librerie necessarie: numpy, pandas, scipy, sys, os, tqdm, plotly.express, seaborn
Passi: 
1- copiare file con i dati pollution_us_2005_2007.csv all'interno della cartella fileCSV della repository
2- eseguire con python il file gestioneDati.py presente all'interno della cartella pollution, questo file seleziona dal csv con tutti i dati solo quelli necessari per l'analisi, in particolare: 
	- in primo luogo estrapola cinque stati rappresentativi (California, New york, Illinois, Florida, Texas) e crea nuovi file csv per ogni stato e lasciando solo i dati di interesse
	- per ognuno dei cinque stati crea due diverse tabelle mediando i valori degli inquinanti, una per l'analisi stati (no distinzione stazioni monitoraggio) e una per l'analisi delle stazioni (dati stazioni vengono mantenuute separate
3- ora è possibile eseguire indistintamente i file analisiStati.py o AnalisiStazioni.py 


ci sono tre distinti file di analisi: 
	a)analisi stati--> prende ognuno dei cinque stati, fa vedere in un unico grafico andamento degli inquinanti senza distinguere le stazioni di monitoraggio, fa la trasformata e fa vedere il grafico dello spettro di potenza
	b)analisi stazioni--> per ogni stato distingue le stazioni di monitoraggio 
	c)analisi inquinanti
