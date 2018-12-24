import re

import re

text= ''
nospace = re.compile(r'\|\S[^\"]*"')
quotation = re.compile(r'\"\S[^\"]*"')
twonum = re.compile(r'[0-9]|^{[0-9]\.\.]]')
likely_name = re.compile(r'[a-z]|[a-z]+\.+[a-z]*|^[a-z]+\.')