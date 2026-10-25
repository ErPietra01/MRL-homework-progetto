'''VERSIONE CON DOUBLE Q-LEARNING E AGGIORNAMENTO A N PASSI'''


import random
import numpy as np
rng = np.random.default_rng(42)
import matplotlib.pyplot as plt

'''----------funzioni ausiliarie----------'''

import nDQaux as aux

'''----------parametri dell'algoritmo----------'''

num_episodes = 350_000
alpha0 = 0.015 #primo test con 0.01
alpha_min = 0.0005 # primo test con 0.001
epsilon0 = 0.1 #0.1
epsilon_min = 0.02 #0.01
decay = 50 / num_episodes
gamma = 0.7 
'''test attuale con i parametri presenti; salvare prima di cambiarli'''


# nota: primo test fallimentare dopo 170.000 episodi
'''numero di passi per l'aggiornamento n-step (come l in ESARSAnstepsms.py)'''
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

'''nota: nDQ sembra funzonare meglio su 4x4'''

'''----------conteggi----------'''

totrew = np.zeros(num_episodes)
vittorie = np.zeros(num_episodes)

'''----------pesi----------'''

'''Due vettori dei pesi, come in DQLearningms.py (Double E-SARSA)'''
w1 = np.zeros(19)
w2 = np.zeros(19)

'''----------Algoritmo Double E-SARSA a n passi----------'''

for e in range(num_episodes):

    '''decadimento lineare di epsilon'''
    epsilon = max (epsilon_min, epsilon0 - (epsilon0 - epsilon_min)*e/num_episodes)

    '''decadimento lineare di alpha'''
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
    index = np.ravel_multi_index((x0,y0),(Xenv,Yenv))

    '''buffer per l'aggiornamento a n passi'''
    buf_x = []
    buf_r = []

    '''----------Double E-SARSA a n passi----------'''

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

            '''valore atteso E-SARSA calcolato separatamente per w1 e w2
            tramite funzione dedicata'''
            valoreatteso1, indicebestvaluew1 = aux.valore_atteso_lambda(ambiente, w1, nascoste,
                                                                          proxlistadict, epsilon, bombe/quantenascoste, bombe)
            valoreatteso2, indicebestvaluew2 = aux.valore_atteso_lambda(ambiente, w2, nascoste,
                                                                          proxlistadict, epsilon, bombe/quantenascoste, bombe)

            '''randomizzazione della scelta'''
            usa_w1 = rng.random() < 0.5
            indicebestvalue = indicebestvaluew1 if usa_w1 else indicebestvaluew2

            '''aggiornamento del buffer a n passi con cross-bootstrap Double Q:'''
            if (len(buf_x) == l):
                G = sum(gamma**i * buf_r[i] for i in range(l))
                if usa_w1:
                    G += (gamma**l) * valoreatteso2
                    valorivecchi = np.dot(w1, buf_x[0])
                    w1 += alpha * (G - valorivecchi) * buf_x[0]
                else:
                    G += (gamma**l) * valoreatteso1
                    valorivecchi = np.dot(w2, buf_x[0])
                    w2 += alpha * (G - valorivecchi) * buf_x[0]
                buf_x.pop(0)
                buf_r.pop(0)

            '''logica greedy'''
            if rng.random() < epsilon:
                '''scelta casuale tra le celle ancora nascoste'''
                index = rng.choice(nascoste)
            else:
                index = indicebestvalue

        else:
            '''termine episodio: svuoto il buffer con ritorni a orizzonte
            decrescente e senza bootstrap'''
            while (buf_x):
                lenx = len(buf_x)
                '''stima della reward cumulativa residua'''
                G = sum(gamma**i * buf_r[i] for i in range(lenx))
                if rng.random() < 0.5:
                    valorivecchi = np.dot(w1, buf_x[0])
                    w1 += alpha * (G - valorivecchi) * buf_x[0]
                else:
                    valorivecchi = np.dot(w2, buf_x[0])
                    w2 += alpha * (G - valorivecchi) * buf_x[0]
                buf_x.pop(0)
                buf_r.pop(0)

    '''RAPPRESENTAZIONE GRAFICA DELL'ANDAMENTO DELL'ALGORITMO'''

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
            plt.savefig(f'nDQ_reward_ep{e}.png')
            plt.close()

            plt.figure()
            plt.plot(winrate)
            plt.xlabel('Episodio')
            plt.ylabel('Tasso di vittoria (media mobile su 1000 episodi)')
            plt.title(f'Tasso di vittoria fino all\'episodio {e}')
            plt.ylim(0, 1)
            plt.savefig(f'nDQ_winrate_ep{e}.png')
            plt.close()

            plt.figure()
            plt.plot(cumwinrate)
            plt.xlabel('Episodio')
            plt.ylabel('Tasso di vittoria cumulativo (vittorie / episodi giocati)')
            plt.title(f'Tasso di vittoria cumulativo fino all\'episodio {e}')
            plt.ylim(0, 1)
            plt.savefig(f'nDQ_tot_win_ep{e}.png')
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
