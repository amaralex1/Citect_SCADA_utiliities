# Гистограмма количества привязанных объектов к мнемосхемам
import glob
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

inputfile = r'C:\Users\1\Desktop\Работа\ПИК\!РАКУРС\!!ПО\Базы с сигналами\Сводная по мнемосхемам.xlsx'
objfile = r'C:\Users\1\Desktop\MS_objects\ '
df = pd.read_excel(inputfile, sheet_name='Данные')
df['MS_fact'] = ''
files = glob.glob(os.path.join(objfile[:-1], '*.txt'))

for file in files:
    f = open(file, 'r')
    f1 = f.readlines()
    for i in range(0, len(f1)):
        f1[i] = f1[i].replace('\n', '')
    for row in f1:
        df["MS_fact"] = np.where(df['Наименов_0'] == row, df["MS_fact"] + format(os.path.basename(file))[:4], df["MS_fact"])
    f.close()

z = df.loc[df["Уникальное значение"] == 1, "MS_fact"].value_counts()
data = pd.DataFrame()
for i in range(1, 45):
    newrow = {"MS": 'MS'+'{:02d}'.format(i), "count": 0}
    data = data.append(newrow, ignore_index=True)
for row in z.keys():
    duplicated = []
    for foo in [row[i:i + 4] for i in range(0, len(row), 4)]:
        if foo in duplicated:
            continue
        else:
            duplicated.append(foo)
            data.loc[data["MS"] == foo, 'count'] = data.loc[data["MS"] == foo, 'count'] + z[row]

fig, ax = plt.subplots(figsize=(14, 10))
for i, v in enumerate(data['count']):
    ax.text(v + 1, i, "{:.0f}".format(v), color='tomato')
ax.barh(data.MS, data["count"], left=0, height=0.5, color="tomato")
ax.set_yticklabels(data.MS, minor=False)
plt.title('Количество привязанных объектов к мнемосхемам')
plt.xlabel('Количество, шт.')
plt.ylabel('Мнемосхема')
plt.show()
