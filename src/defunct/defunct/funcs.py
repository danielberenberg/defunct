#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        def h(*args, **kwargs):
            return g(f(*args, **kwargs))

        return _compose(funcerator, h)

    except StopIteration:
        return f

if __name__ == '__main__':
    pass

