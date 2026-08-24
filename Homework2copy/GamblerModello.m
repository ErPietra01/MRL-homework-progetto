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
gamma = 0.9999;

% vettore del capitale: tutti i possibili capitali
capitale = 0:goal;

% Stato: capitale attualmente disponibile (S1 = 0, S101 = 100)
S = 101;
% Azione: limitata dallo stato corrente, in quanto posso solo scommettere
% una quantità minore del capitale disponibile
A = 100;


% distribuzione di probabilità (lancio di moneta)
heads = 0.6;
tails = 1-heads;
% dovrei fare in modo che tutti gli esiti ammissibili siano equiprobabili 


% Matrice delle ricompense (VERSIONE VECCHIA): 
% a ogni coppia stato-azione associa una
% ricompensa attesa (1 se vado in 100, -1 se vado in 0, 0 altrimenti)
% R = zeros(S,A);
% 
% for s = 2:S-1
%     capitale = s-1;
%     maxa = min(capitale, 100-capitale);
%     for a = 1:maxa
%         er = 0; 
%         if (capitale + a) == 100
%             er = er + (1*heads);
%         end
%         if (capitale - a) == 0
%             er = er + (-1*tails);
%         end
%         % aggiorno le reward dei soli stati che mi portano in uno stato
%         % terminale tramite una azione a
%         R (s,a) = er;
%     end
% end

%disp(R);


% Matrice di transizione: 
P = zeros(S,S,A);

for s = 2:S-1
    % ciclo su tutti gli stati
    capitale = s - 1; 
    % fondi disponibili allo stato s tenendo conto dei vincoli

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
    end
    
end
P(1,1,:) = 1;
P(S,S,:) = 1;
%disp(P(:,:,1))

% versione più semplice di R secondo la formula
R = zeros(S,A);
for s = 1:S
    for a = 1:A
        R(s,a) = P(s,S,a)*1 + P(s,1,a)*(-1);
    end
end

% Maschera delle azioni: assegna un valore -inf a tutte le coppie
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
save GamblerModello.mat P R heads tails  gamma % actionmask