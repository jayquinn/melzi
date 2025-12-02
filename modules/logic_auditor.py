import pandas as pd

def get_auditor_issues(shadow_ledger_df, hr_master_df):
    """
    Retrieves payroll issues (The Auditor) from the Shadow Ledger.
    """
    issues = []
    
    # Filter for Pending issues
    pending_issues = shadow_ledger_df[shadow_ledger_df['status'] == 'Pending']
    
    for _, row in pending_issues.iterrows():
        emp_id = row['employee_id']
        
        # Get employee name
        emp_info = hr_master_df[hr_master_df['employee_id'] == emp_id]
        name = emp_info['name'].values[0] if not emp_info.empty else "Unknown"
        
        # Determine color based on diff
        diff = row['diff']
        
        issues.append({
            'issue_id': row['issue_id'],
            'type': 'Auditor',
            'employee_id': emp_id,
            'name': name,
            'title': row['issue_type'], # e.g., 소급, 일할
            'diff': diff,
            'logic_text': row['logic_text'],
            'action_label': '다빈치 적용',
            'status': 'Pending'
        })
        
    return issues
