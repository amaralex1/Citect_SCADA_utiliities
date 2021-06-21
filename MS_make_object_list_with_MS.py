import pandas as pd
import os
import glob
from datetime import datetime
from GeneratePLCcode import importdf
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
starttime = datetime.now()
inputfile = r'C:\Users\rangin\Desktop\MS_objects\WORK_master_basa.xlsm'
sheetname = 'Лист1'
folder = r'C:\Users\rangin\Desktop\MS_objects\ '
files = glob.glob(os.path.join(folder[:-1], '*.txt'))
ilist = {}
for file in files:
    f = open(file, 'r')
    for line in f:
        ilist.update({line.rstrip(): file.split('\\')[-1]})
    f.close()
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

d = {'Объект': [], 'КИС': [], 'Привязка к мнемосхеме': []}
odf = pd.DataFrame(data=d)
for name in naimen_0:
    try:
        MS = [ilist[name].replace('.RDB.txt', '')]
    except KeyError:
        MS = 'Не используется на мнемосхеме'
    odf = odf.append({'Объект': [name], 'КИС': [df1.loc[df1["Наименов_0"] == name]["Номер КИС к родителю"].values[0]], 'Привязка к мнемосхеме': MS}, ignore_index=True)

odf.to_excel(folder[:-1] + "output.xlsx")
