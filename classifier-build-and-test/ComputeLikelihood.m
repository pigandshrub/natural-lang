function [L, prior] = ComputeLikelihood( x, gmm )
% ComputeLikelihood
%
%  inputs:  x          : a txD matrix of MFCC coefficients
%           gmm        : a structure with the following fields:
%                            gmm.name    : string - the name of the speaker
%                            gmm.weights : 1xM vector of GMM weights
%                            gmm.means   : DxM matrix of means (each column 
%                                          is a vector
%                            gmm.cov     : DxDxM matrix of covariances. 
%                                          (:,:,i) is for i^th feature
%  output: L           : a 1xt vector of the log probs of the t-th frame
%                        given gmm's parameters. 
%          prior       : a Mxt matrix of the prior prob of each component 
%                        given xt.
%

% Capture dimensions of the relevant matrices and set up L, b_m and any
% one time calculations
[t,D] = size(x);
M = size(gmm.means,2);
logb_m = cell(M,t);

% Compute log_bm_xt
for comp=1:M
    
    mu_m = gmm.means(:,comp)';      % 1xD
    cov_m = gmm.cov(:,:,comp);      % DxD
    var_m = sum(cov_m);             % 1xD
    divvar = var_m.^-1;             % 1xD 
    prod_var = prod(var_m);         % 1x1 scalar

    f = sum((mu_m.^2) .* (0.5*divvar));
    g = 0.5 * D * (log(2*pi));
    h = 0.5 * log(prod_var);
    second_term = f + g + h;
    
    for frame=1:t
        % Get each row vector of x, size 1xD
        xt = x(frame,:);
        
        q = 0.5 * (xt.^2) .* divvar;
        r = mu_m .* xt .* divvar;
        
        first_term = sum(q - r);

        % Compute the logb_m value for current xt and store it.
        % We purposefully leave out the 0.5 factor for now.
        logb_m{comp, frame} = - first_term - second_term;   
    end        
    
end

% At this point, logb_m should be a fully updated Mxt cell array

% Compute prior prob of m-th component given xt and theta parameters
% and obtain likelihood L.
logb = cell2mat(logb_m);              % Mxt 
b = exp(logb);                        % Mxt
w = gmm.weights';                     % Mx1
w_stack = repmat(w,[1,t]);            % Mxt
numerator = w_stack .* b;             % Mxt
denominator = sum(numerator);         % 1xt
denom = denominator.^-1;              % 1xt
denom_stack = repmat(denom,[M,1]);    % Mxt

prior = numerator .* denom_stack ;    % Mxt
L = sum(log(denominator));            % 1xt

