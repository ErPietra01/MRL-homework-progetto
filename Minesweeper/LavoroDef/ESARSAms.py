import random
import numpy as np
import pandas as pd
from collections import defaultdict
rng = np.random.default_rng()
import matplotlib.pyplot as plt

'''----------funzioni ausiliarie----------'''

import ausiliarie as aux

'''----------parametri dell'algoritmo E-SARSA----------'''
alpha = 0.01
epsilon = 0.1
gamma = 0.9
num_episodes = 100_000

'''----------inizializzazione dell'ambiente----------'''

from minesweeper_env import MinesweeperEnv
Xenv = 8
Yenv = 8
bombe = 10
ambiente = MinesweeperEnv(width = Xenv, height = Yenv, n_mines = bombe)

'''----------conteggi----------'''

totrew = np.zeros(num_episodes)

'''----------Matrice Q----------'''

'''la matrice Q dei valori delle coppie stato-azione viene codificata come un 
dizionario che associa un valore alle features invece che agli stati'''
Q = defaultdict(float)

'''----------Algoritmo E-SARSA----------'''

for e in range(num_episodes):

    '''rappresentazione grafica dell'andamento dell'algoritmo ogni 10.000 episodi'''
    mostra = (e % 10000 == 0) or (e == num_episodes - 1)
    if mostra:
        sequenza = []

    '''in ogni episodio c'è un nuovo tabellone con
    le mine in posizioni casuali'''
    ambiente.reset()
    done = False

    '''----------exploring start----------'''

    '''parto da una cella casuale sul tabellone'''
    x0, y0 = random.randint(0,Xenv-1), random.randint(0,Yenv-1)
    '''esprimo le coordinate come indice lineare'''
    index0 = np.ravel_multi_index((x0,y0),(Xenv,Yenv))

    '''dizionario coordinate:valore'''
    listadict = aux.lista_dict(ambiente)

    '''features della cella in esame'''
    features = aux.genera_features(ambiente, index0, listadict)

    done = None

    _, reward, done = ambiente.step(index0)
    totrew[e] += reward
    if mostra:
        sequenza.append(ambiente.state[index0]['coord'])

    index = None

    '''ora devo valutare la prima mossa casuale: faccio un passo dell'algoritmo'''

    if done: #ambiente.state[index0]['value'] == 'B':
        '''sconfitta: aggiorno la griglia con step e salvo done = True'''
        Q[features] += alpha * (reward + gamma * 0 - Q[features])

    else:
        '''Il primo passo è andato a buon fine: aggiorno la griglia
        e salvo done = False (ovvero: applico E-SARSA)'''

        '''prendo la lista degli indici delle celle ancora nascoste DOPO l'aggiornamento
        della griglia a seguito di step'''
        nascoste = aux.celle_nascoste(ambiente)

        '''Aggiorno il dizionario coordinate:valore a seguito di step'''
        proxlistadict = aux.lista_dict(ambiente)

        '''----------epsilon greedy----------'''

        if random.random() <= epsilon:
            index = random.choice(nascoste)
        else:

            '''creo una lista dei valori delle prossime celle (per il valore atteso)'''
            prossime = []
            bestvalue = None
            indicebestvalue = None
            for i in nascoste:
                proxfeat = aux.genera_features(ambiente, i, proxlistadict)
                valorefeat = Q.get(proxfeat,0.0)
                prossime.append(valorefeat)
                if bestvalue is None or valorefeat > bestvalue:
                    bestvalue = valorefeat
                    indicebestvalue = i


            valoreatteso = (1-epsilon) * bestvalue + epsilon* (sum (prossime) / len (prossime))
            Q[features] += alpha * (reward + gamma * valoreatteso - Q[features])
            index = indicebestvalue
            #index = nascoste[listadict[max(Q[features])]]


    '''----------E-SARSA----------'''

    while not done:
        
        listadict = aux.lista_dict(ambiente)

        '''features della cella in esame'''
        features = aux.genera_features(ambiente, index, listadict)

        _, reward, done = ambiente.step(index)
        totrew[e] += reward
        if mostra:
            sequenza.append(ambiente.state[index]['coord'])


        '''Iterazione epsilon-greedy'''

        if done: #ambiente.state[index0]['value'] == 'B':
            '''sconfitta: aggiorno la griglia con step e salvo done = True'''
            Q[features] += alpha * (reward + gamma * 0 - Q[features])

        else:
            '''Il passo è andato a buon fine: aggiorno la griglia
            e salvo done = False (ovvero: applico E-SARSA)'''

            '''prendo la lista degli indici delle celle ancora nascoste DOPO l'aggiornamento
            della griglia a seguito di step'''
            nascoste = aux.celle_nascoste(ambiente)

            '''Aggiorno il dizionario coordinate:valore a seguito di step'''
            proxlistadict = aux.lista_dict(ambiente)

            '''epsilon greedy'''
            if random.random() <= epsilon:
                index = random.choice(nascoste)
            else:

                '''creo una lista dei valori delle prossime celle (per il valore atteso)'''
                prossime = []
                bestvalue = None
                indicebestvalue = None
                for i in nascoste:
                    proxfeat = aux.genera_features(ambiente, i, proxlistadict)
                    valorefeat = Q.get(proxfeat,0.0)
                    prossime.append(valorefeat)
                    if bestvalue is None or valorefeat > bestvalue:
                        bestvalue = valorefeat
                        indicebestvalue = i


                valoreatteso = (1-epsilon) * bestvalue + epsilon* (sum (prossime) / len (prossime))
                Q[features] += alpha * (reward + gamma * valoreatteso - Q[features])
                index = indicebestvalue

            # del proxlistadict (non libera memoria, anzi è potenzialmente dannoso)
        
    '''a fine episodio mostro la sequenza di caselle visitate'''
    if mostra:
        print(f"episodio {e}: {sequenza}")

        if mostra and e > 0:
            '''comando che permette di calcolare la media 1000 episodi alla volta'''
            finestra = 1000
            media = np.convolve(totrew[:e], np.ones(finestra) / finestra, mode = 'valid')

            plt.figure()
            plt.plot(media)
            plt.xlabel('Episodio')
            plt.ylabel('Reward (media mobile su 1000 episodi)')
            plt.title(f'Andamento della reward fino all\'episodio {e}')
            plt.savefig(f'reward_ep{e}.png')
            plt.close()



'''----------sezione----------'''
#