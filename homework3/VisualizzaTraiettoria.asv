function VisualizzaTraiettoria(policyX, policyY, grid, gridsize, maxvel, acc, titolo)

% Questa funzione rappresenta la traiettoria seguita dalla macchinina ogni
% 10.000 episodi

if nargin < 7
    titolo = 'Traiettoria dell''agente (policy appresa)';
end

animato = true;    % true = disegna passo-passo, false = solo il risultato finale
pausastep = 0.05;  % secondi di pausa tra un passo e l'altro (solo se animato)
maxstep = 300;     % limite di sicurezza per evitare loop infiniti

% ---- punto di partenza casuale sulla linea di partenza --------------
pos = sub2ind([gridsize, gridsize], gridsize, randi(6));
vx = 0;
vy = 0;

[r0, c0] = ind2sub([gridsize, gridsize], pos);
traiettoria = nan(maxstep+1, 2);
traiettoria(1,:) = [r0, c0];

nstep = 1;
finished = false;
esito = 'incompleto (raggiunto il limite di passi)';

% ---- preparo la mappa colorata del circuito --------------------------
mappacolori = [0.85 0.2  0.2;   % ostacolo: rosso
               0.92 0.92 0.92;  % pista: grigio chiaro
               0.25 0.75 0.35]; % traguardo: verde
immagine = grid + 2; % -1,0,1 -> 1,2,3 (indici validi per la colormap)

% riuso sempre la stessa figura invece di aprirne una nuova ogni volta,
% utile se la chiami ripetutamente durante il training
nomefigura = 'Traiettoria agente - Racecar Monte Carlo';
fig = findobj('Type', 'figure', 'Name', nomefigura);
if isempty(fig)
    fig = figure('Name', nomefigura);
else
    fig = fig(1);
    figure(fig);
    clf(fig);
end

imagesc(immagine);
colormap(mappacolori);
axis equal tight
hold on
xlabel('colonna')
ylabel('riga')
title(titolo)

% evidenzio linea di partenza e traguardo
plot(1:6, gridsize*ones(1,6), 's', 'MarkerSize', 10, ...
    'MarkerEdgeColor','k', 'MarkerFaceColor','y');
plot(gridsize*ones(1,6), 1:6, 's', 'MarkerSize', 10, ...
    'MarkerEdgeColor','k', 'MarkerFaceColor','g');

hp = plot(c0, r0, '-o', 'LineWidth', 2, 'Color', [0.1 0.3 0.9], ...
    'MarkerFaceColor', [0.1 0.3 0.9], 'MarkerSize', 4);

% ---- simulazione dell'episodio con policy greedy ----------------------
while ~finished && nstep <= maxstep

    pos_prec = pos; % la tengo da parte: se l'episodio termina, racecar
                     % restituisce una posizione fittizia (s = 1), quindi
                     % ricostruisco a mano la cella (anche fuori griglia)
                     % davvero raggiunta con quest'ultima mossa

    statocorrente = [pos, vx, vy];
    azionecorrente = [policyX(pos, vx + maxvel + 1, vy + maxvel + 1), ...
                       policyY(pos, vx + maxvel + 1, vy + maxvel + 1)];

    [pos, vx, vy, r, finished] = racecar(statocorrente, azionecorrente, maxvel);

    [pr, pc] = ind2sub([gridsize, gridsize], pos_prec);
    riga = pr + vx;
    colonna = pc + vy;

    nstep = nstep + 1;
    traiettoria(nstep,:) = [riga, colonna];

    if animato
        set(hp, 'XData', traiettoria(1:nstep,2), 'YData', traiettoria(1:nstep,1));
        drawnow
        pause(pausastep)
    end

    if finished
        if r > 0
            esito = sprintf('traguardo raggiunto in %d passi', nstep-1);
        else
            esito = sprintf('uscito di pista dopo %d passi', nstep-1);
        end
    end
end

traiettoria = traiettoria(1:nstep,:);

set(hp, 'XData', traiettoria(:,2), 'YData', traiettoria(:,1));
plot(traiettoria(end,2), traiettoria(end,1), 'p', 'MarkerSize', 14, ...
    'MarkerFaceColor', 'r', 'MarkerEdgeColor','k');

subtitle(esito)
disp(esito)

end
