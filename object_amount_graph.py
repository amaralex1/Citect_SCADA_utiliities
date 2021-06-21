#  Гистограмма количества объектов по типам объектов
import matplotlib.pyplot as plt
import pandas as pd


inputfile = r'C:\Users\1\Desktop\Работа\ПИК\!РАКУРС\!!ПО\Базы с сигналами\Копия WORK_10998_from 19дек 13-40+Сводная.xlsx'
df = pd.read_excel(inputfile, sheet_name='Лист1')
df["Тип объекта"] = df["Тип объекта"].str.replace(r'?', '').copy()
df["Тип объекта"] = df["Тип объекта"].str.strip()
y = df.loc[df["Уникальное значение"] == 1]["Тип объекта"].value_counts()
fig, ax = plt.subplots(figsize=(14, 10))
ind = y.max()
for i, v in enumerate(y):
    ax.text(v + 3, i + 0.15, str(v), color='blue', fontweight='bold')
ax.barh(y.keys(), y.values, left=0, height=0.5, color="blue")
ax.set_yticklabels(y.keys(), minor=False)
plt.title('Количество объектов в базе')
plt.xlabel('Количество, шт.')
plt.ylabel('Тип объекта')
plt.show()
