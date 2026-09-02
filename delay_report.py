from matplotlib import colormaps
from collections import Counter
import sys
import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.pyplot import figure
from datetime import datetime 
import numpy as np

CG_DELAY_REASONS = ['Baggage', 'Resource'] # cargo? potentially damage, 
# CG_DELAY_REASONS = ['Baggage', 'Resource', 'Equipment']
HUBS = ['LAX', 'IAD', 'ORD', 'EWR', 'IAH', 'DEN']
WIDE_BODY = ['777', '77W', '788', '789', '763', '764']
NARROW_BODY = ['319', '320', '321', '737', '738', '7M8', '739', '7M9','752', '753', ]
EXPRESS = ['CR7', 'CRJ', 'E7W', 'ERJ', 'CR5']
INTL = ['AKL', 'AMS', 'BCN', 'BNE', 'CHC', 'CDG', 'CUN', 'FCO', 'FRA', 'HKG', 'HND', 'ICN', 
    'KIX', 'LHR', 'MEL', 'MEX', 'MNL', 'MTY', 'MUC', 'NRT', 'PEK', 'PPT', 'PVG', 
    'PVR', 'SIN', 'SJD', 'SJO', 'SYD', 'TPE', 'YUL', 'YVR', 'YYC', 'YYZ', 'ZRH']
#---------------- I/O -----------------------#

def get_data(folder):
    path = os.getcwd() + folder
    files = os.listdir(path)
    df = pd.DataFrame()
    for f in files:
        if (f.endswith('xlsx')):
            data = pd.read_excel(path + f)
            df = pd.concat([df, data], ignore_index=True)
    return df

def export(df, name):
    df.to_excel(name + '.xlsx')

#---------------- Filters -----------------------#
def filter(df, filter):
    return df[df.apply(filter, axis=1)]

def is_delay(f, criteria=None):
    if (f.at['DELAY DEP'][0] == '-' or f.at['DELAY DEP'] == '00:00'):
        return False
    if (criteria is None): 
        return True
    return f['REASON'].split()[0] in criteria 

def is_cg_delay(f):
    return is_delay(f, CG_DELAY_REASONS)

def is_special(f, special):
    icon = f.at['SPECIALS']
    return False if type(icon) != str else special in icon.split() 

def is_star(f):
    return is_special(f, 'S')

def is_priority(f):
    return is_special(f, 'P')

def is_quick_turn(f):
    return is_special(f, 'Q')

def is_intl(f):
    return f['ARR'] in INTL

def is_widebody(f):
    return f['FLEET TYPE'] in WIDE_BODY

def is_narrowbody(f):
    return f['FLEET TYPE'] in NARROW_BODY

def is_express(f):
    return f['FLEET TYPE'] in EXPRESS

def is_late_departure(f):
    return datetime(f.at['SCHED DEP']) < datetime(f.at['ETD/ACT'])

def is_late_arrival(f):
    # return datetime(f.at['SCHED ARR']) < datetime(f.at['ETA/ACT'])
    return f.at['DELAY AR'][0] != '-'

def filter_by_zone(df, zone):
    return df[df['DEP ZONE'] == zone]

#----------------------- logic --------------#

# Calculates frequency of the n most common delay types 
def get_reasons(df, n = None):
    reasons = df['REASON']
    station_reasons = []
    for index, value in reasons.items():
        first_reason = value.split()[0]
        if (first_reason != '--'):
            station_reasons.append(first_reason)
    return Counter(station_reasons).most_common(n)

def format_for_pie_chart(list, n):
    other = 0
    for i in range(10, len(list)):
        other += list[i][1]
    top_ten_reasons = station_delays_reasons[:10]
    top_ten_reasons.append(('Other', other))
    return top_ten_reasons

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

def line_plot(d):
    return

def pie_chart(dict):
    labels = list(dict.keys())
    sizes = list(dict.values()) 
    figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures the pie is circular
    plt.title('Delays by fleet type')
    plt.show()

def pie_chart_fancy(dict):
    figure(figsize=(6, 6))
    plt.pie(list(dict.values()), 
            labels = list(dict.keys()), 
            explode = (0, 0, 0, 0.15, 0, 0, 0, 0, 0, 0),    
            autopct = '%1.1f%%', 
            colors = plt.cm.Pastel2.colors
            # colors = plt.cm.tab20.colors
    )
    plt.axis('equal')
    plt.show()

def plot_station_pie(data):
    delays = filter(data, is_delay)
    station_delays_reasons = get_reasons(delays)
    other = 0
    for i in range(10, len(station_delays_reasons)):
        # print(f'reason at i = {i}, {station_delays_reasons[i][0]}')
        other += station_delays_reasons[i][1]
    top_ten_reasons = station_delays_reasons[:10]
    top_ten_reasons.append(('Other', other))
    print(top_ten_reasons)
    top_reasons = [('Aircraft-LT', 1121), ('Connections', 659), ('Crew', 617), ('Baggage / Resource', 415), 
        ('Aircraft', 410), ('ATC', 239), ('Aircraft-New', 221), ('Servicing', 198), 
        ('Customer', 186), ('Other', 307)]
    pie_chart_fancy(dict(top_reasons))

def bar_plot(d):
    figure(figsize=(35, 5), dpi=80)
    categories, values = zip(*d)
    plt.bar(categories, values)
    plt.show()   

def plot_station_reasons(df):
    bar_plot(get_reasons(df)) 

#---------------- info -----------------------------$

def info(df):
    return {
        'total': len(df), 
        'delays': len(filter(df, is_delay)),
        'stars': len(filter(df, is_star)),
        'priority': len(filter(df, is_priority)),
        'quick turns': len(filter(df, is_quick_turn))
    }

def fleet_breakdown(df):
    return {
        'Widebody' : len(filter(df, is_widebody)), 
        'Narrowbody' : len(filter(df, is_narrowbody)), 
        'Express' : len(filter(df, is_express)), 
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
    data = get_data('/delay_report/data/SFO_AUG/')
    plot_station_pie(data)
    