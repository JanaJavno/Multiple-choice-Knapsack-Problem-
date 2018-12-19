import pandas as pd
from datetime import datetime

campaignsSettings = pd.ExcelFile('CAMPAIGNS_SETTINGS.xlsx').parse('Sheet 1')
campaignsWithPeIndex = pd.ExcelFile('CAMPAIGNS_WITH_PE_INDEX.xlsx').parse('Sheet1')
campaignNames = campaignsSettings['NAME_CAMPAIGN']

def convertToDate(str):
    return datetime(str[0]//10000,
                    str[0]%10000 // 100,
                    str[0] % 100,
                    str[1] // 100,
                    str[1] % 100)

def convertShifts(shifts):
    shifts = [convertToDate(shift) for shift in shifts]
    startSpot = min(shifts)
    for i, _ in enumerate(shifts):
        shifts[i] -= startSpot
        shifts[i] = shifts[i].days*48 + shifts[i].seconds // 1800
    return shifts


def readSpots():
    data, shifts = [], []
    for campaignName in campaignNames:
        temp = campaignsWithPeIndex[campaignsWithPeIndex['NAME_CAMPAIGN'] == campaignName]
        temp = temp.sort_values(['BROADCAST_DATE', 'TIME_SPOT'], ascending=[0, 0])
        shifts.append((temp.head(1)['BROADCAST_DATE'].values[0], temp.head(1)['TIME_SPOT'].values[0]))
        temp = temp[::-1]
        spotsQualities = []
        for index, row in temp.iterrows():
            spotsQualities.append(row['PE_NORM'])
        data.append(spotsQualities)
    return data, convertShifts(shifts)

def readConfines():
    confines = []
    for index, row in campaignsSettings.iterrows():
        confines.append(row['MAX_SPOTS'])
    return confines
