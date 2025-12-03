import streamlit as st
import pandas as pd
import time
from modules import data_loader, logic_chaser, logic_auditor, logic_welfare, chatbot, mock_generator, insight_engine, config_manager
from ui import cards

# --- Page Config ---
st.set_page_config(
    page_title="Melzi: Payroll Agentic Workflow",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Styling ---
st.markdown("""
<style>
    /* Global Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Card Container */
    .card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #f0f2f6;
        transition: transform 0.2s;
    }
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.1);
    }

    /* Card Header */
    .card-header {
        display: flex;
        justify_content: space-between;
        align_items: center;
        margin-bottom: 15px;
    }
    .card-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1f2937;
    }
    
    /* Badges */
    .badge {
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    .chaser-badge {
        background-color: #e0f2fe;
        color: #0369a1;
    }
    .auditor-badge {
        background-color: #f3e8ff;
        color: #7e22ce;
    }

    /* Stats */
    .stat-row {
        display: flex;
        justify_content: space-between;
    }
    .stat-item {
        display: flex;
        flex-direction: column;
    }
    .stat-label {
        font-size: 0.8rem;
        color: #6b7280;
        margin-bottom: 4px;
    }
    .stat-value {
        font-size: 1.1rem;
        font-weight: 600;
    }
    .positive-diff { color: #059669; }
    .negative-diff { color: #dc2626; }
    .warning-text { color: #d97706; }

    /* Inbox Zero */
    .inbox-zero {
        text-align: center;
        padding: 50px;
        animation: fadeIn 1s;
    }
    .inbox-zero h1 {
        font-size: 3rem;
        margin-bottom: 10px;
    }
    .inbox-zero p {
        font-size: 1.5rem;
        color: #4b5563;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Reset Button in Sidebar */
    .reset-btn-container {
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #e5e7eb;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)
# --- State Management ---
if 'data_loaded' not in st.session_state:
    data = data_loader.load_data()
    st.session_state['data'] = data
    
    # Generate initial issues
    chaser_issues = logic_chaser.get_chaser_issues(data['tna_record'], data['hr_master'])
    auditor_issues = logic_auditor.get_auditor_issues(data['shadow_ledger'], data['hr_master'])
    welfare_issues = logic_welfare.get_welfare_issues(data_loader.DATA_DIR)
    
    all_issues = chaser_issues + auditor_issues + welfare_issues
    
    # --- Mock Data Enrichment for Melzi 2.0 (Refactored) ---
    # Optimized for Demo: Reduced scale to 50 issues (approx 400 employees) for speed
    expanded_issues = mock_generator.generate_mock_data(all_issues, target_count=50)

    st.session_state['issues'] = expanded_issues
    st.session_state['completed_issues'] = []
    st.session_state['chat_history'] = []
    st.session_state['active_issue'] = None
    st.session_state['data_loaded'] = True

def reset_app():
    st.session_state.clear()
    st.rerun()

def handle_approve(issue, rerun=True):
    # Simulate API call
    with st.spinner("메신저 발송 중..."):
        time.sleep(0.1) # Optimized for Demo
    st.toast(f"✅ {issue['name']}님에게 독촉 메시지를 발송했습니다.")
    
    # Move to completed
    issue['status'] = 'Approved'
    issue['action_taken'] = '메시지 발송'
    st.session_state['completed_issues'].insert(0, issue)
    
    # Remove from list
    st.session_state['issues'] = [i for i in st.session_state['issues'] if i['issue_id'] != issue['issue_id']]
    if rerun:
        st.rerun()

def handle_apply(issue, rerun=True):
    # Simulate DB Update
    with st.spinner("Davinci DB 업데이트 중..."):
        time.sleep(0.1) # Optimized for Demo
    st.toast(f"✅ {issue['name']}님의 급여 정보가 업데이트되었습니다.")
    
    # Move to completed
    issue['status'] = 'Applied'
    issue['action_taken'] = 'DB 반영'
    st.session_state['completed_issues'].insert(0, issue)
    
    # Remove from list
    st.session_state['issues'] = [i for i in st.session_state['issues'] if i['issue_id'] != issue['issue_id']]
    if rerun:
        st.rerun()

def handle_ignore(issue, rerun=True):
    st.toast(f"db {issue['name']}님의 이슈를 무시했습니다.")
    
    # Move to completed
    issue['status'] = 'Ignored'
    issue['action_taken'] = '무시하기'
    st.session_state['completed_issues'].insert(0, issue)
    
    # Remove from list
    st.session_state['issues'] = [i for i in st.session_state['issues'] if i['issue_id'] != issue['issue_id']]
    if rerun:
        st.rerun()

def handle_welfare_approve(issue, rerun=True):
    # 1. Simulate API call
    with st.spinner("급여 대장 반영 중..."):
        time.sleep(0.1) # Optimized for Demo
    
    # 2. Create new Payroll Issue (Integration)
    new_payroll_issue = {
        'issue_id': f"PAY-{issue['issue_id']}",
        'type': 'Auditor',
        'employee_id': issue['employee_id'],
        'name': issue['name'],
        'title': '의료비',
        'diff': issue['amount'],
        'logic_text': f"의료비 지원금 ({issue['title']}) - {issue['ai_reason']}",
        'action_label': '다빈치 적용',
        'status': 'Pending'
    }
    
    # 3. Update Session State
    # Move welfare issue to completed
    issue['status'] = 'Approved'
    issue['action_taken'] = '급여 반영'
    st.session_state['completed_issues'].insert(0, issue)
    
    # Remove welfare issue
    st.session_state['issues'] = [i for i in st.session_state['issues'] if i['issue_id'] != issue['issue_id']]
    # Add new payroll issue
    st.session_state['issues'].append(new_payroll_issue)
    
    st.toast(f"✅ 승인 완료! '급여 심사' 탭에 지급 내역({issue['amount']:,}원)이 추가되었습니다.")
    if rerun:
        st.rerun()

def handle_welfare_reject(issue, rerun=True):
    with st.spinner("반려 처리 중..."):
        time.sleep(0.1) # Optimized for Demo
    st.toast(f"🚫 {issue['name']}님의 의료비 청구가 반려되었습니다.")
    
    # Move to completed
    issue['status'] = 'Rejected'
    issue['action_taken'] = '반려'
    st.session_state['completed_issues'].insert(0, issue)
    
    # Remove from list
    st.session_state['issues'] = [i for i in st.session_state['issues'] if i['issue_id'] != issue['issue_id']]
    if rerun:
        st.rerun()

def set_active_issue(issue):
    st.session_state['active_issue'] = issue

def handle_insight_action(insight):
    target_ids = insight['issue_ids']
    processed_count = 0
    
    # Identify issues to move
    to_move = [i for i in st.session_state['issues'] if i['issue_id'] in target_ids]
    
    for issue in to_move:
        # Update status based on insight type
        if insight['type'] == "Role-Pay Mismatch":
            issue['status'] = 'Resolved'
            issue['action_taken'] = '환수 제안'
        elif insight['type'] == "Bottleneck Manager":
            issue['status'] = 'Reminded'
            issue['action_taken'] = '리포트 발송'
        elif insight['type'] == "Unplanned OT":
            issue['status'] = 'Investigating'
            issue['action_taken'] = '부서장 확인'
            
        # Move to completed
        st.session_state['completed_issues'].insert(0, issue)
        processed_count += 1
        
    # Remove from active list
    st.session_state['issues'] = [i for i in st.session_state['issues'] if i['issue_id'] not in target_ids]
    
    st.toast(f"✅ {processed_count}건의 이슈를 처리하고 완료 내역으로 이동했습니다.")
    time.sleep(0.2)
    st.rerun()

# --- Sidebar ---
with st.sidebar:
    # --- Melzi's Deep Insight (Sidebar) ---
    insights = insight_engine.detect_insights(st.session_state['issues'])
    if insights:
        st.markdown("### 🚨 Risk Monitor")
        for i, insight in enumerate(insights):
            with st.expander(f"{insight['title']}", expanded=True):
                st.caption(insight['message'])
                if st.button(insight['action'], key=f"btn_insight_side_{insight['type']}_{i}"):
                    handle_insight_action(insight)
        st.divider()
    
    st.title("Melzi Talk 💬")
    
    # Chat History
    for msg in st.session_state['chat_history']:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    # Chat Input
    if prompt := st.chat_input("무엇을 도와드릴까요?"):
        # User Message
        st.session_state['chat_history'].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
            
        # Bot Response
        response = chatbot.get_bot_response(prompt, st.session_state['active_issue'])
        st.session_state['chat_history'].append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

    # Reset Button (Bottom)
    st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True) 
    if st.button("🔄 데모 초기화", type="primary", use_container_width=True):
        reset_app()
        
    st.markdown("---")
    admin_mode = st.toggle("⚙️ Admin Mode")

def render_admin_page():
    st.title("Melzi Admin: Control Center 🛠️")
    st.caption("급여 계산 파라미터 및 리스크 감지 임계값을 설정합니다.")
    
    config = config_manager.load_config()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["⚙️ 기초 설정", "🧠 심층 분석", "🔔 알림 봇", "🛡️ 시뮬레이션"])
    
    with tab1:
        st.subheader("Global Parameters")
        col1, col2 = st.columns(2)
        with col1:
            new_min_wage = st.number_input("최저임금 (원)", value=config.get('min_wage', 9860))
            new_overtime_rate = st.number_input("야근 할증률 (배)", value=config.get('overtime_rate', 1.5), step=0.1)
        with col2:
            new_meal_limit = st.number_input("식대 비과세 한도 (원)", value=config.get('meal_tax_free_limit', 200000))
            new_family_allowance = st.number_input("가족수당 인당 (원)", value=config.get('family_allowance_per_person', 100000))
            
    with tab2:
        st.subheader("Insight Thresholds")
        new_zombie_months = st.slider("직무 불일치 감지 (개월)", 1, 12, config.get('zombie_months', 3))
        new_bottleneck_limit = st.number_input("결재 병목 경고 (건수)", value=config.get('bottleneck_limit', 15))
        new_ghost_tolerance = st.number_input("유령 근무 허용 오차 (분)", value=config.get('ghost_shift_tolerance', 60))
        
    with tab3:
        st.subheader("Chaser Config")
        new_schedule = st.multiselect("알림 발송 스케줄", ["D-5", "D-3", "D-1", "D-Day"], default=config.get('notification_schedule', ["D-5", "D-3", "D-1"]))
        new_vip_filter = st.multiselect("VIP 필터 (발송 제외)", ["Executive", "Team Lead", "Manager"], default=config.get('vip_filter', ["Executive", "Team Lead"]))
        new_template = st.text_area("메시지 템플릿", value=config.get('msg_template', ""))
        
    with tab4:
        st.subheader("Simulation & Save")
        st.info("설정 변경 후 '시뮬레이션'을 먼저 실행해야 저장이 가능합니다.")
        
        # Draft Config Object
        draft_config = config.copy()
        draft_config.update({
            "min_wage": new_min_wage,
            "overtime_rate": new_overtime_rate,
            "meal_tax_free_limit": new_meal_limit,
            "family_allowance_per_person": new_family_allowance,
            "zombie_months": new_zombie_months,
            "bottleneck_limit": new_bottleneck_limit,
            "ghost_shift_tolerance": new_ghost_tolerance,
            "notification_schedule": new_schedule,
            "vip_filter": new_vip_filter,
            "msg_template": new_template
        })
        
        if st.button("🚀 Run Simulation", type="primary"):
            with st.spinner("영향도 분석 중..."):
                time.sleep(0.3) # Fake simulation
                
            # Mock Impact Analysis
            st.success("시뮬레이션 완료!")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("예상 급여 변동", "+0.5%", delta_color="inverse")
            with col_b:
                st.metric("감지될 이슈 수", "8건 (+3)", delta_color="inverse")
                
            st.warning("⚠️ 변경 사항을 적용하시겠습니까?")
            if st.button("💾 Save & Apply"):
                if config_manager.save_config(draft_config):
                    st.toast("설정이 저장되었습니다!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("저장 실패")
        
        if st.button("초기화 (Reset to Default)"):
            config_manager.reset_config()
            st.rerun()

# --- Main Content ---
if admin_mode:
    render_admin_page()
else:
    st.title("Melzi InBOX 📥")

# --- Daily Briefing Dashboard ---
with st.container():
    st.markdown("### 📊 Daily Briefing")
    col1, col2, col3 = st.columns(3)

    # 1. Attendance Status
    with col1:
        st.metric(label="근태 마감 (11/23)", value="D-3")
        st.progress(0.88) # Mock data: 88% completed
        st.caption("✅ 근태 확정: 88% (352/400명)")

    # 2. Payroll Status
    with col2:
        issue_count = len(st.session_state['issues'])
        st.metric(label="급여 마감 (11/28)", value="D-8")
        # Calculate readiness based on issue count (arbitrary scale for demo)
        readiness = max(0.0, min(1.0, 1.0 - (issue_count / 20))) 
        st.progress(readiness)
        st.caption(f"🚨 잔여 이슈: {issue_count}건")

    # 3. Financial Overview
    with col3:
        st.metric(label="현재 예상 급여 총액", value="15.4억", delta="+1.2% (전월비)")
        st.caption("💰 전월 대비 안정적")
    
    st.divider()

# System Notice
st.info("""
**ℹ️ System Status: Operational**  
Melzi는 매일 오전 3시 Davinci HRIS의 근태/인사 데이터를 동기화하여 변동 사항을 감지합니다.  
감지된 이슈는 실시간으로 급여 시뮬레이션에 반영되며, 담당자의 승인을 통해 최종 확정됩니다.
""")

# Metrics
total_issues = len(st.session_state['issues'])
chaser_count = len([i for i in st.session_state['issues'] if i['type'] == 'Chaser'])
auditor_count = len([i for i in st.session_state['issues'] if i['type'] == 'Auditor'])
welfare_count = len([i for i in st.session_state['issues'] if i['type'] == 'Welfare'])

def render_metric_card(label, value, icon, color_class):
    st.markdown(f"""
    <div class="card metric-card" style="text-align: center; padding: 15px;">
        <div style="font-size: 2rem; margin-bottom: 5px;">{icon}</div>
        <div style="font-size: 0.9rem; color: #6b7280; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">{label}</div>
        <div style="font-size: 1.8rem; font-weight: 800; color: #111827; margin-top: 5px;">{value}</div>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    render_metric_card("총 대기 건수", total_issues, "📮", "text-gray-900")
with col2:
    render_metric_card("근태 소명", chaser_count, "⏰", "text-blue-600")
with col3:
    render_metric_card("급여 심사", auditor_count, "💰", "text-purple-600")
with col4:
    render_metric_card("의료비 심사", welfare_count, "🏥", "text-green-600")

st.markdown("---")

# Inbox Zero Check
if total_issues == 0 and len(st.session_state['completed_issues']) == 0:
    st.markdown("""
    <div class="inbox-zero">
        <h1>&#127881;</h1>
        <p>모든 마감 이슈가 처리되었습니다.</p>
        <p><strong>퇴근하세요!</strong></p>
    </div>
    """, unsafe_allow_html=True)
else:
    # --- Pivot View Controller ---
    st.markdown("### 🔀 Pivot View")
    view_mode = st.radio(
        "기준 선택:",
        ["이슈별 (Issue Type)", "특이사항별 (Special Status)", "사업장별 (Workplace)", "원인별 (Cause)"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Filter Tabs (Keep for now, but content changes based on Pivot)
    # Actually, Pivot View replaces the Tabs concept for the main list. 
    # But to keep existing structure, let's apply Pivot View to "전체 보기" tab primarily.
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["전체 보기", "근태 소명", "급여 심사", "의료비 심사", "완료 내역"])

    def render_grouped_issues(issues, tab_key, mode="이슈별 (Issue Type)"):
        if not issues:
            st.info("대기 중인 이슈가 없습니다.")
            return

        # 1. Dynamic Grouping Logic
        groups = {}
        
        if "이슈별" in mode:
            # Strict 3 Categories
            groups = {
                "🚨 [Action Required] 근태 소명": [],
                "💰 [Approval Pending] 급여 변동 심사": [],
                "🧾 [Claims] 의료비/복리후생": []
            }
            for issue in issues:
                if issue['type'] == 'Chaser':
                    groups["🚨 [Action Required] 근태 소명"].append(issue)
                elif issue['type'] == 'Auditor':
                    groups["💰 [Approval Pending] 급여 변동 심사"].append(issue)
                elif issue['type'] == 'Welfare':
                    groups["🧾 [Claims] 의료비/복리후생"].append(issue)
                    
        elif "특이사항별" in mode:
            for issue in issues:
                status = issue.get('special_status', '일반 (특이사항 없음)')
                # Add emoji based on status
                emoji = "👤"
                if "입사" in status: emoji = "🆕"
                elif "퇴사" in status: emoji = "👋"
                elif "휴직" in status: emoji = "🛌"
                elif "복직" in status: emoji = "🔙"
                elif "변경" in status: emoji = "🔄"
                
                key = f"{emoji} {status}"
                if key not in groups: groups[key] = []
                groups[key].append(issue)
                
        elif "사업장별" in mode:
            for issue in issues:
                key = f"🏭 {issue.get('workplace', 'Unknown')}"
                if key not in groups: groups[key] = []
                groups[key].append(issue)
                
        elif "원인별" in mode:
            for issue in issues:
                key = f"🔗 {issue.get('event_id', 'Unknown Event')}"
                if key not in groups: groups[key] = []
                groups[key].append(issue)

        # 2. Render Expanders
        for title, group_issues in groups.items():
            if not group_issues:
                continue # Skip empty groups
                
            # Calculate Summary
            count = len(group_issues)
            total_diff = sum([i.get('diff', 0) or 0 for i in group_issues])
            diff_str = f" / 합계 {total_diff:+,}원" if total_diff != 0 else ""
            
            # Sort by Impact (Diff absolute value)
            group_issues.sort(key=lambda x: abs(x.get('diff', 0) or 0), reverse=True)
            
            with st.expander(f"{title} ({count}건{diff_str})", expanded=False):
                # Add Description based on title (Only for Issue Type mode)
                if "이슈별" in mode:
                    if "근태 소명" in title:
                        st.caption(f"마감을 막고 있는 병목이 **{count}건** 있습니다.")
                    elif "급여 변동" in title:
                        st.caption("인사 발령과 연결된 급여 변동을 계산했습니다.")
                    elif "의료비" in title:
                        st.caption("제출된 영수증의 규정 위반 여부를 확인했습니다.")

                # Select All Toggle
                select_all_key = f"select_all_{title}_{tab_key}"
                select_all = st.checkbox("전체 선택", key=select_all_key)

                # 3. Prepare Data for Table
                df_data = []
                for i, issue in enumerate(group_issues):
                    df_data.append({
                        "선택": select_all, # Default to Select All state
                        "ID": issue['issue_id'],
                        "이름": issue['name'],
                        "부서": issue.get('department', '-'), # Show Dept
                        "결재권자": issue.get('manager_id', '-'), # Added Manager Column
                        "내용": issue.get('description') or issue.get('reason') or issue.get('title'),
                        "차액": f"{issue.get('diff', 0):+,}원" if issue.get('diff') else "-",
                        "제안": "독촉" if issue['type'] == 'Chaser' else ("반영" if issue['type'] == 'Auditor' else "승인"),
                        "_obj": issue # Hidden object for reference
                    })
                
                df = pd.DataFrame(df_data)
                
                # 4. Table View with Selection
                edited_df = st.data_editor(
                    df,
                    column_config={
                        "선택": st.column_config.CheckboxColumn("선택", default=False),
                        "_obj": None # Hide object column
                    },
                    disabled=["ID", "이름", "부서", "결재권자", "내용", "차액", "제안"],
                    hide_index=True,
                    key=f"editor_{title}_{tab_key}",
                    use_container_width=True
                )
                
                # 5. Bulk Action Button
                selected_indices = edited_df.index[edited_df["선택"]].tolist()
                selected_issues = [group_issues[i] for i in selected_indices]
                
                if selected_issues:
                    # Determine action label based on mixed types if necessary, or just generic
                    # If grouped by Person/Dept, types might be mixed.
                    # For simplicity, we can check if all are same type, or provide generic "Process Selected"
                    
                    types = set([i['type'] for i in selected_issues])
                    if len(types) == 1:
                        # Single type logic (same as before)
                        t = list(types)[0]
                        if t == 'Chaser':
                            if st.button(f"선택 항목 {len(selected_issues)}건 독촉 발송", key=f"bulk_btn_{title}_{tab_key}"):
                                for issue in selected_issues: handle_approve(issue, rerun=False)
                                time.sleep(0.1); st.rerun()
                        elif t == 'Auditor':
                            if st.button(f"선택 항목 {len(selected_issues)}건 급여 반영", key=f"bulk_btn_{title}_{tab_key}", type="primary"):
                                for issue in selected_issues: handle_apply(issue, rerun=False)
                                time.sleep(0.1); st.rerun()
                        elif t == 'Welfare':
                            if st.button(f"선택 항목 {len(selected_issues)}건 승인 및 이관", key=f"bulk_btn_{title}_{tab_key}", type="primary"):
                                for issue in selected_issues: handle_welfare_approve(issue, rerun=False)
                                time.sleep(0.1); st.rerun()
                    else:
                        # Mixed types (e.g. Person View)
                        if st.button(f"선택 항목 {len(selected_issues)}건 일괄 처리", key=f"bulk_btn_{title}_{tab_key}", type="primary"):
                            for issue in selected_issues:
                                if issue['type'] == 'Chaser': handle_approve(issue, rerun=False)
                                elif issue['type'] == 'Auditor': handle_apply(issue, rerun=False)
                                elif issue['type'] == 'Welfare': handle_welfare_approve(issue, rerun=False)
                            time.sleep(0.1); st.rerun()

                # 6. Detailed View (All Items)
                st.markdown("---")
                st.caption(f"👇 {title} 관련 상세 내역 ({len(group_issues)}건)")
                
                for target_issue in group_issues:
                    # Wrapper for visual separation
                    st.markdown(f"##### 🔹 {target_issue['name']} ({target_issue['issue_id']})")
                    
                    # --- Chain View Visualization ---
                    if target_issue.get('event_id'):
                        st.info(f"🔗 **Causality Chain**: [{target_issue['event_id']}] ──▶ [규정/정책] ──▶ [{target_issue['title']}]")
                    
                    # Render Card
                    unique_key = f"{tab_key}_{target_issue['issue_id']}"
                    if target_issue['type'] == 'Chaser':
                        cards.render_chaser_card(target_issue, handle_approve, handle_ignore, key_suffix=unique_key)
                    elif target_issue['type'] == 'Auditor':
                        cards.render_auditor_card(target_issue, handle_apply, handle_ignore, set_active_issue, key_suffix=unique_key)
                    elif target_issue['type'] == 'Welfare':
                        cards.render_welfare_card(target_issue, handle_welfare_approve, handle_welfare_reject, key_suffix=unique_key)
                    
                    st.markdown("<br>", unsafe_allow_html=True) # Spacer

    with tab1:
        render_grouped_issues(st.session_state['issues'], "tab1", view_mode)
                
    with tab2:
        # Tabs 2,3,4 are specific types, so Pivot might not apply fully or we just force Issue Type?
        # Let's keep them simple or apply pivot if it makes sense. 
        # For now, let's just use default grouping for specific tabs to avoid confusion, 
        # OR hide them if Pivot is active. 
        # User request implies Pivot is the main way. Let's just render default for specific tabs.
        render_grouped_issues([i for i in st.session_state['issues'] if i['type'] == 'Chaser'], "tab2")
            
    with tab3:
        render_grouped_issues([i for i in st.session_state['issues'] if i['type'] == 'Auditor'], "tab3")
            
    with tab4:
        render_grouped_issues([i for i in st.session_state['issues'] if i['type'] == 'Welfare'], "tab4")
            
    with tab5:
        if not st.session_state['completed_issues']:
            st.info("완료된 내역이 없습니다.")
        else:
            # Completed items can remain as a simple list or also be grouped. 
            # For now, keeping it simple list for history.
            for issue in st.session_state['completed_issues']:
                if issue['type'] == 'Chaser':
                    cards.render_chaser_card(issue, None, None, key_suffix="done", read_only=True)
                elif issue['type'] == 'Auditor':
                    cards.render_auditor_card(issue, None, None, set_active_issue, key_suffix="done", read_only=True)
                elif issue['type'] == 'Welfare':
                    cards.render_welfare_card(issue, None, None, key_suffix="done", read_only=True)
