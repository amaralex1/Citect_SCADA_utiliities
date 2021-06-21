import glob
import os
import pandas as pd
import numpy as np

inputfile = r'C:\Users\rangin\Desktop\MS_objects\Сводная по мнемосхемам.xlsx'
objfile = r'C:\Users\rangin\Desktop\MS_objects\ '
df = pd.read_excel(inputfile, sheet_name='Данные')
df['MS_fact'] = ''
naimen_0 = df["Наименов_0"].unique().tolist()
naimen_0 = [x for x in naimen_0 if str(x) != 'nan']  # Убираем NaN
files = glob.glob(os.path.join(objfile[:-1], '*.txt'))

for file in files:
    f = open(file, 'r')
    f1 = f.readlines()
    for i in range(0, len(f1)):
        f1[i] = f1[i].replace('\n', '')
    for row in f1:
        df["MS_fact"] = np.where(df['Наименов_0'] == row, df["MS_fact"] + format(os.path.basename(file))[:4], df["MS_fact"])
    f.close()

for name in naimen_0:
    ms_fact = str(df.loc[df['Наименов_0'] == name]["MS_fact"].values[0]).replace('MS', '')
    m = ''
    for slice in [ms_fact[i:i+2] for i in range(0, len(ms_fact), 2)]:
        m = m + slice + '+'

    mnem = str(df.loc[df['Наименов_0'] == name]["MS"].values[0]).replace('МС', '').replace('MC', '').replace('nan', '')
    ms_fact = m
    if mnem not in ms_fact:
        if ms_fact == '':
            print(f'Объект {name} по сводной таблице мнемосхем находится на МС{mnem}, по факту не привязан ({ms_fact})')
        else:
            if mnem == '':
                print(f'Объект {name} по сводной таблице мнемосхем не привязан к мнемосхема ({mnem}), по факту привязан в {ms_fact}')
            else:
                print(f'В объекте {name} мнемосхема по таблице {mnem} и по факту {ms_fact} отличается ')

