clear all
close all
clc

%% VERSIONE A 2 GIOCATORI
% in questo script metterò 2 bot a giocare l'uno contro l'altro. Entrambi
% dovranno provare a prevedere le mosse dell'avversario, partendo da una
% "mossa" iniziale con
% cui far partire l'algoritmo. userò il metodo Epsilon-Greedy in quanto è
% il più semplice da implementare
% l'azione scelta dal primo giocatore sarà quella che il secondo dovrà
% contrastare; è quindi necessario che il primo giocatore abbia una azione
% jolly per partire 

rng(1);

% nell'ordine: spazio delle azioni, spazio delle azioni dell'avversario, e
% numero di iterazioni
A = 5; 
mosse = 5;
exlen = 1e3;

% giocatore 1:
actions1 = zeros(1,exlen);
rewards1 = zeros(1, exlen);

actionnumber1 = zeros (A, exlen);
actionvalues1 = zeros (A, exlen);
actionvalues1(:,1) = 0*ones(A,1);

% azione dell'avversario (G2)
adv1 = 0;

% giocatore 2:
actions2 = zeros(1,exlen);
rewards2 = zeros(1, exlen);

actionnumber2 = zeros (A, exlen);
actionvalues2 = zeros (A, exlen);
actionvalues2(:,1) = 0*ones(A,1);

% azione dell'avversario (G1)
adv2 = 0;

epsilon = 0.1;

% Il giocatore 1 parte in base a una azione casuale
astart = randi(5);

% algoritmo
for t = 2:exlen
    
    % ---- GIOCATORE 1 ----%

    % all'inizio devo usare l'azione jolly
    if t == 2
        adv1 = astart;
    else
        adv1 = actions2(t-1);
    end

    % Ora implemento l'algoritmo per il giocatore 1
    if (rand < epsilon)
        a1 = randi(A);
    else
        greedy1 = find(actionvalues1(:,t-1) == max (actionvalues1(:,t-1)));
        a1 = greedy1(randi(length(greedy1)));
    end

    actions1(t) = a1;

    r1 = HW1(adv1,a1);
    rewards1(t) = r1;

    actionnumber1(:,t) = actionnumber1(:,t-1);
    actionvalues1(:,t) = actionvalues1(:,t-1);

    actionnumber1(a1,t) = actionnumber1(a1,t) + 1;

    % aggiornamento del valore delle azioni: uso uno stepsize variabile
    % oppure costante
    stepsize1 = 1/actionnumber1(a1,t);
    %stepsize = 0.01;
    error1 = r1 - actionvalues1(a1,t);
    actionvalues1(a1,t) = actionvalues1(a1,t-1) + stepsize1*(error1);


    % ---- GIOCATORE 2 ----%

    adv2 = actions1(t);
    %adv2 = actions1((t-1));

    % Ora implemento l'algoritmo per il giocatore 1
    if (rand < epsilon)
        a2 = randi(A);
    else
        greedy2 = find(actionvalues2(:,t-1) == max (actionvalues2(:,t-1)));
        a2 = greedy2(randi(length(greedy2)));
    end

    actions2(t) = a2;

    r2 = HW1(adv2,a2);
    rewards2(t) = r2;

    actionnumber2(:,t) = actionnumber2(:,t-1);
    actionvalues2(:,t) = actionvalues2(:,t-1);

    actionnumber2(a2,t) = actionnumber2(a2,t) + 1;

    % aggiornamento del valore delle azioni: uso uno stepsize variabile
    % oppure costante
    stepsize2 = 1/actionnumber2(a2,t);
    %stepsize = 0.01;
    error2 = r2 - actionvalues2(a2,t);
    actionvalues2(a2,t) = actionvalues2(a2,t-1) + stepsize2*(error2);


end

figure(1)
tiledlayout(3,1,"TileSpacing","compact")

ax1 = nexttile();
plot(actionnumber1')
legend('1','2','3','4','5')

ax2 = nexttile();
plot(actionvalues1')
legend('1','2','3','4','5')

ax3 = nexttile();
plot(cumsum(rewards1))

figure(2)
tiledlayout(3,1,"TileSpacing","compact")

ax1 = nexttile();
plot(actionnumber2')
legend('1','2','3','4','5')

ax2 = nexttile();
plot(actionvalues2')
legend('1','2','3','4','5')

ax3 = nexttile();
plot(cumsum(rewards2))

%% OSSERVAZIONI
% ciascun giocatore riceve sempre la mossa PRECEDENTE dell'avversario,
% perciò entrambi imparano a vincere quasi subito perché in poche
% iterazioni il gioco diventa deterministico! Infatti nessuno dei due
% giocatori è portato a cambiare la propria strategia, poiché il G1 ha
% imparato che, il G2 sceglierà sempre 5, a cui risponderà con 3, viceversa
% per il G2.
% se invece il giocatore 2 ha come mossa dell'avversario la mossa scelta
% all'istante corrente, il risultato è infine lo stesso, ma entrambi i
% giocatori impiegano molto più tempo a raggiungere un equilibrio.