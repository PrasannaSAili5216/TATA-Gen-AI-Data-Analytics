
import zipfile

file_path = 'TASK_DETAILS/TASK_1/Delinquency_prediction_dataset.xlsx'

try:
    with zipfile.ZipFile(file_path, 'r') as z:
        if 'xl/worksheets/sheet1.xml' in z.namelist():
            with z.open('xl/worksheets/sheet1.xml') as f:
                content = f.read(1000) # Read first 1000 bytes
                print(content.decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")
