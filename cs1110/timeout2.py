'''A testing harness support file created by Luther Tychonievich and released into the public domain in 2015.
It provides:

1. threads to create timeouts.  This technique allows for side-effect based timeouts

Provided as-is with no warranty of any kind.
'''

import signal

class TimeoutException(Exception):
    '''Represents a time having expired before a function completed'''
    def __init__(self, limit, func, args=(), kwargs={}):
        '''Should be invoked with the exact arguments to captime, in order'''
        self.msg = func.__name__+'('
        for arg in args:
            self.msg += repr(arg)+', '
        for key in kwargs:
            self.msg += key+'='+repr(kwargs[key])+', '
        if self.msg[-2:] == ', ': self.msg = self.msg[:-2]
        self.msg += ') timed out after '+str(limit)+' seconds'
    def __str__(self): return self.msg
    def __repr__(self): return 'Timeout Exception: '+self.msg


def captime(timeout, func, args, kwargs={}):
    '''Wraps a function in a timeout and returns either the return value or an exception.
    captime is *not* threadsafe
    
    Arguments:
    timeout -- the number of seconds to wait; may be float
    func --    the function to run under timeout
    args --    the positional arguments to pass func
    kwargs --  (optional) the key-word arguments to pass func
    
    Returns:
    the return value of func(*args, **kwargs), or an Exception object
    '''
    def handler(signum, frame):
        raise TimeoutException(timeout, func, args, kwargs)
    signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, timeout)
    try:
        return func(*args, **kwargs)
    except BaseException as e:
        return e
    finally:
        signal.setitimer(0, signal.ITIMER_REAL)
        


__all__ = ['TimeoutException', 'captime']

if __name__ == "__main__":
    def f(x,y,z=3):
        if type(x) is list:
            x[0] = 1112
        else:
            while True:
                pass
    
    x=[1,2,3]
    print(captime(0.2, f, (1,2,3)))
    print(captime(0.2, f, (1,2),{'z':3}))
    print(captime(0.2, f, (x,2,3)))
    print(captime(0.2, f, (1,2,3),{'z':5}))
    print(x)
