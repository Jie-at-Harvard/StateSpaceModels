###################################################
#    This file is part of py-smc2.
#    http://code.google.com/p/py-smc2/
#
#    py-smc2 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    py-smc2 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with py-smc2.  If not, see <http://www.gnu.org/licenses/>.
###################################################

# observ: 
# params[0]: tau
# params[1]: sigma
# params[2]: r
# params[3]: b

#! /usr/bin/env pythonproposal
# -*- coding: utf-8 -*-

from numpy import random, power, sqrt, exp, zeros_like, zeros, \
        ones, mean, average, prod, log, array, repeat
from scipy.stats import norm, truncnorm, gamma, uniform
from src.parametermodel import ParameterModel

#### most functions here take transformed parameters, but rprior returns
#### untransformed parameters

hyperparameters = { \
        "b_mean": 0, "b_sd": sqrt(100), \
        "b1_rate": 1, \
        "low": -10, "high": 10}  
        
L = 4

def logdprior(parameters, hyperparameters):
    """ Takes transformed parameters.  When the parameter is transformed, 
    a jacobian appears in the formula.
    """
    # the following is the log density of expo
    b_all = parameters[0]  + parameters[1] + parameters[3] - 3 * log(hyperparameters["high"]) \
            - log(hyperparameters["high"]-hyperparameters["low"])  
    return b_all

def rprior(size, hyperparameters):
    """ returns untransformed parameters """ 
    parameters = zeros((L, size ))
    parameters[0, :] = random.uniform(low = 0, high = hyperparameters["high"], size = size)
    parameters[1, :] = random.uniform(low = 0, high = hyperparameters["high"], size = size)
    parameters[2, :] = random.uniform(low = hyperparameters["low"], high = hyperparameters["high"], size = size)
    parameters[3, :] = random.uniform(low = 0, high = hyperparameters["high"], size = size)
    #parameters[0, :] = random.exponential(scale = 1 / hyperparameters["b1_rate"], size = size)
    #parameters[ell, :] = norm.rvs(size = size, loc = hyperparameters["b_mean"], scale = hyperparameters["b_sd"]) 
    return parameters

## Prior hyperparameters
modeltheta = ParameterModel(name = "logistic diffusion model theta", dimension = L)
modeltheta.setHyperparameters(hyperparameters)
modeltheta.setPriorlogdensity(logdprior)
modeltheta.setPriorgenerator(rprior)
modeltheta.setParameterNames(["tau, sigma, r, b"])
modeltheta.setTransformation(["log", "log", "none", "log"]) #(["none", "none"])
#modeltheta.setRprior({}) #seems useless
#modeltheta.setRprior(["priorfunction <- function(x) dexp(x, rate = %.5f)" % hyperparameters["b1_rate"],\
#    "priorfunction <- function(x) dnorm(x, sd = %.5f)" % hyperparameters["b_sd"]])
#modeltheta.setRprior(["priorfunction <- function(x) dexp(x, rate = %.5f)" % hyperparameters["b1_rate"],\
#    "priorfunction <- function(x) dexp(x, rate = %.5f)" % hyperparameters["b1_rate"]])
set_argu = []
for m in range(L):
    set_argu.append("priorfunction <- function(x) dexp(x, rate = %.5f)" % hyperparameters["b1_rate"])
modeltheta.setRprior(set_argu) #used by ParameterModel (generatee modeltheta), which does not seem useful anymore 

