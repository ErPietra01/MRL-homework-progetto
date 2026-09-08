% funzione che aggiorna lo stato in base alle decisioni dell'algoritmo
% cosa fa la funzione?
% la macchina riceve la griglia e la posizione corrente sulla griglia, le
% velocità lungo gli assi, e l'azione (ovvero l'accelerazione scelta
% lungo entrambi gli assi); in questo modo aggiorna la posizione sulla
% griglia e valuta se può continuare o se ha perso
function [nuovax, nuovay, nuovavx, nuovavy, r] = racecar(posx, posy, ...
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


% per l'homework: assegno ai pixel una reward istantanea
% sentiero: 0; traguardo: 1; ostacolo: -1
% scelgo una direzione e una accelerazione (1-5) casuale e mi muovo di
% conseguenza; se esco torno al punto di partenza e creo l'associazione tra
% lo stato e l'azione randomica presa, in modo tale da aggiornare la reward
% dello stato
% di conseguenza, basandosi sul codice del prof, bisogna fare una serie di
% if per valutare se l'episodio termina o meno

% sub2ind e ind2sub: matlab memorizza le matrici per colonne e associa, di 
% conseguenza, un indice lineare a ciascun elemento. tramite sub2ind è
% possibile convertire questo indice lineare in coordinate "classiche",
% ovvero per righe. ind2sub fa il contrario: date delle coordinate,
% restituisce l'indice lineare. Di conseguenza la seguente riga di codice:

% [hand, dealer, usableAce] = ind2sub([10, 10, 2], s);

% permette di ottenere le caratteristiche dello stato corrente. L'agente
% riceve uno stato, indicizzato linearmente, e sa che le possibili
% caratteristiche di uno stato sono: carta in mano, carta scoperta del
% dealer, e valore dell'asso. la funzione riceve in ingresso uno dei
% possibili stati in S, con S=10*10*2. in questo modo prendo un indice
% lineare e ne traggo le coordinate di un tensore, ovvero i valori delle
% tre informazioni nello stato corrente. con sub2ind alla fine della
% funzione ottengo nuovamente l'indice lineare.

% bozza in pseudocodice:

% [ascissa, ordinata, velocità, direzione] = ind2sub([20,20,3,2], s)


% commenti
% la gestione delle coordinate dei punti d'interesse (traguardo e bordi)
% devono avvenire dopo sub2ind in modo tale da semplificare la ricerca
% della corrispondenza
% la funzione restituisce la variazione di velocità e la direzione, in modo
% tale che l'algoritmo scelga il nuovo stato 
% azioni: -1,0,1 a seconda di quanto voglio aumentare, e la direzione
% devo modificare l'accelerazione (delta v)
% bisognerebbe anche verificare la posizione sulla mappa per aggiornare la
% reward