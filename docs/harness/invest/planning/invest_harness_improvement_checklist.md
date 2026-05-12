# Invest Harness 개선 체크리스트

> **최종 Goal:** invest_harness를 "단일 종목 리포트 생성기"에서 "아이디어 발굴 → Rating/Price Target 산출 → 실적 업데이트 → 밸류에이션 검증 → QA → HTML 출력까지 가능한 **개인용 투자 리서치 프레임워크**"로 확장한다.

---

## MVP 진행 상태 (2026-05-13)

- ✅ 완료 기준: source layer 계약, generated layer sync, workspace safety, MVP command/skill contract, Rating/Price Target 리포트 구조, screen/comps/dcf/earnings/qa 산출물 계약.
- 🔲 후속 기준: 실제 `/screen`, `/earnings`, `/dcf`, `/comps`, `/qa` CLI/runtime 파서와 실행 엔진은 별도 goal로 남긴다.

### 후속 Runtime-Code Goal

- [ ] Command 입력을 실제 CLI/runtime에서 파싱하고 각 thin command stub으로 dispatch하는 실행 엔진 구현
- [ ] `/screen`, `/earnings`, `/comps`, `/dcf`, `/qa`에 대한 end-to-end command smoke test 추가
- [ ] command runtime이 `${ACTIVE_WORKSPACE}`를 생성/전달하고 source skill 계약의 산출물 경로를 보존하는지 검증

---

## 0. 최종 방향

| 구분 | 설명 |
|------|------|
| **현재** | 한 종목을 깊게 분석하는 Markdown 리포트 생성 하네스 |
| **개선 후** | 아이디어 발굴 → 종목 선정 → 심층 리포트 → 밸류에이션 검증 → 실적 업데이트 → QA → HTML/MD 출력까지 가능한 투자 리서치 운영체제 |

---

## 1. Skill 구조 개선

### Goal 1. 스킬을 원본 계층과 실행 계층으로 분리

- [x] 원본 계층 디렉토리 생성: `plugins/vertical-plugins/invest-research/skills/`
- [x] 실행 계층 디렉토리 생성: `plugins/agent-plugins/invest-harness/skills/`
- [x] 실행 계층 디렉토리 생성: `.agents/skills/`
- [x] 기존 Skill을 원본 계층으로 이동/복사
- [x] 실행용 Skill은 자동 생성 방식으로 전환
- [x] 복수 실행 환경(Claude, Codex, OpenClaw, Gemini 등) 대응 확인

### Goal 2. 공통 정책 계층 추가

- [x] 정책 디렉토리 생성: `plugins/vertical-plugins/invest-research/policies/`
- [x] `workspace-safety.md` 작성
- [x] `market-price-anchor.md` 작성
- [x] `data-source-policy.md` 작성
- [x] `qa-recalculation-policy.md` 작성
- [x] `rating-price-target-policy.md` 작성
- [ ] ~~`investment-advice-boundary.md`~~ → **만들지 않음** (확정)

### Goal 3. Skill Sync 시스템 추가

- [x] `scripts/Sync-InvestSkills.ps1` 작성 (원본 + 정책 → 실행용 Skill 자동 생성)
- [x] `scripts/Test-SkillDrift.ps1` 작성 (원본 ↔ 실행용 불일치 감지)
- [x] Skill drift 감지 시 경고/실패 처리 로직 구현
- [x] 실행용 Skill 직접 수정 방지 가이드 문서화

---

## 2. Workspace 안전성 개선

### Goal 4. plain legacy workspace 직접 저장 금지

- [x] 기존 Skill/문서에서 legacy workspace 직접 경로 사용 부분 전수 조사
- [x] 모든 경로를 동적 Workspace 패턴으로 변경
- [x] 금지 규칙 문서화
  - ❌ `/03_valuation/findings.md` 또는 동적 workspace 없이 쓰는 고정 경로
  - ✅ `_workspace_AAPL_20260512/03_valuation/findings.md`

### Goal 5. 동적 Workspace 도입

- [x] 동적 Workspace 네이밍 규칙 확정: `_workspace_{TICKER_OR_SLUG}_{YYYYMMDD}/`
- [x] 한국 종목 지원: `_workspace_005930KS_20260512/`
- [x] 미국 종목 지원: `_workspace_AAPL_20260512/`
- [x] 동일 폴더 존재 시 시각 접미사 로직 구현: `_workspace_AAPL_20260512_143022/`
- [x] `${ACTIVE_WORKSPACE}` 변수 바인딩 메커니즘 구현

### Goal 6. Workspace Safety 검증 스크립트 추가

- [x] `scripts/Test-WorkspaceSafety.ps1` 작성
- [x] 검사: 문서/Skill에 legacy workspace 직접 경로 잔존 여부
- [x] 검사: `${ACTIVE_WORKSPACE}` 사용 여부
- [x] 검사: plain legacy workspace 저장 지시 → 실패 처리
- [x] 기존 구조 검증 스크립트를 동적 Workspace 기준으로 수정

---

## 3. 기준 주가 및 시장지표 개선

### Goal 7. Market Price Snapshot 추가

- [x] `market-price-snapshot.md` 템플릿 작성
- [x] 저장 위치: `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md`
- [x] PER, PBR, 시가총액, EV, EV/EBITDA, DCF 괴리율 계산용 기준 주가 단일화

### Goal 8. 시장지표는 실제 시장 종가 기준으로 계산

- [x] 강제 규칙 문서화: DART 과거 보고서 기준가 ❌ → 실제 시장 종가 ✅
- [x] 한국 시장: KRX 최근 거래일 종가 (1순위) / yfinance (보조)
- [x] 미국 시장: yfinance 최근 거래일 종가 (1순위) / 거래소·IR (보조)
- [x] 글로벌 시장: yfinance 최근 거래일 종가 (1순위) / 거래소·IR (보조)
- [x] 기준 주가 조회 실패 시 fallback 로직 정의

### Goal 9. QA에서 시장지표 직접 재계산

- [x] 재계산 로직 구현: `시가총액 = 기준 주가 × 상장주식수`
- [x] 재계산 로직 구현: `PER = 기준 주가 ÷ EPS`
- [x] 재계산 로직 구현: `PBR = 기준 주가 ÷ BPS`
- [x] 재계산 로직 구현: `EV = 시가총액 + 순부채`
- [x] 재계산 로직 구현: `EV/EBITDA = EV ÷ EBITDA`
- [x] 재계산 로직 구현: `FCF Yield = FCF ÷ 시가총액`
- [x] 재계산 로직 구현: `DCF 괴리율 = DCF 주당가치 ÷ 기준 주가 - 1`
- [x] 재계산 결과와 리포트 값 불일치 시 경고/실패 처리

---

## 4. Rating / Price Target 정책

### Goal 10. Rating과 Price Target 허용

- [x] 기존 "투자 자문 표현 방지" 정책 폐기
- [x] 허용 표현 목록 확정 및 문서화:
  - [x] Buy / Outperform / Neutral / Hold / Underperform / Sell
  - [x] Price Target / Target Price
  - [x] Implied Upside / Implied Downside
  - [x] Bear / Base / Bull
  - [x] Risk-Reward

### Goal 11. `rating-price-target-policy.md` 추가

- [x] 파일 생성: `plugins/vertical-plugins/invest-research/policies/rating-price-target-policy.md`
- [x] Rating 체계 정의
- [x] Price Target 산출 원칙 정의
- [x] 기준 주가 사용 규칙 정의
- [x] Upside/Downside 계산 방식 정의
- [x] Bear/Base/Bull 시나리오와 Rating 정합성 규칙 정의
- [x] QA 검증 항목 정의

### Goal 12. 최종 리포트 구조 변경

- [x] 기존 섹션 15 변경: ~~종합 점수 및 최종 의견~~ → **Rating, Price Target 및 투자 의견**
- [x] 기존 섹션 16 변경: ~~투자 기간별 전략~~ → **투자 기간별 전략과 Risk-Reward**
- [x] 리포트 템플릿 업데이트
- [x] 관련 Skill의 리포트 구조 참조 업데이트

---

## 5. Command UX 개선

### Goal 13. `/command` 기반 UX 도입

- [x] Command 실행 프레임워크 설계
- [x] Command 디렉토리 구조 생성:
  - [x] `plugins/vertical-plugins/invest-research/commands/`
  - [x] `plugins/agent-plugins/invest-harness/commands/`
  - [x] `.agents/commands/`

### Goal 14. Command는 얇게, 실제 분석은 Skill이 수행

- [x] Command → Skill 매핑 구조 설계
  - Command = 버튼 (진입점)
  - Skill = 실제 업무 매뉴얼
  - Workspace = 결과 저장소
- [x] `/screen` → `idea-screener` 매핑
- [x] `/dcf` → `valuation-analyst` 매핑
- [x] `/earnings` → `earnings update workflow` 매핑
- [x] 기타 Command → Skill 매핑 정의

### Goal 15. 우선 구현 Command (MVP)

**1차 (MVP):**

- [x] `/analyze` 구현
- [x] `/screen` 구현
- [x] `/comps` 구현
- [x] `/dcf` 구현
- [x] `/earnings` 구현
- [x] `/qa` 구현

**2차 (확장):**

- [ ] `/preview` 구현
- [ ] `/sector` 구현
- [ ] `/thesis` 구현
- [ ] `/catalysts` 구현
- [ ] `/report-html` 구현
- [ ] `/morning-note` 구현
- [ ] `/update` 구현

---

## 6. 종목 발굴 기능 추가

### Goal 16. `idea-screener` Skill 추가

- [x] 원본 Skill 생성: `plugins/vertical-plugins/invest-research/skills/idea-screener/SKILL.md`
- [x] 실행 Skill 생성: `.agents/skills/idea-screener/SKILL.md`
- [x] 종목 미정 상태에서의 분석 시작 워크플로우 설계

### Goal 17. `/screen` 명령어 추가

- [ ] `/screen` 명령어 파서 구현 → 후속 runtime-code goal로 분리
- [ ] 입력 예시 지원 확인:
  - [x] `/screen AI 전력 인프라 2차 수혜주`
  - [x] `/screen 저평가 고ROIC 미국 중형주`
  - [x] `/screen 한국 화장품 ODM 수혜주`
- [ ] 출력 항목 구현:
  - [x] 후보군
  - [x] 점수표
  - [x] 투자 논지
  - [x] 예비 Rating
  - [x] 주요 리스크
  - [x] 다음 단계

### Goal 18. `00_screen` Workspace 추가

- [x] `${ACTIVE_WORKSPACE}/00_screen/` 디렉토리 구조 정의
- [x] `screen-criteria.md` 템플릿 작성
- [x] `candidate-universe.md` 템플릿 작성
- [x] `idea-scorecard.md` 템플릿 작성
- [x] `shortlist.md` 템플릿 작성

---

## 7. 밸류에이션 강화

### Goal 19. `/comps` 추가

- [x] `/comps` 명령어 구현
- [x] 필수 비교 항목 구현:
  - [x] PER
  - [x] Forward PER
  - [x] PBR
  - [x] PSR
  - [x] EV/EBITDA
  - [x] EV/Sales
  - [x] FCF Yield
  - [x] 매출 성장률
  - [x] 영업이익률
- [x] 피어 그룹 자동/수동 선정 로직

### Goal 20. `/dcf` 추가

- [x] `/dcf` 명령어 구현
- [x] Comps 선행 확인 로직 구현
- [x] DCF 워크플로우:
  - [x] `/comps` 결과 반영
  - [x] DCF 가정 설정
  - [x] DCF 결과 산출
  - [x] 피어 멀티플과 교차검증
  - [x] 역사적 PER 밴드와 교차검증

### Goal 21. DCF · Comps · 역사적 밴드 교차검증

- [x] 교차검증 항목 구현:
  - [x] DCF implied EV/EBITDA
  - [x] 피어 EV/EBITDA
  - [x] 역사적 PER 밴드
  - [x] 현재 Forward PER
  - [x] FCF Yield
- [x] 단순 "DCF상 저평가" 결론 방지 규칙 적용

---

## 8. 실적 업데이트 기능

### Goal 22. `/earnings` 추가

- [x] `/earnings` 명령어 구현
- [x] 입력 형식 지원:
  - [x] `/earnings 케이엔제이 latest`
  - [x] `/earnings TSLA Q1 2026`
  - [x] `/earnings 005930.KS latest`
- [x] 기능 구현:
  - [x] 최신 실적 발표일 확인
  - [x] 공식 공시 우선 확인
  - [x] 매출, 영업이익, EPS, 마진 변화 확인
  - [x] 컨센서스 대비 Beat/Miss 확인
  - [x] 가이던스 상향/유지/하향 확인
  - [x] Rating / Price Target 변화 판단

### Goal 23. `/preview` 추가

- [ ] `/preview` 명령어 구현
- [ ] 입력 형식 지원: `/preview NVDA`, `/preview 삼성전자`
- [ ] 출력 항목 구현:
  - [ ] 이번 실적에서 봐야 할 핵심 지표
  - [ ] 시장 기대치
  - [ ] Beat 시나리오
  - [ ] Miss 시나리오
  - [ ] 발표 후 업데이트할 항목

---

## 9. 투자 논지 · 촉매 · 섹터 추적

### Goal 24. `/thesis` 추가

- [ ] `/thesis` 명령어 구현
- [ ] 입력 형식 지원: `/thesis CSTM`, `/thesis 파마리서치`
- [ ] 출력 항목 구현:
  - [ ] 기존 투자 논지
  - [ ] 새로운 데이터
  - [ ] 논지를 강화하는 증거
  - [ ] 논지를 약화하는 증거
  - [ ] Rating 변화 가능성
  - [ ] 다음 추적 지표

### Goal 25. `/catalysts` 추가

- [ ] `/catalysts` 명령어 구현
- [ ] 입력 형식 지원:
  - [ ] `/catalysts AI 전력 인프라 next 3 months`
  - [ ] `/catalysts 파마리서치 2026Q2`
- [ ] 촉매 이벤트 캘린더 출력

### Goal 26. `/sector` 추가

- [ ] `/sector` 명령어 구현
- [ ] 입력 형식 지원:
  - [ ] `/sector 한국 화장품 ODM`
  - [ ] `/sector AI 전력 인프라`
  - [ ] `/sector 폐기물 관리 산업`
- [ ] 섹터/산업 리포트 생성

### Goal 27. Watchlist / Morning Note 검토

- [ ] `/morning-note` 명령어 설계 (향후 확장)
- [ ] 입력 형식 검토:
  - [ ] `/morning-note`
  - [ ] `/morning-note AI 반도체`
  - [ ] `/morning-note 내 관심종목`
- [ ] 관심종목 기반 일일 점검 워크플로우 설계

---

## 10. 데이터 연결 개선

### Goal 28. 데이터 소스 정책 분리

- [ ] `plugins/vertical-plugins/invest-research/policies/data-source-policy.md` 작성
- [ ] `docs/harness/invest/data-source-policy.md` 작성 (또는 동기화)
- [ ] 시장별 기본 원칙 문서화:
  - [ ] 한국: DART / KRX 우선
  - [ ] 미국: SEC EDGAR / yfinance 우선
  - [ ] 글로벌: yfinance / 공식 IR / 거래소 우선

### Goal 29. 개인 접근 가능한 무료 · 저가 데이터 우선

- [ ] 기본 데이터 레이어 목록 확정 및 연결 확인:
  - [ ] korea-stock
  - [ ] yfinance
  - [ ] SEC EDGAR
  - [ ] FRED
  - [ ] Alpha Vantage
  - [ ] Financial Modeling Prep
  - [ ] 공식 IR
  - [ ] 웹 검색
- [ ] 각 데이터 소스별 접근 방법 · API 키 관리 가이드

### Goal 30. 기관용 MCP는 Optional Layer로 분리

- [ ] `.mcp.institutional.json` 구조 설계
- [ ] Optional 대상 목록:
  - [ ] Daloopa
  - [ ] Morningstar
  - [ ] S&P Global
  - [ ] FactSet
  - [ ] Moody's
  - [ ] MT Newswires
  - [ ] Aiera
  - [ ] LSEG
  - [ ] PitchBook
  - [ ] Chronograph
  - [ ] Egnyte
- [ ] **핵심 원칙 검증:** 기관 MCP 없이도 기본 분석이 실패하지 않는지 확인
- [ ] 기관 MCP 존재 시 보조 데이터로 활용하는 로직

---

## 11. QA 강화

### Goal 31. `/qa` 명령어 추가

- [x] `/qa` 명령어 구현
- [x] 입력 형식 지원:
  - [x] `/qa report.md`
  - [x] `/qa AAPL latest`

### Goal 32. QA 기준 변경

- [x] 기존 방향 폐기: ~~투자 자문처럼 보이는 표현 방지~~
- [x] 새 방향 적용: **Rating과 Price Target의 근거 검증**
- [x] QA 검사 항목 구현:
  - [x] Rating이 근거와 일치하는가?
  - [x] Price Target 산출 방식이 명시되어 있는가?
  - [x] 기준 주가가 `market-price-snapshot.md`와 일치하는가?
  - [x] Upside/Downside 계산이 맞는가?
  - [x] Bear/Base/Bull 시나리오와 Rating이 모순되지 않는가?
  - [x] PER/PBR/시총/DCF 계산이 직접 재계산 가능한가?

### Goal 33. QA 산출물 확장

- [x] `${ACTIVE_WORKSPACE}/09_qa/review.md` 템플릿 작성
- [x] `${ACTIVE_WORKSPACE}/09_qa/fix-list.md` 템플릿 작성
- [x] `${ACTIVE_WORKSPACE}/09_qa/final-check.md` 템플릿 작성

---

## 12. 출력 형식 개선

### Goal 34. HTML 리포트 추가

- [ ] `/report-html` 명령어 구현
- [ ] 입력 형식 지원:
  - [ ] `/report-html 파마리서치`
  - [ ] `/report-html AAPL`

### Goal 35. `html-report-synthesizer` 추가

- [ ] 원본 Skill 생성: `plugins/vertical-plugins/invest-research/skills/html-report-synthesizer/SKILL.md`
- [ ] 실행 Skill 생성: `.agents/skills/html-report-synthesizer/SKILL.md`
- [ ] HTML 포함 요소 구현:
  - [ ] 핵심 요약 카드
  - [ ] Rating / Price Target
  - [ ] 기준 주가
  - [ ] Upside / Downside
  - [ ] 재무 추이 차트
  - [ ] 피어 비교 테이블
  - [ ] DCF / 역사적 밴드
  - [ ] Bear/Base/Bull 시나리오
  - [ ] 리스크 매트릭스
  - [ ] QA 상태
  - [ ] 출처 목록

---

## 13. 구조 검증 및 자동화

### Goal 36. 구조 검증 스크립트 업데이트

- [ ] `scripts/Test-HarnessStructure.ps1` 수정
- [ ] 기존 legacy workspace 고정 경로 → 동적 Workspace 기준으로 변경
- [ ] 새로운 디렉토리 구조 반영

### Goal 37. 신규 검증 스크립트 추가

- [ ] `scripts/Test-WorkspaceSafety.ps1` 작성 완료 확인
- [ ] `scripts/Test-SkillDrift.ps1` 작성 완료 확인
- [ ] `scripts/Sync-InvestSkills.ps1` 작성 완료 확인
- [ ] 모든 검증 스크립트 통합 실행 및 CI 연동 검토

---

## 14. 최종 권장 폴더 구조

- [ ] 아래 구조 반영 완료 확인:

```
invest_harness/
  plugins/
    vertical-plugins/
      invest-research/
        skills/
        commands/
        policies/
        templates/
    agent-plugins/
      invest-harness/
        skills/
        commands/
        policies/
        AGENTS.md
  .agents/
    skills/
    commands/
  docs/
    harness/
      invest/
        runbook.md
        team-spec.md
        cross-tool-usage.md
        data-source-policy.md
        mcp-routing.md
  scripts/
    Sync-InvestSkills.ps1
    Test-SkillDrift.ps1
    Test-WorkspaceSafety.ps1
    Test-HarnessStructure.ps1
```

---

## 15. MVP 최종 목록

> [!IMPORTANT]
> 아래 14개 항목이 가장 먼저 만들어야 할 최소 기능입니다.

| # | 항목 | 상태 |
|---|------|------|
| 1 | `plugins/vertical-plugins/invest-research/` 구조 생성 | ✅ |
| 2 | 기존 Skill을 원본 계층으로 복사 | ✅ |
| 3-a | 공통 정책: `workspace-safety.md` | ✅ |
| 3-b | 공통 정책: `market-price-anchor.md` | ✅ |
| 3-c | 공통 정책: `data-source-policy.md` | ✅ |
| 3-d | 공통 정책: `qa-recalculation-policy.md` | ✅ |
| 3-e | 공통 정책: `rating-price-target-policy.md` | ✅ |
| 4 | `Sync-InvestSkills.ps1` 작성 | ✅ |
| 5 | `Test-SkillDrift.ps1` 작성 | ✅ |
| 6 | `Test-WorkspaceSafety.ps1` 작성 | ✅ |
| 7 | `market-price-snapshot.md` 템플릿 추가 | ✅ |
| 8 | `/analyze` 추가 | ✅ |
| 9 | `/screen` + `idea-screener` 추가 | ✅ |
| 10 | `/comps` 추가 | ✅ |
| 11 | `/dcf` 추가 | ✅ |
| 12 | `/earnings` 추가 | ✅ |
| 13 | `/qa` 추가 | ✅ |

---

> **범례:** ⬜ = 미착수 · 🔲 = 진행 중 · ✅ = 완료
