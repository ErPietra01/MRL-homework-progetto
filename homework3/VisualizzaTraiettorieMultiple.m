function VisualizzaTraiettorieMultiple(policyX, policyY, grid, gridsize, maxvel, acc, titolo, mantieni)
% VISUALIZZATRAIETTORIEMULTIPLE Disegna la traiettoria dell'agente sulla
% griglia, seguendo la policy corrente in modo greedy (senza
% epsilon-esplorazione). A differenza di VisualizzaTraiettoria, per
% default NON cancella le traiettorie disegnate dalle chiamate
% precedenti: ogni nuova chiamata aggiunge la sua traiettoria, con un
% colore diverso, sulla stessa figura.
%
% USO
%   VisualizzaTraiettorieMultiple(policyX, policyY, grid, gridsize, maxvel, acc)
%   VisualizzaTraiettorieMultiple(policyX, policyY, grid, gridsize, maxvel, acc, titolo)
%   VisualizzaTraiettorieMultiple(policyX, policyY, grid, gridsize, maxvel, acc, titolo, mantieni)
%
%   titolo   (opzionale) etichetta mostrata nella legenda per questa
%            traiettoria (es. 'Episodio 10000').
%   mantieni (opzionale, default true) se true, le traiettorie delle
%            chiamate precedenti restano a schermo, ciascuna con un
%            colore diverso; se false, la figura viene ripulita prima di
%            disegnare la nuova traiettoria (comportamento "una alla
%            volta", come VisualizzaTraiettoria).
%
%   Per confrontare l'evoluzione della policy durante il training, dentro
%   MonteCarloRace.m, subito dopo il "for t = T:-1:1 ... end":
%
%       if mod(ep, 10000) == 0
%           VisualizzaTraiettorieMultiple(policyX, policyY, grid, gridsize, maxvel, acc, ...
%               sprintf('Episodio %d', ep));
%       end

if nargin < 8 || isempty(mantieni)
    mantieni = true;
end
if nargin < 7 || isempty(titolo)
    titolo = 'traiettoria';
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

% ---- preparo/riuso la figura ------------------------------------------
nomefigura = 'Traiettorie agente - Racecar Monte Carlo';
fig = findobj('Type', 'figure', 'Name', nomefigura);

if isempty(fig)
    fig = figure('Name', nomefigura);
    disegna_sfondo = true;
else
    fig = fig(1);
    figure(fig);
    if ~mantieni
        clf(fig);
        disegna_sfondo = true;
    else
        disegna_sfondo = false;
    end
end

if disegna_sfondo
    % -1 ostacolo, 0 pista, 1 traguardo -> 3 colori distinti
    mappacolori = [0.85 0.2  0.2;   % ostacolo: rosso
                   0.92 0.92 0.92;  % pista: grigio chiaro
                   0.25 0.75 0.35]; % traguardo: verde
    immagine = grid + 2;

    imagesc(immagine);
    colormap(mappacolori);
    axis equal tight
    hold on
    xlabel('colonna')
    ylabel('riga')

    plot(1:6, gridsize*ones(1,6), 's', 'MarkerSize', 10, ...
        'MarkerEdgeColor','k', 'MarkerFaceColor','y', 'HandleVisibility','off');
    plot(gridsize*ones(1,6), 1:6, 's', 'MarkerSize', 10, ...
        'MarkerEdgeColor','k', 'MarkerFaceColor','g', 'HandleVisibility','off');
end

title('Traiettorie dell''agente (policy appresa)')

% ---- scelgo un colore diverso per ogni nuova traiettoria --------------
% conto quante traiettorie sono già disegnate in questa figura (invece di
% usare un contatore a parte, che si disallineerebbe se chiudi la figura
% o cancelli le variabili) e ne derivo il colore successivo
righe_esistenti = findobj(gca, 'Tag', 'traiettoria');
palette = lines(64);
colore = palette(mod(numel(righe_esistenti), size(palette,1)) + 1, :);

hp = plot(c0, r0, '-o', 'LineWidth', 1.5, 'Color', colore, ...
    'MarkerFaceColor', colore, 'MarkerSize', 4, ...
    'Tag', 'traiettoria', 'DisplayName', titolo);

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
plot(traiettoria(end,2), traiettoria(end,1), 'p', 'MarkerSize', 12, ...
    'MarkerFaceColor', colore, 'MarkerEdgeColor','k', 'HandleVisibility','off');

% legenda: una voce per ogni traiettoria disegnata finora (usa il titolo
% passato in ciascuna chiamata come etichetta)
if numel(findobj(gca, 'Tag', 'traiettoria')) > 1
    legend('show', 'Location', 'bestoutside')
end

fprintf('%s: %s\n', titolo, esito)

end
