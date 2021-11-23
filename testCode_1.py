x = 9
if x == 2:
    raise ValueError(Val("gas"))

cfgpath = "cfg.txt"
with open(cfgpath) as file:
    readfile = file.read()
    rawlines = readfile.split('\n')
    lines = []
    for rawline in rawlines:
        if len(rawline.split("->")) == 2:
            lines.append(rawline.split("->"))