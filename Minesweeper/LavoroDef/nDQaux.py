# from collections import defaultdict
import numpy as np
'''In questo file sono presenti alcune funzioni ausiliarie
per far comunicare il main con l'ambiente e per facilitare
l'utilizzo di Q come dizionario
L'ambiente usa principalmente un indice, ma per la valutazione delle features
è più comodo usare le coordinate, motivo per cui utilizziamo entrambe

NOTA: file NUOVO, non sovrascrive ausiliarie2.py. celle_nascoste, lista_dict,
valori_vicini, posizione e featuresver2 sono copiate identiche da ausiliarie2.py
(stesse features, stessa normalizzazione). L'unica aggiunta è
valore_atteso_lambda, portata da ausiliarie.py (dove viene usata da
ESARSAnstepsms.py), adattata per richiamare la featuresver2 di questo file.
Serve a nDQ.py per calcolare il valore atteso E-SARSA su un singolo vettore
dei pesi alla volta: nDQ.py la richiama due volte per passo (una per w1, una
per w2) per poter fare l'aggiornamento Double Q-learning anche con i ritorni
a n passi.'''

def celle_nascoste (ambiente):
    nascoste = []

    '''a partire dallo stato definito nell'ambiente ottengo la lista
    degli indici delle celle ancora libere;
    Notare che l'indice della lista state corrisponde all'indice
    lineare della cella sulla griglia'''
    for i, t in enumerate(ambiente.state):
        if t['value'] == 'U':
            nascoste.append(i)

    return nascoste


def lista_dict (ambiente):
    '''funzione che smonta la lista di dizionari e crea
    un unico dizionario coordinate:valore'''
    listadict = {}
    for i in ambiente.state:
        listadict[i['coord']] = i['value']
    return listadict

def valori_vicini (listadict, coordinate, Xenv, Yenv):
    '''funzione che valuta il valore [0-8 + U], rispettando
    le dimensioni della griglia e non contando la cella stessa
    (qui conviene lavorare per coordinate per un controllo
    più semplice)'''
    x,y = coordinate[0], coordinate[1]

    vicini = []
    for i in range (y-1, y+2):
        for j in range (x-1,x+2):
            if (x != j or y != i) and (0<= i < Yenv) and (0 <= j < Xenv):
                vicini.append (listadict[(j,i)])
    return vicini

def posizione (vicini):
    '''Calcolo una posizione approssimativa della cella:
    bordo, angolo o centrale'''
    num_vicini = len(vicini)

    if num_vicini == 3:
        pos = "angolo"
    elif num_vicini == 5:
        pos = "bordo"
    else:
        pos = "centrale"
    return pos


def featuresver2 (ambiente, a, listadict,proporzione, bombe):
    '''funzione che genera un vettore con il conteggio
    dei possibili valori (U, 0-8) delle celle vicine'''
    coord = ambiente.state[a]['coord']
    #valori dei vicini:
    valvicini = valori_vicini(listadict,coord,ambiente.nrows, ambiente.ncols)

    features = np.zeros(19)
    '''Termine di bias'''
    features[10] = 1


    '''for che aggiorna il conteggio per le celle nascoste e per le celle
    con un numero sopra nell'intorno della cella in esame.'''
    num = 0
    cellevicine = []
    for i in valvicini:
        if i == 'U':
            features[9]+=1
        else:
            features[i] += 1
            cellevicine.append(i)
            num += 1

    '''feature di deduzione: è un contatore che, per ogni cella scoperta nell'intorno,
    calcola quante celle coperte ha intorno; se tale numero è pari al numero sopra la cella,
    allora incremento il contatore'''
    deduzione = 0

    '''Funzione di deduzione'''

    '''coordinate della cella in esame'''
    x = coord[0]
    y = coord[1]

    '''dimensioni dell'ambiente per non uscire dai confini'''
    Xenv = ambiente.nrows
    Yenv = ambiente.ncols

    checkvicini = []

    for i in range (y-1, y+2):
        for j in range (x-1,x+2):
            '''gestione dei vicini del vicino'''
            if (x != j or y != i) and (0<= i < Yenv) and (0 <= j < Xenv) and listadict[(j,i)] != 'U':
                xVicina = j
                yVicina = i
                coord2 = (xVicina, yVicina)
                '''valore 0-8,U della cella vicina in esame'''
                valsquared = listadict[(xVicina, yVicina)]
                vicinisquared = valori_vicini (listadict,coord2, Xenv, Yenv)
                if vicinisquared.count('U') == valsquared:
                    deduzione += 1
                '''rapporto tra il valore della cella vicina e il numero di celle coperte intorno ad essa'''
                checkvicini.append(valsquared/vicinisquared.count('U')) if vicinisquared.count('U') != 0 else 0

    features[11] = deduzione

    '''features presenti anche nella versione precedente:'''
    nascoste = 0
    occupate = 0
    for i in valvicini:
        if i == 'U':
            nascoste += 1
        else:
            occupate += 1

        rischio = None
        if  occupate/len(valvicini) < 0.33: #rischiose >= sicure:
            rischio = 0
        else:
            rischio = 1

    features[12] = rischio

    prop = None
    '''valore indicativo della proporzione di bombe rimaste'''
    features[13] = proporzione

    sommavicini = sum(cellevicine)
    avg = sommavicini/num if num > 0 else 0
    features[14] = avg/8

    '''posizione descritta anche dal numero dei vicini: 3 angolo, 5 bordo, 8 centrale
    n.b. feature normalizzata direttamente sul suo massimo teorico'''
    features[15] = len(valvicini)/8

    hidden = celle_nascoste(ambiente)
    features[16] = len(hidden) /len(ambiente.state)

    sx = x/(Xenv-1)
    dx = (Xenv-1-x)/(Xenv-1)
    up = y/(Yenv-1)
    down = (Yenv-1-y)/(Yenv-1)
    pos = min(sx,dx,up,down)
    features[17] = pos

    features[18] = max(checkvicini) if checkvicini else 0

    '''normalizzazione delle features'''
    for i in [0,1,2,3,4,5,6,7,8,9,11,18]:
        features[i] = features[i]/len(valvicini)

    return features


'''Funzione per l'aggiornamento a n passi (porting di valore_atteso_lambda da
ausiliarie.py, usata in ESARSAnstepsms.py): calcola il valore atteso E-SARSA
sulle celle ancora nascoste a partire da UN SOLO vettore dei pesi w.
In nDQ.py viene richiamata due volte per passo (una con w1, una con w2) così
da poter fare il cross-bootstrap tipico del Double Q-learning anche con
ritorni a n passi: per aggiornare w1 si usa il valore atteso restituito da
questa funzione chiamata con w2, e viceversa.'''
def valore_atteso_lambda (ambiente, w, nascoste, proxlistadict, epsilon, proporzione, bombe):

    prossime = []

    bestvalue = None
    indicebestvalue = None

    for i in nascoste:
        x_next = featuresver2 (ambiente, i, proxlistadict, proporzione, bombe)
        valorefeat = np.dot(w,x_next)
        prossime.append(valorefeat)
        if bestvalue is None or valorefeat > bestvalue:
            bestvalue = valorefeat
            indicebestvalue = i
    valoreatteso = (1-epsilon) * bestvalue + epsilon* (sum (prossime) / len (prossime))
    return valoreatteso, indicebestvalue
