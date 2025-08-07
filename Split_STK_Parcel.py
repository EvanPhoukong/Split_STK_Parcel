"""
Given a list of pdfs containing parcel updates in the county, this script will be able to isolate those that pertain to Basic Stockton Parcels.

Pipeline:

1. Convert PDF to csvs to extract APNs.
2. Delete old apn in basic stockton parcels layer.
3. Add new features from assessor parcels to basic stockton parcels. Select them using the APN field.

"""

"IMPORTS"
from pathlib import Path
import pandas as pd
import arcpy
import os
from pypdf import PdfReader
import re
from tkinter import filedialog
import pdfplumber
import numpy as np

"CONSTANTS"
apns_csv = Path("apns.csv")
layer = r"BasicStocktonParcels"
attribute = "APN"

def initialize_csv() -> None:
    headers = ["Doc Number", "Date", "Existing_APNS", "NA", "New_APNS", "Tax_Change", "Doc_Type", "Activity"]
    print("Please select the folder containing the pdfs to process: ")
    files = Path(filedialog.askdirectory())
    ye = True
    for file_path in files.iterdir():
        with pdfplumber.open(file_path) as pdf:
            page = pdf.pages[0]
            table = page.extract_table()
            df = pd.DataFrame(table[1:], columns=headers)
            df = df[["Existing_APNS", "New_APNS", "Activity"]]
            for column in df:
                df[column].replace('', np.nan, inplace=True)
            df = df.dropna(how='all')
            print(df)

def extract_apns(file: str) -> list:
    pass

def delete_old_apns() -> None:
    pass

def add_new_features() -> None:
    pass

def main() -> None:
    initialize_csv()

if __name__ == "__main__":
    main()