
import zipfile
import pandas as pd
import xml.etree.ElementTree as ET
import re

file_path = 'TASK_DETAILS/TASK_1/Delinquency_prediction_dataset.xlsx'

try:
    with zipfile.ZipFile(file_path, 'r') as z:
        print("Zip content:")
        for name in z.namelist():
            print(name)
        
        # Try to read shared strings
        if 'xl/sharedStrings.xml' in z.namelist():
            with z.open('xl/sharedStrings.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                # Namespace usually http://schemas.openxmlformats.org/spreadsheetml/2006/main
                ns = {'a': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                shared_strings = [t.text for t in root.findall('.//a:t', ns)]
                print(f"Found {len(shared_strings)} shared strings.")
        
        # Try to read sheet1
        if 'xl/worksheets/sheet1.xml' in z.namelist():
            print("Sheet1 exists.")
            
except zipfile.BadZipFile:
    print("Bad zip file.")
except Exception as e:
    print(f"Error: {e}")
