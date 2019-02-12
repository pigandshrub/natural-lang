function gmm = UpdateParameters( x, gmm, prior)
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
%           prior      : a Mxt matrix of prior probs of m-th component given
%                        xt.
%
%  output:   
%          gmm         : the gmm structure with updated parameters
%                        
[t,D] = size(x);
M = size(gmm.means,2);

% Update parameters for each component
for comp = 1:M
    
    mu_m = gmm.means(:,comp)';                      % 1xD
    prior_m = prior(comp,:);                        % 1xt
    prior_m_stack = repmat(prior_m',[1,D]);         % txD
    prior_times_x = prior_m_stack .* x;             % txD
    prior_times_xsquared = prior_m_stack .* (x.^2); % txD 
    sum_prior = sum(prior_m);                       % 1x1 :scalar
    
    % Compute new parameters
    w_new = sum_prior * (1/t);                      % 1x1 :scalar
    mu_new = sum(prior_times_x) * (sum_prior^-1);    % 1xD 
    var_new = (sum(prior_times_xsquared) * (sum_prior^-1)) - (mu_new.^2); % 1xD
    % Shape var_new vector to diagonal matrix
    var_shaped = diag(var_new);                     % DxD

    % Update parameters in gmm struct.
    gmm.weights(:,comp) = w_new;                   % 1x1
    gmm.means(:,comp) = mu_new';                   % Dx1
    gmm.cov(:,:,comp) = var_shaped;                % DxD
    
end



