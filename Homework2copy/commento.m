% GAMBLER'S PROBLEM
% Il problema consiste nel fare una scommessa sull'esito del lancio di una
% moneta, avendo a disposizione un capitale s iniziale e volendo arrivare a
% 100. se possiedo s e punto "a"
% dollari, se vinco il mio capitale sarà s+a, altrimenti avrò s-a. Ho una
% reward r=1 se arrivo a 100 e r=-1 se arrivo a 0; in tutti gli altri casi,
% r=0. 

% IMPLEMENTAZIONE
% per prima cosa bisogna definire un modello per il problema, in cui siano
% introdotte le variabili e le matrici di transizione; queste ultime devono
% essere definite in base alla distribuzione di probabilità, perciò a
% seconda degli esiti del lancio di monete posso andare in uno stato con un
% capitale maggiore o minore. Devo anche impedire che la potenziale vincita
% sia superiore a 100 e che la potenziale perdita sia inferiore a 0.

% La difficoltà maggiore risiede nel fatto che a ogni lancio, cambia la
% matrice di transizione: avrò un nuovo capitale e due nuovi possibili
% esiti, mentre tutti gli altri avranno probabilità nulla

% La policy sarà un vettore che mapperà l'azione migliore in base allo
% stato corrente: dovrà essere aggiornata a ogni iterazione

% come costruisco la matrice di transizione in base alle azioni?
% sweep sugli stati e sulle azioni (vincolate allo stato corrente); dovrei
% ottenere un tensore: P(S1,S2,A), in cui S1 è lo stato corrente, A è
% l'azione che prendo, e S2 è lo stato in cui finisco
% dovrebbe essere quindi costruito nel seguente modo:
% ogni strato è una matrice SxS in cui, per ogni riga a, ho gli stati in
% cui finisco se esce testa o se esce croce, tenendo conto del vincolo
% sulle possibili puntate.

% actionmask: utile per l'implementazione degli algoritmi; assegna un
% valore -inf invece di 0 alle azioni illegali, impedendo che possano
% essere scelte.