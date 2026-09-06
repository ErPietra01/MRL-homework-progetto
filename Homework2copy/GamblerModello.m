clear all
close all
clc

% obiettivo
goal = 100;

% guadagno/perdita
gain = 1;
lose = -1;

% fattore di sconto per l'equazione di Bellman
% Nota: sul Sutton il fattore di sconto dovrebbe essere 1, perché
% altrimenti il gambler sarebbe portato a fare scommesse più grandi e
% rischiose al diminuire della reward nel tempo, ma così facendo il policy
% evaluation fornisce una matrice singolare per V. Ho messo un gamma molto
% prossimo a 1 per evitare questo problema senza alterare
% significativamente il risultato.
gamma = 0.9;

% vettore del capitale: tutti i possibili capitali (vettore dei numeri da
% 0 a 100)
capitale = 0:goal;

% Definiamo ora lo spazio degli stati e delle azioni
% Stato: capitale attualmente disponibile (S1 = 0, S101 = 100)
S = 101;
% Azione: limitata dallo stato corrente, in quanto posso solo scommettere
% una quantità minore del capitale disponibile
A = 100;


% distribuzione di probabilità (lancio di moneta)
heads = 0.6;
tails = 1-heads;
% dovrei fare in modo che tutti gli esiti ammissibili siano equiprobabili 


% Matrice di transizione: mappa la transizione da uno stato ad un altro in
% base all'azione scelta
P = zeros(S,S,A);

%  popolare la matrice di transizione
for s = 2:S-1
    % ciclo su tutti gli stati
    capitale = s - 1; 
    % fondi disponibili allo stato s tenendo conto dei vincoli (in ciascuno
    % stato ho a disposizione un capitale minore di s)

    % L'azione a va da 1 fino al minimo tra il capitale posseduto
    % e ciò che manca per arrivare a 100
    maxa = min(capitale, 100 - capitale);

    for a = 1:maxa
        % per ciascuna azione, partendo da ciascuno stato, definisco gli
        % stati di arrivo
        win = (capitale + a) + 1;
        loss = (capitale - a) + 1;

        % Assegno la probabilità di finire in uno stato s' partendo da s e
        % compiendo l'azione a ammissibile
        P(s, win, a) = heads;
        P(s, loss, a) = tails;
        % con queste due righe di codice, sto dicendo che, se parto da s e
        % compio l'azione a, con probabilità heads finisco nello stato win
        % e con probabilità tails finisco nello stato loss
    end
    
end
% nello stato in cui si vince (s = 100) o si perde (s = 0) l'agente rimane
% nello stato con probabilità 1
P(1,1,:) = 1;
P(S,S,:) = 1;
%disp(P(:,:,1))
% se ho zero capitale oppure ho raggiunto l'obiettivo, non faccio
% transizioni



% versione più semplice di R secondo la formula presente nelle slide
R = zeros(S,A);
for s = 1:S
    for a = 1:A
        vittoria = P(s,S,a);
        sconfitta = P(s,1,a);
        R(s,a) = vittoria*gain + sconfitta*lose;
    end
end

% stato-azione illegali in modo tale che non possano essere scelte negli
% algoritmi
% Nota: è inutile
% actionmask = -inf(S,A);
% for s = 2:S-1
%     capitale = s - 1;
%     maxa = min(capitale, 100 - capitale);
%     actionmask(s, 1:maxa) = 0; 
% end
% 
% actionmask(1, 1) = 0;
% actionmask(S, 1) = 0;

%%
% nomefilefile.mat: salva tutte le matrici, le variabilie gli array 
% in memoria, in modo tale che siano istantaneamente accessibili da altri 
% file
save GamblerModello.mat P R heads tails  gamma

%