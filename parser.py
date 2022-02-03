from cProfile import label
from posixpath import split
from turtle import title
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def formatData(df, pos, data):

    df['date'].append(data[0]),
    df['hour'].append(data[1]),
    df['latitude'].append(data[2].lstrip("Lat. ")),
    df['longitude'].append(data[3].lstrip("Lon. ")),
    df['temperature'].append(float(data[4].lstrip("Temp. "))),
    df['pressure'].append(float(data[5].lstrip("Press. "))),
    df['humidity'].append(float(data[6].lstrip("humid. ").rstrip(' %'))),
    df['wind'].append(float(data[7].lstrip("Wind "))),
    df['co2'].append(float(data[8].lstrip("Co2 "))),
    df['tvoc'].append(float(data[9].lstrip("TVOC"))),
    df['pm'].append(data[10].lstrip())

    pos['latitude'].append(data[2].lstrip("Lat. ")),
    pos['longitude'].append(data[3].lstrip("Lon. ")),
    
    return [df, pos]

def parser():
    
    df = {
        'date': [],
        'hour':[],
        'latitude':[],
        'longitude':[],
        'temperature':[],
        'pressure':[],
        'humidity':[],
        'wind':[],
        'co2':[],
        'tvoc':[],
        'pm':[]
    }

    positions = {
        'latitude':[],
        'longitude':[],
        
    }

    with open('DATALOG.TXT','r') as file:
        file.readline()
        line = file.readline()
        while line:
            split_line = line.split(" - ")
            df, positions = formatData(df, positions, split_line)
            line = file.readline()
    

    
    tuples = list(zip(positions['latitude'], positions['longitude']))
    set_of_positions = set(zip(positions['latitude'], positions['longitude']))
    index = pd.MultiIndex.from_tuples(tuples, names=['latitude', 'longitude'])
    print('set    : ', set_of_positions)
    df = pd.DataFrame(df, index=index)
   
    return [df, set_of_positions]

def plotData(df, positions):
    print(df.index)
    for pos in positions:
        
        print('pos: ', pos[0], pos[1])
        print(df.loc([[('0.000000',  '0.000000')]]))
        # # .plot(subplots=True)

    plt.show()


def main():
    df, positions = parser()
    plotData(df, positions)
    
if __name__ == "__main__":
    main()
