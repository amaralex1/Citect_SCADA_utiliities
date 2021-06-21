import pandas as pd


def importdf(filename, sheet):
    dataframe = pd.read_excel(filename, sheet_name=sheet)
    return dataframe


inputfile = r'C:\Users\1\Desktop\Работа\ПИК\!РАКУРС\!!ПО\Базы с сигналами\Копия WORK_10998_from 19дек 13-40+Сводная.xlsx'
outputfile = r'C:\Users\1\Desktop\Работа\ПИК\!РАКУРС\!!ПО\Базы с сигналами\WORK_10998_from 14авг 13-00+Сводная.xlsx'
sheetname = 'Лист1'
df = importdf(inputfile, sheetname)
df['Номер элемента в массиве пересылки'] = ''
df.sort_values(by=['Код'])
indexes = {
    "КИС320.1": 0,
    "КИС336.1": 0,
    "КИС336.2": 0,
    "КИС336.3": 0,
    "КИС420.1": 0,
    "КИС420.2": 0,
    "КИС420.3": 0,
    "КИС420.4": 0,
    "КИС420.5": 0,
    "КИС420.6": 0,
    "КИС420.7": 0}
for index, row in df.iterrows():
    if row['Номер КИС'] != row['Номер КИС к родителю'] and "КИС" in str(row['Номер КИС к родителю']):
        df.at[index, 'Номер элемента в массиве пересылки'] = indexes[row['Номер КИС к родителю']]
        indexes[row['Номер КИС к родителю']] = indexes[row['Номер КИС к родителю']] + 1

df.to_excel(inputfile, sheet_name=sheetname)
print(indexes)

