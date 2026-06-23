# https://data.nasa.gov/resource/eva.json (with modifications)
import matplotlib.pyplot as plt
import pandas as pd
import re # added this line
import sys

"""
Script to analyse the data from the NASA EVA dataset. 
It reads the data from a JSON file, converts it to a CSV file, and then creates a graph of the cumulative time spent in space over the years. 
The graph is saved as a PNG file and displayed on the screen.
"""
def main(input_file, output_file, graph_file):
    print("--START--")

    # Read the data from JSON file
    eva_data = read_json_to_dataframe(input_file)

    # Calculate and add crew size to data
    eva_data = add_crew_size_column(eva_data) # added this line

    # Convert and export data to CSV file
    write_dataframe_to_csv(eva_data, output_file)

    # Sort dataframe by date ready to be plotted (date values are on x-axis)
    eva_data.sort_values('date', inplace=True)

    # Plot cumulative time spent in space over years
    plot_cumulative_time_in_space(eva_data, graph_file)

    print("--END--")

def read_json_to_dataframe(input_file):
    """
    Converting JSON file to a Pandas DataFrame and cleaning the data

    Args:
        input_file (file or string): The file object or path to the JSON file 

    Returns:
        eva_df (pd.DataFrame): The processed DataFrame
    """
    print(f'Reading JSON file {input_file}')
    # Read the data from a JSON file into a Pandas dataframe
    eva_df = pd.read_json(input_file, convert_dates=['date'], encoding='ascii')
    eva_df['eva'] = eva_df['eva'].astype(float)
    # Clean the data by removing any rows where duration is missing
    eva_df.dropna(axis=0, subset=['duration', 'date'], inplace=True)
    
    return eva_df


def write_dataframe_to_csv(df, output_file):
    """
    Writing a dataframe generated from json file to a csv file

    Args:
        df (pd.DataFrame): The DataFrame to write to CSV
        output_file (file or string): The file object or path to the CSV file
    """
    print(f'Saving to CSV file {output_file}')
    # Save dataframe to CSV file for later analysis
    df.to_csv(output_file, index=False, encoding='utf-8')


def plot_cumulative_time_in_space(df, graph_file):
    """
    Plotting data from a data frame and saving the png file

    Args:
        df (pd.DataFrame): The DataFrame containing the EVA data
        graph_file (file or string): The file object or path to the PNG file
    """
    print(f'Plotting cumulative spacewalk duration and saving to {graph_file}')
    df['duration_hours'] = df['duration'].str.split(":").apply(lambda x: int(x[0]) + int(x[1])/60)
    df['cumulative_time'] = df['duration_hours'].cumsum()
    plt.plot(df['date'], df['cumulative_time'], 'ko-')
    plt.xlabel('Year')
    plt.ylabel('Total time spent in space to date (hours)')
    plt.tight_layout()
    plt.savefig(graph_file)
    plt.show()


def text_to_duration(duration):
    """Convert a text format of duration "HH:MM" to duration in hours

    Args:
        duration (str): the text format duration

    Returns:
        duration_hours (float): the duration in hours
    """
    hours, minutes = duration.split(":")
    duration_hours = int(hours) + int(minutes)/60

    return duration_hours

def add_duration_hours(df):
    """Add duration in hours varible to a dataset

    Args:
        df (pd.DataFrame): The input dataframe.

    Returns:
        df_copy (pd.DataFrame): A copy of df with the new duration_hours variable added
    """
    df_copy = df.copy()
    df_copy["duration_hours"] = df_copy["duration"].apply(
        text_to_duration
    )
    return df_copy

def calculate_crew_size(crew):
    """
    Calculate the size of the crew for a single crew entry

    Args:
        crew (str): The text entry in the crew column containing a list of crew member names

    Returns:
        (int): The crew size
    """
    if crew.split() == []:
        return None
    else:
        return len(re.split(r';', crew))-1
    
def add_crew_size_column(df):
    """
    Add crew_size column to the dataset containing the value of the crew size

    Args:
        df (pd.DataFrame): The input data frame.

    Returns:
        df_copy (pd.DataFrame): A copy of the dataframe df with the new crew_size variable added
    """
    print('Adding crew size variable (crew_size) to dataset')
    df_copy = df.copy()
    df_copy["crew_size"] = df_copy["crew"].apply(
        calculate_crew_size
    )
    return df_copy

if __name__ == "__main__":
    if len(sys.argv) < 3:
        input_file = './data/eva-data.json'
        output_file = './results/eva-data.csv'
        print(f'Using default input and output filenames')

    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        print('Using custom input and output filenames')

    graph_file = "./results/cumulative_eva_graph.png"

    main(input_file, output_file, graph_file)
