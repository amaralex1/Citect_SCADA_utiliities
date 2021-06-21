import glob
import os
folder = r'C:\Users\rangin\Desktop\MS_tags\ '
folderobj = r'C:\Users\rangin\Desktop\MS_objects\ '
files = glob.glob(os.path.join(folder[:-1], '*.txt'))
for file in files:
    inputfile = open(file, 'r')
    outputfile = open(folderobj[:-1] + file.split("\\")[-1], 'w+')
    inputlist = []
    ilist = []
    forbidden_combos = ('ST01', 'RG01', 'AM01', 'ST02', 'ST03', 'RJ01', 'AM02', 'AM03')
    forbidden_combos = tuple([x+'\n' for x in forbidden_combos])
    for line in inputfile:
        ilist.append(line)
    for line in ilist:
        if line.split('_')[:2] in inputlist:
            continue
        else:
            try:
                if not line.split('_')[1].endswith(forbidden_combos):
                    inputlist.append(line.split('_')[:2])
            except IndexError:
                continue
    for line in inputlist:
        if line.__len__() > 1:
            outputfile.write(line[0] + '_' + line[1] + '\n')
        else:
            outputfile.write(line[0] + '\n')
