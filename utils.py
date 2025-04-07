import pandas as pd
from pathlib import Path
from config.settings import TRANSLATION_TABLE_PATH, DEFAULT_TESTCASE_PATH

def load_translation_table(path=None):
    path = Path(path) if path else TRANSLATION_TABLE_PATH
    if not path.exists():
        raise FileNotFoundError(f"Translation table not found at {path}")
    
    df = pd.read_excel(path)
    return dict(zip(df['Command'], df['Selenium Code']))

def load_testcase(path=None):
    path = Path(path) if path else DEFAULT_TESTCASE_PATH
    if not path.exists():
        raise FileNotFoundError(f"Test case file not found at {path}")
    
    df = pd.read_excel(path)
    required_columns = {'Step', 'Command'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Test case file must contain columns: {required_columns}")
    
    return df.fillna('')
    
def generate_code_from_testcase(testcase_df, translation_table):
    """Generate executable Python code from test case dataframe using translation table"""
    script_lines = []
    for _, row in testcase_df.iterrows():
        command = row['Command']
        template = translation_table.get(command, '')
        if not template:
            continue
            
        line = template
        if '{locator}' in template:
            line = line.replace('{locator}', str(row.get('Locator', '')))
        if '{value}' in template:
            line = line.replace('{value}', str(row.get('Value', '')))
        if '{url}' in template:
            line = line.replace('{url}', str(row.get('Value', '')))
            
        script_lines.append(line)
    return script_lines