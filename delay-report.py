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

def is_delay(f):
    return f['REASON'].split() == '--'

def is_cg_delay(f):
    return f['REASON'].split()[0] == ('Baggage' or 'Resource')
    # return f['REASON'].split()[0] == 'Baggage' or f['REASON'].split()[0] == 'Resource'

def is_special(f, special):
    icon = f.at['SPECIALS']
    if (type(icon) != str): return False
    return special in icon.split() 

def is_star(f):
    return is_special(f, 'S')

def is_priority(f):
    return is_special(f, 'P')

def is_quick_turn(f):
    return is_quick_turn(f, 'Q')

def delay_test():
    data = get_data('/data/SFO-Aug/')
    # delays = data[data['REASON'] != '--']
    # stars = filter(data, is_star)
    # print(is_cg_delay(data.iloc[4]))
    cg_delays = filter(data, is_cg_delay)
    # cg = data[data['REASON'] == 'Baggage']
    print(len(cg_delays))
    print(len(data))

delay_test()

def get_delays(df):
    return df[df['REASON'] != '--']

# Returns new dataframe with only delayed flights
# def get_delays(df):
#     delays = []
#     delay_lengths = df['DELAY DEP']
#     for i in range(len(delay_lengths)):
#         if (delay_lengths[i][0] != '-' and delay_lengths[i] != '00:00'):
#             delays.append(i)
#     return df.iloc[df.index.isin(delays)]

def get_delays_by_reason(df, criteria):
    reasons = df['REASON']
    delays = []
    for index, value in reasons.items():
        first_reason = value.split()[0]
        if (first_reason in criteria):
            delays.append(index)
    return df.iloc[df.index.isin(delays)]

# Calculates frequency of each delay type for all station delays 
def get_station_reasons(df):
    reasons = df['REASON']
    station_reasons = []
    for index, value in reasons.items():
        first_reason = value.split()[0]
        if (first_reason != '--'):
            station_reasons.append(first_reason)
    return Counter(station_reasons).most_common(12)

def get_delays_by_hour(df):
    return     

def filter_by_zone(df, zone):
    return df[df['DEP ZONE'] == zone]

def export(df, name):
    df.to_excel(name + '.xlsx')

def get_gates(data):
    gates = data['DEP GATE']
    gate_freq = Counter(gates)
    gate_freq = gate_freq.most_common(10)
    return gate_freq

def get_aircrafts(data):
    aircrafts = data['AIRCRAFT']
    aircrafts = Counter(aircrafts)
    return aircrafts

#---------------- plots -----------------------#

def bar_plot(df):
    categories, values = zip(*df)
    plt.bar(categories, values)
    plt.show()   

def plot_station_reasons(df):
    bar_plot(get_station_reasons(df)) 

#---------------- tests -----------------------------$

def info(df):
    return {
        'total': len(df), 
        # 'delays': len(get_delays(df)),
        'stars': len(filter(df, is_star)),
        'priority': len(filter(df, is_priority)),
        'quick turns': len(filter(df, is_quick_turn))
    }

def cg_delays_info(df):
    return info(get_delays_by_reason(df, CG_DELAY_REASONS))

# Returns list of worst performing routes in dataframe
def route_test(df):
    flights = []
    for index, value in df['FLIGHT OUT'].items():
        flights.append(value.rsplit('-')[0])
    return Counter(flights).most_common(10)

def print_list(list):
    for index, value in list:
        print(f'{index} - {value}')


def desinations_info(data):    
    all_arr = dict(Counter(data['ARR']).most_common())
    cg_delays_arr = dict(Counter(get_delays_by_reason(data, CG_DELAY_REASONS)['ARR']).most_common())
    ratios = {}
    for key, value in cg_delays_arr.items():
        ratios[key] = round(value / all_arr[key] * 100, 2)
    ratios = sorted(ratios.items(), key=lambda item: item[1])
    print_list(ratios)

#-------------------- main -------------------------------#

# if __name__ == '__main__':
#     data = get_data('/data/SFO-Aug/')
#     plot_station_reasons(data)