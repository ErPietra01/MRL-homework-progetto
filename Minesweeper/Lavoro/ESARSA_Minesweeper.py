import numpy as np
import pandas as pd
from collections import defaultdict
import random
rng = np.random.default_rng()

# import delle funzioni ausiliarie in state_bridge: sarà sufficiente richiamarle con sb.nome()
import state_bridge as sb
#sb.get_hidden_cells()

# import dell'ambiente Minesweeper: ora ho accesso a tutte le funzioni
from minesweeper_env import MinesweeperEnv


'''inizializzazione dell'ambiente, d'ora in poi posso chiamare tutte le funzioni 
tramite ambiente.funzione()'''
larghezza = 8
altezza = 8
bombe = 10
# nota: dimensioni allocate separatamente per poterle modificare in seguito
ambiente = MinesweeperEnv(width = larghezza, height = altezza, n_mines = bombe)


# parametri dell'algoritmo
numepisodes = 100_000
gamma = 0.9
alpha = 0.01
epsilon = 0.1
totrew = np.zeros(numepisodes)

# Dizionario Q con chiave = vettore delle features + azione e valore = valore della coppia stato-azione
# nota: l'azione è solo "rivela", di conseguenza la chiave sarà il solo vettore delle features
# e non ci sarà da scegliere una azione
Q = defaultdict(float) # tutte le nuove chiavi sono inizializzate con valore 0
'''Usare il dizionario permette inoltre di inizializzare un tabellone di gioco diverso
per ogni episodio: l'agente impara a giocare a prescindere dalla board specifica'''

for e in range(numepisodes):
    ambiente.reset()
    done = False


    '''exploring start: scelgo una cella a caso da cui partire, la rivelo e aggiorno 
    lo stato (oppure l'episodio termina se la cella scelta è una mina)'''
    x0, y0 = random.randint(0, larghezza-1), random.randint(0, altezza-1)
    index = np.ravel_multi_index ((x0,y0), (larghezza,altezza))
    
    # step con l'azione casuale: primo aggiornamento dello stato
    _, rew, done = ambiente.step(index)
    featinit = sb.get_features(ambiente, index, sb.build_coord_lookup(ambiente))
    primachiave = sb.features_to_key(featinit)
    _, reward, done = ambiente.step(index)

    # comincia l'iterazione che terminerà quando l'agente finirà in uno stato terminale
    while done == False:

        '''con get_hidden_cells ottengo la lista degli indici delle celle nascoste'''
        nascoste = sb.get_hidden_cells(ambiente)
        '''state crea una lista di dizionari: con lookup costruisco invece un singolo
        dizionario coordinata:valore per fare tutte le operazioni successive'''
        lookup = sb.build_coord_lookup(ambiente)

        '''ora popolo una lista di candidati, ovvero di associazioni tra cella e vettore delle features'''
        candidate = []
        for cella in nascoste:
            '''calcolo il vettore delle features per tutte le celle ricavando le features per ogni cella
            nascosta, inserendole in una tupla e aggiornando le possibili celle candidate
            mantenendo una corrispondenza tra le features e l'indice'''
            features = sb.get_features(ambiente, cella, lookup)
            key = sb.features_to_key(features)
            candidate.append((key, cella))

        '''A questo punto ho la lista delle celle candidate e la rispettiva tupla delle features
        -> posso implementare la logica epsilon greedy per popolare Q scegliendo la cella (indice)
        con valore maggiore oppure una qualunque tra le candidate'''
        action = None # indice della cella scelta
        bestkey = None # chiave scelta in base alla policy greedy
        bestvalue = None # valore associato alla chiave migliore

        if random.random() < epsilon:
            # azione casuale: scelgo un indice casuale tra le celle ancora nascoste
            action = random.choice(nascoste)
            scelta = sb.get_features(ambiente, action, lookup)
            bestkey = sb.features_to_key(scelta)
        else: 
            #azione greedy: scansiono le coppie chiave-indice in candidateS
            for key, cella in candidate:
                valore = Q.get(key, 0.0)
                if bestvalue is None or valore > bestvalue:
                    action = cella
                    bestkey = key


        '''Ora passo l'indice a step per aggiornare la griglia, ottenere la reward istantanea,
        verificare se mi trovo in uno stato terminale e aggiornare il valore delle features in Q'''

        _, reward, done = ambiente.step (action)
        totrew[e] += reward

        '''devo calcolare il valore atteso delle prossime azioni; l'ambiente è
            stato già aggiornato da step e ora devo valutare il prossimo stato, ovvero
            la nuova griglia ottenuta dopo l'azione'''
        
        prossime = sb.get_hidden_cells(ambiente)
        prossimalookup = sb.build_coord_lookup(ambiente)
        
        prossimivalori = []

        if done == True:
            Q[bestkey] += alpha * (reward + gamma *0 - Q[bestkey])

        elif done == False:

            for n in prossime:
                prossimafeat = sb.get_features(ambiente, n, prossimalookup)
                prossimachiave = sb.features_to_key(prossimafeat)
                prossimivalori[n] = Q.get (prossimachiave)

            expectedvalue = (1-epsilon) * np.max(Q.values()) + epsilon * np.sum(Q.values())
            Q[bestkey] += alpha * (reward + gamma * expectedvalue - Q[bestkey])
      



'''Schema generale dell'algoritmo E-SARSA: 
- per ogni episodio inizializzo l'ambiente (creo quindi una nuova board) e scelgo una exploring start
- scelgo una azione greedy basata sullo stato corrente (anche se in teoria dovrbbe essere deterministica)
- costruisco l'episodio in un ciclo while finché non si raggiunge uno stato terminale
- per ogni passo calcolo la reward istantanea e aggiorno il valore della feature in Q

SEQUENZA DELL'USO DELLE FUNZIONI AUSILIARIE:
hidden = get_hidden_cells(env)
coord_lookup = build_coord_lookup(env)

candidates = []
for idx in hidden:
    features = get_features(env, idx, coord_lookup)
    key = features_to_key(features)
    candidates.append((key, idx))

# epsilon-greedy su candidates, usando Q.get(key, 0.0) per ciascuno
# ... (questa parte la scrivi tu, e' il cuore del tuo E-SARSA)

action_index = ...  # scelto sopra

state_before = [dict(t) for t in env.state] if env.n_clicks == 0 else None
_, reward, done = env.step(action_index)

if state_before is not None:
    changed = detect_actually_revealed(state_before, env.state)
    # se necessario, usa 'changed' per capire quale cella e' stata
    # davvero rivelata al posto di action_index (redirect prima mossa)
    # '''


#
