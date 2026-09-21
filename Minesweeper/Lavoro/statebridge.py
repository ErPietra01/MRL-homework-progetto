'''In questo file sono presenti alcune funzioni ausiliarie che consentono di 
lavorare con l'ambiente scelto e di studiare la matrice Q come dizionario che associa
un valore a un vettore di features'''

'''la funzione cellenascoste si occupa di verificare quali celle sulla griglia sono
ancora nascoste e di aggiungerne l'indice alla lista delle celle nascoste '''
def cellenascoste(ambiente):
    hidden = []
    for i, t in enumerate(ambiente.state):
        if t['value'] == 'U':
            hidden.append(i)

    return hidden

'''state è una lista di dizionari; con dizionariolookup costruisco un unico dizionario
coordinata : valore numerico per lavorarci più facilmente'''
def dizionariolookup(ambiente):
    return {t['coord'] : t['value'] for t in ambiente.state}


'''date le coordinate di una cella, questa funzione studia i valori di tutti i
vicini usando il dizionario di lookup della funzione precedente'''
def valorivicini (lookup, coord, larghezza, altezza):
    x,y = coord[0], coord[1]

    vicini = []
    for colonna in range(y-1,y+2):
        for riga in range (x-1,x+2):
            #verifico di trovarmi nel range delle dimensioni della griglia e di non essere nella cella candidata
            if ((x != riga) or y != colonna) and(0 <= colonna < larghezza) and (0 <= riga < altezza):
                '''aggiungo ai vicini il valore delle celle vicine, non le coordinate!
                sto lavorando per features, non mi interessano le posizioni specifiche ma le caratteristiche'''
                vicini.append(lookup[(riga, colonna)])

'''Funzione che crea le tuple con le features della cella nascosta indicizzata da indice: a partire da 
state, calcola tutte le caratteristiche dei vicini e la posizione approssimativa'''
def features (ambiente, indice, lookup):

    coordinate = ambiente.state[indice]['coord']
    vicini = valorivicini (lookup, coordinate, ambiente.ncols, ambiente.nrows)

    contanascoste = sum (1 for v in vicini if v == 'U')
    scoperte = [v for v in vicini if v != 'U']
    '''misura di "sicurezza"': se nei dintorni c'è un vicino con una sola mina accanto, 
    allra dovrebbe essere più sicuro scoprire una cella'''
    minimo = min(scoperte) if scoperte else -1

    '''tramite valorivicini ho controllato di non uscire dai bordi e, di conseguenza,
    avrò più o meno vicin a seconda che mi trovo sul bordo o in una casella centrale'''
    nvicini = len (vicini)
    if nvicini == 3:
        posizione = "angolo"
    elif nvicini == 5:
        posizione = "bordo"
    else:
        posizione = "interno"

    '''restituisco un dizionario con le features in modo tale da poter costruire la tupla'''
    return {"nascosti" : contanascoste,
            "minimo" : minimo,
            "posizione" : posizione}


def associazioneFQ(features):
    '''ora costruisco la tupla da mettere come chiave di Q'''
    return (features["nascosti"], features["minimo"], features["posizione"])


def controllosvelate (prima, dopo):
    cambiate = []
    for i, (p, d) in enumerate(zip(prima, dopo)):
        if p['value'] == 'U' and d['value'] == 'U':
            cambiate.append(i)
    return cambiate






#