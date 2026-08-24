function Vpi = IterativePolicyEvaluation (P,R,pi,V0,gamma)
% Utilizzo l'equazione di Bellman iterativamente finché, con la policy
% attuale, non ottengo il valore migliore

% criterio di stop
theta = 1e-12;

S = size(R,1);

Ppi = zeros(S,S);
Rpi = zeros(S,1);

for s = 1:S
    Ppi(s,:) = P(s,:,pi(s));
    Rpi(s) = R(s,pi(s));
end

% applicazione dell'equazione di Bellman finché non soddisfo il criterio di
% stop
while true
    Vs = gamma*Ppi*V0 + Rpi;
    if norm(Vs - V0, Inf) < theta
        %interrompo l'algoritmo
        V0 = Vs;
        break
    else
    %altrimenti aggiorno il valore
    V0 = Vs;
    end

end

% Fine algoritmo: restituisco il valore ottimo per pi corrente
Vpi = V0;

end
