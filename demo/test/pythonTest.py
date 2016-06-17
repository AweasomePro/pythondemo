import re

p = re.compile(r'(?P<word>\b\w+\b)')
m = p.search('(((( Lots of punctuation )))')