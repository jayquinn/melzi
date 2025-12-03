import random
from datetime import datetime, timedelta

def generate_mock_data(base_issues, target_count=150):
    """
    Generates enriched mock data based on a list of base issues.
    Scales up the data to target_count and assigns random attributes.
    """
    
    # Base data for randomization
    first_names = ["지훈", "서준", "민준", "도윤", "예준", "시우", "하준", "주원", "지우", "서현", "서연", "지민", "민서", "하은", "다은", "수빈", "소율", "예린", "지원", "수아"]
    last_names = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임", "한", "오", "서", "신", "권", "황", "안", "송", "류", "전"]
    
    workplaces = ["본사", "장항", "천안", "대전", "신탄진"]
    managers = {"본사": "강전무", "장항": "김공장장", "천안": "이센터장", "대전": "박지점장", "신탄진": "최소장"}
    
    # Clone and expand issues
    expanded_issues = []
    original_count = len(base_issues)
    
    for i in range(target_count):
        # Cycle through original issues as templates
        template = base_issues[i % original_count].copy()
        
        # Randomize Identity
        new_name = f"{random.choice(last_names)}{random.choice(first_names)}"
        template['name'] = new_name
        template['employee_id'] = f"E{20240000 + i}"
        template['issue_id'] = f"{template['type'][0]}-{20240000 + i}" # e.g., C-20240001
        
        # 1. Assign Workplace & Manager
        wp_idx = hash(new_name) % len(workplaces)
        template['workplace'] = workplaces[wp_idx]
        template['manager_id'] = managers[template['workplace']]
        
        # 2. Assign Special Status
        # Weighted random choice: '일반' is most common
        rand_val = random.random()
        if rand_val < 0.05: template['special_status'] = "중도입사자"
        elif rand_val < 0.1: template['special_status'] = "중도퇴사자"
        elif rand_val < 0.15: template['special_status'] = "휴직자"
        elif rand_val < 0.2: template['special_status'] = "복직자"
        elif rand_val < 0.3: template['special_status'] = "근무형태 변경자"
        else: template['special_status'] = "일반 (특이사항 없음)"
        
        # 3. Overwrite Details based on Special Status (Consistency Logic)
        if template['special_status'] == "중도입사자":
            template['type'] = 'Auditor'
            template['title'] = "신규 입사자 일할 계산"
            template['event_id'] = "신규 입사"
            template['logic_text'] = "입사일(11/15) 기준 급여 일할 계산 필요"
            template['diff'] = random.randint(120, 180) * 10000
            
        elif template['special_status'] == "중도퇴사자":
            template['type'] = 'Auditor'
            template['title'] = "중도 퇴사자 급여/연차 정산"
            template['event_id'] = "퇴직 정산"
            template['logic_text'] = "퇴사일(11/20) 기준 급여 및 잔여 연차 정산"
            template['diff'] = random.randint(-80, -30) * 10000
            
        elif template['special_status'] == "휴직자":
            template['type'] = 'Auditor'
            template['title'] = "휴직 발령에 따른 급여 중단"
            template['event_id'] = "휴직 발령"
            template['logic_text'] = "휴직 시작일(11/01)부터 급여 지급 중단 확인"
            template['diff'] = random.randint(-350, -250) * 10000
            
        elif template['special_status'] == "복직자":
            template['type'] = 'Auditor'
            template['title'] = "복직자 급여 재개"
            template['event_id'] = "복직 발령"
            template['logic_text'] = "복직일(11/10) 기준 급여 일할 계산 및 지급 재개"
            template['diff'] = random.randint(200, 280) * 10000
            
        elif template['special_status'] == "근무형태 변경자":
            template['type'] = 'Auditor'
            template['title'] = "교대조 변경 수당 차액"
            template['event_id'] = "근무조 변경"
            template['logic_text'] = "3교대 -> 주간 근무 변경에 따른 야간 수당 제외"
            template['diff'] = random.randint(-20, -10) * 10000
            
        else: # "일반" - Keep original template logic but refine Event ID
            if template['type'] == 'Auditor':
                if "소급" in template['title']:
                    template['event_id'] = "10/1 정기 승진"
                elif "일할" in template['title']:
                    template['event_id'] = "11/1 조직 개편"
                else:
                    template['event_id'] = "수시 인사이동"
            elif template['type'] == 'Chaser':
                template['event_id'] = "11월 근태 마감"
            else:
                template['event_id'] = "상시 복리후생"

        # 4. Role-Pay Mismatch Mock Data (Only for General)
        # Force at least one occurrence for demo (i==0 ensures it appears)
        if i == 0 or (template['special_status'] == "일반 (특이사항 없음)" and template['type'] == 'Auditor' and i % 50 == 0):
             # Force type to Auditor if it's the forced case
             template['type'] = 'Auditor'
             template['job_change_date'] = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
             template['title'] = "위험수당 (Role-Pay Mismatch)"
             template['diff'] = 150000
             template['logic_text'] = "사무직 발령(3개월 전) 후에도 위험수당이 계속 지급되고 있습니다."
             template['event_id'] = "11/1 조직 개편"
        else:
            template.pop('job_change_date', None) 

        # 5. Bottleneck Manager Mock Data (Only for General)
        # Force bottleneck for demo: Accumulate issues for Park
        # Ensure at least 6 issues are Chasers for Park to hit the limit (5)
        if i < 6:
            template['special_status'] = "일반 (특이사항 없음)"
            template['type'] = 'Chaser'
            template['workplace'] = "대전"
            template['manager_id'] = "박지점장"
            template['event_id'] = "11월 근태 마감" # Ensure valid event ID
            template['description'] = "11월 근태 확정 미완료" # Fix KeyError
        elif template['special_status'] == "일반 (특이사항 없음)" and template['type'] == 'Chaser': 
            template['workplace'] = "대전"
            template['manager_id'] = "박지점장"
            
        expanded_issues.append(template)

    # 6. Inject Work Plan vs OT Mismatch (Mock) - "Fresh" Insight
    # Scenario: OT Record exists but no Work Plan
    candidates = [i for i in expanded_issues if i['special_status'] == "일반 (특이사항 없음)" and i['type'] == 'Auditor']
    if candidates:
        target = candidates[0]
        target['issue_id'] = f"{target['issue_id']}-WPM"
        target['title'] = "계획되지 않은 초과근무 (Unplanned OT)"
        target['diff'] = 85000
        target['logic_text'] = "사전 업무 계획 없이 4시간의 초과근무가 기록되었습니다."
        target['event_id'] = "근태 불일치"
        target['description'] = "업무 계획 미수립"
        
    return expanded_issues
