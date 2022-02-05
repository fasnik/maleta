from cProfile import label
from posixpath import split
from turtle import color, title
from matplotlib.colors import Colormap
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from math import ceil

def formatData(df, data):

    df['date'].append(data[0]),
    df['hour'].append(data[1]),
    df['latitude'].append(float(data[2].lstrip("Lat. "))),
    df['longitude'].append(float(data[3].lstrip("Lon. "))),
    df['temperature'].append(float(data[4].lstrip("Temp. "))),
    df['pressure'].append(float(data[5].lstrip("Press. "))),
    df['humidity'].append(float(data[6].lstrip("humid. ").rstrip(' %'))),
    df['wind'].append(float(data[7].lstrip("Wind "))),
    df['co2'].append(float(data[8].lstrip("Co2 "))),
    df['tvoc'].append(float(data[9].lstrip("TVOC"))),
    df['pm'].append(data[10].lstrip())
    
    return df

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


    with open('DATALOG.TXT','r') as file:
        file.readline()
        line = file.readline()
        while line:
            split_line = line.split(" - ")
            df = formatData(df, split_line)
            line = file.readline()
    

    
    #tuples = list(zip(positions['latitude'], positions['longitude']))
    df = pd.DataFrame(df)
    # df.set_index('date', inplace=True)
   
    return df

def plotData(df):

    grouped = df.groupby(['latitude', 'longitude'])
    mesures = { 'temperature':0,
                'pressure':1,
                'humidity':2,
                'wind':3,
                'co2':4,
                'tvoc':5,
                'pm':6}
    fig, axes = plt.subplots(nrows=7, ncols=1)
    plt.subplots_adjust(wspace=0.5, hspace=0.5)
    # for name,group in grouped:
    #     print (name)
    #     print (group)

    keys =list(grouped.groups.keys())
    y = grouped.get_group(keys[0])
    y_mean = y.mean(numeric_only=True)
    
    for mesure in mesures:
        color = np.random.rand(3,)
        axis = axes[mesures[mesure]]
        
        y.plot(        kind='scatter',
                       y=mesure, 
                       x='date',
                       marker = '+',
                       ax=axis,
                       title='At '+str(keys[0]), 
                       subplots=True,
                        color=color,
                        )
        if mesure!='pm':
            axis.plot( [y_mean[mesure],y_mean[mesure]], ':',
                        c=color,
                        label= 'mean',
                        )
   
    plt.show()

def plotMap(df):

    dfOrdered= df.sort_values(by=['date', 'hour'])[['latitude', 'longitude']]
    print( df.sort_values(by=['date', 'hour']).head(60))
    img = mpimg.imread("wmap.png")
    fig, ax = plt.subplots( figsize=(16,9))
    
    ax.set(xlim=(-90,90), ylim=(-90,90))
    ax.set_xticks( [xtick for xtick in range(-90, 91, 15)])
    ax.set_yticks( [ytick for ytick in range(-90, 91, 15)])
    
    ax.imshow(img, alpha=0.6, origin='upper', 
                    extent=(-90,90,-90,90)
                    )
    
    lon = dfOrdered['longitude']
    lat = dfOrdered['latitude']
    # dfOrdered.plot('longitude', 'latitude',linestyle=':',legend=False, ax=ax)
    dfOrdered.plot(kind='scatter', 
                                                    x='longitude', 
                                                    y='latitude', 
                                                    ax=ax,
                                                    marker='x',
                                                    color='r'
                                                    )
    
    u=lon[1:].values-lon[:-1].values 
    v=lat[1:].values-lat[:-1].values
    
    ax.quiver(  
                lon[:-1].values, 
                lat[:-1].values, 
                u,
                v,
                angles='xy', 
                scale_units='xy', 
                scale=1,
                alpha=0.5,
                linestyle= ':'
                )
    ax.set_aspect(9/16.)
    fig.tight_layout()
    plt.show()

def main():
    df = parser()
    plotMap(df)
    #plotData(df)
    
    
if __name__ == "__main__":
    main()
