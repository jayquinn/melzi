def get_bot_response(user_input, context):
    """
    Returns a hardcoded response based on keywords and context (selected issue).
    """
    user_input = user_input.lower()
    
    if not context:
        return "어떤 안건에 대해 궁금하신가요? 카드를 선택해주세요."
    
    issue_type = context.get('title', '')
    emp_name = context.get('name', '')
    
    # Scenario 1: Retroactive (Kim Cheol-su)
    if "소급" in issue_type or "김철수" in emp_name:
        if "근거" in user_input or "왜" in user_input or "이유" in user_input:
            return f"{emp_name}님의 경우, 10월 1일자 과장 승진 발령이 11월 15일에 입력되었습니다. 이에 따라 10월분 급여 차액(기본급 인상분) 1개월치가 소급 적용되었습니다. (규정: 인사규정 제5조 급여의 계산)"
        if "계산" in user_input:
            return "계산식: (변경 후 기본급 5,450,000 - 변경 전 기본급 5,000,000) * 1개월 = 450,000원"

    # Scenario 2: Prorated (Lee Young-hee) - Leave
    if "일할" in issue_type or "이영희" in emp_name:
        if "근거" in user_input or "왜" in user_input:
            return f"{emp_name}님은 11월 10일부터 육아휴직이 시작되었습니다. 따라서 11월 급여는 1일부터 9일까지 9일치만 일할 계산되어 지급됩니다."
            
    # Scenario 3: Allowance (Choi Sawon) - Child
    if "수당" in issue_type or "최사원" in emp_name:
        if "근거" in user_input:
            return f"{emp_name}님의 자녀 출산 사실이 확인되어, 가족수당 지급 대상이 1명 추가되었습니다. (배우자1 + 자녀2 = 총 3명분 지급)"

    return "죄송합니다. 해당 질의에 대한 정확한 근거를 찾지 못했습니다. 담당자 확인이 필요합니다."
