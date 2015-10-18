# Parses json and collects interesting data

import json
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))
print fileDir

def readFile(filename):
    filehandle = open(filename)
    for line in filehandle:
        print line
    # print filehandle.read()
    filehandle.close()

#For accessing the file in the parent folder of the current folder
filename = os.path.join(fileDir, '../output/foo.jl')
readFile(filename)