#It will delete the pair reads mapped to different chromosome and rRNA region. Single read will be also deleted
import bamnostic as bs
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--i",help="Input file",type=str)
parser.add_argument("--o",help="Output file",type=str)
args = parser.parse_args()

rRNA = {}
with open("rRNA.txt","r") as r:
    for i in r:
        line = i.split("\t")
        if line[0] not in rRNA.keys():
            rRNA[line[0]] = [[int(line[1])],[int(line[2])]]
        else:
            rRNA[line[0]][0].append(int(line[1]))
            rRNA[line[0]][1].append(int(line[2]))
for i in rRNA.keys():
    rRNA[i][0] = np.array(rRNA[i][0])
    rRNA[i][1] = np.array(rRNA[i][1])

bam = bs.AlignmentFile(args.i,"rb")
ans = bs.AlignmentFile(args.o,"wb")
flag = 1
for i in bam:
    read1 = i
    read2 = next(bam)
    while read1.read_name != read2.read_name:
        read1 = read2
        read2 = next(bam)
    while read1.reference_name != read2.reference_name:
        read1 = next(bam)
        read2 = next(bam)
    if (read1.reference_name not in rRNA.keys()) and (read2.reference_name not in rRNA.keys()):
        ans.write(str(read1))
        ans.write(str(read2))
    else:
        if ((rRNA[read1.reference_name][0] < read1.pos) & (rRNA[read1.reference_name][0] > read1.pos+read1.l_seq)).any() or ((rRNA[read1.reference_name][1] < read1.pos) & (rRNA[read1.reference_name][1] > read1.pos+read1.l_seq)).any():
            flag = 0
        if ((rRNA[read2.reference_name][0] < read2.pos) & (rRNA[read2.reference_name][0] > read2.pos+read2.l_seq)).any() or ((rRNA[read2.reference_name][1] < read2.pos) & (rRNA[read2.reference_name][1] > read2.pos+read2.l_seq)).any():
            flag = 0
        if flag:
            ans.write(str(read1))
            ans.write(str(read2))
        flag = 1
