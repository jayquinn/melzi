def detect_insights(issues):
    """
    Analyzes the list of issues and detects potential risks or anomalies.
    Returns a list of insight dictionaries.
    """
    insights = []
    
    # 1. Role-Pay Mismatch (Limit to 1 for variety)
    mismatch_issues = [i for i in issues if i.get('job_change_date')]
    if mismatch_issues:
        issue = mismatch_issues[0] 
        insights.append({
            "type": "Role-Pay Mismatch",
            "title": "직무 불일치 수당 발견",
            "message": f"**{issue['name']}**님은 3개월 전 사무직으로 발령 났으나, 규정에 어긋난 **'{issue['title']}'**이 계속 지급되고 있습니다.",
            "action": "지급 중단 및 환수 제안",
            "color": "red",
            "issue_ids": [issue['issue_id']] 
        })

    # 2. Work Plan vs OT Mismatch (New & Impactful!)
    unplanned_ot = [i for i in issues if i.get('title') == "계획되지 않은 초과근무 (Unplanned OT)"]
    if unplanned_ot:
        count = len(unplanned_ot)
        insights.append({
            "type": "Unplanned OT",
            "title": "업무 계획 불일치 감지",
            "message": f"**{count}명**의 직원이 사전 업무 계획 없이 초과근무를 수행했습니다. 부서장 승인 여부를 확인해야 합니다.",
            "action": "부서장 확인 요청",
            "color": "red",
            "issue_ids": [i['issue_id'] for i in unplanned_ot]
        })

    # 3. Bottleneck Manager
    chaser_issues = [i for i in issues if i['type'] == 'Chaser']
    if chaser_issues:
        manager_counts = {}
        manager_issue_ids = {} 
        
        for i in chaser_issues:
            mgr = i.get('manager_id', 'Unknown')
            manager_counts[mgr] = manager_counts.get(mgr, 0) + 1
            if mgr not in manager_issue_ids: manager_issue_ids[mgr] = []
            manager_issue_ids[mgr].append(i['issue_id'])
            
        total_chasers = len(chaser_issues)
        for mgr, count in manager_counts.items():
            if count >= total_chasers * 0.5 and total_chasers > 1: 
                insights.append({
                    "type": "Bottleneck Manager",
                    "title": "결재 병목 감지",
                    "message": f"현재 미마감 건의 **{int(count/total_chasers*100)}%**가 **'{mgr}'** 결재함에 멈춰 있습니다. 개별 독촉보다 리마인드가 효과적입니다.",
                    "action": f"{mgr}에게 요약 리포트 발송",
                    "color": "orange",
                    "issue_ids": manager_issue_ids[mgr] 
                })
                
    return insights
