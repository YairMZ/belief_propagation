import numpy as np
from typing import Callable


def bsc_llr(p: float) -> Callable:
    """
    bsc llr is defined as:
        L(c_i) = log(Pr(c_i=0| y_i) / Pr(c_i=1| y_i)) = (-1)^y log((1-p)/p)
    :param float p: the llr is parameterized by the bit flip probability of the channel p.
    :returns: return a callable which accepts a single argument - y_i (a bit from the channel), and returns its llr
    """
    return lambda y: np.power(-1, y) * np.log((1-p)/p)

# Simply add more channel models by writing a function which receives a channel symbol as input and returns an LLL as
# output
