% launch_ins.m  —  Always run THIS script to start the simulation.
%
% IMPORTANT: MATLAB caches classdef files. If you re-run after editing
% rocket_ins_simulation.m without clearing the cache, MATLAB uses the
% OLD version and you will see wrong results (diverging filters, etc.).
%
% This script forces a clean reload every time.

% 1. Close any existing simulation window
close all force;

% 2. Clear the class cache — this is the critical step
clear classes;    %#ok<CLCLS>

% 3. Clear all variables too
clear all;        %#ok<CLALL>

% 4. Launch fresh
app = rocket_ins_simulation();
