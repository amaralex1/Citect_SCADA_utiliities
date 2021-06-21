import os
from os import listdir
from os.path import isfile, join


def diff(list1, list2):
    return (list(list(set(list1)-set(list2)) + list(set(list2)-set(list1))))


directory1 = r'C:\Users\1\Desktop\PLC code\2020_08_24 13_56'
dirlist1 = [x[0] for x in os.walk(directory1)]
directory2 = r'C:\Users\1\Desktop\PLC code\2020_08_24 17_22'
dirlist2 = [x[0] for x in os.walk(directory2)]
# difdirrlist1 = list(map(lambda x: x.replace(directory1, ""), dirlist1))
# difdirrlist2 = list(map(lambda x: x.replace(directory2, ""), dirlist2))
# print(diff(difdirrlist1, difdirrlist2))
allfiles1 = []
allfiles2 = []
difference = []
for folder in dirlist1:
    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
    for n, i in enumerate(onlyfiles):
        onlyfiles[n] = folder + '\\' + onlyfiles[n]
    allfiles1.append(onlyfiles)
for folder in dirlist2:
    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
    for n, i in enumerate(onlyfiles):
        onlyfiles[n] = folder + '\\' + onlyfiles[n]
    allfiles2.append(onlyfiles)
for file in allfiles1:
    try:
        with open(file[0], 'r') as f1:
            next(f1)
            text1 = ''
            for line in f1:
                text1 = text1 + line
    except FileNotFoundError:
        print(f'Нет файла {file[0]}')
    try:
        with open(file[0].replace(directory1, directory2), 'r') as f2:
            next(f2)
            text2 = ''
            for line in f2:
                text2 = text2 + line
    except (FileNotFoundError, StopIteration) as e:
        print(f'Нет файла {file[0].replace(directory1, directory2)}')
    if text1 != text2:
        difference.append(file[0])
print(f'Разница между версий в файлах: {difference}')
