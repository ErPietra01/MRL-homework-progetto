clear all
close all
clc

rng(2);

load GamblerModello.mat

% soglia del value iteration
theta = 0.9;

S = size(R,1);
A = size(R,2);

% valore iniziale random
V = randn(S,1);

i = 0;

while true
    i = i+1;

    Delta = 0;
    for s = 1:S
        % valuto qualsiasi azione in ciascuno stato
        q = zeros(A,1);
        for a = 1:A
            q(a) = R(s,a) + gamma*P(s,:,a)*V;
        end
        % Il nuovo valore è calcolato dalla funzione qualità
        Vp = max(q);
        %Delta rimane zero finché
        Delta = max([Delta, Vp - V(s)]);

        % aggiornamento della stima
        V(s) = Vp;
    end

    % criterio di stop
    if Delta < theta
        break;
    end
   disp([i,Delta]);
end

pi = PolicyImprovementGambler(P,R,V,gamma);

disp(V)

save vstarVI.mat V

% questo non converge...