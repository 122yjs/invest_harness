# BKNG Research Operational Reliability Plan

## 상태

- 기준 사례: BKNG 심층 리서치 실행
- 목적: 실전 실행에서 확인된 병목을 다음 전체 리포트 실행 전에 운영 계약으로 고정한다.
- 완료 조건: source availability, template fallback, staged delegation, synthesis input-size guardrail이 문서와 검증 스크립트에 반영된다.

## 발견된 문제

| 우선순위 | 문제 | 증상 | 영향 |
|---|---|---|---|
| P0 | yfinance runtime 미가용 | `mcporter list`에서 yfinance MCP가 확인되지 않음 | 미국 기업 분석에서 주력 MCP 경로가 끊기고 FMP, Alpha Vantage, Web Search + Fetch에 의존 |
| P0 | 템플릿 파일 읽기 실패 | `docs/harness/invest/templates/input-intake.md`, `request-summary.md` 읽기 중 `Resource deadlock avoided` | 입력 게이트와 요청 요약을 템플릿 기반으로 생성하지 못함 |
| P1 | `financial-analyst` 장시간 타임아웃 | 600초 제한에서 2회 실패 | 재무 findings를 오케스트레이터가 직접 보강해야 함 |
| P1 | `risk-scenario-analyst` 중단 | 선행 findings를 모두 읽는 과정에서 interrupted | 리스크/시나리오 findings를 오케스트레이터가 직접 작성 |
| P1 | `report-synthesizer` 타임아웃 | 6개 findings의 대용량 입력을 18개 섹션으로 합성하다 600초 초과 | 초안 통합을 오케스트레이터가 직접 수행 |
| P1 | 서브에이전트 파일 I/O 불안정 | `mkdir` 이후 `write_file` 실패 또는 짧은 byte error만 반환 | findings 저장 실패 시 fan-in 단계가 끊김 |
| P2 | source 간 수치 불일치 | FCF, EV/EBITDA, PER 등에서 FMP/Alpha Vantage/웹 출처 차이 | `conflicts.md`와 최종 한계 섹션 부담 증가 |
| P2 | 동시 child 제한 | `max_concurrent_children=3` 조건에서 6개 전문가를 2배치로 실행 | 전체 실행 시간이 늘고 risk/synthesis 대기 시간이 증가 |

## 운영 Guardrail

### 1. Runtime Source Availability Preflight

- `source-capability-registry.md`의 `connected`는 repo-evidence 상태일 뿐 live runtime proof가 아니다.
- 오케스트레이터는 analyst fan-out 전에 현재 세션의 callable source inventory를 확인하고 `${ACTIVE_WORKSPACE}/00_evidence/source-call-plan.md`에 `Runtime Availability`와 `Live Tool Probe`를 남긴다.
- yfinance가 live runtime에서 없으면 `yfinance`를 주력 경로로 강제하지 않는다. reported financial fact는 SEC EDGAR/company IR/DART-KRX/local regulator filing 같은 T0 official disclosure를 먼저 검토한다. FMP 또는 Alpha Vantage가 실제 callable이면 보조 structured source로 사용하고, Web Search + Fetch는 source discovery와 원문 retrieval 보조로 사용한다.
- MCP 미가용은 `${ACTIVE_WORKSPACE}/00_evidence/unresolved-data-gaps.md`에 기록한다.

### 2. Template Fallback

- 오케스트레이터는 실행 시작 시 필요한 템플릿을 읽어보고, 파일 시스템 오류가 나면 inline fallback template을 사용한다.
- fallback 사용 여부와 에러 원문은 `${ACTIVE_WORKSPACE}/00_evidence/api-call-log.md` 또는 `${ACTIVE_WORKSPACE}/00_evidence/unresolved-data-gaps.md`에 남긴다.
- fallback은 템플릿 형식을 축약할 수 있지만 필수 필드와 gate 판정은 유지해야 한다.

### 3. Workspace Pre-Creation

- analyst fan-out 전에 `00_input`, `00_evidence`, `01_financial`부터 `09_qa`까지 필수 출력 디렉터리를 오케스트레이터가 먼저 만든다.
- 서브에이전트에게는 `mkdir` 책임을 넘기지 않고 `${ACTIVE_WORKSPACE}/.../findings.md` 쓰기만 맡긴다.
- 파일 저장 실패 시 해당 역할의 상태를 누락으로 표시하고 한 번만 재시도한다.

### 4. Staged Delegation

- `max_concurrent_children`가 6보다 작으면 전문가 6개를 무조건 두 배치로만 나누지 않는다.
- `risk-scenario-analyst`는 `01`~`05` 산출물이 존재한 뒤 실행한다.
- `financial-analyst`는 공식 공시/IR/FMP/yfinance/Web Fetch 중 실제 callable source order를 먼저 확정하고, 웹 대형 페이지를 무제한으로 열지 않는다.
- `report-synthesizer`에는 원문 findings 전체가 아니라 각 findings의 compact handoff summary와 conflicts table을 우선 전달한다. 원문 전체는 수치 검산 때만 참조한다.

### 5. Data Conflict Handling

- FMP, Alpha Vantage, yfinance, company IR, SEC EDGAR, Web Fetch 사이의 차이는 평균 처리하지 않는다.
- 재무/밸류에이션 공통 입력은 가능하면 `${ACTIVE_WORKSPACE}/00_evidence/evidence-ledger.md`에 1차 캐시로 모으고, 각 전문가가 같은 evidence ID를 참조한다.
- BKNG처럼 특정 재무 항목을 별도 공시하지 않는 기업은 추정치를 `e` 또는 `추정`으로 표시하고 공식 미공시 사유를 남긴다.

## 후속 구현 항목

| 우선순위 | 항목 | 완료 기준 |
|---|---|---|
| P0 | yfinance 미가용 fallback 계약 | source-router와 orchestrator가 runtime availability를 기록 |
| P0 | 템플릿 fallback 계약 | 템플릿 read 실패 시 inline fallback과 data gap 기록 |
| P1 | staged delegation 계약 | risk는 선행 findings 이후, synthesis는 compact handoff summary 사용 |
| P1 | source cache 계약 | evidence-ledger가 공통 재무/밸류에이션 수치의 우선 참조점 역할 |
| P2 | timeout sizing guidance | 고위험 역할에 source scope 축소 또는 분할 실행 지시 |
