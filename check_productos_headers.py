import pandas as pd
import os

file_path = 'productos.xlsx'

if not os.path.exists(file_path):
    print(f"Error: File '{file_path}' not found.")
else:
    try:
        df = pd.read_excel(file_path)
        print("Columns found in Excel file:")
        print(df.columns.tolist())
        print("\nFirst few rows:")
        print(df.head())
    except Exception as e:
        print(f"Error reading Excel file: {e}")
