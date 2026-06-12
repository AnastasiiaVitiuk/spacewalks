# https://data.nasa.gov/resource/eva.json (with modifications)
import matplotlib.pyplot as plt
import pandas as pd

"""
Script to analyse the data from the NASA EVA dataset. 
It reads the data from a JSON file, converts it to a CSV file, and then creates a graph of the cumulative time spent in space over the years. 
The graph is saved as a PNG file and displayed on the screen.
"""

input_file = open('./eva-data.json', 'r', encoding='ascii')
output_file = open('./eva-data.csv','w', encoding="utf-8")
graph_file = 'cumulative_eva_graph.png'

#reading a json file and converting into a dataframe
eva_df = pd.read_json(input_file, convert_dates=['date'], encoding='ascii')
#converting eva column to float and dropping na values from the duration and data columns
eva_df['eva'] = eva_df['eva'].astype(float)
eva_df.dropna(axis=0, subset=['duration', 'date'], inplace=True)

#writing the file to a csv file
eva_df.to_csv(output_file, index=False, encoding='utf-8')

#sorting the dataframe by date
eva_df.sort_values('date', inplace=True)

#convert duration from "HH:MM" format to hours as a float
eva_df['duration_hours'] = eva_df['duration'].str.split(":").apply(lambda x: int(x[0]) + int(x[1])/60)
#calculating cululative time spend in space over the years
eva_df['cumulative_time'] = eva_df['duration_hours'].cumsum()

#plotting the cumulative time spend in space over the years
plt.plot(eva_df['date'], eva_df['cumulative_time'], 'ko-')
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(graph_file)
plt.show()
