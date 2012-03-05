def pm_tree(bot,parts):
    try:
        size= int(parts[3].split()[-1])
    except:
        return "enter size"
    if size > 40:
        return "too big"
    ret = ""
    for x in range(size):
        ret += (size-x) * " " + "/" + (x * 2) * " " + "\\" + "\n"
    ret += " " + "-" * (size * 2) + "\n"
    for x in range(int(size * .25) + 1):
        ret += " " * int(size * .75) + "\"" + " " * (size /2) + "\"" + "\n"
    return ret
    
def pm_cock(bot,parts):
    try:
        size= int(parts[3].split()[-1])
    except:
        return "enter size"
    if size > 40:
        return "too big"
    ret = ""
    ret += size * " " + (size*2) * "#" + "\n"
    for x in range(size - 2):
        ret += size * " " + "#" + ((size * 2) - 2) * " " + "#\n"
    ret += size * " " + ((size/4) + 1) * "#" + (int(size * 1.5) - 2) * " " + ((size/4) + 1) * "#" + "\n"
    for x in range(int(size * 2.5)):
        ret += int(1.25 * size) * " " + "#" + (int(size * 1.5) - 2) * " " + "#\n"
    ret += (int(1.25 * size) + 1) * "#" + (int(size*1.5) - 2) * " " + (int(1.25 * size) + 1) * "#" + "\n"
    for x in range(int(size * .75)):
        ret += "#" + ((size * 4) - 2) * " " + "#\n"
    ret += (4 * size) * "#"
    return ret