# Helper Functions

# Imports 
import csv
import pandas as pd

# Data Loader 
def process_csv_data(file_path):
    data = []
    if '.csv' not in file_path:
        print("Error: CSV Required")
    else:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                data.append(row)
    return data

# Create Table
def sum_table(data):
    df = pd.read_csv(data)
    # Select numeric columns only
    num_df = df.select_dtypes(include='number')    
    # Build the summary table
    summary = pd.DataFrame({
        'Median': num_df.median(),
        'Count': num_df.count(),
        'MAX': num_df.max(),
        'MIN': num_df.min(),
        'NAs': num_df.isna().sum()
    })
    return summary
    