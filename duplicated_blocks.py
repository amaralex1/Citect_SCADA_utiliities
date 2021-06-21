# Поиск дубликатов в разных КИС по названию объекта

import os
path = r'C:\Users\1\Desktop\Работа\ПИК\!РАКУРС\!!ПО\Объекты\Электронагреватель\el_nagr_TXT\ '
files = os.listdir(path[:-1])
analyzed = []
for x in files:
    if "analyzed.txt" in x:
        analyzed.append(x)
for i in range(0, len(analyzed)-1):
    for j in range(i+1, len(analyzed)-1):
        f1 = open(path[:-1] + analyzed[i])
        f2 = open(path[:-1] + analyzed[j])
        for f in f1:
            if f in f2:
                print(f + ' встречается в ' + analyzed[i][:9] + ' и в ' + analyzed[j][:9])
        f1.close()
        f2.close()
print(analyzed)
