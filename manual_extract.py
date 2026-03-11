
import zipfile

import xml.etree.ElementTree as ET
import pandas as pd
import re

file_path = 'TASK_DETAILS/TASK_1/Delinquency_prediction_dataset.xlsx'

def extract_excel_manual(file_path):
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            # 1. Parse Shared Strings
            shared_strings = []
            if 'xl/sharedStrings.xml' in z.namelist():
                with z.open('xl/sharedStrings.xml') as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    # Namespace for spreadsheetml
                    ns = {'a': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                    # Some files use 't', some use 'si/t'
                    for t in root.iter():
                        if t.tag.endswith('}t'):
                             shared_strings.append(t.text if t.text else "")
            
            print(f"Found {len(shared_strings)} shared strings.")

            # 2. Parse Sheet 1
            if 'xl/worksheets/sheet1.xml' in z.namelist():
                with z.open('xl/worksheets/sheet1.xml') as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    
                    data = []
                    # Rows are usually in {ns}sheetData/{ns}row
                    for row in root.iter():
                        if row.tag.endswith('}row'):
                            row_data = []
                            cells = list(row)
                            
                            # We need to handle column indices to ensure alignment
                            # cell tag usually contains 'r' attribute like "A1", "B1"
                            # But simple iteration often works if sparse not heavily used
                            
                            current_col_idx = 0
                            parsed_row = {}
                            
                            for cell in cells:
                                if not cell.tag.endswith('}c'):
                                    continue
                                
                                # specific cell coordination
                                r_attr = cell.attrib.get('r', '')
                                # simple check for type
                                t_attr = cell.attrib.get('t', 'n') # default number
                                
                                # Get value
                                v_val = ""
                                for child in cell:
                                    if child.tag.endswith('}v'):
                                        v_val = child.text
                                        break
                                    if child.tag.endswith('}is'): # Inline string
                                         for t_node in child:
                                             if t_node.tag.endswith('}t'):
                                                 v_val = t_node.text
                                
                                # Resolve value
                                final_val = v_val
                                if t_attr == 's' and v_val: # Shared string
                                    try:
                                        idx = int(v_val)
                                        if 0 <= idx < len(shared_strings):
                                            final_val = shared_strings[idx]
                                    except:
                                        pass
                                elif t_attr == 'b': # Boolean
                                    final_val = True if v_val == '1' else False
                                
                                # Store based on column 'r' if possible, else append
                                # Simplified: just extract column letter to sort
                                col_match = re.search(r"[A-Z]+", r_attr)
                                if col_match:
                                    col_letter = col_match.group(0)
                                    parsed_row[col_letter] = final_val
                            
                            data.append(parsed_row)
                            
                    # Convert list of dicts to DataFrame
                    # Using dataframe from dict list handles missing columns automatically
                    df = pd.DataFrame(data)
                    
                    # Sort columns A, B, C... (basic sort might fail for AA, but dataset likely small width)
                    # We can enforce column order if we know headers? 
                    # Let's just trust pandas default alignment first
                    
                    # Assuming first row is header
                    if len(df) > 0:
                        new_header = df.iloc[0]
                        df = df[1:]
                        df.columns = new_header
                        
                    return df
            else:
                print("Sheet1 not found.")
                return None

    except Exception as e:
        print(f"Extraction failed: {e}")
        return None

df = extract_excel_manual(file_path)

if df is not None:
    print("Extraction successful!")
    print(df.info())
    print(df.head())
    df.to_csv('parsed_dataset.csv', index=False)
else:
    print("Could not extract data.")
