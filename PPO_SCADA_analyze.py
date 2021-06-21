import pandas as pd
from dbfread import DBF


def readdbftolistofdict(name):
    equip = DBF(name, encoding='cp1251', load=True)
    outputlist = []
    for record in equip:
        recorddict = {}
        for key, value in record.items():
            recorddict[key] = value
        if recorddict['IODEVICE'] == 'OFSDevice':
            outputlist.append(recorddict)
    return outputlist


# Формирование списка словарей equip, который содержит данные из ППО СКАДА
DBFFile = r'C:\ProgramData\Schneider Electric\Citect SCADA 2016\User\Current_20_03_16\equip.dbf'
equip = readdbftolistofdict(name=DBFFile)
dbfequip = pd.DataFrame(equip[0], index=[0])
for record in equip[1:]:
    # print(record['NAME'])
    dbfequip = dbfequip.append(record, ignore_index=True)
# Формирование DataFrame с данными из excel базы данных
inputfile = r'C:\Users\1\Desktop\Работа\ПИК\!РАКУРС\!!ПО\Базы с сигналами\Старое\Бэкап от 29062020 Ревизия + WORK_10998_from 19дек 13-40+Сводная.xlsx'
df = pd.read_excel(inputfile, sheet_name='Лист1')
naimen_0 = df["Наименов_0"].unique().tolist()
naimen_0 = [x for x in naimen_0 if str(x) != 'nan']  # Убираем NaN

# Словари, ключи которых - название в базе Excel, а значение - название в базе ППО СКАДА, для составления соответствия между записями
type_aliases = {'AI': 'AI_udt',
                'Сигн AI': 'AI_sign_udt',
                'вентилятор': 'vent_udt',
                'Клапан': 'Valve_udt',
                'kid': 'Valve_kid_udt',
                'AI_complicate': 'AI_cmp_udt',
                'Signalizator': 'Sign_udt',
                'Насос': 'Pump_udt',
                'el_nagr': 'el_nagr_udt',
                'flt_rulon': 'flt_rulon_udt',
                'мешалка': 'mesh_udt',
                'Шибер': 'shiber_udt'}
eu_aliases = {'Гр.С': 'Гр.С',
              r'куб.м/ч': r'куб.м/ч',
              'МПа': 'мПа',
              'мПа': 'мПа',
              'град.С': 'град.С',
              'мм': 'мм',
              r'М3/Ч': r'куб.м/час',
              'NO_INF': 'отс инф',
              '%': '%',
              r'г/л': r'г/л',
              'кПа': 'кПа',
              'КПа': 'кПа',
              'мм рт.ст': 'мм рт.ст.',
              r'КГС/СМ2': r'КГС/СМ2',
              'м': 'м',
              r'м/с2': 'отс инф',
              r'кг/ч': r'кг/ч',
              r'л/ч': r'л/ч',
              r'моль/л': r'моль/л',
              'pH': 'pH',
              r'мкСм/см': r'мкСм/см',
              r'мг/куб.м': r'мг/куб.м',
              r'мг/л': 'мг/л'}

object_name_flag = []
for name in naimen_0:
    KIS = df.loc[df['Наименов_0'] == name]["Номер КИС к родителю"].values[0]
    object_type = df.loc[df['Наименов_0'] == name]["Тип объекта"].values[0]
    try:
        KIS_equip = dbfequip.loc[dbfequip['TAGPREFIX'] == name]["CUSTOM3"].values[0]
    except IndexError:
        print(f'В DBF отсутствует переменная {name}')
        continue
    object_type_equip = dbfequip.loc[dbfequip['TAGPREFIX'] == name]["TYPE"].values[0]
    if str(KIS)[3:].replace('.', '_') != KIS_equip:
        print(f'Номер КИС к родителю и CUSTOM3 не совпадают для объекта {name}, Excel - {KIS}, DBF - {KIS_equip}')
    try:
        if type_aliases[str(object_type).strip()].lower() != object_type_equip.lower():
            print(f'Тип объекта и TYPE не совпадают для объекта {name}, Excel - {object_type}, DBF - {object_type_equip}')
    except KeyError:
        pass
    if object_type == 'AI' or object_type == 'Сигн AI':
        object_name = name.split('_')[0]
        if object_name in object_name_flag:
            pass
        else:
            object_name_flag.append(object_name)
            # Проверка правильности заполнения поля CUSTOM1 (Количество каналов сигнала)
            quantity = sum(object_name in s for s in naimen_0)
            custom1 = dbfequip.loc[dbfequip['TAGPREFIX'] == name]["CUSTOM1"].values[0]
            if custom1 != '':
                if custom1 != str(quantity):
                    print(f'Поле с количеством каналов в ППО СКАДА заполнено не верно для объекта {name}, - тип - {object_type}, CUSTOM1 - {custom1}, количество каналов объекта - {quantity}')
            else:
                print(f'Поле с количеством каналов в ППО СКАДА не заполнено для объекта {name}, тип - {object_type}, количество каналов объекта - {quantity}')
            try:
                custom6 = dbfequip.loc[dbfequip['TAGPREFIX'] == name]["CUSTOM6"].values[0]
                custom7 = dbfequip.loc[dbfequip['TAGPREFIX'] == name]["CUSTOM7"].values[0]
                custom8 = dbfequip.loc[dbfequip['TAGPREFIX'] == name]["CUSTOM8"].values[0]
                scale_max = df.loc[df['Наименов_0'] == name][df['Тип сигнала'] == 'А']["верхний предел парам"].values[0]
                scale_min = df.loc[df['Наименов_0'] == name][df['Тип сигнала'] == 'А']["нижн предел парам"].values[0]
                eng_units = df.loc[df['Наименов_0'] == name][df['Тип сигнала'] == 'А']["Единицы измер параметра"].values[0]
                if custom8 == 'КПа':
                    print(f'В объекте {name} изменить единицы измерения с "КПа" на "кПа"')
                if custom8 == 'мПа':
                    print(f'В объекте {name} изменить единицы измерения с "мПа" на "МПа"')
                if custom6 == '' or custom7 == '' or custom8 == '':
                    print(f'Незаполненные поля в ППО СКАДА для объекта {name} - CUSTOM6 = {custom6}, по базе - {scale_max}, CUSTOM7 = {custom7}, по базе - {scale_min}, CUSTOM8 = {custom8}, по базе - {eng_units}')
                else:
                    # Проверка правильности заполнения поля CUSTOM6 (верхнее значение диапазона)
                    if str(scale_max) == 'отс инф':
                        print(f'Верхний предел параметра для объекта {name} не задано в базе Excel - {scale_max} , в ППО СКАДА - "{custom6}"')
                    else:
                        if str(scale_max).replace(',', '.') != str(custom6):
                            print(f'Верхний предел параметра для объекта {name} отличается в базе Excel - {scale_max} и в ППО СКАДА - "{custom6}"')
                    # Проверка правильности заполнения поля CUSTOM7 (нижнее значение диапазона)
                    if str(scale_min) == 'отс инф':
                        print(f'Нижний предел параметра для объекта {name} не задано в базе Excel - {scale_min} , в ППО СКАДА - "{custom7}"')
                    else:
                        if str(scale_min).replace(',', '.') != str(custom7):
                            print(f'Нижний предел параметра для объекта {name} отличается в базе Excel - {scale_min} и в ППО СКАДА - "{custom7}"')
                    # Проверка правильности заполнения поля CUSTOM8 (единицы измерения параметра)
                    if str(eng_units) == 'отс инф':
                        print(f'Единицы измерения для объекта {name} не задано в базе Excel - {eng_units} , в ППО СКАДА - {custom8}')
                    else:
                        if str(eng_units).lower() != eu_aliases[str(custom8)].lower():
                            print(f'Единицы измерения для объекта {name} отличается в базе Excel - {eng_units} и в ППО СКАДА - {custom8}')
            except IndexError:
                print(f'В объекте {name} типа {object_type} отсутствует аналоговый сигнал')
