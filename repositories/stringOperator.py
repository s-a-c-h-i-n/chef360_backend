import json
import re

def splitUnderscores(str):
    strs=str.split('_')
    return strs

def mergeUnderscores(strs):
    str=""
    for i in strs:
        if(str!=""):
            str+="_"
        str+=i
    return str
