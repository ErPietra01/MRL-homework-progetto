clear all
close all
clc

load vstarPI.mat
VPI = V;

load vstarVI.mat
VVI = V;

disp (norm(VPI - VVI))