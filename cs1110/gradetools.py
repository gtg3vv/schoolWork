import timeout, runpy, sys, re, timeout2


def student(*args, **kwargs):
    '''Provides a message the student will see as feedback'''
    kwargs['file'] = sys.stdout
    print(*args, **kwargs)

def grader(*args, **kwargs):
    '''Provides a message only the grader will see'''
    kwargs['file'] = sys.stderr
    print(*args, **kwargs)

def output_match(outputs, expected, inputs, message):
    if len(expected) != len(outputs):
        student(message)
        grader("Given",inputs,"got",outputs)
        return False
    cnt=0
    for want,got in zip(expected, outputs):
        cnt += 1
        if want is None: continue
        if 'search' in dir(want):
            if want.search(got): continue
            student(message)
            grader("Given",inputs,"expected output",cnt,"to match regular expression",want.pattern,"but it was",repr(got),"instead")
            return False
        if callable(want):
            if want(got): continue
            student(message)
            grader("Given",inputs,"output",cnt,"should not be",got)
            return False
        if got == want: continue
        student(message)
        grader("Given",inputs,"expected output",cnt,"to be",repr(want),"but it was",repr(got),"instead")
        return False
    return True

def expect(module, inputs, expected, message, maxtime=0.5, showOtherErrors=True):
    '''A testing harness for console I/O programs.  Parameters are:
    module: the string name of a modeul to run (e.g. "hello" will run hello.py)
    inputs: a list of inputs to simulate the user typing
    expected: a list of expected outputs.  Should be 1 longer than inputs.  The
        first will be matched against things printed before requesting input,
        the second against things between the first and second input, etc.,
        with the last matched against things printed after the last input.
        May contains strings (matched with ==), re.compile(...) objects (matched
        with search), or None (meaning no checks on this piece of input).'''
    timedOut, outputs = timeout.wrapModuleIO(maxtime, module, inputs)
    if timedOut:
        student("File took too long; did you have an infinite loop?")
        grader("Given",inputs,"timed out after",maxtime,"seconds")
        return False
    if type(outputs) is EOFError:
        student("Your program tried to read more inputs than it should have needed.")
        grader("Given",inputs,"tried to read at least",len(inputs)+1,"inputs.")
        return False
    elif type(outputs) is NameError:
        student("You tried to use a variable that is not available in scope: " + message)
        grader("Failed test " + message + " with a variable used not in scope.")
        return False
    elif type(outputs) is TypeError:
        student("You tried to use a variable that is not allowed with its particular type (i.e. add a string to an int): " + message)
        grader("Failed test " + message + " with a type error.")
        return False
    elif type(outputs) is KeyError:
        student("You tried to access something from a dictionary or list that does not exist: " + message)
        grader("Failed test " + message + " with a missing key error.")
        return False
    elif type(outputs) is ValueError:
        student("You tried to access something that does not exist: " + message)
        grader("Failed test " + message + " with a value error.")
        return False
    elif type(outputs) is IndexError:
        student("You tried to access an index in a list that is beyond the size of the list: " + message)
        grader("Failed test " + message + " with an index out of bounds error.")
        return False
    elif isinstance(outputs, BaseException):
        if showOtherErrors:
            student(message, '\n    your program failed with an exception:\n   ',repr(outputs))
        else:
            student(message)
        grader("Given",inputs,"threw exception",outputs)
        return 0
    if len(expected) != len(outputs):
        student(message)
        grader("Given",inputs,"got",outputs)
        return False
    
    return output_match(outputs, expected, inputs, message)

def test_func(mname, fname, retval, output, args, inputs=[], full=False):
    '''A testing harness for functions.
    mname: the name of a module
    fname: the name of a function in that module
    retval: the expected return value
    output: the expected values to be printed
    inputs: the things to simulate the user typing
    full: if Frue, checks outputs and None return type; if False does not
    returns 0 or 1 (if not full) or 0, 1, 2, or 3 (if full)
    '''
    try:
        mod = safeImport(mname)
        if isinstance(mod, BaseException):
            student(mname+'.py failed to load:\n  ',repr(mod))
            grader(mname+'.py failed to load:\n  ',repr(mod))
            return 0
        elif mod[1] != ['']:
            student(mname+'.py printed within invoking a function; did you forget to remove some debugging or testing code before submitting?')
            grader(mname+'.py printed', mod[1])
            return 0
        else:
            mod = mod[0]
    except BaseException as e:
        if full: grader('file',mname+'.py','could not be parsed', repr(e))
        return 0
    if fname not in dir(mod):
        if full: 
            grader('no',fname,'defined in module', mname)
            student('no',fname,'defined in module', mname)
        return 0
    f = mod.__getattribute__(fname)
    overtime, returned, printed = timeout.wrapIO(1, f, inputs, *args)
    if overtime:
        student(fname, "took too long; did you have an infinite loop?")
        grader("Given",inputs,"timed out after",maxtime,"seconds")
        return 0
    if type(returned) is EOFError:
        student(fname, "tried to read more inputs than it should have needed.")
        grader("Given",inputs,args,"tried to read at least",len(inputs)+1,"inputs.")
        return 0
    elif type(returned) is NameError:
        student(fname, "tried to use a variable that is not available in scope")
        grader("Failed test ",inputs,args," with a variable used not in scope.")
        return 0
    elif type(returned) is TypeError:
        student(fname, "either had the wrong number of arguments or tried to do something that is not allowed with its particular type (i.e. add a string to an int)")
        grader("Failed test ",inputs,args," with a type error.")
        return 0
    elif type(returned) is KeyError:
        student(fname, "tried to access something from a collection that does not exist")
        grader("Failed test ",inputs,args," with a missing key error.")
        return 0
    elif type(returned) is ValueError:
        student(fname, "tried to access something that does not exist")
        grader("Failed test ",inputs,args," with a value error.")
        return 0
    elif type(returned) is IndexError:
        student(fname, "tried to access an index in a list that is beyond the size of the list")
        grader("Failed test ", args, " with an index out of bounds error.")
        return 0
    elif isinstance(returned, BaseException):
        student(fname, 'failed with an exception:\n   ',repr(returned))
        grader("Given",inputs,args,"threw exception",returned)
        return 0
    ans = 1 if full else 0
    if overtime:
        if full: grader(fname,'timed out')
        return ans
    if full:
        if not output:
            if printed == ['']: ans += 1
            else: grader(fname,'printed something')
    if output:
        if output_match(printed, output, inputs, fname+' didn\'t print what we expected it to'):
            ans += 1
        # if printed != output:
        #    grader(fname,tuple(args),'printed',printed,'not',output)
        # else: ans += 1
    if full or (retval is not None):
        try:
            if type(retval) is float:
                if abs(retval - returned) > 1e-5:
                    grader(fname,tuple(args),'returned',returned,'not',retval)
                else: ans += 1
            else:
                if retval != returned:
                    grader(fname,tuple(args),'returned',returned,'not',retval)
                else: ans += 1
        except:
            student(fname, 'returned the wrong type of value; expected a', str(type(retval)).split("'")[1], 'not a', str(type(returned)).split("'")[1])
            grader(fname,tuple(args),'returned',returned,'not',retval)
    return ans

def getSource(module):
    if not module.endswith(".py"): module += ".py"
    with open(module) as f:
        txt = f.read()
    return txt

def checkSource(module, *restrings):
    '''Checks one or more regular expression strings or re.compile(...) objects 
    against the .py file of the specified module and returns which ones are 
    satisfied (as a bool or tuple of bools).  If expressions use /text/gim type 
    syntax, the flags will be honored; g will mean use search and no g will mean 
    use fullmatch. Otherwise, re.search is used with no flags.'''
    if not module.endswith(".py"): module += ".py"
    with open(module) as f:
        txt = f.read()
    ans = [False for f in restrings]
    for i in range(len(restrings)):
        want = restrings[i]
        if 'search' in dir(want):
            if want.search(txt) is not None: ans[i] = True
        elif type(want) is str:
            if len(want) > 2 and want[0] == '/' and want.rfind('/') != 0:
                end = want.rfind('/')
                want, end = want[1:end], want[end+1:]
                flags = 0
                if 'i' in end: flags |= re.IGNORECASE
                if 'm' in end: flags |= re.MULTILINE
                if 's' in end: flags |= re.DOTALL
                if 'g' in end:
                    if re.search(want, txt, flags) is not None: ans[i] = True
                else:
                    if re.fullmatch(want, txt, flags) is not None: ans[i] = True
            else:
                if re.search(want, txt) is not None: ans[i] = True
        else:
            raise Exception("unexpected type "+str(type(want)))
    if len(ans) == 1: return ans[0]
    else: return tuple(ans)


def getmod(mod):
    import sys, timeout
    newio = timeout.CustomIO()
    save = sys.stdout, sys.stdin
    try:
        sys.stdout, sys.stdin = newio, newio
        mod = __import__(mod)
    except BaseException as e:
        return e
    finally:
        sys.stdout, sys.stdin = save
    return mod, newio.printed

def safeImport(mod):
    '''imports a module and returns either (a) an Exception or (b) (the module object, anything the module printed)
    '''
    return timeout2.captime(5, getmod, [mod])

