clear all
close all
clc

% definizione della griglia da passare all'algoritmo
% gridsize = 20;
gridsize = 36;

grid = zeros (gridsize, gridsize);

% griglia di partenza
for p = 1:6
    grid(gridsize,p) = 0;
end

% traguardo
for t = 1:6
    grid(t,gridsize) = 1;
end

if gridsize == 20
    % bordo dx
    for i = 11:gridsize
        for j = 7:gridsize
            grid(i,j) = -1;
        end
    end
    for i = 12:gridsize
        grid (10,i) = -1;
    end
    for i = 7:9
        for j = 15:gridsize
            grid (i,j) = -1;
        end
    end

    % bordo sx
    for i = 3:6
        for j = 1:4
            grid(i,j) = -1;
        end
    end
    for i = 1:2
        for j = 1:10
            grid(i,j) = -1;
        end
    end

% N.B.: abbiamo appreso un metodo per popolare una matrice senza cicli for
% e lo abbiamo applicato per costruire un secondo percorso più grande;
% commentando i singoli blocchi è possibile semplificare o complicare il
% percorso
elseif gridsize == 36
    % bordo sx
    grid (1:12,1:15) = -1;
    grid (1:2,16:26) = -1;
    grid (3:10,16:20) = -1;
    grid (13:20,1:14) = -1;
    grid (21:25,1:6) = -1;

    % bordo dx
    grid (29:gridsize,7:18) = -1;
    grid (16:25,21:27) = -1;
    grid (26:28,14:18) = -1;
    grid (26:gridsize,19:27) = -1;
    grid (9:gridsize,28) = -1;
    grid (7:gridsize,29:gridsize) = -1;

end

save CircuitoMonteCarlo.mat gridsize grid