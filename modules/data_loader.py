import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def load_data():
    """Loads all mock data CSVs into a dictionary of DataFrames."""
    data = {}
    try:
        data['hr_master'] = pd.read_csv(os.path.join(DATA_DIR, 'hr_master.csv'))
        data['hr_event_log'] = pd.read_csv(os.path.join(DATA_DIR, 'hr_event_log.csv'))
        data['tna_record'] = pd.read_csv(os.path.join(DATA_DIR, 'tna_record.csv'))
        data['shadow_ledger'] = pd.read_csv(os.path.join(DATA_DIR, 'shadow_ledger.csv'))
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        # Return empty DFs if files missing to prevent crash
        data['hr_master'] = pd.DataFrame()
        data['hr_event_log'] = pd.DataFrame()
        data['tna_record'] = pd.DataFrame()
        data['shadow_ledger'] = pd.DataFrame()
    
    return data

def reset_data():
    """Reloads data from CSVs to reset the session state."""
    return load_data()
