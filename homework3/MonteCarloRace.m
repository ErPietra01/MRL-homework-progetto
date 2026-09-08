clear all
close all
clc

gridsize = 20;
acceleration = [-1,0,1]; % accelerazioni (1=avanti, 0=fermo, -1=indietro
% lungo l'asse scelto con directions)
directions = [1,2]; % direzioni (1=ascisse, 2=ordinate)
S = gridsize*gridsize*3*2;
s = randi(S);
a = 1; 
grid = ones(20,20); %gridworld su cui si muove la macchina
acc = 1;
v = 3;

% [nuovax, nuovay, nuovavx, nuovavy, r] = racecar2(posx, posy, ...
%     velx, vely, accx, accy, griglia)

%