clear all
close all
clc

% upper confidence bound: seleziono le azioni non greedy in base a quante
% volte le ho provate in precedenza

% nell'ordine: spazio delle azioni, spazio delle azioni dell'avversario, e
% numero di iterazioni
A = 5; 
mosse = 5;
exlen = 1e6;

rng(1);

actions = zeros(1,exlen);
rewards = zeros(1, exlen);

actionnumber = zeros (A, exlen);
actionvalues = zeros (A, exlen);
actionvalues(:,1) = 0*ones(A,1);

% vettore che tiene conto dell'azione dell'avversario
advactions = zeros(mosse,exlen);

epsilon = 0.1;
c = 100;

% algoritmo
for t = 2:exlen

    % MOSSA DELL'AVVERSARIO
    % l'avversario fa una mossa casuale 
    mossa = randi(mosse);
    % l'avversario fa una mossa deterministica
    %mossa = 5;
    % l'avversario fa una mossa secondo una distribuzione gaussiana
    % x = 1:5;
    % mu = 3;
    % sigma = 1;
    % pesi = exp(-(x - mu).^2 / (2 * sigma^2));
    % prob = pesi / sum(pesi);
    % mossa = randsample(x, 1, true, prob);

    advactions(:, t) = advactions(:,t-1);
    advactions (mossa, t) = advactions (mossa, t) + 1;

    % calcolo il vettore dei valori in base al numero di volte in cui la
    % specifica azione è stata presa
    q = actionvalues(:,t-1) + c*(sqrt(log(t-1)./ (actionnumber(:,t-1) + 1)));
    greedy = find(q == max(q));

    a = greedy(randi(length(greedy)));

    actions(t) = a;

    %calcolo la reward
    r = HW1(mossa, a);
    rewards(t) = r;

    actionnumber(:,t) = actionnumber(:,t-1);
    actionnumber(a,t) = actionnumber(a,t-1) + 1;

    actionvalues(:,t) = actionvalues(:,t-1);
    % aggiornamento del valore delle azioni: uso uno stepsize variabile
    % oppure costante
    stepsize = 1/actionnumber(a,t);
    %stepsize = 0.01;
    error = r - actionvalues(a,t);
    actionvalues(a,t) = actionvalues(a,t-1) + stepsize*(error);


end

figure(1)
tiledlayout(3,1,"TileSpacing","compact")

ax1 = nexttile();
plot(actionnumber')
legend('1','2','3','4','5')

ax3 = nexttile();
plot(actionvalues')
legend('1','2','3','4','5')

ax4 = nexttile();
plot(cumsum(rewards))

figure(2)
tiledlayout(3,1,"TileSpacing","compact")
ax1 = nexttile();
plot(advactions')
legend('1','2','3','4','5')
