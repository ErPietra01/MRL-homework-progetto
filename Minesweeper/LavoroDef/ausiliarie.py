from collections import defaultdict
'''In questo file sono presenti alcune funzioni ausiliarie
per far comunicare il main con l'ambiente e per facilitare
l'utilizzo di Q come dizionario'''

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
    for i in ambiente.state: #for i in range(ambiente.state):
        listadict[i['coord']] = i['value']
    return listadict

def valori_vicini (lookup, coordinate, Xenv, Yenv):
    '''funzione che valuta il valore [0-8 + U], rispettando 
    le dimensioni della griglia e non contando la cella stessa
    (qui conviene lavorare per coordinate per un controllo 
    più semplice)'''
    x,y = coordinate[0], coordinate[1]

    vicini = []
    for i in range (y-1, y+2):
        for j in range (x-1,x+2):
            if (x != j or y != i) and (0<= i < Yenv) and (0 <= j < Xenv):
                vicini.append (lookup[(j,i)])
    return vicini

def posizione (vicini):
    '''Calcolo una posizione approssimativa della cella: 
    bordo, angolo o centrale'''
    num_vicini = len(vicini)

    if num_vicini == 3: 
        pos = "angolo"
    elif num_vicini == 5:
        pos = "bordo"
    else: #elif num_vicini == 8: pos = "centrale" else return fail
        pos = "centrale"
    return pos

def genera_features (ambiente, a, listadict):
    '''Questa funzione genera la tupla delle features in base
    ai valori vicini e alla posizione approssimativa sulla griglia
    (quindi non le coordinate esatte)'''

    # posizione sulla griglia: conversione da indice a coordinate
    coord = ambiente.state[a]['coord']
    #valori dei vicini:
    valvicini = valori_vicini(listadict,coord,ambiente.nrows, ambiente.ncols)

    # posizione sulla griglia:
    pos = posizione(valvicini)

    '''features: quante celle sono nascoste, quante celle sono rivelate, e posizione indicativa'''
    nascoste = 0
    '''controllo di sicurezza: se il valore più basso delle celle vicine è
        minore o uguale a 3, allora le celle sono meno rischiose, altrimenti ci sono 
        molte bombe intorno e liberare celle in prossimità potrebbe comportare
        la sconfitta con probabilità maggiore'''
    sicure = 0
    rischiose = 0
    for i in valvicini:
        if i == 'U':
            nascoste += 1
        else:
            if i >=3:
                rischiose += 1
            else:
                sicure += 1

    rischio = None
    if rischiose >= sicure:
        rischio = 0
    else:
        rischio = 1

    '''fornisco le features come tupla dei tre valori calcolati'''
    features = (nascoste, pos, rischio)

    '''features = defaultdict(float)
    features["nascoste"] = nascoste
    features["posizione"] = pos
    features["rischio"] = rischio'''

    return features



#
