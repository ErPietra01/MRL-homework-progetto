'''VERSIONE CON DOUBLE Q-LEARNING'''

import random
from matplotlib.pylab import rand
import numpy as np
# import pandas as pd
# from collections import defaultdict
rng = np.random.default_rng(42)
import matplotlib.pyplot as plt

'''----------funzioni ausiliarie----------'''

'''nota: le feature in ausiliarie2 partono peggio ma arrivano agli stessi 
risultati con meno oscillazioni'''
import ausiliarie2 as aux

'''----------parametri dell'algoritmo E-SARSA----------'''

''' NOTA IMPORTANTE: QUESTI SONO I PARAMETRI MIGLIORI FINORA;
    PRIMA DI MODIFICARLI, BISOGNA COMMENTARLI PER POTERLI RIPRISTINARE'''

num_episodes = 250_000
#alpha = 0.001
alpha0 = 0.01 #test con alpha decrescente
alpha_min = 0.0005
#epsilon = 0.1 # epsilon decrescente migliora la convergenza!
epsilon0 = 0.1
epsilon_min = 0.01
decay = 50 / num_episodes #20
gamma = 0.7 #0.9, rimettere 0.7

# nota: sembrerebbe che alpha decrescente abbia un tasso di crescita più rapido ma che tende
# a rallentare, ma la reward è leggermente più alta

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


'''Vettore dei valori dei numeri sulle celle (U, 0-8); questa è la struttura che verrà aggiornata
ad ogni passo.
Stiamo sostanzialmente creando un approssimatore lineare aggiornato tramite E-SARSA!
Con Double-Q espandiamo a due vettori ma l'algoritmo è molto simile'''
w1 = np.zeros(19)
w2 = np.zeros(19)


'''----------Algoritmo E-SARSA----------'''

for e in range(num_episodes):

    '''decadimento lineare: dovrebbe migliorare l'apprendimento'''
    epsilon = max (epsilon_min, epsilon0 - (epsilon0 - epsilon_min)*e/num_episodes)

    '''decadimento esponenziale: l'algoritmo ha smesso di esplorare quasi subito'''
    #epsilon = epsilon_min + (epsilon0 - epsilon_min) * np.exp(-decay * e)

    '''decadimento lineare di alpha per velocizzare l'apprendimento'''
    alpha = max (alpha_min, alpha0 - (alpha0 - alpha_min)*e/num_episodes)


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

    nascoste0 = aux.celle_nascoste(ambiente)
    quantenascoste0 = len(nascoste0)

    '''features calcolate con il metodo nuovo (usiamo la notazione della regressione lineare)'''
    x = aux.featuresver2 (ambiente, index0, listadict, bombe/quantenascoste0, bombe)

    done = None

    _, reward, done = ambiente.step(index0)
    totrew[e] += reward
    sequenza.append(ambiente.state[index0]['coord'])

    index = None

    '''ora devo valutare la prima mossa casuale: faccio un passo dell'algoritmo'''

    if done:

        Q1 = np.dot(w1,x)
        Q2 = np.dot(w2,x)
        if rng.random() < 0.5:
            w1 += alpha *(reward + gamma * 0 - Q1) * x
        else:
            w2 += alpha *(reward + gamma * 0 - Q2) * x

    else:
        '''Il primo passo è andato a buon fine: aggiorno la griglia
        e salvo done = False (ovvero: applico E-SARSA)'''

        '''prendo la lista degli indici delle celle ancora nascoste DOPO l'aggiornamento
        della griglia a seguito di step'''
        nascoste = aux.celle_nascoste(ambiente)
        quantenascoste = len(nascoste)

        '''Aggiorno il dizionario coordinate:valore a seguito di step'''
        proxlistadict = aux.lista_dict(ambiente)

        '''----------epsilon greedy----------'''

        '''creo una lista dei valori delle prossime celle (per il valore atteso)'''
        '''DQLearning: calcolo 2 valori attesi'''

        prossimew1 = []
        bestvaluew1 = None
        indicebestvaluew1 = None
    
        prossimew2 = []
        bestvaluew2 = None
        indicebestvaluew2 = None
        for i in nascoste:
            '''i è l'indice (azione)'''
            x_next = aux.featuresver2 (ambiente, i, proxlistadict, bombe/quantenascoste, bombe)
                
            valorefeat1 = np.dot(w1,x_next)
            prossimew1.append(valorefeat1)
            if bestvaluew1 is None or valorefeat1 > bestvaluew1:
                bestvaluew1 = valorefeat1
                indicebestvaluew1 = i
    
            valorefeatw2 = np.dot(w2,x_next)
            prossimew2.append(valorefeatw2)
            if bestvaluew2 is None or valorefeatw2 > bestvaluew2:
                bestvaluew2 = valorefeatw2
                indicebestvaluew2 = i
                
        valoreatteso1 = (1-epsilon) * bestvaluew1 + epsilon* (sum (prossimew1) / len (prossimew1))
        valoreatteso2 = (1-epsilon) * bestvaluew2 + epsilon* (sum (prossimew2) / len (prossimew2))

        indicebestvalue = None
        Q1 = np.dot (w1,x)
        Q2 = np.dot (w2,x)
        if rng.random() < 0.5:
            w1 += alpha * (reward + gamma * valoreatteso2 - Q1) * x
            indicebestvalue = indicebestvaluew1
        else:
            w2 += alpha * (reward + gamma * valoreatteso1 - Q2) * x
            indicebestvalue = indicebestvaluew2

        if rng.random() <= epsilon:
            index = rng.choice(nascoste)
        else:
            index = indicebestvalue


    '''----------E-SARSA----------'''

    while not done:
        
        listadict = aux.lista_dict(ambiente)

        nascoste = aux.celle_nascoste(ambiente)
        quantenascoste = len(nascoste)

        x = aux.featuresver2 (ambiente, index, listadict, bombe/quantenascoste, bombe)
        Q1 = np.dot(w1,x)
        Q2 = np.dot(w2,x)

        _, reward, done = ambiente.step(index)

        if reward == 1:
             vittorie[e] = 1
        
        totrew[e] += reward
        sequenza.append(ambiente.state[index]['coord'])


        '''Iterazione epsilon-greedy'''

        if done:
            if rng.random() < 0.5:
                w1 += alpha * (reward + gamma * 0 - Q1) * x
            else:
                w2 += alpha * (reward + gamma * 0 - Q2) * x

        else:
            '''Il passo è andato a buon fine: aggiorno la griglia
            e salvo done = False (ovvero: applico E-SARSA)'''

            '''prendo la lista degli indici delle celle ancora nascoste DOPO l'aggiornamento
            della griglia a seguito di step'''
            nascoste = aux.celle_nascoste(ambiente)

        

            quantenascoste = len(nascoste)

            '''Aggiorno il dizionario coordinate:valore a seguito di step'''
            proxlistadict = aux.lista_dict(ambiente)


            '''creo una lista dei valori delle prossime celle (per il valore atteso)'''
            prossimew1 = []
            bestvaluew1 = None
            indicebestvaluew1 = None

            prossimew2 = []
            bestvaluew2 = None
            indicebestvaluew2 = None
            for i in nascoste:
                '''i è l'indice (azione)'''
                x_next = aux.featuresver2 (ambiente, i, proxlistadict, bombe/quantenascoste, bombe)
            
                valorefeat1 = np.dot(w1,x_next)
                prossimew1.append(valorefeat1)
                if bestvaluew1 is None or valorefeat1 > bestvaluew1:
                    bestvaluew1 = valorefeat1
                    indicebestvaluew1 = i

                valorefeatw2 = np.dot(w2,x_next)
                prossimew2.append(valorefeatw2)
                if bestvaluew2 is None or valorefeatw2 > bestvaluew2:
                    bestvaluew2 = valorefeatw2
                    indicebestvaluew2 = i
            
            valoreatteso1 = (1-epsilon) * bestvaluew1 + epsilon* (sum (prossimew1) / len (prossimew1))
            valoreatteso2 = (1-epsilon) * bestvaluew2 + epsilon* (sum (prossimew2) / len (prossimew2))


            indicebestvalue = None
            Q1 = np.dot (w1,x)
            Q2 = np.dot (w2,x)
            if rng.random() < 0.5:
                w1 += alpha * (reward + gamma * valoreatteso2 - Q1) * x
                indicebestvalue = indicebestvaluew1
            else:
                w2 += alpha * (reward + gamma * valoreatteso1 - Q2) * x
                indicebestvalue = indicebestvaluew2

            '''epsilon greedy'''
            if rng.random() <= epsilon:
                index = rng.choice(nascoste)
            else:
                index = indicebestvalue


    
    '''aggiunto il dato sul winrate cumulativo e non solo la media su 1000 episodi'''

    '''a fine episodio mostro la sequenza di caselle visitate'''
    if mostra or reward == 1:         
        if reward == 1:
            print ("VITTORIA!")
        print(f"episodio {e}: {sequenza}")

        if mostra and e > 0:

            '''aggiunto il dato sul winrate cumulativo e non solo la media su 1000 episodi'''
            totwin = np.cumsum(vittorie[:e])
            totepisodes = np.arange(1,e+1)
            cumwinrate = totwin/totepisodes

            '''comando che permette di calcolare la media 1000 episodi alla volta'''
            finestra = 1000
            media = np.convolve(totrew[:e], np.ones(finestra) / finestra, mode = 'valid')
            winrate = np.convolve(vittorie[:e], np.ones(finestra) / finestra, mode='valid')

            plt.figure()
            plt.plot(media)
            plt.xlabel('Episodio')
            plt.ylabel('Reward (media mobile su 1000 episodi)')
            plt.title(f'Andamento della reward fino all\'episodio {e}')
            plt.savefig(f'DQ_reward_ep{e}.png')
            plt.close()

            plt.figure()
            plt.plot(winrate)
            plt.xlabel('Episodio')
            plt.ylabel('Tasso di vittoria (media mobile su 1000 episodi)')
            plt.title(f'Tasso di vittoria fino all\'episodio {e}')
            plt.ylim(0, 1)
            plt.savefig(f'DQ_winrate_ep{e}.png')
            plt.close()

            plt.figure()
            plt.plot(cumwinrate)
            plt.xlabel('Episodio')
            plt.ylabel('Tasso di vittoria cumulativo (vittorie / episodi giocati)')
            plt.title(f'Tasso di vittoria cumulativo fino all\'episodio {e}')
            plt.ylim(0, 1)
            plt.savefig(f'DQ_tot_win_ep{e}.png')
            plt.close()

print(w1)
print(w2)

        


'''----------sezione----------'''
#

'''CAMBIO DI PARADIGMA:
Invece di aggiornare un dizionario, aggiorno i valori di ciascun numero che si può trovare sulle celle
scoperte; l'azione viene presa sulla base dei valori che circondano la cella scelta.
Non è necessario un cambio drastico dell'algoritmo o delle ausiliarie
maledizione, è un approssimatore lineare.
'''