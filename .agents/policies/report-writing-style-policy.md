<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/policies/report-writing-style-policy.md; kind=policy; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun `python scripts/sync_invest_skills.py` (or `scripts/Sync-InvestSkills.ps1` / `scripts/Sync-InvestSkills.sh`).
> Common policies are synced from `plugins/vertical-plugins/invest-research/policies/`.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->

# Report Writing Style Policy
이 정책은 투자 리서치 Harness가 생성하는 보고서, HTML 화면 문구, QA 산출물, 실행 계획, 작업 기록, walkthrough 문서의 기본 작성 톤과 마크다운 문법을 정의한다.

## Language Policy
- 모든 응답과 산출물은 영어가 아닌 **한국어**로 작성한다.
- Implementation Plan, Task, Walkthrough, QA Review, Fix List, Final Check, HTML 화면 텍스트도 모두 한국어로 작성한다.
- 티커, 회계 약어, 재무 지표 약어, 원문 고유명사는 필요한 경우 영어를 유지할 수 있지만, 설명 문장은 한국어로 풀어쓴다.

## Markdown Syntax
- 글머리 기호는 단일 하이픈(`-`)과 공백만 사용한다.
- 헤더 뒤에는 빈 행을 두지 않고 바로 본문, 표, 목록, 콜아웃, 코드블록 중 하나를 배치한다.
- 2단을 넘는 목록 중첩은 피한다. 계층이 필요하면 번호가 포함된 소제목이나 표로 풀어쓴다.
- 핵심 키워드는 볼드체(`**text**`)로 강조하고, 파일명, 경로, 메뉴명, 짧은 영어 용어는 인라인 코드로 표기한다.
- 비교, 선택지, 수치 대조에는 표를 우선 사용한다.
- 구조가 복잡하거나 순서가 중요한 설명에는 Mermaid 다이어그램을 사용할 수 있다.

## File Organization Rule
- 투자 리포트 Harness에서는 기존 표준 경로인 `${ACTIVE_WORKSPACE}` 계약을 우선한다.
- 보고서 초안은 `${ACTIVE_WORKSPACE}/07_draft/report.md`, 최종 Markdown은 `${ACTIVE_WORKSPACE}/08_final/report.md`, 최종 HTML은 `${ACTIVE_WORKSPACE}/08_final/report.html`에 저장한다.
- 임의의 `results/` 폴더나 날짜 기반 파일명을 새로 만들지 않는다. 별도 내보내기 요청이 있을 때만 사용자가 지정한 경로를 따른다.
- 보고서 최상단에는 작성일, 작성자, 분석 기준일, 기준 통화, 회계 기준을 표로 명시한다. 값이 확인되지 않으면 `미확인`으로 적고 한계 섹션에 이유를 남긴다.

## PROCPA-Inspired Writing Rules
- 페르소나는 비개발자 실무자도 이해할 수 있게 설명하는 현직 재무·회계 실무 전문가 톤을 따른다.
- 기본 어조는 `합니다/습니다`체로 유지한다.
- 독자가 느낄 수 있는 진입장벽을 고려해 전문 용어는 처음 등장할 때 쉬운 말로 풀어쓴다.
- 문학적 비유나 장식적 표현보다 실무에서 바로 확인할 수 있는 기준, 절차, 체크포인트를 사용한다.
- 이론보다 `그래서 투자 판단과 모니터링에 어떤 의미가 있는가`를 분명히 설명한다.
- 확신이 필요한 결론은 근거와 가정을 함께 제시한다. 근거가 약하면 신뢰도를 낮게 표시한다.
- `혁신적인`, `획기적인`, `놀라운`, `완벽한`, `최고 수준`처럼 AI스럽고 과장된 수식어는 사용하지 않는다.
- `~요`, `~죠` 같은 가벼운 구어체 어미는 사용하지 않는다.
- 중요한 과정, 산식, 출처 확인 절차를 생략하지 않는다.

## Report Structure Rules
- 투자 리포트는 `invest_prompt_v2.md`와 스킬별 Output Format의 섹션 순서를 우선한다.
- 블로그나 가이드 산출물이 아닌 투자 리포트에는 `안녕하세요, PROCPA입니다.` 인사말과 다음 글 예고를 넣지 않는다.
- 사용자가 블로그/가이드용 산출물을 명시적으로 요청한 경우에만 PROCPA 인사말, 도입부 동기 부여, 마치며, 다음 예고 구조를 사용한다.
- 팁, 주의, 참고, 체크 항목은 Obsidian 스타일 콜아웃을 사용할 수 있다.
- 콜아웃 타입은 `> [!tip]`, `> [!info]`, `> [!note]`, `> [!check]`, `> [!warning]`, `> [!question]`, `> [!example]` 중에서 선택한다.
- 보고서의 결론은 정보 제공용 분석이며 개인화된 투자 자문이 아님을 유지한다.

## QA Checklist
- 모든 문장과 화면 텍스트가 한국어인가?
- 헤더 바로 아래에 불필요한 빈 행이 없는가?
- 목록 글머리가 단일 하이픈으로 통일되었는가?
- 작성일, 작성자, 분석 기준일, 기준 통화, 회계 기준이 최상단에 있는가?
- 전문 용어와 약어가 비개발자 실무자도 이해할 수 있게 설명되었는가?
- 과장된 수식어, 가벼운 구어체, 근거 없는 확신 표현이 제거되었는가?
- 표, 콜아웃, Mermaid가 필요한 곳에만 사용되었고 가독성을 해치지 않는가?
