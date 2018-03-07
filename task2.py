#! /usr/bin/env python
def combine(a,b):
    if not type(a) == type(b): return None
    if type(a) == int or type(a) == float: return a*b
    if type(a) == str: return '.'.join([a,b])
    if type(a) == list: return a+b
print(combine(3,2))
print(combine("James","D"))
print(combine([1,2],["hey"]))

l = ['James',1.23,True,['Luna','Loves','James'],[1,'hey'],13]
for i in l:
    if type(i) == list:
        try:
            print(' '.join(i))
        except TypeError as e:
            print(e)
