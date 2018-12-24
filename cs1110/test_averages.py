from gradetools import grader, student, test_func


correct = 0
mod = 'averages'







import ast

def has_loops(astnode):
    for part in ast.walk(astnode):
        if isinstance(part, ast.For): return True
        if isinstance(part, ast.While): return True
    return False

opnames = {
    ast.Add : '+',
    ast.Sub : '-',
    ast.Mult : '*',
    ast.Div : '/',
    ast.Mod : '%',
    ast.Pow : '**',
    ast.FloorDiv : '//',
}

def name_as_string(astnode):
    if isinstance(astnode, ast.Attribute):
        return name_as_string(astnode.value)+'.'+name_as_string(astnode.attr)
    if isinstance(astnode, ast.Name):
        return name_as_string(astnode.id)
    if isinstance(astnode, ast.NameConstant):
        return name_as_string(astnode.value)
    return str(astnode)

def invokes_and_operators(astnode):
    ans = []
    for part in ast.walk(astnode):
        if isinstance(part, ast.Call): 
            ans.append(name_as_string(part.func))
        if isinstance(part, ast.BinOp): 
            for key in opnames:
                if isinstance(part.op, key):
                    ans.append(opnames[key])
    return ans

funcs = {}

with open(mod+'.py') as f:
    src = f.read()
    tree = ast.parse(src, mod+'.py')
    for kid in ast.iter_child_nodes(tree):
        if isinstance(kid, ast.FunctionDef):
            funcs[str(kid.name)] = has_loops(kid), invokes_and_operators(kid)









fcor = 0
func = 'mean'
try:
    fcor += test_func(mod, func, 2.0, None, [2, 2, 2], full=True)
    fcor += test_func(mod, func, 2.0, None, [1, 2, 3])
    fcor += test_func(mod, func, 8.0/3, None, [1, 1, 6])
except:
    student("something unexpected happened in our autograding; your score below might be incorrectly small")
student(func+' passed', fcor, 'out of', 5, 'automated test cases')

correct += fcor

fcor = 0
func = 'median'
try:
    fcor += test_func(mod, func, 2.0, None, [2, 2, 2], full=True)
    fcor += test_func(mod, func, -2.0, None, [-3, -1, -2])
    fcor += test_func(mod, func, -2.0, None, [-3, -2, -1])
    fcor += test_func(mod, func, -2.0, None, [-2, -3, -1])
    fcor += test_func(mod, func, -2.0, None, [-1, -3, -2])
    fcor += test_func(mod, func, -2.0, None, [-1, -2, -3])
    fcor += test_func(mod, func, -2.0, None, [-2, -1, -3])
except:
    student("something unexpected happened in our autograding; your score below might be incorrectly small")
student(func+' passed', fcor, 'out of', 9, 'automated test cases')

correct += fcor

fcor = 0
func = 'rms'
try:
    fcor += test_func(mod, func, 2.0, None, [2, 2, 2], full=True)
    fcor += test_func(mod, func, 2.160246899469287, None, [1, 2, 3])
    fcor += test_func(mod, func, 3.559026084010437, None, [1, 1, 6])
    if func in funcs and funcs[func][1].count('mean') == 1: fcor += 1
    else: student(func, 'was supposed to invoke mean once')
except:
    student("something unexpected happened in our autograding; your score below might be incorrectly small")
student(func+' passed', fcor, 'out of', 6, 'automated test cases')

correct += fcor


fcor = 0
func = 'middle_average'
try:
    fcor += test_func(mod, func, 8/3, None, [1, 1, 6], full=True)
    fcor += test_func(mod, func, 4.932882862316247, None, [1, 6, 6])
    fcor += test_func(mod, func, .1, None, [.1, -.6, .6])
    if func in funcs and funcs[func][1].count('mean') == 1: fcor += 1
    else: student(func, 'was supposed to invoke mean once')
    if func in funcs and funcs[func][1].count('rms') == 1: fcor += 1
    else: student(func, 'was supposed to invoke rms once')
    if func in funcs and funcs[func][1].count('median') == 2: fcor += 1
    else: student(func, 'was supposed to invoke median twice')
except:
    student("something unexpected happened in our autograding; your score below might be incorrectly small")
student(func+' passed', fcor, 'out of', 8, 'automated test cases')

correct += fcor










grader('Score:', correct, '/', 28)
