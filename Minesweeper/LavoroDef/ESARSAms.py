import random
import numpy as np
import pandas as pd
from collections import defaultdict
rng = np.random.default_rng

'''----------funzioni ausiliarie----------'''
import ausiliarie as aux

'''----------parametri dell'algoritmo E-SARSA----------'''
alpha = 0.01
epsilon = 0.1
gamma = 0.9
num_episodes = 100_000

'''----------inizializzazione dell'ambiente----------'''
from minesweeper_env import MineSweepeerEnv
Xenv = 8
Yenv = 8
bombe = 10
ambiente = MineSweepeerEnv(width = Xenv, height = Yenv, n_mines = bombe)

'''----------Matrice Q----------'''

'''la matrice Q dei valori delle coppie stato-azione viene codificata come un 
dizionario che associa un valore alle features invece che agli stati'''
Q = defaultdict(float)

'''----------Algoritmo E-SARSA----------'''
for e in num_episodes:

    '''in ogni episodio c'è un nuovo tabellone con
    le mine in posizioni casuali'''
    ambiente.reset()
    done = False

    '''----------exploring start----------'''

    '''parto da una cella casuale sul tabellone'''
    x0, y0 = random.randint(0,Xenv-1), random.randint(0,Yenv-1)
    '''esprimo le coordinate come indice lineare'''
    index0 = np.ravel_multi_index((x0,y0),(Xenv,Yenv))

    




'''----------sezione----------'''
#