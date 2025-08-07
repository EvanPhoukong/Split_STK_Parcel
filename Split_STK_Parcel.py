"""
Given a list of pdfs containing parcel updates in the county, this script will be able to isolate those that pertain to Basic Stockton Parcels.

"""

"IMPORTS"
from pathlib import Path
import pandas as pd
import arcpy
import os
from pypdf import PdfReader
import re
from tkinter import filedialog

"CONSTANTS"
apns_csv = Path("apns.csv")
layer = r"BasicStocktonParcels"
attribute = "APN"

def initialize_csv() -> None:
    """
    Creates csv with pdf metadata and corresponding apns
    """
    with open("apns.csv", "w+") as output_file:
        output_file.write("file_path,file_name,apns\n")
        print("Extracting apns from pdf")
        for file_path in files.iterdir():
            output_file.write(f"\"{file_path}\",\"{file_path.name}\",")
            output_file.write("/".join(extract_apns(file_path)) +"\n")


def extract_apns(file: str) -> list:
    apn_format = r"[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9]"
    apn_subformat = r"[0-9][0-9][0-9]-[0-9][0-9]"
    range_format = r"thru"
    apns = []
    filename, file_ext = os.path.splitext(file)
    if file_ext != '.pdf':
        return ["-1"]
    reader = PdfReader(file)
    tokens = reader.pages[0].extract_text().split()
    range = False
    for token in tokens:
        apn = re.search(apn_format, token)
        apn_sub = re.search(apn_subformat, token)
        # if apn_sub:
        #     print('SUBS', apn_sub.group())
        if range:
            if apn:
                apns[-1] = apns[-1] + "-" + apn.group().replace('-', "")
                range = False
        elif apn:
            apns.append(apn.group().replace('-', ""))
        elif re.search(range_format, token.lower()):
            range = True
        # elif apn_sub:
        #     apns.append(apn_sub.group().replace('-', "$"))
    if apns == []:
        apns = ["-1"]
        # print(tokens)
    return apns


def select_by_attr(features: list) -> None:
    """
    See if apns exist in the BasicStocktonParcels Layer, and isolate pdf files that correspond to Stockton
    """
    df = pd.read_csv("apns.csv")
    print("Finding parcels located in the BasicStocktonParcel Layer...")
    for _, row in df.iterrows():
        try:
            found = False
            if row['apns'] == "-1":
                new_path = os.path.join(man_directory, row['file_name'])
                os.rename(row['file_path'], new_path)
                continue
            attr_vals = row['apns'].split('/')
            for val in attr_vals:
                if "-" in val:
                    lower, upper = val.split('-')
                    for i in range(int(lower), int(upper)):
                        if i in features:
                            new_path = os.path.join(out_directory, row['file_name'])
                            os.rename(row['file_path'], new_path)
                            found = True
                            break
                # elif "$" in val:
                #     val = str(val).replace("$", "")
                #     if [str(num).startswith(val) for num in features]:
                #         new_path = os.path.join(out_directory, row['file_name'])
                #         os.rename(row['file_path'], new_path)
                #         found = True
                else:
                    if int(val) in features:
                        new_path = os.path.join(out_directory, row['file_name'])
                        os.rename(row['file_path'], new_path)
                        found = True
                if found:
                    found = False
                    break
        except:
            new_path = os.path.join(man_directory, row['file_name'])
            os.rename(row['file_path'], new_path)
            print("Double check this file: ", new_path)


if __name__ == "__main__":
    print("Please select the geodatabase: ")
    layer = os.path.join(filedialog.askdirectory(), layer)
    print("Please select the folder containing the pdfs to process: ")
    files = Path(filedialog.askdirectory())
    print("Please select the folder to store files that need manual checking: ")
    man_directory = Path(filedialog.askdirectory())
    print("Please select the folder to output the STK pdfs to: ")
    out_directory = Path(filedialog.askdirectory())
    initialize_csv()
    cursor = arcpy.SearchCursor(layer)
    features = {row.getValue(attribute) for row in cursor}
    select_by_attr(features)
    print("Finished")