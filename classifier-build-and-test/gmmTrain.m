function gmms = gmmTrain( dir_train, max_iter, epsilon, M, reduceS)
% gmmTrain
%
%  inputs:  dir_train  : a string pointing to the high-level
%                        directory containing each speaker directory
%           max_iter   : maximum number of training iterations (integer)
%           epsilon    : minimum improvement for iteration (float)
%           M          : number of Gaussians/mixture (integer)
%           reduceS    : number of optional speakers to exclude in training
%                       (optional integer argument for discussion analysis)
%
%  output:  gmms       : a 1xN cell array. The i^th element is a structure
%                        with this structure:
%                            gmm.name    : string - the name of the speaker
%                            gmm.weights : 1xM vector of GMM weights
%                            gmm.means   : DxM matrix of means (each column 
%                                          is a vector
%                            gmm.cov     : DxDxM matrix of covariances. 
%                                          (:,:,i) is for i^th mixture
%  
%  This function uses two helper functions, ComputeLikelihood and
%  UpdateParameters.
%

%  Check if optional argument given; if not, set to zero
if (nargin < 5)
    reduceS = 0;
end

% Get array of folders in the given path and remove . and .. folder.
DD = dir(dir_train);
DD = DD(~strncmpi('.', {DD.name}, 1));
N = length(DD)-reduceS;

% Initialize output structure
gmms = cell(1,N);

for iFolder=1:N 
        
    subdir = strcat(dir_train, DD(iFolder).name);
    listing = dir([dir_train, filesep, DD(iFolder).name, '/*.mfcc']);
    
    % Collect lines from the files and concatenate to an input matrix
    % Collect from first file.
    lines = textread([subdir, filesep, listing(1).name], '%s','delimiter','\n');
    x = str2num(char(lines)); 
    % Collect from remaining files
    for iFile = 2:length(listing)
        lines = textread([subdir, filesep,listing(iFile).name], '%s','delimiter','\n');
        y = str2num(char(lines)); 
        x = [x;y];
    end
    
    % Capture dimensions of the input matrix
    [t,D] = size(x);

    % Initialize parameters
    w = 1/M * ones(1,M);            % weights

    ind = randperm(t);              % means: randomly choose M frames from 
    mu = x(ind(1:M),:)';            %        x and transpose it to get dxM
 
    sig = eye(D);                   % cov: use identity matrix as the cov 
    var = repmat(sig,[1,1,M]);      %      matrix for each m-th Gaussian.

    % Place initialized values into gmm structure
    gmm.name = DD(iFolder).name;
    gmm.weights = w;
    gmm.means = mu;
    gmm.cov = var;
    
    % Place gmm structure into gmms cell array
    gmms{iFolder} = gmm;
    
    % Train the model
    q = 0;
    prev_L = -Inf;
    improvement = Inf;
    while ((q <= max_iter) && (improvement >= epsilon))
        % Compute likelihood and update parameters
        [L, prior] = ComputeLikelihood(x, gmms{iFolder});
        gmms{iFolder} = UpdateParameters(x, gmms{iFolder}, prior);
        improvement = L - prev_L;
        prev_L = L;
        q = q + 1;
    end
end