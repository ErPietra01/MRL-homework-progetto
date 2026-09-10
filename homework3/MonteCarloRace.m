clear all
close all
clc

gridsize = 20;
A = 9; % spazio delle azioni: combinazioni delle possibili accelerazioni 
       % lungo i due assi
acceleration = [-1,0,1]; % accelerazioni (1=avanti, 0=fermo, -1=indietro)

% RAPPRESENTAZIONE DEL PERCORSO
grid = zeros(gridsize,gridsize); %gridworld su cui si muove la macchina

for i = 6:gridsize
    for j = 0: gridsize

    end
end

% [nuovax, nuovay, nuovavx, nuovavy, r] = racecar2(posx, posy, ...
%     velx, vely, accx, accy, griglia)

%