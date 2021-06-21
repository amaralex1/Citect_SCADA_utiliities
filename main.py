path = r'C:\Users\1\Desktop\Работа\ПИК\!РАКУРС\!!ПО\Объекты\Электронагреватель\el_nagr_TXT\ '
filenames = [["KIS_336_1", 1],
             ["KIS_336_2", 1],
             ["KIS_336_3", 1],
             ["KIS_320_1", 0],
             ["KIS_420_1", 1],
             ["KIS_420_2", 1],
             ["KIS_420_3", 1],
             ["KIS_420_4", 1],
             ["KIS_420_5", 1],
             ["KIS_420_6", 1],
             ["KIS_420_7", 1]]

# filename = path + r'KIS_420_7_Ventilator'
for filename in filenames:
    if filename[1] == 1:
        outputfile = path[:-1] + filename[0] + '_analyzed.txt'
        f = open(path[:-1] + filename[0] + '_Nasos' + '.txt', "r")
        list_of_blocks = []
        for x in f:
            if "_block" in x:
                list_of_blocks.append(x.split("_block")[0])
        f.close()
        print(list_of_blocks)
        print(list_of_blocks.__len__())
        f = open(outputfile, "w")
        for row in list_of_blocks:
            f.write(row+'\n')
