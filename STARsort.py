import argparse

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--i",help="Input the list of STAR .out file",type=str)
parser.add_argument("--o",help="Output file",type=str)
args = parser.parse_args()

file = args.i
ans = {}
item = []
with open(file,"r") as r:
    for i in r:
        if i[-1] == "\n":
            STARfile = i[:-1]
        else:
            STARfile = i
        with open(STARfile,"r") as r:
            ans[STARfile] = {}
            for i in r:
                line = i.split("|")
                if len(line) < 2:
                    pass
                else:
                    while line[0][0] == " " or line[0][0] == "\t" or line[0][0] == "\n":
                        line[0] = line[0][1:]
                    while line[0][-1] == " " or line[0][-1] == "\t" or line[0][-1] == "\n":
                        line[0] = line[0][:-1]
                    while line[1][0] == " " or line[1][0] == "\t" or line[1][0] == "\n":
                        line[1] = line[1][1:]
                    while line[1][-1] == " " or line[1][-1] == "\t" or line[1][-1] == "\n":
                        line[1] = line[1][:-1]
                    ans[STARfile][line[0]] = line[1]
                    if line[0] not in item:
                        item.append(line[0])
items = ["file"] + item

file = args.o
with open(file,"w",encoding="utf-8",newline="") as w:
    w.write("\t".join(items)+"\n")
    for i in ans.keys():
        line = [i]
        for item in items[1:]:
            if item in ans[i].keys():
                line.append(ans[i][item])
            else:
                line.append("")
        w.write("\t".join(line)+"\n")
