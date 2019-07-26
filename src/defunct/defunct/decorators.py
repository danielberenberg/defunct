#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
decorators.py

collection of decorous decorators to make your computational life easier
"""
import warnings
import operator as op
from functools import wraps
from inspect import isclass, isfunction
                
from .utils import text_loader, text_dumper
from .funcs import rpartial

__all__ = ['autocache', 'check_that']

def autocache(loader=text_loader, 
             dumper=text_dumper,
             opener=open,
             read_as='t',
             write_as='t',
             verbose=True):
    """
    Cache the output of a computation-intensive routine by automatically
    serializing onto disk.
    
    This function is meant to decorate a value-returning callable,
    the `handler`. The added routines of @autocache are (keyword) argument
    agnostic. 

    The decorated function inherits two keyword arguments:
        :cache_to - valid path to persist outputs to disk
        :overwrite - a boolean that forces the routine to cache, but not 
                     check for disk persistence

    That is, `handler` positional args are treated as a some-dimensional
    array of inputs called *args and keywords are given by the mapping **kwargs

    args:
    =====
        :loader, dumper ------ (callable) - loading and dumping procedures for the cached object
        :opener -------------- (callable) - the method used to open the cached output
        :read_as, write_as --- (str) ------ read/write as bytes 'b' or text 't'
        :verbose ------------- (bool) ----- print output messages
    returns:
    ========
        :(function) - the decorated, auto-caching routine
           - this auto-cacher will now take an additional keyword argument called
             `cache_to` that instructs where the output should be written on disk
    
    caveats:
    ========
    `loader` and `dumper` ought to have the same call signature as 
    pickle.load, pickle.dump 
    
    usage:
    ======
    Suppose a computationally intensive procedure exists in some code and
    it's going to be accessed multiple times, perhaps after the program
    has vacated volatile storage. 
    
    In this case, @autocache is applicable to save time on next-startup.
    
    >>> @cache(loader=pickle.load, dumper=pickle.dump,
    >>>        read_opts='rb', write_opts='wb',
    >>>        verbose=False) # suppress output messages
    >>> def comp_intensive_func(arg1, arg2, ..., kwarg1=foo, kwarg2=bar, ...):
    >>>     ...
    >>>     return output
    
    `comp_intensive_func` has no inherited a final kwarg called `cache_to` which
    is used to specify the location to which the routine will cache output data
    
    Call this decorated function by:
    >>> comp_intensive_func(arg1, arg2, ..., cache_to="mypickle.bin")
    
    In this case, the output of `comp_intensive_func` will be written to 'mypickle.bin'
    """

    err_msgs = ["bad load, dump, open, or handle routines (not callable)",
                "bad read/write modes (should be 'b' or 't')"]

    def decorator(handler):
        if not all(callable(func) for func in (loader, dumper, opener, handler)):
            raise TypeError(err_msgs[0])

        if not all(mode in {'b','t'} for mode in (read_as, write_as)):
            raise ValueError(err_msgs[1])

        @wraps(handler)
        def wrapper(*args, cache_to="cached.txt", overwrite=False,**kwargs):
            try:
                if overwrite: raise FileNotFoundError
                with opener(cache_to, 'r' + read_as) as lod:
                    if verbose:
                        print("{} is cached!".format(cache_to))
                    return loader(lod)
            except FileNotFoundError: # the pickle was not found
                out = handler(*args, **kwargs)
                with opener(cache_to, 'w' + write_as) as dmp:
                    dumper(out, dmp)
                    if verbose:
                        print("cached content to {}".format(cache_to))
            return out
        return wrapper
    return decorator

def deprecated(reason):
    """
    This is a decorator which can be used to mark functions
    as deprecated.
    
    Results in a warning being emitted when the function is used

    Adapted from:
    [https://stackoverflow.com/questions/2536307/decorators-in-the-python-standard-lib-deprecated-specifically]
    """
    string_types = (type(b''), type(u''))
    if isinstance(reason, string_types):
        # @deprecated('some reason')
        # def deprec_func(...): pass

        _fmt = "Call to deprecated {t} :: [{name}] ({reason})" 
 
        def decorated(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                warnings.simplefilter('always', DeprecationWarning)
                warnings.warn(
                        _fmt.format(name=func.__name__,
                                    t="class" if isclass(func) else "function",
                                    reason=reason),
                        category=DeprecationWarning,
                        stacklevel=2)
                warnings.simplefilter('default', DeprecationWarning)
                return func(*args, **kwargs)
            return wrapper
        return decorated

    elif isclass(reason) or isfunction(reason):
        # @deprecated
        # def old_function(..): pass
        _func = reason
        _fmt = "Call to deprecated {t} :: [{name}]"
        
        @wraps(_func)
        def wrapper(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(
                    _fmt.format(name=_func.__name__,
                                t="class" if isclass(reason) else "function"),
                    category=DeprecationWarning,
                    stacklevel=2)

            warnings.simplefilter('default', DeprecationWarning)
            return _func(*args, **kwargs)
        return wrapper

    else:
        raise TypeError(f'Bad deprecation reason: {repr(type(reason))}')

def watch_for(*signals):
    """
    Watch for an error; if it occurs, let it pass through, prepending
    the function that caused it. Useful for apps that want to (eventually)
    hide traceback errors but retain their messages. 

    args:
        :*exs - expected exceptions
    returns:
        :decorator

    usage:

        >>> @watch_for(ZeroDivisionError, TypeError)
        >>> def average(*points):
        >>>     return sum(points)/len(points)

        >>> average(1,2,3)
            2.0
        >>> average(1,2,'x')
            TypeError: (- average -): unsupported operand type(s) for +: 'int' and 'str'

        >>> average()
            ZeroDivisionError: (- average -): division by zero
    """
    if not all(issubclass(sig, BaseException) for sig in signals):
        bad = [sig for sig in signals if not issubclass(sig, BaseException)]
        raise TypeError(f"Bad signals: {bad}")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)  # try to evaluate the function
            except(signals) as sig:           # a watched signal occurred
                is_sig = rpartial(op.is_, type(sig))
                raised = next(filter(is_sig, signals))
                # prepend the responsible function and raise
                raise raised(f"(- {func.__name__} -): {str(sig)}") 
        return wrapper
    return decorator



#def check_that(assertion=lambda x: True, onfail=None):
#    """
#    a decorator to validate some arbitrary truthy statement
#    prior to the actual computation
#
#    args:
#        :assertion (callable) - the assertion to be validated
#        :onfail  (str) 
#    """
#    assert callable(assertion), 'Invalid assertion; should be callable'
#    def wrap(func):
#        failure_msg = onfail if onfail else f"[{func.__name__}]: assertion failed" 
#        def wrapped(*args, **kwargs):
#            assert assertion(*args), failure_msg
#            return func(*args, **kwargs)
#        return wrapped
#    return wrap

