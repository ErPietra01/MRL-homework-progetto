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

def dizioario_lookup (ambiente):
    '''funzione che smonta la lista di dizionari e crea
    un unico dizionario coordinate:valore'''
    lookup = {}
    for i in ambiente.state:
        lookup[i['coord']] = i['value']
    return lookup

def valori_vicini (lookup, coordinate, Yenv, Xenv):
    '''funzione che valuta quanti vicini ci sono, rispettando 
    le dimensioni della griglia e non contando la cella stessa'''
    x,y = coordinate[0], coordinate[1]

    vicini = []
    for i in range (y-2, y+2):
        for j in range (x-2,x+2):
            if (x != j or y != i) and (0<= i < Yenv) and (0 <= j < Xenv):
                vicini.append (lookup[(i,j)])
    return vicini

