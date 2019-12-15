import scipy.stats as ss
import numpy as np
import scipy.optimize as so

import numba

@numba.jit(nopython=True)
def online_update(*, n, m1, m2, x):
    """ m1 and m2 can be vector and matrix respectively! """
    assert x.ndim == 1
    n += 1
    m1 += (x - m1) / n
    x_ = np.atleast_2d(x)
    x2 = x_ * x_.T
    assert x2.ndim == 2
    m2 = m2 + (x2 - m2) / n
    return n, m1, m2

def pareto_from_mean_median(mu, median):
    """
    scipy form has loc and scale.
    (mu - loc) / scale = b / (b - 1)
    (m - loc) / scale = 2 ** (1 / b)

    This problem is abiguous so just force some assumptions.

    b / (b - 1) * 2 ** (-1 / b) = (mu - loc) / (med - loc) ... just choose loc=0, scale=1 for now
    """
    r = mu / median
    def _f(b):
        return (b / (b - 1)) / (2 ** (1 / b)) - r
    b = so.bisect(_f, 1.01, 100)
    loc = 0
    scale = (mu - loc) * (b - 1) / b
    return b, loc, scale
