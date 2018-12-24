import random

def ellipses(s):
    return s[:2] + "..." + s[-2:]
    
def eighteen(s):
    return s[0] + (str(len(s)-2) if len(s) >= 2 else str(0)) + s[-1]

def allit(s1, s2):
    return s1.upper().startswith(s2.upper()[0])
    
def between(s1, s2):
    a = s1.find(s2)
    if a == -1:
        return None
    b = s1.find(s2, a+1, len(s1)-1)
    if  b == -1:
        return None
    return s1[a+len(s2):b]
    
def rbetween(s1, s2):
    a = s1.rfind(s2)
    if a == -1:
        return None
    b = s1.rfind(s2, 0, a)
    if  b == -1:
        return None
    return s1[b+len(s2):a]
    
def rand_between(s1,s2):
    return random.choice([between(s1,s2),rbetween(s1,s2)])
    
def temperature(s):
    return s[s.find('class="myforecast-current-lrg">')+31:s.find('deg;F')-1]
    
def unhide(s):
    s = s.replace(' at ', '@').replace(' (at) ', '@').replace(' AT ','@')
    return s.replace(' dot ', '.').replace(' (dot) ', '.').replace(' DOT ','.')

def vowel_confusion(s):
    s = s.replace('e','~~/').replace('E', '~/~')
    s = s.replace('I','E').replace('i','e')
    return s.replace('~~/', 'i').replace('~/~', 'I')

print(ellipses("computer science"))
print(eighteen("fun"))
print(allit("hi", 'Hello'))
print(between("loan me a lovely loon to look at", "lo"))
print(rbetween("loan me a lovely loon to look at", "lo"))
print(rand_between("loan me a lovely loon to look at", "lo"))
print(temperature('<p class="myforecast-current-lrg">83&deg;F</p>'))
print(unhide("mst3k (at) virginia (dot) edu"))
print(vowel_confusion("I sang, and thought I sang very well; but he just looked up into my face with a very quizzical expression, and said, 'How long have you been singing, Mademoiselle?'"))