def get_chaser_issues(tna_df, hr_master_df):
    """
    Identifies attendance issues (The Chaser).
    Logic: Status != 'Approved' (In this mock, we just check for '미마감')
    """
    issues = []
    
    # Filter for unapproved records
    unapproved = tna_df[tna_df['status'] == '미마감']
    
    # Group by employee to count missing days
    if not unapproved.empty:
        # Group by employee and aggregate dates
        grouped = unapproved.groupby('employee_id')['date'].apply(list).reset_index(name='dates')
        
        for _, row in grouped.iterrows():
            emp_id = row['employee_id']
            dates = row['dates']
            count = len(dates)
            
            # Format dates (e.g., "11월 28일, 11월 29일")
            formatted_dates = ", ".join([d.split('-')[1] + "월 " + d.split('-')[2] + "일" for d in dates])
            
            # Get employee name
            emp_info = hr_master_df[hr_master_df['employee_id'] == emp_id]
            name = emp_info['name'].values[0] if not emp_info.empty else "Unknown"
            
            issues.append({
                'issue_id': f"CHASER-{emp_id}",
                'type': 'Chaser',
                'employee_id': emp_id,
                'name': name,
                'title': '근태 미마감',
                'description': f"{formatted_dates} ({count}건) 미마감",
                'action_label': '발송 승인',
                'status': 'Pending'
            })
            
    return issues
