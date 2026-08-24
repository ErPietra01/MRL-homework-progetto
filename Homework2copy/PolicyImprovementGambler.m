function pip = PolicyImprovementGambler(P, R, V, gamma)

S = size(R, 1);
A = size(R, 2);

%policy aggiornata

pip = zeros(S,1);

% funzione qualità
for s = 1:S
    q = zeros(A,1);
    for a = 1:A
        q(a) = R(s,a) + gamma*P(s,:,a)*V;
    end
    pip(s) = find(q == max(q), 1);
    % if s == 1
    %     size(q)
    % end

end