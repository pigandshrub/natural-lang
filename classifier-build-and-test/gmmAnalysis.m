function gmmAnalysis
%
%  gmmAnalysis
% 
%
%  A script that calculates the changes in accuracy and log likelihood based
% on changes in the number of components, epsilon, number of possible
% speakers for each test utterance N, and writes the results to a file named 
% gmmAnalysisResults.txt.
%
%  This script calls two functions, gmmTrain and ComputeLikelihood.
%
%  Please note that this script produces 252 experiments and can take up to 24 
%  hours to finish running.  
%

% Specify training directory.
dir_train = '/u/cs401/speechdata/Training/';

% Specify testing directory.
dir_test = '/u/cs401/speechdata/Testing/';

% Specify experiment parameters.
max_iter = 50;

% Factor 1: All else constant, change M.
% Factor 2: All else constant, change epsilon.
% Factor 3: Reduce the number of possible speakers.
M = [8, 1, 2, 4, 6, 10, 16];
eps = [0.0001, 0.01, 0.001, 0.00001, 0.000001, 0.0000001];
reduceS = [0, 5, 10, 15, 20, 25];

% Open file to write results
fid = fopen('gmmAnalysisResults.txt', 'w');

% Keep track of the number of analyses done
counter = 0;
benchlog = 0;
benchnum = 0;

for m=1:length(M)
    for e=1:length(eps)
        for s=1:length(reduceS)
            
            counter = counter + 1;
            fprintf(fid,'\r\n\r\nEXPERIMENT %.0f\r\n', counter);
            fprintf(fid,'Number of components = %.0f\r\n', M(m));
            fprintf(fid,'Epsilon = %f\r\n', eps(e));
            fprintf(fid,'Number of Speakers = %.0f\r\n', 30-reduceS(s));

            % Then obtain a trained model for each speaker based on the given
            % parameters.
            gmms = gmmTrain(dir_train, max_iter, eps(e), M(m), reduceS(s)); 

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
		
		fprintf(fid, '\r\n\r\n%s:\r\n', DD(iFile).name(1:end-5));
 
                % Calculate comparison results
                if ((M(m) == 8) && (eps(e) == 0.0001) && (reduceS(s) == 0))
                    fprintf(fid, 'Benchmark numbers\r\n');
                    benchlog = sortrows(logLike,1);
                    benchnum = cell2mat(benchlog(:,2));
                end
                
                if (iscell(benchlog))
                    currentlog = sortrows(logLike,1);
                    numS = size(currentlog,1);
                    comparelog = (cell2mat(currentlog(:,2)) - benchnum(1:numS))./benchnum(1:numS);
                                    
                    fprintf(fid, 'Percentage change in Likelihood \r\n');
                    for sp = 1:length(comparelog)
                        fprintf(fid, '%s : %.3f \r\n', cell2mat(benchlog(sp,1)),comparelog(sp));
                    end
                    fprintf(fid, 'Average percentage change in Likelihood: %.3f \r\n\r\n', mean(comparelog));
                end
                
                fprintf(fid, '%s: Top Five Likely Speakers \r\n', DD(iFile).name(1:end-5));
                fprintf(fid, '%s : %s : %s \r\n', 'Rank', 'Speaker', 'Log Likelihood');
                for ind = 1:5
                    fprintf(fid, '%.0f : %s : %.3f \r\n', ind, ...
                        cell2mat(logLikeMatrix(ind,1)),cell2mat(logLikeMatrix(ind,2))); 
                end
                
            end
        end
    end
end
fclose(fid);

