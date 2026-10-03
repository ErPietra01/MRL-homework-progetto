import random
import numpy as np
# import pandas as pd
# from collections import defaultdict
rng = np.random.default_rng(42)
import matplotlib.pyplot as plt

'''----------funzioni ausiliarie----------'''

import ausiliarie as aux

'''----------parametri dell'algoritmo E-SARSA----------'''

num_episodes = 150_000
alpha = 0.001
#epsilon = 0.1 # epsilon decrescente migliora la convergenza!
epsilon0 = 0.1
epsilon_min = 0.01
decay = 5 / num_episodes
gamma = 0.9

'''----------inizializzazione dell'ambiente----------'''

from minesweeper_env import MinesweeperEnv
Xenv = 4
Yenv = 4
'''percentuale di bombe in base alla difficoltà:
facile: circa 12%
medio: circa 16%
difficile: circa 20%
'''
bombe = 8
ambiente = MinesweeperEnv(width = Xenv, height = Yenv, n_mines = bombe)

'''----------conteggi----------'''

totrew = np.zeros(num_episodes)
vittorie = np.zeros(num_episodes)

'''----------Matrice Q----------'''

'''la matrice Q dei valori delle coppie stato-azione viene codificata come un 
dizionario che associa un valore alle features invece che agli stati
Q = defaultdict(float)'''

'''Vettore dei valori dei numeri sulle celle (U, 0-8); questa è la struttura che verrà aggiornata
ad ogni passo.
Stiamo sostanzialmente creando un approssimatore lineare aggiornato tramite E-SARSA!'''
w = np.zeros(12)
# w = np.random.rand(12)

'''----------Algoritmo E-SARSA----------'''

for e in range(num_episodes):

    epsilon = epsilon_min + (epsilon0 - epsilon_min) * np.exp(-decay * e)

    '''rappresentazione grafica dell'andamento dell'algoritmo ogni 10.000 episodi'''
    mostra = (e % 10000 == 0) or (e == num_episodes - 1)

    '''lista delle caselle visitate: utile per una stampa
    in caso di vittoria e ogni 10.000 passi'''
    sequenza = []

    '''in ogni episodio c'è un nuovo tabellone con
    le mine in posizioni casuali'''
    ambiente.reset()
    done = False

    '''----------exploring start----------'''

    '''parto da una cella casuale sul tabellone'''
    x0, y0 = rng.integers(0,Xenv), rng.integers(0,Yenv)
    '''esprimo le coordinate come indice lineare'''
    index0 = np.ravel_multi_index((x0,y0),(Xenv,Yenv))

    '''dizionario coordinate:valore'''
    listadict = aux.lista_dict(ambiente)

    '''nascoste0 = aux.celle_nascoste(ambiente)
    quantenascoste0 = len(nascoste0)'''

    '''features della cella in esame
    features = aux.genera_features(ambiente, index0, listadict, bombe/quantenascoste0, bombe)'''

    '''features calcolate con il metodo nuovo (usiamo la notazione della regressione lineare)'''
    x = aux.featuresver2 (ambiente, index0, listadict)

    done = None

    _, reward, done = ambiente.step(index0)
    totrew[e] += reward
    sequenza.append(ambiente.state[index0]['coord'])

    index = None

    '''ora devo valutare la prima mossa casuale: faccio un passo dell'algoritmo'''

    if done: #ambiente.state[index0]['value'] == 'B':
        '''sconfitta: aggiorno la griglia con step e salvo done = True
        Q[features] += alpha * (reward + gamma * 0 - Q[features])'''

        Q = np.dot(w,x)
        w += alpha *(reward + gamma * 0 - Q) * x

    else:
        '''Il primo passo è andato a buon fine: aggiorno la griglia
        e salvo done = False (ovvero: applico E-SARSA)'''

        '''prendo la lista degli indici delle celle ancora nascoste DOPO l'aggiornamento
        della griglia a seguito di step'''
        nascoste = aux.celle_nascoste(ambiente)
        # quantenascoste = len(nascoste)

        '''Aggiorno il dizionario coordinate:valore a seguito di step'''
        proxlistadict = aux.lista_dict(ambiente)

        '''----------epsilon greedy----------'''

        '''creo una lista dei valori delle prossime celle (per il valore atteso)'''
        prossime = []
        bestvalue = None
        indicebestvalue = None
        for i in nascoste:
            '''proxfeat = aux.genera_features(ambiente, i, proxlistadict, bombe/quantenascoste, bombe)
            valorefeat = Q.get(proxfeat,0.0)'''

            x_next = aux.featuresver2 (ambiente, i, proxlistadict)
            valorefeat = np.dot(w,x_next)
            prossime.append(valorefeat)
            if bestvalue is None or valorefeat > bestvalue:
                bestvalue = valorefeat
                indicebestvalue = i


        valoreatteso = (1-epsilon) * bestvalue + epsilon* (sum (prossime) / len (prossime))
        '''Q[features] += alpha * (reward + gamma * valoreatteso - Q[features])'''
        '''x = aux.featuresver2(ambiente, index, proxlistadict)'''
        Q = np.dot (w,x)
        w += alpha * (reward + gamma * valoreatteso - Q) * x
        #index = indicebestvalue

        if rng.random() <= epsilon:
            index = rng.choice(nascoste)
        else:
            index = indicebestvalue


    '''----------E-SARSA----------'''

    while not done:
        
        listadict = aux.lista_dict(ambiente)

        nascoste = aux.celle_nascoste(ambiente)
        # quantenascoste = len(nascoste)

        x = aux.featuresver2 (ambiente, index, listadict)
        Q = np.dot(w,x)

        _, reward, done = ambiente.step(index)

        if reward == 1:
             vittorie[e] = 1
        
        totrew[e] += reward
        sequenza.append(ambiente.state[index]['coord'])


        '''Iterazione epsilon-greedy'''

        if done:

            w += alpha * (reward + gamma * 0 - Q) * x

        else:
            '''Il passo è andato a buon fine: aggiorno la griglia
            e salvo done = False (ovvero: applico E-SARSA)'''

            '''prendo la lista degli indici delle celle ancora nascoste DOPO l'aggiornamento
            della griglia a seguito di step'''
            nascoste = aux.celle_nascoste(ambiente)
            # quantenascoste = len(nascoste)

            '''Aggiorno il dizionario coordinate:valore a seguito di step'''
            proxlistadict = aux.lista_dict(ambiente)


            '''creo una lista dei valori delle prossime celle (per il valore atteso)'''
            prossime = []
            bestvalue = None
            indicebestvalue = None
            for i in nascoste:
                x_next = aux.featuresver2 (ambiente, i, proxlistadict)
                valorefeat = np.dot(w,x_next)
                prossime.append(valorefeat)
                if bestvalue is None or valorefeat > bestvalue:
                    bestvalue = valorefeat
                    indicebestvalue = i
            
            
            valoreatteso = (1-epsilon) * bestvalue + epsilon* (sum (prossime) / len (prossime))
            w += alpha * (reward + gamma * valoreatteso - Q) * x

            '''epsilon greedy'''
            if rng.random() <= epsilon:
                index = rng.choice(nascoste)
            else:
                index = indicebestvalue


    
    '''aggiunto il dato sul winrate cumulativo e non solo la media su 1000 episodi'''
    totwin = np.cumsum(vittorie[:e])
    totepisodes = np.arange(1,e+1)
    cumwinrate = totwin/totepisodes

    '''a fine episodio mostro la sequenza di caselle visitate'''
    if mostra or reward == 1:
        if reward == 1:
            print ("VITTORIA!")
        print(f"episodio {e}: {sequenza}")

        if mostra and e > 0:
            '''comando che permette di calcolare la media 1000 episodi alla volta'''
            finestra = 1000
            media = np.convolve(totrew[:e], np.ones(finestra) / finestra, mode = 'valid')
            winrate = np.convolve(vittorie[:e], np.ones(finestra) / finestra, mode='valid')

            plt.figure()
            plt.plot(media)
            plt.xlabel('Episodio')
            plt.ylabel('Reward (media mobile su 1000 episodi)')
            plt.title(f'Andamento della reward fino all\'episodio {e}')
            plt.savefig(f'reward_ep{e}.png')
            plt.close()

            plt.figure()
            plt.plot(winrate)
            plt.xlabel('Episodio')
            plt.ylabel('Tasso di vittoria (media mobile su 1000 episodi)')
            plt.title(f'Tasso di vittoria fino all\'episodio {e}')
            plt.ylim(0, 1)
            plt.savefig(f'winrate_ep{e}.png')
            plt.close()

            plt.figure()
            plt.plot(cumwinrate)
            plt.xlabel('Episodio')
            plt.ylabel('Tasso di vittoria cumulativo (vittorie / episodi giocati)')
            plt.title(f'Tasso di vittoria cumulativo fino all\'episodio {e}')
            plt.ylim(0, 1)
            plt.savefig(f'tot_win_ep{e}.png')
            plt.close()

print(w)

        


'''----------sezione----------'''
#

'''CAMBIO DI PARADIGMA:
Invece di aggiornare un dizionario, aggiorno i valori di ciascun numero che si può trovare sulle celle
scoperte; l'azione viene presa sulla base dei valori che circondano la cella scelta.
Non è necessario un cambio drastico dell'algoritmo o delle ausiliarie
maledizione, è un approssimatore lineare.
'''