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
decay = 20 / num_episodes
gamma = 0.9

'''implementazione TD(lambda)'''
l = 3

'''----------inizializzazione dell'ambiente----------'''

from minesweeper_env import MinesweeperEnv
Xenv = 8
Yenv = 8
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
w = np.zeros(18)
# w = np.random.rand(12)

'''----------Algoritmo E-SARSA----------'''

for e in range(num_episodes):

    epsilon = epsilon_min + (epsilon0 - epsilon_min) * np.exp(-decay * e)

    #coda = []

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
    index = np.ravel_multi_index((x0,y0),(Xenv,Yenv))

    '''aggiungo due buffer per E-SARSA(lambda); uno per memorizzare 
    le features dei passi precedenti e uno per memorizzare le reward corrispondenti'''
    buf_x = []
    buf_r = []

    '''----------E-SARSA(lambda) a n passi----------'''

    while not done:

        '''dizionario coordinate:valore'''
        listadict = aux.lista_dict(ambiente)

        '''vettore delle features della cella scelta'''
        features = aux.featuresver2 (ambiente, index, listadict, bombe/len(aux.celle_nascoste(ambiente)), bombe)

        '''aggiornamento del tabellone'''
        _, reward, done = ambiente.step(index)

        if reward == 1:
            vittorie[e] += 1
        totrew[e] += reward
        sequenza.append(ambiente.state[index]['coord'])

        buf_x.append(features)
        buf_r.append(reward)

        if not done:
            ''' celle ancora nascoste'''
            nascoste = aux.celle_nascoste(ambiente)
            quantenascoste = len(nascoste)

            '''informazioni sullo stato successivo'''
            proxlistadict = aux.lista_dict(ambiente)

            '''valore atteso per SARSA(lambda)'''
            # valore_atteso_lambda (ambiente, w, nascoste, proxlistadict, epsilon):
            '''di fatto fa esattamente ciò che faceva
            il codice originale'''
            valoreatteso, indicebestvalue = aux.valore_atteso_lambda(ambiente, w, nascoste, 
                                                                            proxlistadict, epsilon, bombe/quantenascoste, bombe)

            '''aggiornamento dei buffer'''
            if (len(buf_x)== l):
                G = sum(gamma**i * buf_r[i] for i in range(l))
                G+= (gamma**l)*valoreatteso
                valorivecchi = np.dot(w,buf_x[0])
                w += alpha * (G-valorivecchi) * buf_x[0]
                buf_x.pop(0)
                buf_r.pop(0)

            '''logica greedy'''
            if rng.random() < epsilon:
                '''scelta casuale tra le celle ancora nascoste'''
                index = rng.choice(nascoste)
            else:
                '''scelta della cella con il valore atteso più alto'''
                index = indicebestvalue

        else:
            '''termine episodio'''
            while (buf_x):
                lenx = len(buf_x)    
                '''stima della reward cumulativa a 3 passi'''
                G = sum(gamma**i * buf_r[i] for i in range(lenx))
                '''modello attuale'''
                valorivecchi = np.dot(w,buf_x[0])
                '''discesa del gradiente'''
                w += alpha * (G-valorivecchi) * buf_x[0]
                buf_x.pop(0)
                buf_r.pop(0)

    '''RAPPRESENTAZIONE GRAFICA DELL'ANDAMENTO DELL'ALGORITMO'''
    
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
            plt.savefig(f'reward_ep{e}lambda.png')
            plt.close()

            plt.figure()
            plt.plot(winrate)
            plt.xlabel('Episodio')
            plt.ylabel('Tasso di vittoria (media mobile su 1000 episodi)')
            plt.title(f'Tasso di vittoria fino all\'episodio {e}')
            plt.ylim(0, 1)
            plt.savefig(f'winrate_ep{e}lambda.png')
            plt.close()

            plt.figure()
            plt.plot(cumwinrate)
            plt.xlabel('Episodio')
            plt.ylabel('Tasso di vittoria cumulativo (vittorie / episodi giocati)')
            plt.title(f'Tasso di vittoria cumulativo fino all\'episodio {e}')
            plt.ylim(0, 1)
            plt.savefig(f'tot_win_ep{e}lambda.png')
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