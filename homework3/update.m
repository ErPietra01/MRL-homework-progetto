function [axottima, ayottima] = update (Q, statot)

% isolo la matrice delle possibili coppie di azioni
sqz = squeeze(Q(statot(1),statot(2),statot(3),:,:));
[~, indx] = max(sqz(:));

% restituisco gli indici delle accelerazioni ottime
[axottima,ayottima] = ind2sub(size(sqz), indx);

end

%
