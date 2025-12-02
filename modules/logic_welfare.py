import pandas as pd
import os

def get_welfare_issues(data_dir):
    """
    Loads welfare claims from CSV.
    """
    try:
        df = pd.read_csv(os.path.join(data_dir, 'welfare_claims.csv'))
        issues = []
        
        # Filter for Pending
        pending = df[df['status'] == 'Pending']
        
        for _, row in pending.iterrows():
            issues.append({
                'issue_id': row['claim_id'],
                'type': 'Welfare',
                'employee_id': row['employee_id'],
                'name': row['name'],
                'title': row['treatment_type'],
                'amount': row['amount'],
                'receipt_items': row['receipt_items'].replace('\\n', '\n'),
                'ai_verdict': row['ai_verdict'],
                'ai_reason': row['ai_reason'],
                'policy_ref': row['policy_ref'],
                'status': 'Pending'
            })
            
        return issues
    except Exception as e:
        print(f"Error loading welfare claims: {e}")
        return []
