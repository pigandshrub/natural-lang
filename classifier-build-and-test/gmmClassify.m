function gmmClassify
%
%  gmmClassify
% 
%
%  A script that calculates and reports the likelihoods for the five
% most likely speakers for each test utterance.  The results are reported
% in files called unkn_N.lik for each test utterance N.
%
%  This script calls two functions, gmmTrain and ComputeLikelihood.
%
%

% Specify parameters for training.
dir_train = '/u/cs401/speechdata/Training/';
max_iter = 20;
M = 8;
epsilon = 0.0001;

% Specify testing directory
dir_test = '/u/cs401/speechdata/Testing/';

% Then obtain a trained model for each speaker based on the given
% parameters.
gmms = gmmTrain(dir_train, max_iter, epsilon, M); 

% Now examine the testing data using the trained model.
DD = dir([dir_test, filesep, '/*.mfcc']);

for iFile = 1:length(DD)

    lines = textread([dir_test, filesep, DD(iFile).name], '%s','delimiter','\n');
    x = str2num(char(lines)); 

    % Calculate likelihood for each speaker and store in a cell array.
    logLike = cell(length(gmms),2);
  
    for speaker = 1:length(gmms)
        [L,] = ComputeLikelihood(x, gmms{speaker});        
        logLike{speaker,1} = gmms{speaker}.name;
        logLike{speaker,2} = L;
    end
    
    logLikeMatrix = sortrows(logLike,-2);
    
    % Write results to file
    filename = strcat(DD(iFile).name(1:end-5), '.lik');
    fid = fopen(filename, 'w');
    fprintf(fid, '%s : %s : %s \r\n', 'Rank', 'Speaker', 'Log Likelihood');
    for ind = 1:5
        fprintf(fid, '%.0f : %s : %.3f \r\n', ind, ...
            cell2mat(logLikeMatrix(ind,1)),cell2mat(logLikeMatrix(ind,2))); 
    end
    fclose(fid);

end
    

