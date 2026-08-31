from collections import Counter
import sys
import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.pyplot import figure

figure(figsize=(35, 5), dpi=80)

# CG_DELAY_REASONS = ['Baggage', 'Resource'] cargo? 
CG_DELAY_REASONS = ['Baggage', 'Resource', 'Equipment']
HUBS = ['LAX', 'IAD', 'ORD', 'EWR', 'IAH', 'DEN']
WIDE_BODY = ['777', '77W', '788', '789', '763', '764']
NARROW_BODY = ['319', '320', '321', '737', '738', '7M8', '739', '7M9','752', '753', ]
EXPRESS = ['CR7', 'CRJ', 'E7W', 'ERJ', 'CR5']
INTL = ['AKL', 'AMS', 'BCN', 'CHC', 'CDG', 'CUN', 'FCO', 'FRA', 'HKG', 'HND', 'ICN', 'KIX', 'LHR', 'MEL', 'MEX', 'MNL', 'MTY', 'MUC', 'NRT', 'PEK', 'PPT', 'PVG', 'PVR', 'SIN', 'SJD', 'SJO', 'SYD', 'TPE', 'YUL', 'YVR', 'YYC', 'YYZ', 'ZRH']

#---------------- Methods -----------------------#
def get_data(folder):
    path = os.getcwd() + folder
    files = os.listdir(path)
    df = pd.DataFrame()
    for f in files:
        if (f.endswith('xlsx')):
            data = pd.read_excel(path + f)
            df = pd.concat([df, data], ignore_index=True)
    return df

def filter(df, filter):
    return df[df.apply(filter, axis=1)]

def is_delay(f, criteria=None):
    if (criteria is None):
        return f['REASON'].split() != '--'
    return f['REASON'].split()[0] in criteria

def is_cg_delay(f):
    return is_delay(f, CG_DELAY_REASONS)

def is_special(f, special):
    icon = f.at['SPECIALS']
    if (type(icon) != str): return False
    return special in icon.split() 

def is_star(f):
    return is_special(f, 'S')

def is_priority(f):
    return is_special(f, 'P')

def is_quick_turn(f):
    return is_special(f, 'Q')

def get_delays(df):
    return df[df['REASON'] != '--']

# Calculates frequency of each delay type for all station delays 
def get_station_reasons(df):
    reasons = df['REASON']
    station_reasons = []
    for index, value in reasons.items():
        first_reason = value.split()[0]
        if (first_reason != '--'):
            station_reasons.append(first_reason)
    return Counter(station_reasons).most_common(12)

def filter_by_zone(df, zone):
    return df[df['DEP ZONE'] == zone]

def export(df, name):
    df.to_excel(name + '.xlsx')

def get_gates(df):
    gates = df['DEP GATE']
    gate_freq = Counter(gates)
    gate_freq = gate_freq.most_common(10)
    return gate_freq

def get_aircrafts(df):
    aircrafts = df['AIRCRAFT']
    aircrafts = Counter(aircrafts)
    return aircrafts

'''delays per scheduled hour'''
def get_delays_by_hour(df):

    return     

#---------------- plots -----------------------#

def bar_plot(df):
    categories, values = zip(*df)
    plt.bar(categories, values)
    plt.show()   

def plot_station_reasons(df):
    bar_plot(get_station_reasons(df)) 

#---------------- info -----------------------------$

def info(df):
    return {
        'total': len(df), 
        # 'delays': len(get_delays(df)),
        'stars': len(filter(df, is_star)),
        'priority': len(filter(df, is_priority)),
        'quick turns': len(filter(df, is_quick_turn))
    }

# Returns list of worst performing routes in dataframe
def route_test(df):
    flights = []
    for index, value in df['FLIGHT OUT'].items():
        flights.append(value.rsplit('-')[0])
    return Counter(flights).most_common(10)

def print_list(list):
    for index, value in list:
        print(f'{index} - {value}')

"""calculate, format and print specials performance"""
def specials_performance():
    return
    
def desinations_info(df):    
    all_arr = dict(Counter(df['ARR']).most_common())
    cg_delays_arr = dict(Counter(filter(df, is_cg_delay)['ARR']).most_common())
    ratios = {}
    for key, value in cg_delays_arr.items():
        ratios[key] = round(value / all_arr[key] * 100, 2)
    ratios = sorted(ratios.items(), key=lambda item: item[1])
    print_list(ratios)

#-------------------- main -------------------------------#

if __name__ == '__main__':
    data = get_data('/data/SFO-Aug/')
    # cg_delays = filter(data, is_cg_delay)
    # cg_info = info(cg_delays)
    print(info(data))
    print(desinations_info(data))
    # plot_station_reasons(data)