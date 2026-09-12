% funzione che aggiorna lo stato in base alle decisioni dell'algoritmo
% cosa fa la funzione?
% la macchina riceve la griglia e la posizione corrente sulla griglia, le
% velocità lungo gli assi, e l'azione (ovvero l'accelerazione scelta
% lungo entrambi gli assi); in questo modo aggiorna la posizione sulla
% griglia e valuta se può continuare o se ha perso

% [snew, vx, vy, r] = racecar(statocorrente, azionecorrente);
function [s, nuovavx, nuovavy, r, finished] = racecar(statocorrente, azionecorrente, maxvel)

load CircuitoMonteCarlo.mat grid gridsize

% variabili dello stato
pos = statocorrente(1);
vx = statocorrente(2);
vy = statocorrente(3);

accelerazioni = [-1,0,1];
ax = accelerazioni(azionecorrente(1));
ay = accelerazioni(azionecorrente(2));

% spacchetto la velocità indicizzata
[posx, posy] = ind2sub([gridsize, gridsize], pos);

% aggiorno la velocità in entrambe le direzioni in base all'accelerazione
% scelta
nuovavx = max (-maxvel, min(vx + ax, maxvel)); 
nuovavy = max (-maxvel, min(vy + ay, maxvel));
% fprintf ('nuove velocità: vx = %d, vy = %d', nuovavx, nuovavy)

% aggiorno la posizione sulla griglia in base a di quanto mi sposto grazie
% alle nuove velocità
nuovax = posx + min(nuovavx,maxvel);
nuovay = posy + min(nuovavy,maxvel);

finished = false;

% fprintf ('nuove coordinate sulla griglia: %d, %d',nuovax, nuovay);
if nuovax > gridsize || nuovax < 1 ||nuovay > gridsize || nuovay < 1 || grid(nuovax,nuovay) == -1 
    % sono uscito dai bordi del circuito o dai confini della griglia
    % con s = -1 interrompo il while perché arrivo nello stato terminale
    finished = true;
    r = -1000; % perdo e devo ricominciare l'episodio
    s = 1;

elseif grid(nuovax, nuovay) == 0 % mi trovo sul circuito
    s = sub2ind([gridsize,gridsize], nuovax, nuovay);
    r = -1;

else % mi trovo sulla linea del traguardo
    r = 1000;
    finished = true;
    s = 1;

end


end

% 
