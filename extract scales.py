import pandas as pd
import re

inputfile = r'C:\Users\1\Desktop\input_AI\file.txt'
outputfile = r'C:\Users\1\Desktop\input_AI\file.xlsx'
f = open(inputfile, 'r')
name = 'fail'
EU = 'fail'
min_scale = 'fail'
max_scale = 'fail'
index = 0
df = pd.DataFrame(columns=['Наименов_0', 'Min_Scale', 'Max_Scale', 'EU'])
for line in f:
    if 'UDT :=' in line:
        if name != 'fail':
            df.at[index, 'Наименов_0'] = name
            df.at[index, 'Min_Scale'] = min_scale
            df.at[index, 'Max_Scale'] = max_scale
            df.at[index, 'EU'] = EU
            index = index + 1
        name = line.split('_block')[0].split('(')[0].replace(',', '').replace(';', '').replace(')', '').strip()
    if 'Scale_min' in line:
        min_scale = line.split(':=')[1].split('(')[0].replace(',', '').replace(';', '').replace(')', '').strip()
    if 'Scale_max' in line:
        max_scale = line.split(':=')[1].split('(')[0].replace(',', '').replace(';', '').replace(')', '').strip()
    if 'eдиницы измерения параметра' in line:
        try:
            EU = re.search(r'\[.{1,10}\]', line.split('eдиницы измерения параметра')[1]).group(0)[1:-1].strip()
        except AttributeError:
            pass
df.at[index, 'Наименов_0'] = name
df.at[index, 'Min_Scale'] = min_scale
df.at[index, 'Max_Scale'] = max_scale
df.at[index, 'EU'] = EU
index = index + 1
fyv = df.loc[df['Наименов_0'] == "Y0A01010_0"]["EU"]
df.to_excel(outputfile)
f.close()
