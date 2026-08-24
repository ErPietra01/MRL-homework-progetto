clear all
close all
clc

% Algoritmo che seleziona l'azione in base alle preferenze: a ogni
% iterazione, verrà modificata la probabilità di scegliere una azione in
% base al suo successo nelle passate iterazioni

rng(1);

% nell'ordine: spazio delle azioni, spazio delle azioni dell'avversario, e
% numero di iterazioni
A = 5; 
mosse = 5;
exlen = 1e6;

actions = zeros(1,exlen);
rewards = zeros(1, exlen);

actionnumber = zeros (A, exlen);
actionvalues = zeros (A, exlen);
actionvalues(:,1) = 0*ones(A,1);

% vettore che tiene conto dell'azione dell'avversario
advactions = zeros(mosse,exlen);

% matrice delle preferenze (inizializzato a 1 per stima ottimistica)
pref = ones(A,exlen);

alpha = 0.01;

%reward media (da aggiornare a ogni iterazione)
meanrew = 0;

% algoritmo 
for t = 2:exlen

    % MOSSA DELL'AVVERSARIO
    % l'avversario fa una mossa casuale 
    mossa = randi(mosse);
    % l'avversario fa una mossa deterministica
    % mossa = 5;
    % l'avversario fa una mossa secondo una distribuzione gaussiana
    % x = 1:5;
    % mu = 3;
    % sigma = 1;
    % pesi = exp(-(x - mu).^2 / (2 * sigma^2));
    % prob = pesi / sum(pesi);
    % mossa = randsample(x, 1, true, prob);

    advactions(:, t) = advactions(:,t-1);
    advactions (mossa, t) = advactions (mossa, t) + 1;

    % per prima cosa, calcolo l'azione più probabile in base alla
    % distribuzione soft-max
    % considero la colonna delle preferenze al tempo t
    H = pref(:,t-1);
    pi = (exp(H))/(sum(exp(H)));
    
    % tramite probs ho calcolato, per ogni azione, la probabilità che essa
    % venga presa, in base al vettore di preferenze H al tempo t. Con
    % cumsum invece costruisco un vettore con la distribuzione di
    % probabilità invece della probabilità singola. la randomizzazione
    % favorisce l'esplorazione: aggiornando H so qual è l'azione migliore,
    % ma con un certo grado di esplorazione valuto anche le altre opzioni.
    probs = cumsum(pi);
    a = find(probs >= rand, 1, 'first');
    actions(t) = a;

    r = HW1(mossa, a);
    rewards(t) = r; 

    % aggiornamento della reward media
    meanrew = meanrew + 1/t* (r - meanrew);

    % Algoritmo per l'aggiornamento delle preferenze
    for act = 1:A
        if act == a
            pref(act, t) = pref(act, t-1) + alpha*(r-meanrew)*(1-pi(act));
        else
            pref(act, t) = pref(act, t-1) - alpha*(r-meanrew)*pi(act);
        end %if act == a
    end % algoritmo preferenze

    actionnumber(:,t) = actionnumber(:,t-1);
    actionnumber(a,t) = actionnumber(a,t-1) + 1;

end

figure(1)
tiledlayout(3,1,"TileSpacing","compact")

ax1 = nexttile();
plot(actionnumber')
legend('1','2','3','4','5')

ax3 = nexttile();
plot(cumsum(rewards))

figure(2)
tiledlayout(3,1,"TileSpacing","compact")
ax1 = nexttile();
plot(advactions')
legend('1','2','3','4','5')
