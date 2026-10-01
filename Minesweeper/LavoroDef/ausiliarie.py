# from collections import defaultdict
import numpy as np
'''In questo file sono presenti alcune funzioni ausiliarie
per far comunicare il main con l'ambiente e per facilitare
l'utilizzo di Q come dizionario
L'ambiente usa principalmente un indice, ma per la valutazione delle features 
è più comodo usare le coordinate, motivo per cui utilizziamo entrambe
'''

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

def genera_features (ambiente, a, listadict, proporzione, bombe):
    '''Questa funzione genera la tupla delle features in base
    ai valori vicini e alla posizione approssimativa sulla griglia
    (quindi non le coordinate esatte)'''

    # posizione sulla griglia: conversione da indice a coordinate
    coord = ambiente.state[a]['coord']
    #valori dei vicini:
    valvicini = valori_vicini(listadict,coord,ambiente.nrows, ambiente.ncols)

    numerivicini = []
    for i in valvicini:
        if i != 'U':
            numerivicini.append(i)

    if len (numerivicini) > 0:
        minvicini = min (numerivicini)
        maxvicini = max (numerivicini)
    else:
        minvicini = 0
        maxvicini = 0

    # popsizione sulla griglia:
    pos = posizione(valvicini)

    '''features: quante celle sono nascoste posizione indicativa e livello di rischio'''
    nascoste = 0
    '''controllo di sicurezza: se il valore più basso delle celle vicine è
        minore o uguale a 3, allora le celle sono meno rischiose, altrimenti ci sono 
        molte bombe intorno e liberare celle in prossimità potrebbe comportare
        la sconfitta con probabilità maggiore'''
    sicure = 0
    rischiose = 0
    occupate = 0
    for i in valvicini:
        if i == 'U':
            nascoste += 1
        else:
            occupate += 1
        '''else:
            if i >=3:
                rischiose += 1
            else:
                sicure += 1'''

    rischio = None
    if  occupate < 3: #rischiose >= sicure:
        rischio = 0
    else:
        rischio = 1

    prop = None
    '''valore indicativo della proporzione di bombe rimaste'''
    if proporzione < 0.33:
        prop = 'bassa'
    elif 0.33 <= proporzione <= 0.66:
        prop = 'media'
    else:
        prop = 'alta'

    '''Restituisco le features in base a quanto è grande la griglia'''
    if bombe <= 3:
        '''fornisco le features come tupla dei 6 valori calcolati'''
        features = (nascoste, pos, rischio, prop, minvicini, maxvicini)
    else: 
        features = (nascoste, pos, rischio)

    '''features = defaultdict(float)
    features["nascoste"] = nascoste
    features["posizione"] = pos
    features["rischio"] = rischio'''

    return features


def featuresver2 (ambiente, a, listadict):
    '''funzione che genera un vettore con il conteggio
    dei possibili valori (U, 1-8) delle celle vicine'''
    coord = ambiente.state[a]['coord']
    #valori dei vicini:
    valvicini = valori_vicini(listadict,coord,ambiente.nrows, ambiente.ncols)

    features = np.zeros(11)
    '''Termine di bias'''
    features[10] = 1

    '''for che aggiorna il conteggio per le celle nascoste e per le celle
    con un numero sopra nell'intorno della cella in esame.'''
    for i in valvicini:
        if i == 'U':
            features[9]+=1
        else:
            features[i] += 1
            '''vicini_squared = valori_vicini(listadict)
            Implementare feature aggiuntiva con il check delle vicine delle celle scoperte'''
    
    return features



#