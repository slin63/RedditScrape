# Parses json and collects interesting data

import json
from os import path, chroot

chroot = ("tutoral/spiders")  # "ch.ange root"
file_placeholder = path.relpath("output/foo.jl")

def open_json(file):
    open(file, 'r')

open_file = open(file_placeholder, 'rb')

for line in open_file:
    print line