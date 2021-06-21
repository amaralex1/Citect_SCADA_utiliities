import pandas as pd
import os
from datetime import datetime

def importdf(filename, sheet):
    dataframe = pd.read_excel(filename, sheet_name=sheet)
    return dataframe


def logerror(text):
    ff = open(currentdirname + '\\errors.txt', 'a+')
    ff.write(text + '\n')
    ff.close()


def foo(data, block_inputs):
    parent_KIS = data['Номер КИС к родителю'].values[0]
    if 'КИС' not in str(parent_KIS):
        parent_KIS = data['Номер КИС'].values[0]
    obj_type = data['Тип объекта'].values[0]
    obj_name = data['Наименов_0'].values[0]

    # Print для того, чтобы видеть, что не виснет
    print(f'{obj_name} - {nomer} из {total}')
    print(f'{currentdirname} q {parent_KIS} q {obj_type.replace("?", "q")}  q {parent_KIS} q ')
    #
    try:
        f = open(currentdirname + '\\' + parent_KIS + '\\' + obj_type.replace("?", "q") + " " + parent_KIS + '\\' + obj_type.replace("?", "q") + ' ' + parent_KIS + '.txt', 'a+')
    except FileNotFoundError:
        os.mkdir(currentdirname + '\\' + parent_KIS + '\\' + obj_type.replace("?", "q") + " " + parent_KIS)
        f = open(currentdirname + '\\' + parent_KIS + '\\' + obj_type.replace("?", "q") + " " + parent_KIS + '\\' + obj_type.replace("?", "q") + ' ' + parent_KIS + '.txt', 'a+')

    # Если файл пустой, сделать header
    f.seek(0, os.SEEK_END)  # go to end of file
    if f.tell():  # if current position is truish (i.e != 0)
        f.seek(0)  # rewind the file for later use
    else:
        f.write(f'(*-----------  {parent_KIS} обработка объекта {obj_type}   {datetime.now().strftime("%Y_%m_%d %H:%M:%S")}     --------------------*)\n\n')
    no_AI = 0
    ai_module = 0
    ai_channel = 0
    ai_EU = 0
    ai_scale_min = 0
    ai_scale_max = 0
    ai_rakurs_index = 0
    ai_sign_name = 0
    ai_klemma = 0
    if obj_type == "Сигн AI":
        try:
            ai_module = data.loc[data["Вход блока"] == "In"]["Номер модуля"].values[0]
            ai_channel = data.loc[data["Вход блока"] == "In"]["Канал модуля"].values[0]
            ai_EU = data.loc[data["Вход блока"] == "In"]["Единицы измер параметра"].values[0]
            ai_scale_min = data.loc[data["Вход блока"] == "In"]["нижн предел парам"].values[0]
            ai_scale_max = data.loc[data["Вход блока"] == "In"]["верхний предел парам"].values[0]
            ai_rakurs_index = data.loc[data["Вход блока"] == "In"]["Ракурс индекс"].values[0]
            ai_sign_name = data.loc[data["Вход блока"] == "In"]["Наименование сигн"].values[0]
            ai_klemma = data.loc[data["Вход блока"] == "In"]["Номер клемника и клеммы"].values[0]
            # Добавить запись по объекту
            ## Заголовок
            f.write(f"(*____{obj_name}_____  {ai_module} CH_[{ai_channel}]  eдиницы измерения параметра {ai_EU}  объект {object_counter[KISes.index(parent_KIS)][list(foo_switcher.keys()).index(obj_type)]}*)\n")
            no_AI = 0
        except IndexError:
            logerror(f'Sign AI {obj_name} не содержит AI сигнала')
            f.write(f"(*____{obj_name}_____ БЕЗ AI ]    объект {object_counter[KISes.index(parent_KIS)][list(foo_switcher.keys()).index(obj_type)]}*)\n")
            no_AI = 1

        for inp in block_inputs:
            if inp != "In":
                try:
                    module = data.loc[data["Вход блока"] == inp]["Номер модуля"].values[0]
                    channel = data.loc[data["Вход блока"] == inp]["Канал модуля"].values[0]
                    sign_KIS = data.loc[data["Вход блока"] == inp]["Номер КИС"].values[0]
                    rakurs_index = data.loc[data["Вход блока"] == inp]["Ракурс индекс"].values[0]
                    sign_name = data.loc[data["Вход блока"] == inp]["Наименование сигн"].values[0]
                    klemma = data.loc[data["Вход блока"] == inp]["Номер клемника и клеммы"].values[0]
                    if channel == 'не опред' or module == 'A0СУ':
                        logerror(f'не определен канал или модуль для {rakurs_index}')
                        continue
                    if parent_KIS == sign_KIS:
                        f.write(f'{obj_name}_DI.{inp}:={module}_DI{"%.02d" % channel}.STS; (* {rakurs_index}, {sign_name} *)(*{klemma}*)\n')
                    else:
                        try:
                            array_element_in = int(
                                data.loc[data["Вход блока"] == inp]["Номер элемента в массиве пересылки"].values[0])
                        except ValueError:
                            f.write(f'{obj_name}_DI.{inp}:=ZeroByte;  (*ВНИМАНИЕ! ЗДЕСЬ БЫЛА ОШИБКА В БАЗЕ, УСТРАНИТЬ И ОБРАТИТЬ ВНИМАНИЕ*)\n')
                            logerror(f'не определен номер элемента в массиве пересылки для {rakurs_index}')
                            continue
                        # Выставление соответствия номеров массивов (посылка Modbus TCP содержит не более 250 переменных BYTE)
                        if array_element_in > 249:
                            data_array_number = 2
                            array_element_for = array_element_in - 250
                        else:
                            data_array_number = 1
                            array_element_for = array_element_in
                        f.write(f'{obj_name}_DI.{inp}:={sign_KIS.replace("КИС", "KIS").replace(".", "_")}.Inputs.{sign_KIS.replace("КИС", "KIS").replace(".", "_")}_IN[{array_element_in}]; (*FOR_{parent_KIS.replace("КИС", "KIS").replace(".", "_")}_DATA0{data_array_number}[{array_element_for}]:= {module}_DI{"%.02d" % channel}.STS;*)(*{klemma}*)\n')
                        with open(currentdirname + '\\' + sign_KIS + '\\!' + sign_KIS + 'Массив пересылок.txt', 'a+') as outfile:
                            outfile.seek(0, os.SEEK_END)  # go to end of file
                            if outfile.tell():  # if current position is truish (i.e != 0)
                                outfile.seek(0)  # rewind the file for later use
                            else:
                                outfile.write(f'(*-----------  массив пересылки из {sign_KIS} {datetime.now().strftime("%Y_%m_%d %H:%M:%S")}     --------------------*)\n\n')
                            outfile.write(f'FOR_{parent_KIS.replace("КИС", "KIS").replace(".", "_")}_DATA0{data_array_number}[{array_element_for}]:= {module}_DI{"%.02d" % channel}.STS;(*{obj_name} {inp} из {sign_KIS} в {parent_KIS} {module} {channel} *)\n')
                except (KeyError, IndexError) as e:
                    pass
        f.write(f'{obj_name}_block (UDT :={obj_name},\n')
        if no_AI:
            f.write(f'			In:=Empty_AI, (* Без АИ*)\n')
            f.write(f'			Scale_min := 0.0,\n')
            f.write(f'			Scale_max := 0.0,\n')
        else:
            f.write(f'			In:={ai_module}.ANA_CH_IN[{ai_channel}], (* {ai_rakurs_index}, {ai_sign_name} *)(*{ai_klemma}*)\n')
            f.write(f'			Scale_min := {ai_scale_min},\n')
            f.write(f'			Scale_max := {ai_scale_max},\n')
            try:
                f.write(f'			Address := {ai_module[len(ai_module)-2::]}.{ai_channel},\n')
            except TypeError:
                f.write(f'			Address := 0.0,\n')
        f.write(f'			DI := {obj_name}_DI);\n\n')
    else:
        # Добавить запись по объекту
        ## Заголовок
        f.write(f"(*____{obj_name}_____  объект {object_counter[KISes.index(parent_KIS)][list(foo_switcher.keys()).index(obj_type)]}*)\n")
        # Записываем объект
        f.write(f'{obj_name}_block (UDT :={obj_name},\n')

        if "In" in block_inputs:
            ai_module = data.loc[data["Вход блока"] == "In"]["Номер модуля"].values[0]
            ai_channel = data.loc[data["Вход блока"] == "In"]["Канал модуля"].values[0]
            ai_rakurs_index = data.loc[data["Вход блока"] == "In"]["Ракурс индекс"].values[0]
            ai_sign_name = data.loc[data["Вход блока"] == "In"]["Наименование сигн"].values[0]
            f.write(f'			{"In"}:={ai_module}.ANA_CH_IN[{ai_channel}], (* {ai_rakurs_index}, {ai_sign_name} *)\n')
            scale_min = data.loc[data["Вход блока"] == "In"]["нижн предел парам"].values[0].replace(',', '.')
            scale_max = data.loc[data["Вход блока"] == "In"]["верхний предел парам"].values[0].replace(',', '.')
            try:
                f.write(f'			Address := {ai_module[len(ai_module)-2::]}.{ai_channel},\n')
            except TypeError:
                f.write(f'			Address := 0.0,\n')
            f.write(f'			Scale_min := {scale_min},\n')
            f.write(f'			Scale_max := {scale_max});\n\n')
        else:
            for inp in block_inputs:
                try:
                    sign_KIS = data.loc[data["Вход блока"] == inp]["Номер КИС"].values[0]
                    module = data.loc[data["Вход блока"] == inp]["Номер модуля"].values[0]
                    rakurs_index = data.loc[data["Вход блока"] == inp]["Ракурс индекс"].values[0]
                    channel = data.loc[data["Вход блока"] == inp]["Канал модуля"].values[0]
                    sign_name = data.loc[data["Вход блока"] == inp]["Наименование сигн"].values[0]
                    if channel == 'не опред' or module == 'A0СУ':
                        logerror(f'не определен канал или модуль для {rakurs_index}')
                        continue
                    if parent_KIS == sign_KIS:
                        if inp == "In": # AI
                            f.write(f'			{inp}:={module}.ANA_CH_IN[{channel}], (* {rakurs_index}, {sign_name} *)\n')
                            scale_min = data.loc[data["Вход блока"] == inp]["нижн предел парам"].values[0].replace(',', '.')
                            scale_max = data.loc[data["Вход блока"] == inp]["верхний предел парам"].values[0].replace(',', '.')
                            f.write(f'			Scale_min := {scale_min},\n')
                            f.write(f'			Scale_max := {scale_max});\n\n')
                            continue
                        else:
                            f.write(f'			{inp}:={module}_DI{"%.02d" % channel}.STS, (* {rakurs_index}, {sign_name} *)\n')
                    else:
                        try:
                            array_element_in = int(data.loc[data["Вход блока"] == inp]["Номер элемента в массиве пересылки"].values[0])
                        except ValueError:
                            f.write(f'			{inp}:=ZeroByte,  (*ВНИМАНИЕ! ЗДЕСЬ БЫЛА ОШИБКА В БАЗЕ, УСТРАНИТЬ И ОБРАТИТЬ ВНИМАНИЕ*)\n')
                            logerror(f'не определен номер элемента в массиве пересылки для {rakurs_index}')
                            continue
                        # Выставление соответствия номеров массивов (посылка Modbus TCP содержит не более 250 переменных BYTE)
                        if array_element_in > 249:
                            data_array_number = 2
                            array_element_for = array_element_in - 250
                        else:
                            data_array_number = 1
                            array_element_for = array_element_in
                        f.write(f'			{inp}:={sign_KIS.replace("КИС", "KIS").replace(".", "_")}.Inputs.{sign_KIS.replace("КИС", "KIS").replace(".", "_")}_IN[{array_element_in}], (*FOR_{parent_KIS.replace("КИС", "KIS").replace(".", "_")}_DATA0{data_array_number}[{array_element_for}]:= {module}_DI{"%.02d" % channel}.STS;  {rakurs_index}, {sign_name}*)\n')
                        with open(currentdirname + '\\' + sign_KIS + '\\!' + sign_KIS + 'Массив пересылок.txt', 'a+') as outfile:
                            outfile.seek(0, os.SEEK_END)  # go to end of file
                            if outfile.tell():  # if current position is truish (i.e != 0)
                                outfile.seek(0)  # rewind the file for later use
                            else:
                                outfile.write(f'(*-----------  массив пересылки из {sign_KIS} {datetime.now().strftime("%Y_%m_%d %H:%M:%S")}     --------------------*)\n\n')
                            outfile.write(	f'FOR_{parent_KIS.replace("КИС", "KIS").replace(".", "_")}_DATA0{data_array_number}[{array_element_for}]:= {module}_DI{"%.02d" % channel}.STS;(*{obj_name} {inp} из {sign_KIS} в {parent_KIS} {module} {channel} *)\n')
                except (KeyError, IndexError) as e:
                    f.write(f'			{inp}:=ZeroByte,\n')
            f.write('			TimeCtrl := t#5m);\n\n')
        ## Итерируем счетчик
    object_counter[KISes.index(parent_KIS)][list(foo_switcher.keys()).index(obj_type)] = object_counter[KISes.index(parent_KIS)][list(foo_switcher.keys()).index(obj_type)] + 1
    f.close()


if __name__ == '__main__':
    KISes = [
        "КИС320.1",
        "КИС336.1",
        "КИС336.2",
        "КИС336.3",
        "КИС420.1",
        "КИС420.2",
        "КИС420.3",
        "КИС420.4",
        "КИС420.5",
        "КИС420.6",
        "КИС420.7"]
    object_types = [
        "Клапан",
        "Электронагреватель",
        "AI",
        "AI_Sign",
        "Электрофорезный фильтр",
        "Фильтр рулонный",
        "КИД",
        "МЕО1",
        "Сигнализатор",
        "Вентилятор",
        "Избиратель",
        "Контактный аппарат",
        "Мешалка",
        "Насос",
        "Шибер"]
    foo_switcher = {
        "Клапан": [
            "OP",
            "CL",
            "Local",
            "Remoute",
            "Power_En",
            "CMD_OP_GCHU",
            "CMD_CL_GCHU",
            "CMD_STP_GCHU",
            "CMD_OP_RCHU",
            "CMD_CL_RCHU",
            "CMD_STP_RCHU",
            "Auto_mode",
            "Man_mode"],
        'el_nagr': [
            "Run",
            "Cmd_Strt_Local",
            "Cmd_Strt_Rchu"],
        "AI": ["In"],
        "AI_complicate": [
            "Limit4_H",
            "Limit9_L_PS2",
            "Limit10_LL_PS2_Dis",
            "Limit7_L_Dis",
            "Limit8_LL_Dis",
            "Limit4_H_Dis",
            "Limit8_LL",
            "Limit10_LL_PS2",
            "Limit7_L",
            "Limit9_L_PS2_Dis",
            "Limit1_HH_PS2",
            "Limit1_HH_PS2_Dis",
            "Limit3_HH",
            "Limit3_HH_Dis",
            "Limit3_HH_Cmd",
            "Limit8_LL_Cmd",
            "Limit10_LL_PS2_Cmd",
            "Limit4_H_Cmd",
            "Limit1_HH_PS2_Cmd",
            "Limit7_L_Cmd",
            "Limit9_L_PS2_Cmd",
            "Power_En",
            "Limit2_H_PS2",
            "Limit2_H_PS2_Cmd",
            "Limit2_HH_PS2_Dis",
            "In"],
        "Сигн AI": [
            "Limit3_HH_Cmd",
            "Limit4_H_Cmd",
            "Limit7_L",
            "Limit4_H",
            "Limit4_H_Dis",
            "Limit3_HH_Dis",
            "Limit3_HH",
            "Limit7_L_Dis",
            "Limit8_LL_Dis",
            "Limit8_LL",
            "Limit7_L_Cmd",
            "Limit8_LL_Cmd",
            "Limit9_L_PS2_Cmd",
            "Limit6_Ln",
            "Limit6_Ln_Dis",
            "Limit6_Ln_Cmd",
            "Limit5_Hn",
            "Power_En",
            "Limit2_HH_PS2_Dis",
            "Limit2_H_PS2",
            "Limit2_H_PS2_Cmd",
            "Limit10_LL_PS2_Cmd",
            "Limit5_Hn_Cmd",
            "Limit9_L_PS2",
            "Limit10_LL_PS2",
            "Limit9_L_PS2_Dis",
            "Limit10_LL_PS2_Dis",
            "In"],
        "Сигн AI  ??": [
            "Limit3_HH_Cmd",
            "Limit4_H_Cmd",
            "Limit7_L",
            "Limit4_H",
            "Limit4_H_Dis",
            "Limit3_HH_Dis",
            "Limit3_HH",
            "Limit7_L_Dis",
            "Limit8_LL_Dis",
            "Limit8_LL",
            "Limit7_L_Cmd",
            "Limit8_LL_Cmd",
            "Limit9_L_PS2_Cmd",
            "Limit6_Ln",
            "Limit6_Ln_Dis",
            "Limit6_Ln_Cmd",
            "Limit5_Hn",
            "Power_En",
            "Limit2_HH_PS2_Dis",
            "Limit2_H_PS2",
            "Limit2_H_PS2_Cmd",
            "Limit10_LL_PS2_Cmd",
            "Limit5_Hn_Cmd",
            "Limit9_L_PS2",
            "Limit10_LL_PS2",
            "Limit9_L_PS2_Dis",
            "Limit10_LL_PS2_Dis"
            "In"],
        "Elektroforez": [
            "Limit7_L",
            "Limit8_LL",
            "On_Perepolus",
            "On_Rabota"],
        "flt_rulon": [
            "Run",
            "Remoute",
            "Local",
            "Cmd_Strt_Gchu",
            "Cmd_Strt_Local"],
        'kid': [
            "Cmd_Cl_Gchu",
            "Cmd_Op_Gchu",
            "Power_En_Rchu",
            "CL",
            "OP",
            "Remoute",
            "Power_En_Cho"],
        'meo_1': [
            "na_back",
            "na_forw"],
        'NO': [],
        "Signalizator": ["Sign"],
        "вентилятор": [
            "Cmd_Strt_Rchu",
            "Man_Mode",
            "Run",
            "Local",
            "Remoute",
            "Pozar_Run",
            "Avaria_Stp",
            "Stp",
            "Auto_Mode",
            "Auto_Main_On",
            "No_Power_En",
            "Cmd_Strt_Local",
            "Klapan_Cl",
            "Avaria_Off",
            "Klapan_Op",
            "Auto_Back_On",
            "Remoute_On"],
        "вентилятор  ??": [
            "Cmd_Strt_Rchu",
            "Man_Mode",
            "Run",
            "Local",
            "Remoute",
            "Pozar_Run",
            "Avaria_Stp",
            "Stp",
            "Auto_Mode",
            "Auto_Main_On",
            "No_Power_En",
            "Cmd_Strt_Local",
            "Klapan_Cl",
            "Avaria_Off",
            "Klapan_Op",
            "Auto_Back_On",
            "Remoute_On"],
        "избиратель": [
            "Manual_mode",
            "Auto_Mode"],
        "Контактный аппарат": [
            "Man_Mode_2",
            "Cmd_Strt_Gchu_2",
            "Auto_Mode_2",
            "Man_Mode_1",
            "Cmd_Strt_Gchu_1",
            "Auto_Mode_1",
            "Cmd_Stp_Rchu_2",
            "Cmd_Stp_Rchu_1",
            "Cmd_Strt_Rchu_2",
            "Cmd_Strt_Rchu_1",
            "Run_2",
            "Run_1",
            "On_Run_1",
            "Power_En",
            "On_Stp_1",
            "Cmd_Stp_Gchu_1",
            "Cmd_Stp_Gchu_2",
            "Power_En_1",
            "Power_En_2",
            "Main_Mode_1",
            "Main_Mode_2"],
        "мешалка": [
            "Run",
            "Local",
            "Remoute",
            "Cmd_On"],
        "Насос": [
            "Cmd_Strt_Rchu",
            "Cmd_Stp_Rchu",
            "Cmd_Strt_Gchu",
            "Cmd_Stp_Gchu",
            "Main_Mode",
            "Cmd_Stp_Local",
            "Auto_Mode",
            "Local",
            "Remoute",
            "Backup_Mode",
            "Run",
            "Power_En",
            "Auto_Main_On",
            "Membrana",
            "Stp",
            "Auto_Back_On",
            "Cmd_Strt_Local",
            "Man_Mode"],
        "Насос  ??": [
            "Cmd_Strt_Rchu",
            "Cmd_Stp_Rchu",
            "Cmd_Strt_Gchu",
            "Cmd_Stp_Gchu",
            "Main_Mode",
            "Cmd_Stp_Local",
            "Auto_Mode",
            "Local",
            "Remoute",
            "Backup_Mode",
            "Run",
            "Power_En",
            "Auto_Main_On",
            "Membrana",
            "Stp",
            "Auto_Back_On",
            "Cmd_Strt_Local",
            "Man_Mode"],
        "Насос ??": [
            "Cmd_Strt_Rchu",
            "Cmd_Stp_Rchu",
            "Cmd_Strt_Gchu",
            "Cmd_Stp_Gchu",
            "Main_Mode",
            "Cmd_Stp_Local",
            "Auto_Mode",
            "Local",
            "Remoute",
            "Backup_Mode",
            "Run",
            "Power_En",
            "Auto_Main_On",
            "Membrana",
            "Stp",
            "Auto_Back_On",
            "Cmd_Strt_Local",
            "Man_Mode"],
        "РЕЗЕРВ": [],
        "Шибер": []
    }
    outputdirectory = r'C:\Users\1\Desktop\PLC code'
    currentdirname = outputdirectory + '\\' + datetime.now().strftime("%Y_%m_%d %H_%M")
    try:
        os.makedirs(currentdirname)  # Создаем общую папку для всех папок
    except FileExistsError:
        currentdirname = currentdirname + '(2)'
        os.makedirs(currentdirname)
    for KIS in KISes:
        os.mkdir(currentdirname + '\\' + KIS)
    object_counter = [[1] * len(foo_switcher.keys()) for _ in range(len(KISes))]

    starttime = datetime.now()
    inputfile = r'C:\Users\1\Desktop\Работа\ПИК\!РАКУРС\!!ПО\Базы с сигналами\WORK_10998_20_11_17.xlsm'
    sheetname = 'Лист1'
    df = importdf(inputfile, sheetname)
    # Заполнить строку с номерами элементов в массиве пересылки
    df['Номер элемента в массиве пересылки'] = ''
    df.sort_values(by=['Наименов_0'])
    df1 = df.loc[df['Не использовать сигнал'] != 1]
    array_indexes = {
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
    arr_index_KIS = [0] * len(KISes)
    for i in range(0, len(KISes)):
        arr_index_KIS[i] = array_indexes.copy()
    for index, row in df1.iterrows():
        if row['Номер КИС'] != row['Номер КИС к родителю'] and "КИС" in str(row['Номер КИС к родителю']):
            df1.at[index, 'Номер элемента в массиве пересылки'] = arr_index_KIS[KISes.index(row['Номер КИС'])][row['Номер КИС к родителю']]            #  =array_indexes[row['Номер КИС к родителю']]
            arr_index_KIS[KISes.index(row['Номер КИС'])][row['Номер КИС к родителю']] = arr_index_KIS[KISes.index(row['Номер КИС'])][row['Номер КИС к родителю']] + 1

    naimen_0 = df1["Наименов_0"].unique().tolist()
    naimen_0 = [x for x in naimen_0 if str(x) != 'nan']  # Убираем NaN
    total = len(naimen_0) - 1
    for nomer, name in enumerate(naimen_0):
        type_inputs = foo_switcher.get(df1.loc[df1['Наименов_0'] == name]['Тип объекта'].values[0], "Fail")
        if type_inputs == "Fail":
            logerror(f'{name} имеет неправильный тип')
            continue
        if df1.loc[df1['Наименов_0'] == name]['Номер КИС'].values[0] not in KISes:
            logerror(f'{name} имеет неправильный номер КИС')
            continue
        raw_data = df1.loc[df1['Наименов_0'] == name]
        data_without_bad_signs = raw_data.loc[raw_data['Не использовать сигнал'] != '1']
        if len(data_without_bad_signs.index) > 0:
            foo(data_without_bad_signs, foo_switcher.get(data_without_bad_signs['Тип объекта'].values[0]))
    print("Экспорт датафрейма в файл...")
    df1.to_excel(currentdirname + r"\output.xlsx")
    endtime = datetime.now()
    minutes = divmod((endtime-starttime).seconds, 60)
    print('Время выполнения программы ', minutes[0], ' минут ', minutes[1], ' секунд')



