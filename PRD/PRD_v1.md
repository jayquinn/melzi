
# [PRD] Project Melzi: DaVinci Payroll Shadow Operator

| 문서 버전 | **v1.0** | 작성일 | 2025. 12. 02 |
| :--- | :--- | :--- | :--- |
| **Target** | 각사 및 SSC 급여담당자 | **Platform** | **Streamlit Web Dashboard** |

## 1. Product Identity
**"급여 담당자의 업무를 '수작업 취합·계산'에서 'Agent 제안 승인'으로 전환하고, 월말 마감 병목을 '일일 상시 모니터링' 체계로 분산시키는 급여 전용 쉐도우 오퍼레이터."**

---

## 2. Background & Strategy
*   **Context:** 급여 업무는 정형적·반복적이나 계열사별 중복 수행으로 비효율적임. 담당자는 4가지 과업(입력, 행정, 검증, 해석)에 시달림.
*   **Strategy:**
    *   **일 1 (입력):** PI(프로세스 혁신)로 해결 (Agent Scope 제외).
    *   **일 4 (해석):** 금번 Scope 제외.
    *   **일 2 (행정) & 일 3 (검증):** **Agent가 주도하고 사람이 승인하는 'Shadow Operator' 체제로 전환.**
*   **Core Premises:**
    1.  **Always-On:** 백그라운드 상시 구동.
    2.  **Trust-But-Verify:** 독립 로직으로 사후 검증.
    3.  **Proof-Based:** 산출 근거(Logic) 제시.
    4.  **Action-Oriented:** 리포팅을 넘어 실행(반영/발송)까지 연결.
    5.  **Timeline-Aware:** 기간과 이력을 해석하여 계산.

---

## 3. Objectives (To-Be Image)

| 구분 | As-Is | To-Be (Melzi) | 변화의 핵심 |
| :--- | :--- | :--- | :--- |
| **일 2**<br>(행정) | 담당자가 미마감자 색출 후 개별 연락 | Agent가 병목 지점 자동 탐지 후 **독촉 알림 카드 생성** → 담당자 승인 | **Chasing**<br>↓<br>**Monitoring** |
| **일 3**<br>(검증) | 30가지 예외 사항 수기 선별 및 엑셀 계산 | Agent가 교란 요인 선제적 계산 후 **승인 대기 안건 상정** → 담당자 클릭 | **Calculation**<br>↓<br>**Approval** |
| **UX** | 엑셀과 ERP 화면을 오가며 작업 | **Inbox 형태의 대시보드**에서 처리하고, 의문점은 **사이드바 챗봇**으로 해소 | **Excel**<br>↓<br>**Chat & Click** |

---

## 4. Core Features & Logic Specs

### Feature 1. [일 2] 근태 모니터링 및 독촉 (The Chaser)
*   **목표:** 급여 계산에 악영향을 주는 근태 결함을 비용(Cost) 관점에서 사전 제거.
*   **트리거:** `TNA_RECORD` 테이블 실시간 스캔.
*   **Logic (Python):**
    *   `Condition 1`: 근태일자 < Today AND 결재상태 != '승인완료'
    *   `Condition 2`: 주간 근로시간 > 52시간 (법적 리스크)
*   **Agent Action:**
    *   대시보드에 **[독촉 알림 카드]** 생성 (대상자, 미마감 건수, 사유).
    *   **`[발송 승인]`** 클릭 시 → "메신저 발송 완료" Toast 메시지 출력 & 카드 삭제.

### Feature 2. [일 3] 급여 교란 요인 해결 (The Auditor)
*   **목표:** 30가지 교란 요인을 '그림자 계산'하여 차액을 보정.
*   **관리 대상 (30 Disturbances):**
    > 소급, 일할(휴복직/입퇴사), 수당변동(가족/직책/자격), 감급, 회입 등.
*   **Logic (Python):**
    *   **Timeline Slicer:** `HR_EVENT_LOG`를 조회하여 `발령일`과 `효력일` 사이의 구간(Duration)을 계산.
    *   **Shadow Calc:** `(변경된 기본급 - 기지급액) * 구간` 공식 적용.
*   **Agent Action:**
    *   대시보드에 **[급여 보정 제안 카드]** 생성.
        *   **Timeline View:** 기간 분할 시각화 (1~10일 정상 / 11~31일 휴직).
        *   **Formula:** 계산 수식 텍스트 표시.
        *   **Diff:** `Melzi값` vs `Davinci값` 비교.
    *   **`[다빈치 적용]`** 클릭 시 → DB 업데이트 시뮬레이션 & 카드 삭제(처리완료 이동).

### Feature 3. [Support] Melzi Talk (Context-Aware Chatbot)
*   **목표:** 승인 전 담당자의 의구심 해소 (규정/근거/데이터 조회).
*   **Logic:**
    *   **Context Injection:** 사용자가 현재 보고 있는 이슈 카드(Feature 2)의 데이터(사번, 발령내용)를 프롬프트에 자동 주입.
*   **Interaction:**
    *   User: "이거 계산 근거가 뭐야?"
    *   Bot: "(김철수 소급 데이터를 참조하여) 10월 1일자 승진 발령이 11월에 입력되어, 1개월치 차액이 발생했습니다. 규정 제5조에 따릅니다."

---

## 5. Assumptions & Data Structure (목업 구현용)

### 5.1 시스템 환경 가정 (System Landscape)
1.  **HRIS (Davinci):** Master DB. 외부 직접 쓰기(Write) 불가.
2.  **ERP (SAP):** 재무 System.
3.  **Agent (Melzi):**
    *   **권한:** Davinci에 대해 Read-Only 권한을 가지나, **목업에서는 `[적용]` 버튼 클릭 시 API를 통해 데이터를 입력한다고 가정(Simulation).**
    *   **DB:** 별도의 Shadow DB에 시뮬레이션 결과 저장.

### 5.2 데이터 구조 (Mockup Schema)

**A. [Source] Davinci (가상 엑셀 데이터)**
*   `HR_MASTER`: 사번, 성명, 직급, 기본급, 가족수.
*   `HR_EVENT_LOG`: 사번, 발령일(Event), 효력일(Effective), 발령구분.
    *   *Key Logic: 발령일 > 효력일 = 소급.*
*   `TNA_RECORD`: 사번, 일자, 결재상태.

**B. [Processing] Melzi (Shadow DB)**
*   `SHADOW_LEDGER`:
    *   `Issue_ID`, `사번`, `이슈유형`, `Melzi_Calc`, `Davinci_Calc`, `Diff`, `Logic(텍스트)`, `Status(Pending/Done)`.
    *   **목적:** 대시보드는 이 테이블의 `Status='Pending'`인 건만 조회하여 보여줌.

### 5.3 시나리오 (11월 급여 D-3 상황)
1.  **[소급] 김철수:** 10/1 승진, 11/15 입력됨. (+450,000원 제안)
2.  **[일할] 이영희:** 11/10 육아휴직 시작. (-1,200,000원 감액 제안)
3.  **[근태] 박민수:** 근태 미마감. (독촉 알림 제안)
4.  **[수당] 최사원:** 자녀 출산 후 가족수당 미반영. (+100,000원 제안)

### 5.4 UI/UX 정의
*   **Main Dashboard:** **Inbox 스타일**. 카드 리스트 + 우측 **[승인]** 버튼.
*   **Sidebar:** 챗봇 + 시스템 상태(동기화 됨).
*   **Feedback:** 승인 버튼 클릭 시 카드가 사라지고 상단에 "처리 완료" 메시지 표시.