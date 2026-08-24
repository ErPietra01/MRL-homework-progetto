clear all
close all
clc 

rng(2);
load GamblerModello.mat % P R heads tails  gamma 

% Ricavo, dalla matrice delle reward, lo spazio delle azioni e gli stati
S = size(R,1);
A = size(R,2);

%inizializzo il vettore dei valori e della policy
V = randn(S,1); % vettore colonna con un elemento per ciascuno stato
pi = randi(A, [S,1]);
% vettore colonna di numeri casuali tra 0 e A, con un elemento per ciascuno
% stato

% Ciclo while per l'algoritmo: continuo ad aggiornare pi calcolando pip
% all'iterazione i-esima, fino al momento in cui pi == pip (ovvero la 
% policy non migliora ulteriormente)

i = 0;

while true
    i = i + 1;
    disp(i);

    % Policy Evaluation
    V = PolicyEvaluationGambler(P, R, pi, gamma);
    % Policy Evaluation Iterativa
    %V = IterativePolicyEvaluation (P,R,pi,V,gamma);

    % Policy Improvement
    pip = PolicyImprovementGambler(P, R, V, gamma);

    % Interruzione
    if norm(pip - pi) == 0
        fprintf('iterazione finale: pip-pi = ');
        disp(norm(pip-pi));
        
        break
    else
        pi = pip;
    end

end

disp (V)

% salvo v come funzione valore ottima
save vstarPI.mat V

% i due algoritmi sembrano metterci lo stesso numero di iterazioni

% Rappresentazione grafica della policy ottima 
capitale = 0:100;

figure('Name', 'Risultati Gambler''s Problem', 'Position', [100, 100, 1200, 400]);

% --- 1. Grafico della Funzione Valore V(s) ---
subplot(1, 3, 1);
plot(capitale, V, 'LineWidth', 2, 'Color', 'b');
grid on;
title('Funzione Valore Ottima');
xlabel('Capitale posseduto (Stato)');
ylabel('Probabilità di vittoria stimata');
xlim([1 99]); 

% --- 2. Grafico della Policy Ottima pi(s) ---
subplot(1, 3, 2);
stairs(capitale, pi, 'LineWidth', 1.5, 'Color', 'r');
grid on;
title('Policy Ottima (Scommessa)');
xlabel('Capitale posseduto (Stato)');
ylabel('Azione (Capitale da scommettere)');
xlim([1 99]); 
ylim([0 55]);

