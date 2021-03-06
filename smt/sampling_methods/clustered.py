"""
Author: Dr. John T. Hwang <hwangjt@umich.edu>

This package is distributed under New BSD license.

Nonuniformly spaced sampling.
"""
from __future__ import division
import numpy as np
import scipy.interpolate
from six.moves import range

from smt.sampling_methods.sampling_method import SamplingMethod
from smt.sampling_methods.full_factorial import FullFactorial

class Clustered(SamplingMethod):

    def _initialize(self):
        self.options.declare('kernel', types=SamplingMethod)
        self.options.declare('spacing')

    def __call__(self, n):
        """
        Compute the requested number of sampling points.

        Arguments
        ---------
        n : int
            Number of points requested.

        Returns
        -------
        ndarray[n, nx]
            The sampling locations in the input space.
        """
        xlimits = self.options['kernel'].options['xlimits']
        nx = xlimits.shape[0]
        x = self.options['kernel']._compute(n)

        x -= 0.5
        x *= 2.0
        x[:, :] = x ** 2. * np.sign(x)
        x /= 2.0
        x += 0.5
        for kx in range(nx):
            x[:, kx] = xlimits[kx, 0] + x[:, kx] * (xlimits[kx, 1] - xlimits[kx, 0])

        return x
