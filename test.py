import pandas as pd


class Valve:
    def __init__(self, name):
        self.name = name  # instance variable unique to each instance
    OP = ""
    CL = ""
    Remote = ""
    Local = ""
    Power_En = ""
    Auto_Mode = ""
    Man_Mode = ""
    CMD_OP_GCHU = ""
    CMD_CL_GCHU = ""
    CMD_OP_RCHU = ""
    CMD_CL_RCHU = ""
    CMD_STP_RCHU = ""
    CMD_STP_GCHU = ""

    vhodblokatocode = {"OP":"",
                       "CL":"",
                       "Local":"",
                       "Remoute":"",
                       "Power_En":"",
                       "CMD_OP_GCHU":"",
                       "CMD_CL_GCHU":"",
                       "CMD_STP_GCHU":"",
                       "CMD_OP_RCHU":"",
                       "CMD_CL_RCHU":"",
                       "CMD_STP_RCHU":"",
                       "Auto_mode":"",
                       "Man_mode": "",
                       }
    def fill(self, dataframe):
        for index, row in dataframe:
            if


df = pd.DataFrame([["Valve", "KIS336.1 A036 1", "Local"],
                   ["Valve", "KIS336.1 A036 2", "Remoute"],
                   ["Valve", "KIS336.1 A036 3", "OP"],
                   ["Valve", "KIS336.1 A036 4", "CL"],
                   ["Valve", "KIS336.1 A036 5", "Power_En"],
                   ["Valve", "KIS336.1 A036 6", "Auto_mode"],
                   ["Valve", "KIS336.1 A036 7", "Man_mode"],
                   ["Valve", "KIS336.1 A036 8", "CMD_OP_GCHU"]],
                  columns=['Type', 'NeededData', 'Vhod bloka'])

print(0)
VC01S01 = Valve("Valve")
VC01S01.fill(df)









