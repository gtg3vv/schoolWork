'''A testing harness support file created by Luther Tychonievich and released into the public domain in 2015.
It provides two features:

1.  It uses the multiprocessing library to create timeouts.  Because of the global interpreter lock, this is the only cross-platform form of timeouts of which I am aware.

2.  It allows a simple interface for testing command-line programs using "input" and "print".

Provided as-is with no warranty of any kind.
'''

from multiprocessing import Process, Queue
import sys, runpy
from io import UnsupportedOperation

class CustomIO(object):
    def __init__(self, *inputLines):
        self.lines = inputLines
        self.pos = 0
        self.printed = [""]
    def fileno(self): raise OSError("not a file")
    def write(self,s): self.printed[-1] += s
    def flush(self): pass
    def close(self): pass
    def readline(self):
        if self.pos < len(self.lines):
            self.printed.append("")
            self.pos += 1
            return str(self.lines[self.pos-1])+"\n"
        else:
            return ""
    def __getattr__(self, name): raise UnsupportedOperation(name)

def wrapper(tocall, args, kwargs, q):
    try:
        try: result = tocall(*args, **kwargs)
        except SystemExit: result = None
        try:    q.put(result)
        except: q.put("(unpickleable) "+repr(result))
    except BaseException as e:
        q.put(e)

def iowrapper(tocall, inputs, args, kwargs, q):
    newio = CustomIO(*inputs)
    try:
        sys.stdout, sys.stdin = newio, newio
        try: result = tocall(*args, **kwargs)
        except SystemExit: result = None
        try:    q.put(result)
        except: q.put("(unpickleable) "+repr(result))
        q.put(newio.printed)
    except BaseException as e:
        q.put(e)
        q.put(newio.printed)

def iowrapper2(tocall, inputs, args, kwargs, q):
    newio = CustomIO(*inputs)
    try:
        sys.stdout, sys.stdin = newio, newio
        try: tocall(*args, **kwargs)
        except SystemExit: pass
        q.put(newio.printed)
    except BaseException as e:
        q.put(e)


def run(timeout, tocall, *args, **kwargs):
    '''Runs the provided callable with a timeout (expressed in seconds)
    returns either (True, None) on a timeout or (False, returnValueOfCallable) if callable completes
    
    If the callable throws an exception, the exception is passed back as the return value
    
    WARNING: because threads may not be interrupted and processes cannot share stdin,
    this will detach the called method from stdin
    
    WARNING: return values that cannot be pickle'd will not be returned

    Example:
    ---
>>> import timeout
>>> def foo(n):
...     tmp = [0]
...     while len(tmp) < n:
...         tmp.append(max(tmp)+min(tmp))
...         tmp.sort()
...         tmp.reverse()
...     return len(tmp)
...
>>> timeout.run(0.1, foo, 10)
(False, 10)
>>> timeout.run(0.1, foo, 10000)
(True, None)
>>> timeout.run(0.1, foo, {})
(False, TypeError('unorderable types: int() < dict()',))
    ---
    '''
    q = Queue()
    p = Process(target=wrapper, args=(tocall, args, kwargs, q))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        return True, None
    else:
        try:
            return False, q.get(True, timeout)
        except:
            return False, None


def wrapIO(timeout, tocall, inputs, *args, **kwargs):
    '''Runs the provided callable with a timeout (expressed in seconds)
    and the provided set of input lines (a list with no trailing newlines).
    returns either (True, None, []) on a timeout 
    or (False, returnValueOfCallable, [list,of,outputs]) if callable completes
    The first output is what was printed before the first line was read, etc.
    The length of the list is always 1 more than the number of lines read.
    
    If the callable throws an exception, the exception is passed back as the return value
    
    Example:
    ---
>>> import timeout, runpy
>>> with open("example.py") as f: print(f.read())
...
x = input("How many do you want? ")
while x not in ['0','1']:
    print("Sorry, there is only one available; I can't give you "+x+".")
    x = input("How many do you want? ")
print("Thanks for requesting "+x+".")    
>>> timeout.wrapIO(0.1, runpy.run_module, ['3','0.5','1'], 'example')
(False, {'x': '1'}, ['How many do you want? ', "Sorry, there is only one available; I can't give you 3.\nHow many do you want? ", "Sorry, there is only one available; I can't give you 0.5.\nHow many do you want? ", 'Thanks for requesting 1.\n'])
    ---
    '''
    q = Queue()
    p = Process(target=iowrapper, args=(tocall, inputs, args, kwargs, q))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        return True, None, []
    else:
        a, b = None, []
        try:
            a = q.get(True, timeout)
            b = q.get(True, timeout)
        except: pass
        return False, a, b


def runModuleNoOutput(modname):
    runpy.run_module(modname)

def wrapModuleIO(timeout, modname, inputs):
    '''Like wrapIO, but for modules instead of functions.
    Needs to be separate because runpy has lots of... quirks.
    
    returns either (True, []) on a timeout 
    or (True, Exception object) on an exception
    or (False, [list, of, outputs]) if callable completes.
    The first output is what was printed before the first line was read, etc.
    The length of the list is always 1 more than the number of lines read.
    
    If the callable throws an exception, the exception is passed back as the return value
    
    Example:
    ---
>>> import timeout
>>> with open("example.py") as f: print(f.read())
...
x = input("How many do you want? ")
while x not in ['0','1']:
    print("Sorry, there is only one available; I can't give you "+x+".")
    x = input("How many do you want? ")
print("Thanks for requesting "+x+".")    
>>> timeout.wrapModuleIO(0.1, 'example', ['3','0.5','1'])
(False, ['How many do you want? ', "Sorry, there is only one available; I can't give you 3.\nHow many do you want? ", "Sorry, there is only one available; I can't give you 0.5.\nHow many do you want? ", 'Thanks for requesting 1.\n'])
    ---
    '''
    q = Queue()
    p = Process(target=iowrapper2, args=(runModuleNoOutput, inputs, [modname], {}, q))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        return True, []
    else:
        b = []
        try:
            b = q.get(True, timeout)
        except: pass
        return False, b



__all__ = ['run', 'wrapIO', 'wrapModuleIO']

