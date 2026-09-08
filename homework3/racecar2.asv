% cosa fa la funzione?
% la macchina riceve la griglia e la posizione corrente sulla griglia, le
% velocità lungo gli assi, e l'azione (ovvero l'accelerazione scelta
% lungo entrambi gli assi); in questo modo 
function [nuovax, nuovay, nuovavx, nuovavy, r] = racecar2(posx, posy, ...
    velx, vely, accx, accy, griglia)

vx = velx;
vy = vely;
ax = accx;
ay = accy;

% aggiorno la velocità in entrambe le direzioni in base all'accelerazione
% scelta
nuovavx = vx + ax; 
nuovavy = vy + ay; 
fprintf ('nuove velocità: vx = %d, vy = %d', nuovavx, nuovavy)

% aggiorno la posizione sulla griglia in base a di quanto mi sposto grazie
% alle nuove velocità
nuovax = posx + min(nuovavx,5);
nuovay = posy + min(nuovavy,5);

% verifica della posizione sulla griglia: vittoria, sconfitta o continua
% disp("stampo la griglia");
% disp(griglia);

fprintf ('nuove coordinate sulla griglia: %d, %d',nuovax, nuovay);
if griglia(nuovax, nuovay) == 0 % mi trovo sul circuito
    r = -1;
elseif griglia(nuovax,nuovay) == -1 % sono uscito dai bordi
    r = -5; % perdo e devo ricominciare l'episodio
else % mi trovo sulla linea del traguardo
    r = 1;

end

% 