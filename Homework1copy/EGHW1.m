clear all
close all
clc

rng(1);

% nell'ordine: spazio delle azioni, spazio delle azioni dell'avversario, e
% numero di iterazioni
A = 5; 
mosse = 5;
exlen = 1e3;

actions = zeros(1,exlen);
rewards = zeros(1, exlen);

actionnumber = zeros (A, exlen);
actionvalues = zeros (A, exlen);
actionvalues(:,1) = 0*ones(A,1);

% vettore che tiene conto dell'azione dell'avversario
advactions = zeros(mosse,exlen);

epsilon = 0.1;

% iterazioni della policy epsilon greedy

for t = 2:exlen
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

    %l'avversario sceglie 2 (carta) se t è pari, 5 altrimenti
    % c = mod((t-1),2);
    % if c == 0
    %     mossa = 2;
    % else 
    %     mossa = 5;
    % end
    % disp(mossa)

    advactions(:, t) = advactions(:,t-1);
    advactions (mossa, t) = advactions (mossa, t) + 1;

    if rand < epsilon
        a = randi(A);
    else
        % se scelgo l'azione greedy, cerco l'azione che corrisponde al
        % valore massimo nella colonna t-1; per rompere l'eventuale parità,
        % scelgo un valore massimo a caso
        greedy = find(actionvalues(:,t-1) == max (actionvalues(:,t-1)));
        a = greedy(randi(length(greedy)));
    end

    actions (t) = a; 
    r = HW1 (mossa, a);
    rewards(t) = r;

    actionnumber(:,t) = actionnumber(:,t-1);
    actionvalues(:,t) = actionvalues(:,t-1);

    actionnumber(a,t) = actionnumber(a,t) + 1;

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

%% OSSERVAZIONI
% azione avversaria randomica: 
% L'algoritmo non impara a rispondere alla mossa dell'avversario poiché
% questa è randomica; dopo un numero di iterazioni, utilizzerà una azione
% specifica per tutto il resto dell'esperimento.
% con uno stepsize costante, si osserva che due azioni saranno prese più
% spesso delle altre.

% azione avversaria deterministica:
% L'algoritmo apprende immediatamente la mossa corretta per rispondere alla
% mossa dell'avversario.