import struct

l = ["1"]

with open("data", "wb") as fout:
    for x in l:
        fout.write(x.encode())