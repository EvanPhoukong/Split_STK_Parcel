"""
Given a list of pdfs containing parcel updates in the county, this script will be able to isolate those that pertain to Basic Stockton Parcels.

Pipeline:

1. Convert PDF to csvs to extract APNs.
2. Delete old apn in basic stockton parcels layer.
3. Add new features from assessor parcels to basic stockton parcels. Select them using the APN field.

A split can be narrowed down to two basic functionalities.

1. Delete old features in selected layer. (Locate using Existing APNS)
2. Copy feature from updated layer to selected layer.
3. Update APNS in associated addresses

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

def extract_apns() -> None:

    headers = ["Doc Number", "Date", "Existing_APNS", "NA", "New_APNS", "Tax_Change", "Doc_Type", "Activity"]
    print("Please select the folder containing the pdfs to process: ")
    files = Path(filedialog.askdirectory())

    for file_path in files.iterdir():
        with pdfplumber.open(file_path) as pdf:
            page = pdf.pages[0]
            table = page.extract_table()
            df = pd.DataFrame(table[1:], columns=headers)
            df = df[["Existing_APNS", "New_APNS", "Activity"]]
            for column in df:
                df[column].replace('', np.nan, inplace=True)
            df = df.dropna(how='all')
            yield df

"Below are the three basic functions encompassed by a Split"

def delete_old_parcels(df: pd.DataFrame) -> None:
    """
    Parcels in the Basic Stockton Parcel Layer corresponding to the Existing_APNs are deleted
    """
    pass

def add_new_parcel(df: pd.DataFrame) -> None:
    """
    Parcels from Assessor Layer corresponing to New_APN is added to Basic Stockton Parcel Layer
    """
    pass

def update_addresses(df: pd.DataFrame) -> None:
    """
    Addresses corresponding to the Existing_APNs are updated to the New_APNs
    """
    pass

def main() -> None:
    parcel_dfs = extract_apns()
    for df in parcel_dfs:
        delete_old_parcels(df)
        add_new_parcel(df)
        update_addresses(df)

if __name__ == "__main__":
    main()