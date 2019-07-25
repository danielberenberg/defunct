#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools

def compose(*functions):
    """
    Compose a sequence of functions to a one routine.

    functions appearing in order [f1, f2, f3, ..., fn] are wrapped as
        fn( ••• (f3 ∘ (f2 ∘ f1)))

    
    usage:
    ------
    >>> fns = [lambda x: x + 1, lambda y: str(y), lambda z: z + ' got funct']
    >>> comp = compose(fns)
    >>> comp(68)
        "69 got funct"

    args:
        (iterable of callable) - functions to compose
    returns:
        :(function) - composed function
    """
    funcerator = iter(functions)
    def identity(x):
        return x

    return _compose(funcerator, identity)

def _compose(funcerator, f):
    """Recursively composes functions into a stack"""
    try:
        g = next(funcerator)

        @functools.wraps(g)
        def h(*args, **kwargs):
            return g(f(*args, **kwargs))

        return _compose(funcerator, h)

    except StopIteration:
        return f


def rpartial(func, *args):
    """
    Set positional arguments a la functools `partial`.
    `rpartial` is used to set partial positional arguments 'to the right of'
    variable args

    E.g.,
    >>> is_int = rpartial(isinstance, int)
    >>> is_int(6)
        True
    >>> is_int('no such int')
        False
    """
    @functools.wraps(func)
    def wrapper(*a):
        return func(*(a + args))

    return wrapper

def lpartial(func, *args):
    """
    Set positional arguments a la functools `partial`
    `lpartial` is used to set partial positional arguments 'to the left of'
    variable args.

    E.g.,
    >>> range_100 = lpartial(range, 100)
    >>> list(range_100(110 + 1, 2))
        [100, 102, 104, 106, 108, 110]

    """
    @functools.wraps(func)
    def wrapper(*a):
        return func(*(args + a))
    return wrapper

if __name__ == '__main__':
    pass

