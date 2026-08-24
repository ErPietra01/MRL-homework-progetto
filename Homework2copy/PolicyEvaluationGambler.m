function Vpi = PolicyEvaluationGambler(P, R, pi, gamma)

% numero di stati
S = size(R,1);

% Algoritmo PI: calcolo la matrice di transizione associata ad una azione
% specifica (in pi, inizialmente casuale) e la relativa ricompensa;
% dopodiché calcolo Vpi tramite l'equazione di Bellman compatta

% "strato" del tensore di transizione P nel modello
Ppi = zeros(S,S);

% riga della matrice delle reward (presente anche nel modello ma commentata)
Rpi = zeros(S,1);

% ciclo su tutte le azioni: prendo la reward associata e la matrice di
% transizione per ciascuna azione ammissibile 

for s = 1:S
    Ppi(s,:) = P(s,:,pi(s));
    Rpi(s) = R(s,pi(s));

end

% Algoritmo compatto
% size(eye(S))
% size(Rpi)
% size(Ppi)
Vpi = (eye(S) - gamma*Ppi)\Rpi;

end