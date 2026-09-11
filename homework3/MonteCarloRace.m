clear all
close all
clc

% accesso alla griglia
load CircuitoMonteCarlo.mat % gridsize, grid

% Ho due azioni simultanee
a1 = [-1,0,1]; % accelerazioni (1=avanti, 0=fermo, -1=indietro)
l1 = length(a1);
a2 = [-1,0,1];
l2 = length(a2);
% RAPPRESENTAZIONE DEL PERCORSO
% disp(grid);
% fprintf("dimensione griglia: %d",gridsize);

% for i = 1:numel(grid)
%     if grid(i) == 1;
%         fprintf ("elemento in posizione %d \n", i);
%     end
% end

% spazio degli stati: indice della posizione sulla griglia
S = numel(grid); 

% matrice Q: tensore che associa a ogni posizione sulla griglia
% il valore delle tre possibili accelerazioni
Q = zeros(S,l1,l2);

% policy: assegna a ciascuno stato (righe) due valori per le azioni
policy = randi([-1,1], [S,2]);

% inizializzo i valori degli stati
valinit = -ones(S, 1);

minvisits = 500;
epsilon = 0.1;
gamma = 1;
stepsize = 1e-3;
tolerance = 8e-2;

% accesso all'indice sulla griglia di partenza
% s0 = sub2ind([gridsize,gridsize],gridsize,randi(6))

% ALGORITMO MONTE CARLO

while true

    % Aggiorno il numero di volte che la tripla
    % stato s, azione a1 e azione a2 è stata visitata
    N = zeros(S,l1,l2);

    while min (N(:)) < minvisits
        % episodio iniziale casuale: prendo un indice s0 sulla
        % linea di partenza e due azioni a10, a20 casuali
        s0 = sub2ind([gridsize,gridsize],gridsize,randi(6))
        a10 = randi(-1,1);
        a20 = randi(-1,1);
        vx0 = 0;
        vy0 = 0;

        % chiamata della funzione racecar: passo 
        % le velocità attuali, le accelerazioni e l'indice
        % sulla griglia di partenza
        [s1, vx, vy, r] = racecar(s0, vx0, vy0, a10, a20);


    end % while minvisits

end % while true


%