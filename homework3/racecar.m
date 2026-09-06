
function [next, reward] = racecar[s,a]
% seguendo la logica dell'algoritmo, la funzione viene utilizzata in ogni
% stato per valutare la reward e lo stato successivo.


% stato: posizione, accelerazione, direzione

end



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

% [ascissa, ordinata, accelerazione, direzione] = ind2sub([20,20,5,4], s)


% commenti;
% per rendere tutto più agevole, si potrebbe pensare di indicizzare le
% coordinate con un unico valore, per poi usarle nell'ind2sub principale
% la gestione delle coordinate dei punti d'interesse (traguardo e bordi)
% devono avvenire dopo sub2ind in modo tale da semplificare la ricerca
% della corrispondenza
