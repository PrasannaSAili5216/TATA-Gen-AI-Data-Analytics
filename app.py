
import os
import sys
import subprocess
import pandas as pd
from flask import Flask, render_template, jsonify, request, send_file

app = Flask(__name__)

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'cleaned_dataset.csv')
RAW_FILE = os.path.join(BASE_DIR, 'parsed_dataset.csv')
SCRIPTS = {
    'preprocess': 'preprocess_data.py',
    'train': 'train_model.py',
    'bias': 'evaluate_bias.py',
    'shap': 'explain_model_shap.py'  # Assuming this exists based on files list
}

def run_script(script_name):
    """Executes a python script and returns the output."""
    script_path = os.path.join(BASE_DIR, script_name)
    if not os.path.exists(script_path):
        return False, f"Script {script_name} not found."
    
    try:
        # Run the script and capture output
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            cwd=BASE_DIR
        )
        if result.returncode != 0:
            return False, f"Error (Exit Code {result.returncode}):\n{result.stderr}\n{result.stdout}"
        return True, result.stdout
    except Exception as e:
        return False, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data_summary')
def data_summary():
    """Returns summary of the current dataset."""
    target_file = DATA_FILE if os.path.exists(DATA_FILE) else RAW_FILE
    if not os.path.exists(target_file):
        return jsonify({'error': 'No dataset found. Run preprocessing first.'})
    
    try:
        df = pd.read_csv(target_file)
        summary = {
            'filename': os.path.basename(target_file),
            'rows': len(df),
            'columns': list(df.columns),
            'preview': df.head().to_dict(orient='records'),
            'missing_values': df.isnull().sum().to_dict()
        }
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/run_preprocess', methods=['POST'])
def run_preprocess():
    success, output = run_script(SCRIPTS['preprocess'])
    return jsonify({'success': success, 'output': output})

@app.route('/api/run_train', methods=['POST'])
def run_train():
    success, output = run_script(SCRIPTS['train'])
    return jsonify({'success': success, 'output': output})

@app.route('/api/run_bias', methods=['POST'])
def run_bias():
    success, output = run_script(SCRIPTS['bias'])
    # formatting output to include the report file content if successful
    if success:
        report_path = os.path.join(BASE_DIR, 'bias_report.txt')
        if os.path.exists(report_path):
            with open(report_path, 'r', encoding='utf-8') as f:
                report_content = f.read()
            output += f"\n\n--- Report Content ---\n{report_content}"
    return jsonify({'success': success, 'output': output})

@app.route('/api/run_shap', methods=['POST'])
def run_shap():
    # Only if shap script exists
    if not os.path.exists(os.path.join(BASE_DIR, SCRIPTS['shap'])):
         return jsonify({'success': False, 'output': "SHAP script not found."})
         
    success, output = run_script(SCRIPTS['shap'])
    return jsonify({'success': success, 'output': output})

@app.route('/api/get_shap_plot')
def get_shap_plot():
    plot_path = os.path.join(BASE_DIR, 'shap_summary_plot.png')
    if os.path.exists(plot_path):
        return send_file(plot_path, mimetype='image/png')
    return jsonify({'error': 'Plot not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
