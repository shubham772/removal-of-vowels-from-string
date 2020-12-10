# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 16:19:22 2020

@author: SHUBHAM
"""

def anti_vowel(c):
    newstr = ""
    vowels = ('a', 'e', 'i', 'o', 'u')
    for x in c.lower():
        if x in vowels:
            newstr = c.replace(x, "")        
    return newstr

c =input()

print(anti_vowel(c))