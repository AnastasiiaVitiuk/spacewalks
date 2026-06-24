# Spacewalks

## Overview
Spacewalks is a Python-based software for generate a summary of NASA's extravehicular activity datasets.

## Features
- generates a CSV file of a summary statistics of vehicular activity and cre size
- generate a plot to showcast the cumulative duration of space walsk over time

## Pre-requisites
- Python version >= 3.12
- NumPy >= 2.4.6
- Matplotplib >= 3.10.9
- pytest >= 9.1.1
- Pandas >= 3.0.3

## Instalation
1. Clone the spacewalks repo to your local machine using git
- git clone https://github.com/AnastasiiaVitiuk/spacewalks.git
2. Instantiate a virtual environment using the following commmad
- python3 -m venv ./path-to-new-venv
- source venv/bin/activate
3. Install all the necessary dependencies
- python3 -m pip install -r requirements.txt
4.  Check your setup by running the pytests
- python3 -m pytest

## Usage
To run an analysis using the eva_data_analysis.py script from the command line terminal,
launch the script using Python as follows:

- python3 eva_data_analysis.py eva-data.json eva-data.csv

The first argument is path to the JSON data file.
The second argument is the path the CSV output file.