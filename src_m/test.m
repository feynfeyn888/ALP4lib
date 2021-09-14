%% Setup
close all;
clear all;

%%
% path_info.txt
path_info='../path_info.txt'
info=split(fileread(path_info),',')
date=info{1}
time=info{2}

file_path_input='../data/Input_Matrix/'+date+'/'+time+'.csv'
file_path_output='../data/Output_Matrix/'+date+'/'+time+'.csv'

%% read csv
Input_Matrix = transpose(readmatrix(filename))
Output_Matrix = transpose(readmatrix(filename))
Output_Matrix = double(Output_Matrix)/65535;