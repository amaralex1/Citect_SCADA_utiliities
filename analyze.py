import pandas as pd
inputfile = r'C:\Users\1\Desktop\Работа\ПИК\!РАКУРС\!!ПО\Базы с сигналами\Старое\Бэкап от 29062020 Ревизия + WORK_10998_from 19дек 13-40+Сводная.xlsx'
df = pd.read_excel(inputfile, sheet_name='Лист1')
# print(df.head())
naimen_0 = df["Наименов_0"].unique().tolist()
naimen_0 = {x for x in naimen_0 if x == x}  # Убираем NaN
questionable_names = []
for name in naimen_0:
    # print(str(name)+'\n')
    types = df.loc[df['Наименов_0'] == name]["Вход блока"]
    unique_types = types.unique()
    duplicated_types = types.duplicated()
#    if len(types) > 1:
    if "True" in str(duplicated_types):
        print(str(name)+str(unique_types))
        questionable_names.append(name)
print('end')
