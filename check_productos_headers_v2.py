import pandas as pd

file_path = 'productos.xlsx'
try:
    # Read with header=1 (second row as header)
    df = pd.read_excel(file_path, header=1)
    print("Columns found in Excel file:")
    print(df.columns.tolist())
    print("\nFirst few rows:")
    print(df.head())
except Exception as e:
    print(f"Error reading Excel file: {e}")
