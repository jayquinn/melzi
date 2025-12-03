import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render_chaser_card(issue, on_approve, on_ignore=None, key_suffix="", read_only=False):
    """Renders a card for Attendance Issues (The Chaser)."""
    with st.container():
        st.markdown(f"""
        <div class="card chaser-card">
            <div class="card-header">
                <span class="badge chaser-badge">근태 소명 (Attendance Chasing)</span>
                <span class="card-title">{issue['name']}</span>
            </div>
            <div class="card-body">
                <div class="stat-row">
                    <div class="stat-item">
                        <span class="stat-label">이슈</span>
                        <span class="stat-value">{issue['title']}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">미마감 내역</span>
                        <span class="stat-value warning-text">{issue.get('description', '미마감')}</span>
                    </div>
                </div>
                <div style="margin-top: 15px; padding: 10px; background-color: #f8fafc; border-radius: 8px; border-left: 4px solid #3b82f6;">
                    <p style="margin: 0; font-size: 0.9rem; color: #4b5563;"><strong>🤖 Agent Action:</strong></p>
                    <p style="margin: 5px 0 0 0; font-size: 0.9rem;">해당 직원에게 근태 마감 요청 메시지를 발송하여 급여 계산 지연을 방지합니다.</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if not read_only:
            with st.expander("메시지 미리보기", expanded=True):
                st.info(f"👋 안녕하세요 {issue['name']}님, 11월 급여 마감을 위해 {issue['description']}에 대한 확인이 필요합니다. 금일 중으로 처리 부탁드립니다.")
            
            col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
            with col2:
                if on_ignore and st.button("무시하기", key=f"btn_ignore_chaser_{issue['issue_id']}_{key_suffix}"):
                    on_ignore(issue)
            with col3:
                if st.button("발송 승인", key=f"btn_approve_{issue['issue_id']}_{key_suffix}", type="primary"):
                    on_approve(issue)
        else:
            status_color = "#059669" if issue.get('status') == 'Approved' else "#6b7280"
            st.markdown(f"<div style='text-align: right; color: {status_color}; font-weight: bold;'>Status: {issue.get('status', 'Completed')}</div>", unsafe_allow_html=True)

def render_auditor_card(issue, on_apply, on_ignore, on_select, key_suffix="", read_only=False):
    """Renders a card for Payroll Issues (The Auditor)."""
    diff = issue['diff']
    diff_fmt = f"{diff:+,}"
    diff_class = "positive-diff" if diff > 0 else "negative-diff"
    
    with st.container():
        st.markdown(f"""
        <div class="card auditor-card">
            <div class="card-header">
                <span class="badge auditor-badge">급여 심사 (Payroll Auditing)</span>
                <span class="card-title">{issue['name']}</span>
            </div>
            <div class="card-body">
                <div class="stat-row">
                    <div class="stat-item">
                        <span class="stat-label">유형</span>
                        <span class="stat-value">{issue['title']}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">차액</span>
                        <span class="stat-value {diff_class}">{diff_fmt}원</span>
                    </div>
                </div>
                <div style="margin-top: 15px; padding: 10px; background-color: #f8fafc; border-radius: 8px; border-left: 4px solid #8b5cf6;">
                    <p style="margin: 0; font-size: 0.9rem; color: #4b5563;"><strong>🤖 Agent Action:</strong></p>
                    <p style="margin: 5px 0 0 0; font-size: 0.9rem;">{issue.get('reason', '변동 내역')}에 따른 급여 차액을 계산하고 다빈치 DB에 반영합니다.</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if not read_only:
            with st.expander("상세 분석 & 시뮬레이션", expanded=True):
                # When expanded, we consider this "Selected" for the chatbot context
                if on_select:
                    on_select(issue)
                
                st.markdown(f"**분석 로직:** {issue['logic_text']}")
                
                # Visualization & Calculation
                if issue['title'] == '소급':
                    # Calculation Detail
                    st.markdown("""
                    <div style="background-color: #f0fdf4; padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #bbf7d0; text-align: center;">
                        <strong style="font-size: 1.1rem; color: #166534;">🧮 산출 근거 (Calculation Detail)</strong><br>
                        <div style="margin-top: 10px; font-size: 1.3rem; font-weight: bold; color: #15803d;">
                            (5,450,000원 - 5,000,000원) × 1개월 = <span style="background-color: #dcfce7; padding: 2px 8px; border-radius: 4px;">+450,000원</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Waterfall Chart simulated with Bar Chart for full color control
                    fig = go.Figure(go.Bar(
                        x = ["기존 급여", "승진 인상분", "최종 급여"],
                        y = [5000000, 450000, 5450000],
                        base = [0, 5000000, 0], # Start positions for the bars
                        text = ["500만", "+45만", "545만"],
                        textposition = "outside",
                        marker_color = ["#9ca3af", "#10b981", "#3b82f6"], # Gray, Green, Blue
                        width = [0.5, 0.5, 0.5]
                    ))

                    fig.update_layout(
                        title = "<b>급여 변동 워터폴 분석</b>",
                        showlegend = False,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=350,
                        margin=dict(l=20, r=20, t=50, b=20),
                        yaxis=dict(range=[4000000, 6000000])
                    )
                    st.plotly_chart(fig, use_container_width=True, key=f"chart_retro_{issue['issue_id']}_{key_suffix}")
                    
                elif issue['title'] == '일할':
                    # Calculation Detail
                    st.markdown("""
                    <div style="background-color: #fff7ed; padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #fed7aa; text-align: center;">
                        <strong style="font-size: 1.1rem; color: #9a3412;">🧮 산출 근거 (Calculation Detail)</strong><br>
                        <div style="margin-top: 5px; font-size: 1.0rem; color: #4b5563;">적용 기간: <strong>11/01 ~ 11/09 (9일간)</strong></div>
                        <div style="margin-top: 10px; font-size: 1.3rem; font-weight: bold; color: #c2410c;">
                            (4,000,000원 ÷ 30일) × 9일 = <span style="background-color: #ffedd5; padding: 2px 8px; border-radius: 4px;">1,200,000원</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Gantt Chart for Proration
                    df_timeline = pd.DataFrame([
                        dict(Task="근무 (유급)", Start='2025-11-01', Finish='2025-11-09', Resource='Work'),
                        dict(Task="휴직 (무급)", Start='2025-11-10', Finish='2025-11-30', Resource='Leave')
                    ])
                    colors = {'Work': '#3b82f6', 'Leave': '#e5e7eb'}
                    fig = px.timeline(
                        df_timeline, x_start="Start", x_end="Finish", y="Task", color="Resource", 
                        title="<b>일할 계산 기간 시각화</b>", color_discrete_map=colors, height=200
                    )
                    fig.update_yaxes(autorange="reversed")
                    fig.update_layout(showlegend=True, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=250)
                    st.plotly_chart(fig, use_container_width=True, key=f"chart_proration_{issue['issue_id']}_{key_suffix}")
                
                col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
                with col2:
                    if on_ignore and st.button("무시하기", key=f"btn_ignore_auditor_{issue['issue_id']}_{key_suffix}"):
                        on_ignore(issue)
                with col3:
                    if st.button("다빈치 적용", key=f"btn_apply_{issue['issue_id']}_{key_suffix}", type="primary"):
                        on_apply(issue)
        else:
            status_color = "#059669" if issue.get('status') == 'Applied' else "#6b7280"
            st.markdown(f"<div style='text-align: right; color: {status_color}; font-weight: bold;'>Status: {issue.get('status', 'Completed')}</div>", unsafe_allow_html=True)

def render_welfare_card(issue, on_approve, on_reject, key_suffix="", read_only=False):
    """Renders a card for Welfare Auditing (Medical Expenses)."""
    amount_fmt = f"{issue['amount']:,}"
    verdict_color = "#dc2626" if issue['ai_verdict'] == 'Reject' else "#059669"
    verdict_bg = "#fef2f2" if issue['ai_verdict'] == 'Reject' else "#f0fdf4"
    verdict_text = "지급 반려 권고" if issue['ai_verdict'] == 'Reject' else "지급 승인 권고"
    
    # Determine rejection message content
    if issue['ai_verdict'] == 'Reject':
        reject_msg = f"{issue['name']}님, 청구하신 의료비는 <strong>'{issue['ai_reason']}'</strong> 사유로 반려되었습니다. (근거: {issue['policy_ref']})"
    else:
        # For cases recommended for approval, if the user decides to reject, show a generic message
        reject_msg = f"{issue['name']}님, 청구하신 의료비는 <strong>기타 사유</strong>로 반려되었습니다. HR팀에 문의해주세요."
    
    with st.container():
        st.markdown(f"""<div class="card welfare-card"><div class="card-header"><span class="badge" style="background-color: #fef3c7; color: #d97706;">복리후생 심사 (Welfare)</span><span class="card-title">{issue['name']}</span></div><div class="card-body"><div class="stat-row"><div class="stat-item"><span class="stat-label">청구 항목</span><span class="stat-value">{issue['title']}</span></div><div class="stat-item"><span class="stat-label">청구 금액</span><span class="stat-value">{amount_fmt}원</span></div></div><div style="margin-top: 15px; display: flex; gap: 10px;"><div style="flex: 1; padding: 10px; background-color: #f3f4f6; border-radius: 8px; font-size: 0.85rem;"><strong>🧾 OCR 영수증 분석</strong><br><pre style="white-space: pre-wrap; margin-top: 5px; color: #4b5563;">{issue['receipt_items']}</pre></div><div style="flex: 1; padding: 10px; background-color: {verdict_bg}; border-radius: 8px; border: 1px solid {verdict_color};"><strong style="color: {verdict_color};">🤖 AI 심사 결과: {verdict_text}</strong><br><ul style="margin-top: 5px; padding-left: 20px; font-size: 0.9rem; color: #374151;"><li><strong>사유:</strong> {issue['ai_reason']}</li><li><strong>근거:</strong> {issue['policy_ref']}</li></ul></div></div><div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #f0f2f6; display: flex; gap: 20px;"><div style="flex: 1;"><div style="font-size: 0.85rem; color: #6b7280; margin-bottom: 5px;">📋 필수 증빙 서류 (2/2)</div><div style="display: flex; gap: 10px;"><span style="font-size: 0.85rem; color: #059669; background-color: #ecfdf5; padding: 2px 8px; border-radius: 4px;">✅ 진료비 영수증</span><span style="font-size: 0.85rem; color: #059669; background-color: #ecfdf5; padding: 2px 8px; border-radius: 4px;">✅ 진료비 세부내역서</span></div></div><div style="flex: 1.5;"><div style="font-size: 0.85rem; color: #6b7280; margin-bottom: 5px;">📤 반려 시 발송 메시지 예시</div><div style="font-size: 0.85rem; color: #4b5563; background-color: #f9fafb; padding: 8px; border-radius: 6px; border: 1px dashed #d1d5db;">"{reject_msg}"</div></div></div></div></div>""", unsafe_allow_html=True)
        
        if not read_only:
            col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
            with col2:
                if st.button("반려 (Reject)", key=f"btn_reject_{issue['issue_id']}_{key_suffix}", type="secondary"):
                    on_reject(issue)
            with col3:
                if st.button("승인 (급여반영)", key=f"btn_approve_welfare_{issue['issue_id']}_{key_suffix}", type="primary"):
                    on_approve(issue)
        else:
            status_color = "#059669" if issue.get('status') == 'Approved' else ("#dc2626" if issue.get('status') == 'Rejected' else "#6b7280")
            st.markdown(f"<div style='text-align: right; color: {status_color}; font-weight: bold;'>Status: {issue.get('status', 'Completed')}</div>", unsafe_allow_html=True)
