# formagent 진행 계획: 서식 이미지 → 서식 추가 에이전트 (ReLab + studio 탭)

상태: **진행기·검사·studio 탭 완료** — `python -m formagent` (사용법 [README.md](README.md)), 스킬 `check.py`·`test_draft.py`, studio 메뉴 **이미지로 서식 만들기** (`studio/api_form_agent.py`, `static/js/form-agent.js`). 등록: 결과 탭 [등록] · `python -m formagent register` · 스킬 `register.py`. 남은 것: 내부망 실제 모델 시험(11절 6).

## 1. 목적

서식 이미지를 넣으면 사내 모델(DeepSeek, vLLM)이 **스킬 `form-from-image` 를 따라** docgen 서식 하나를 만들고,
사람은 studio 화면에서 진행과 결과를 보고 이어서 지시하거나 등록한다.

- 만드는 서식: `template.html.j2` + `fields.json`(초안에서는 `form.json` 안) + `form.json` (+ 칸끼리 관계가 있으면 `generate.py`).
  서류 한 건마다 다른 값을 채워 그림과 정답(키·값·위치)을 찍어 내는 합성 데이터 생성기다 (`.claude/skills/form-from-image/SKILL.md` 목표).
- 에이전트는 새로 만들지 않고 사내 코딩 에이전트 CLI **ReLab**(`relab chat`)을 쓴다. 이 폴더는 ReLab 을 회차로 돌리는 진행기와 studio 연결만 맡는다.

## 2. 정한 것

| 무엇 | 결정 | 까닭 |
|---|---|---|
| 에이전트 | ReLab CLI 0.3.46 `relab chat -p … --auto` | 파일 읽기·쓰기·명령 실행·권한 정책·기록이 이미 있음 |
| 모델 | 사내 vLLM 의 DeepSeek 4.1 Flash (이미지 입력 가능, 도구 호출 켜짐, max-model-len 1,240,000, 이미지 요청당 약 5장) | 내부망 |
| 화면 | studio 새 탭 **이미지로 서식 만들기** | 서식 등록·검수가 studio 에 있음 |
| 코드 위치 | 저장소 최상위 `formagent/` (이 폴더) | docgen 엔진·studio 와 섞지 않음 |
| 그림 보기 | **회차 방식**: 회차마다 요청에 `@그림` 을 붙인다 (3절 제약) | ReLab 은 작업 중에 만든 그림을 열어 볼 수 없음 |
| 초안 위치 | `out/form_drafts/<ID>/` (저장소 안, `.gitignore`) | ReLab 은 작업 폴더(저장소) 안에만 쓴다. `docker/build.sh` 는 git 에 올라간 파일만 묶으므로 반입 묶음에 섞이지 않음 |
| 회차 잇기 | **회차마다 새 대화**, 앞 회차의 결과는 초안 폴더의 파일(`fields.md`·`review.md`·`report.md`·`check_<n>/check.json`)로 넘긴다 | `-p` 에서는 `-c` 가 무시됨 (13절 시험) |
| ReLab 설정 | `defaultRules: false` (기본 규칙이 `docs/` 문서를 만들게 함), `planFirst: false` (새 `.py` 를 계획 승인 없이 못 씀) | 13절 시험 |
| 검사 명령 | `python -m pytest .claude/skills/form-from-image/test_draft.py --draft <초안> -q` (안에서 `check.py` 를 부름) | ReLab 은 바뀐 `.py`·`.json` 을 덮는 검사가 통과해야 끝내기를 받음. 테스트 실행기에 초안 경로를 넘기면 덮은 것으로 침 (13절) |
| 동시 실행 | 한 번에 한 건 (대기열) | 같은 저장소에서 미리보기·검사가 겹치지 않게, 화면도 단순하게 |
| 등록 | 사람이 화면 [등록] 을 누를 때만 (2차) | 스킬 7단계, AGENTS.md 규칙 7 |

## 3. ReLab 에서 확인한 것 (배포 묶음의 MANUAL.md·코드를 읽고, 13절에서 가짜 모델로 돌려 봄)

| 필요한 것 | ReLab | 비고 |
|---|---|---|
| 설치 | 파이썬 패키지, 묶음의 wheel 로 인터넷 없이 (`sh install.sh`), Python 3.10~3.13 | studio 컨테이너에 설치 |
| 비대화 실행 | `relab chat -p "요청"` · 종료 코드 0 완료, 1 미완료, 2 시작 실패, **3 모델이 사람에게 묻고 기다림** | |
| 자동 승인 | `--auto` (ReLab 의 금지 명령은 그대로 막힘) | |
| 모델 지정 | `--provider vllm --endpoint <주소> --model <이름>` 또는 `.relab/config.json` | 키는 `VLLM_API_KEY` |
| 이어 하기 | `-c` 는 대화형에서만. **`-p` 와 같이 쓰면 무시되고 새 대화** (`relab_cli/chat.py` 가 `-p` 를 먼저 처리하고 끝남) | 회차는 파일로 잇는다 |
| 명령 실행 (`run`) | 셸 문자열이 아니라 인자 목록. `bash -c`·`rm`·`git push/reset` 은 `--auto` 여도 거부. `python -m <저장소 모듈>`·저장소 안 `.py` 스크립트·`pytest`·읽기 명령은 바로 실행, `python -c` 등은 묻고(`--auto` 면 실행) | 스킬의 `for`·heredoc 명령은 못 씀 → `check.py`·`register.py` 스크립트로 |
| 끝내기 조건 | 마지막으로 바뀐 `.py`·`.json`(등) 을 **덮는 검사가 통과**해야 `finish` 를 받음. 두 번 거절되면 "미완료"(종료 코드 1)로 끝남 | `python -m docgen.preview` 는 검사로 안 침. 테스트 실행기 + 초안 경로는 침 |
| 작업 폴더 | `--workspace <폴더>` | 저장소 폴더 |
| 파일 도구의 경로 | 작업 폴더 기준 상대 경로만 (`..` 안 됨). 경로 조각에 `.git`·`.relab`·`.env`·`secrets`·`private` 가 있으면 막힘 (`relab_core/targets.py`) | 초안은 저장소 안 `out/form_drafts/<ID>/`, ID 에 `private`·`secrets` 금지. 셸 명령은 이 제한을 받지 않음 (10절) |
| 규칙·스킬 | `.claude/skills` 자동 인식은 **없음**. `AGENTS.md`·`CLAUDE.md`·`.relab/RELAB.md` 를 매 단계 규칙으로 읽음 | `AGENTS.md` 에 스킬 경로가 있음 + 요청에 "SKILL.md 를 읽고 따르라" |
| 기록 | 화면 출력(`●` 모델 말, `⎿` 한 일), `relab code list --json` | 진행 탭에 씀 |
| **그림** | **요청에 `@경로` 로 적은 그림만**, 요청당 4장, 한 장 2MB, png·jpg·gif·webp | 작업 중 `read_file` 로 그림을 열 수 없음 → 회차 방식 |

**내부망에서 먼저 확인할 것** (계획의 전제, 12절): 그림이 실제로 모델에 붙는지, `SKILL.md` 를 읽고 따르는지, `-c` 로 이어지는지, 종료 코드.

## 4. 흐름

```
studio [새로 만들기]  이미지·ID·원본 종류·추가 요청
  └─► python -m formagent run …   (studio 작업 틀 studio/jobs.py 로 백그라운드. 화면 없이도 같은 명령)
        1회차  relab chat -p "@원본  스킬을 읽고 따라라 … 1~4단계, 검사 명령으로 끝" --auto
        검사    python .claude/skills/form-from-image/check.py <초안> --out check_<n>   → 비교 그림·렌더 모음·검사 JSON
        2회차  relab chat -p "@비교 그림 @렌더 모음  초안 폴더의 fields.md·review.md 를 먼저 읽고 … 5단계대로 고쳐라" --auto   (새 대화)
        검사 → 3회차 → 검사 → 4회차   (모델이 "고칠 것 없음"이면 멈춤, 고치기 최대 3회)
        끝      check.py 로 마지막 재검사 → report.json, 상태 "끝남"
studio [진행]   ReLab 출력 실시간
studio [결과]   회차별 비교 그림, 렌더, 검사, review.md, 재검사 결과
studio [파일]   fields.md(표), template, form.json, generate.py
studio [이어서 지시]  "…고쳐"   → python -m formagent continue … → relab chat -p "@최신 비교 그림 + 앞 회차 요약 + 지시" (새 회차) → 검사
studio [질문에 답]   종료 코드 3 이면 모델의 질문을 띄우고, 질문과 답을 다음 회차 요청에 넣는다
studio [멈추기]      relab 프로세스 종료, 상태 "멈춤"
studio [등록] (2차)  check.py 통과·사람 확인 → docgen/forms/<ID> 또는 비공개 폴더 → 서식 › 미리보기/검수
```

회차 안에서는 ReLab 이 스스로 파일을 읽고 쓰고 명령을 돌린다. 진행기는 **회차 사이에 그림과 검사 결과를 붙여 다음 요청을 넣는 일**만 한다.

## 5. 입력 · 중간 출력 · 최종 출력

**입력**

| 무엇 | 어디서 | 꼴 |
|---|---|---|
| 서식 이미지 | 화면 (새로 만들기) | png·jpg, 쪽마다 1장, 최대 3쪽, 한 장 2MB 이하로 줄여 저장 |
| 서식 ID | 화면 | `[a-z][a-z0-9_]{2,50}`, 이미 있으면 거부 (`python -m docgen.formdir path`) |
| 원본 종류 | 화면 | 빈 서식 / 견본 / 실서류 |
| 추가 요청 | 화면 (선택) | 글 |
| 모델·ReLab 설정 | studio `config.json` 의 `form_agent` | 8절 |
| 스킬 | 저장소 `.claude/skills/form-from-image/` | `SKILL.md`, `check.py`, `compare.py`, `example/` |

**중간 출력** (`out/form_drafts/<ID>/`)

| 파일 | 누가 | 언제 |
|---|---|---|
| `source.png`, `source_2.png` … | 진행기 | 시작 |
| `run.json` | 진행기 | 계속 (상태·회차·종료 코드·시각·질문) |
| `relab_<회차>.log` | 진행기 (ReLab 출력 그대로) | 회차마다 |
| `fields.md` | 모델 | 스킬 1단계 |
| `template.html.j2`, `form.json`, `generate.py` | 모델 | 2·3단계 |
| `check_<회차>/` : `check.json`, `side_<쪽>.png`, `renders.png`, `render_*/` | `check.py` | 회차 끝마다 |
| `review.md` | 모델 | 2회차부터 |

**최종 출력**

| 파일 | 내용 |
|---|---|
| `report.md` | 모델의 마지막 보고 (스킬 6단계 표) |
| `report.json` | 진행기가 `check.py` 로 **직접 다시 검사한 결과** (모델 말과 따로): `pages`·`checks`·`overflow`·관계 경고·다른 사람 칸·표기 섞임, 회차 수, 남은 "아니오", 바뀐 저장소 파일(초안 밖) |
| 등록 가능한 초안 | `template.html.j2` + `form.json` (+ `generate.py`) |
| (등록 후) | `docgen/forms/<ID>/` 또는 `$DOCGEN_PRIVATE_FORMS/<ID>/` 의 `look/template.html.j2`·`fields.json`·`form.json`·`generate.py`·`source.png`·`FORM.md` |

## 6. 회차별 요청 문장 (초안)

```text
[1회차]
@out/form_drafts/<ID>/source.png [@…source_2.png]
.claude/skills/form-from-image/SKILL.md 를 끝까지 읽고 그 순서를 따라 이 이미지로 서식을 만들어라.
서식 ID <ID>, 초안 폴더 out/form_drafts/<ID>/ (원본 그림은 이미 들어 있음), 원본 종류 <빈 서식|견본|실서류>.
이번 회차는 0~4단계까지: fields.md → template.html.j2 · form.json (· generate.py) →
python -m pytest .claude/skills/form-from-image/test_draft.py --draft out/form_drafts/<ID> -q 가 통과할 때까지 고친다.
비교 그림은 다음 요청에 붙여 준다. 초안 폴더 밖의 파일은 고치지 않는다. 등록하지 않는다.
<추가 요청>

[2회차 ~]  (새 대화라 앞 회차를 모른다: 필요한 것을 모두 적는다)
@out/form_drafts/<ID>/check_<n>/side_0.png @out/form_drafts/<ID>/check_<n>/renders.png
.claude/skills/form-from-image/SKILL.md 를 따르는 서식 만들기의 <n+1>회차다. 서식 ID <ID>, 초안 폴더 out/form_drafts/<ID>/,
원본 종류 <…>. 앞 회차까지 fields.md · template.html.j2 · form.json (· generate.py · review.md) 를 썼다 — 먼저 읽어라.
붙인 그림: 원본(왼쪽)|렌더(오른쪽) 나란히, 렌더 4장 모음. <n>회차 검사 결과: <check.json 요약 — pages, checks, overflow, 관계·표기 경고>.
스킬 5단계대로 review.md 에 <n+1>회차 8문항을 더하고, "아니오"를 고친 뒤 검사 명령(pytest … test_draft.py --draft …)을 통과시켜라.
고칠 것이 없으면 review.md 에 그렇게 적고 6단계 보고를 report.md 로 써라.

[이어서 지시]
@<최신 비교 그림> (2회차와 같은 머리말) + 사람의 지시: <글> (+ 모델이 물은 것과 사람의 답). 고친 뒤 검사 명령을 통과시키고 report.md 를 고쳐라.
```

## 7. 폴더 구성

```
formagent/                     (새로)
  PLAN.md                      이 문서
  README.md                    사용법 (만든 뒤)
  __init__.py · __main__.py    python -m formagent run | continue | answer | stop | status
  runner.py                    회차 진행: 요청 만들기 → relab 실행 → check.py → 다음 회차, run.json·report.json
  relab.py                     relab 명령 만들기·실행·출력 읽기·종료 코드
  tests/                       가짜 relab(대본대로 파일을 쓰는 스크립트)로 회차·종료 코드 3·멈추기·동시 실행 막기

.claude/skills/form-from-image/
  check.py                     (새로) 미리보기 min·max·seed 1~3, 통과 판정, {{ d. 찾기, 정답 값 요약(관계·다른 사람 칸·표기 섞임),
                               원본|렌더 나란히 + 렌더 4장 모음 그림(한 장 2MB 이하), JSON 하나, 통과면 종료 코드 0
                               — 사람·Cline·studio 가 같은 명령
  test_draft.py · conftest.py  (새로) pytest 로 check.py 를 부르는 얇은 겉: `python -m pytest …/test_draft.py --draft <초안> -q`.
                               ReLab 이 검사로 알아보게 하는 것. --draft 가 없으면 건너뜀 (저장소 전체 pytest 는 testpaths 라 이 파일을 안 모음)
  SKILL.md                     (손질) 4단계를 check.py 하나로, "그림은 회차마다 요청에 붙는다", 초안 폴더는 요청에 적힌 곳,
                               등록은 화면, 여러 개 체크 묶음·part 꼴·날짜 보기 줄·review.md 꼴 보강
  register.py                  (2차) 초안 → 등록 폴더 (화면 [등록] 과 Cline 이 같은 명령)

studio/
  form_agent.py                (새로) API: 목록·새로 만들기·상태·로그·파일·그림·이어서 지시·답·멈추기 (+등록)
  static/js/…                  (새로) 탭 화면
  config                       form_agent 설정 칸
```

## 8. 설정 (studio `config.json`)

```json
"form_agent": {
  "relab": "/opt/relab-cli/bin/relab",
  "provider": "vllm",
  "endpoint": "http://<host>:<port>/v1",
  "model": "<served model name>",
  "max_fix_rounds": 3,
  "round_minutes": 60
}
```

키는 환경 변수 `VLLM_API_KEY`. ReLab 자체 설정(`~/.relab/config.json`)의 `modelContextWindows`·`contextBudget` 은 내부망에서 정한다.

## 9. studio 탭 화면

| 화면 | 내용 |
|---|---|
| 목록 | ID · 서식 이름 · 상태(대기/진행 n회차/질문 대기/끝남/멈춤/실패) · 마지막 검사 요약 |
| 새로 만들기 | 이미지(쪽마다) · ID(바로 확인) · 원본 종류 · 추가 요청 → [시작] |
| 진행 | ReLab 출력 (회차별 접기), 종료 코드 3 이면 질문과 답 칸, [멈추기] |
| 결과 | 회차별 원본|렌더 나란히 그림 · 렌더 모음 · 검사 JSON · review.md 8문항 · report.md · 진행기 재검사(report.json) |
| 파일 | fields.md (표, 확신 낮음·판단이 안 선 것 강조) · template.html.j2 · form.json · generate.py (**실행되는 코드 — 사람이 읽을 것**) |
| 이어서 지시 | 글 → continue |
| (2차) 등록 | 공개/비공개 고르기 → 등록 → 서식 › 미리보기/검수 로 이동 |

## 10. 안전

- ReLab `--auto` 는 ReLab 의 금지 명령 정책을 따른다. 그 밖의 명령은 묻지 않고 돈다.
- 진행기는 회차 시작 전과 끝에 `git status` 와 `docgen/forms/`·비공개 서식 폴더를 비교해, **초안 폴더 밖에서 바뀐 것**을 `report.json` 과 화면에 경고로 띄운다 (막지는 못하고 알린다).
- 모델이 쓴 `generate.py` 는 미리보기 때 실행되는 코드다. 등록 전에 사람이 화면에서 읽는다.
- 실서류 그림은 사내 vLLM 에만 간다. 초안(`out/`)은 git·반입 묶음에 들어가지 않는다. 실서류에서 만든 서식은 비공개 폴더에만 등록한다.
- 회차 시간 한도(`round_minutes`), ReLab 의 호출 수·시간 한도.

## 11. 만드는 순서와 확인

| # | 만드는 것 | 확인 (개발 환경) |
|---|---|---|
| 1 ✓ | `check.py` | 기존 시험 초안 3개(`out/form_drafts/…`)에 돌려 JSON·그림 확인, 일부러 틀린 초안(값 직접 찍기·다른 사람 칸·표기 섞임·넘침)이 잡히는지 pytest |
| 2 ✓ | `SKILL.md` 손질 | (문서) ReLab 회차·검사 명령·체크 묶음·나뉜 날짜·review 꼴 반영. Haiku 재시험은 아직 |
| 3 ✓ | `formagent` 진행기 | 가짜 relab 로 회차 진행·종료 코드 3·멈추기·동시 실행 막기·초안 밖 변경 경고 pytest |
| 4 ✓ | studio API·탭 | API pytest(`studio/tests/test_form_agent_api.py`) + 실제 ReLab·가짜 모델로 studio 를 띄워 시작(ReLab 자동 설치)→1·2회차→끝까지 화면 확인 |
| 5 ✓ | `register.py`·[등록] | 예시 초안을 임시 비공개 폴더로 등록(pytest) + studio 화면에서 [등록] → 서식 목록에 미검수로 나옴, 카드·formdir check 통과 |
| 6 | 내부망 | ReLab 설치, 실제 DeepSeek 로 공개 서식 3장(예금잔액증명 의뢰서 hf011, 일괄처리(지급) 요청서 hf021, 금융거래 정보제공 요구(동의)서 hf024) — Haiku 결과와 비교 |

각 단계가 끝나면 바뀐 파일만 zip 으로 내부망에 옮긴다.

## 12. 내부망 사전 확인 (계획의 전제)

13절에서 ReLab 동작(그림 첨부·규칙 전달·명령 정책·끝내기 조건·종료 코드)은 확인했다. 남은 것은 **실제 모델**이다. 저장소 폴더에서
`~/.relab/config.json` 에 `"defaultRules": false, "planFirst": false` 를 넣고:

1. 그림: `relab chat -p "@<아무 서식 png> 이 그림의 제목과 항목명을 읽어 줘" --auto` → DeepSeek 이 제대로 읽는지 (`the model does not take images` 면 계획 변경)
2. 스킬: `relab chat -p ".claude/skills/form-from-image/SKILL.md 를 읽고 0단계에서 할 일을 요약해 줘" --auto`
3. 도구 호출: 2번 출력에 `● …` / `⎿ 읽음 .claude/skills/…` 줄이 나오는지 (vLLM 의 tool-call parser 가 맞는지)
4. 각 실행의 종료 코드(`echo $?`)와 출력 끝부분

## 13. 시험 기록: ReLab 0.3.46 + 가짜 모델 (개발 환경, 2026-11)

실제 ReLab 을 저장소 사본(git worktree)에서 돌리고, 모델 자리에 요청을 기록하고 대본대로 도구를 부르는 가짜 OpenAI 호환 서버를 두었다.
(DeepSeek 이 스킬을 얼마나 잘 따르는지는 여기서 볼 수 없다.)

| 확인한 것 | 결과 |
|---|---|
| 요청의 `@그림` | ✓ 첫 user 메시지에 `image_url` 로 붙음 (원본 252KB, 비교 그림 885KB) |
| 규칙 전달 | ✓ `AGENTS.md` 전문이 `project_rules` 로 감 (스킬 경로 포함). ReLab 기본 규칙("코드를 쓰면 `docs/` 에 README·CHANGELOG… 남긴다")도 붙음 → `defaultRules: false` 로 끔 |
| 도구 | 22개 (`read_file`, `write_file`, `edit_file`, `run`(argv), `list_files`, `search`, `ask`, `todo`, `finish` …). 한 번에 여러 개 부를 수 있음 |
| 새 `.py` 쓰기 | ✗ `planFirst: true` 면 "plan first" 로 거부 → `planFirst: false` 로 됨 |
| `python -m docgen.preview …` · `python .claude/…/compare.py …` | ✓ 묻지 않고 실행 (저장소 코드·저장소 스크립트). 환경 변수 `PLAYWRIGHT_BROWSERS_PATH` 도 전달됨 |
| `bash -c "ls out"` | 셸 없이 `ls out` 으로 풀어서 실행 (셸 문법은 안 됨) |
| `finish` | ✗ "마지막으로 바뀐 `generate.py` 를 덮는 검사가 통과하지 않음"으로 두 번 거절 → 종료 코드 1. 미리보기 명령은 검사로 안 침 → `test_draft.py`(pytest) 로 |
| `.md` 만 바꾼 회차 | ✓ 바로 완료, 종료 코드 0 |
| `-c -p` | ✗ 앞 대화가 비어 있음 (`earlier_in_this_conversation: []`). 코드상 `-p` 에서는 `-c` 를 안 봄 → 회차를 파일로 잇기 |
| 기록 위치 | `RELAB_PRIVATE_HOME`(또는 `~/.relab`) 아래 `workspaces/…/coding_loops` — 작업 폴더에는 안 남음 |
| **프로젝트 폴더** | ✗ ReLab 은 요청에 적힌 폴더(`out/form_drafts/<ID>`)나 쓴 파일들의 맨 위 폴더(`out`)를 "프로젝트"로 잡고, 그 밖 코드의 import(`generate.py` 의 `docgen.formkit`)를 거부하고 명령을 그 안에서 돌림(검사 명령의 경로가 어긋나 pytest 옵션 오류). 그 폴더가 맨 위까지 파이썬 패키지면 작업 공간 전체를 프로젝트로 봄(`project_scope.project_of`) → 진행기가 `out/`·`out/form_drafts/`·초안 폴더에 빈 `__init__.py` 를 둠 → ✓ `project_folder: null`, import·검사 통과 |
| **처음부터 끝까지** (`python -m formagent run`, ReLab 없는 상태에서) | ✓ 묶음으로 설치 → 1회차: SKILL.md 읽기·칸 표·템플릿·form.json·generate.py·검사(pytest) 통과 → **종료 코드 0(완료)** → 진행기 검사·비교 그림 → 2회차 요청에 그림 2장 첨부 → review.md·report.md → 끝남. 초안 밖 변경 없음 (약 30초) |
| 요청에 적힌 파일 | 경로("폴더/파일")로 적힌 파일을 그 회차에서 읽지 않으면 `finish` 를 거절 ("the request names …" — 쓰기만 한 `report.md`, 읽을 일 없는 `check.json` 도). 요청에는 읽을 파일만 경로로, 나머지는 이름만 적는다 |
| 1회차의 `Not done:` | 모델이 "원본 비교는 다음 회차"를 `Not done` 에 적으면 ReLab 이 미완료(1)로 끝냄 → 1회차 요청에 "그것을 Not done 에 적지 않는다" |

## 14. 열린 질문

- ReLab 설치 위치: studio 도커 이미지에 넣을지(`docker/`), 서버에 따로 설치하고 경로만 적을지.
- (고침) `generate.py` 가 있는 html 서식에서 `formdir check` 가 overlay 로 보고 `KeyError: 'items'` 로 멈추던 것 — overlay 일 때만 그 검사 (`docgen/formdir.py check_form`).

## 15. 모델이 그림 대신 짐작으로 쓰는 문제 (2026-11)

내부망 DeepSeek 결과가 원본(선적서류 (일부) 매입(추심)의뢰서)의 고유 항목(COMMODITY · H.S. CODE · ACCOUNTEE (drawee) · 고객번호 · 매입번호 · 일부 매입금액)을 빼고,
원본에 없는 흔한 항목(과장/차장 결재란, ADVICE NO.)을 지어냈다. 지어낸 글자는 스킬이 읽히는 문서 어디에도 없다 → 예시를 베낀 게 아니라 짐작.

| 확인 | 결과 |
|---|---|
| ReLab 이 그림을 보내나 | ✓ 중계 서버로 받은 그림이 원본과 바이트 동일 (1697×2400, 434KB), 매 단계 첫 user 메시지에 `image_url`. 서버가 그림을 거절(400)하면 ReLab 은 실패로 끝남 — 조용히 빼지 않음. 2MB 넘는 그림만 "not shown" 글로 바뀜 (진행기는 1.9MB 아래로 저장) |
| 그 해상도로 읽히나 | ✓ 같은 그림에서 위 항목·약정문·서식 번호까지 읽힘 |
| 스킬 쪽 의심 | 그림을 보기 전에 문서 약 120KB(NEW_FORM_SPEC·keys·values·예시·SKILL)를 읽힘 · "회차 안에서는 그림 파일을 열어 볼 수 없다"(그림을 못 본다로 읽힐 수 있음) · 글자 옮기기 없이 바로 키·source 설계 |

고친 것:
- **글자 옮기기 회차**: 1회차는 문서 없이 그림만 보고 인쇄 글자를 `source_text.md` 에 옮긴다. 2회차(만들기)는 글자를 거기서 가져온다.
- **검사**: 템플릿 글자 ↔ `source_text.md` 대조 → "지어낸 글자"(템플릿에만) · "빠진 글자"(원본에만) 경고. `source_text.md` 없으면 문제.
- **읽기 줄임**: NEW_FORM_SPEC 2·3·4·11절, keys.md 3~5절, values.md 는 검색만. 예시는 파일 꼴만 참고.
- **문장**: "요청에 `@`로 붙은 그림은 보인다, 붙지 않은 그림만 못 연다". 요청 예시 글자에 시험 원본 글자를 쓰지 않음.
- ReLab: 1회차 요청에 쓸 파일(`source_text.md`)을 경로로 적으면 "읽지 않았다"며 끝내기를 거절 → 이름만 적음 (중계 서버로 확인, 종료 코드 0).

Haiku 시험 (hf294 공개 빈 서식, 진행기와 같은 요청 문장, 회차마다 새 에이전트): 아래 기록.

| 서식 | 1 글자 옮기기 | 2 만들기 | 3 고치기 |
|---|---|---|---|
| hf294 선적서류 매입의뢰서 (영문 항목 많은 표) | 원본 고유 항목·약정문 전부, 지어낸 글자 없음 | 검사 통과, 글자 대조 경고 0, 표 구조 원본과 같음. 값 뜻 틀림: TENOR "주소 변경", FROM/TO "계좌 정리", 은행 코드·HS 코드에 계좌번호 꼴, 부수 칸 36·60 | 9번 문항·값 예시로 source 를 `rule:choice`·`rule:pattern` 으로 바꿔 모두 고침, `generate.py` 로 금액 꼴 통일. 놓침: 약정문 정렬, BENE CERT 머리글 겹침 (→ 4번 문항 보강) |
| hf025 대여금고 신청서 (체크 보기·이용대리인 2명) | 전부, 회색 안내 글자까지 | 검사 통과. 경고 4 (대리인 주소 = 고객 주소, 생년 표기 섞임, 로고, '선택항목') — **모델은 "경고 없음"이라 보고** | 대리인 주소 source 변경, 관계·생년 맞춤, 머리글 두 줄, 표기 통일 → 문제 0·경고 0 |

시험에서 찾아 고친 것:
- **검사 명령이 통과하면 경고가 출력에 안 보였다** (`print` 는 pytest 가 통과 시 숨김) → 모델이 경고를 못 봄. `DraftWarning` 으로 내 `-q` 에서도 `warnings summary` 에 나옴.
- 고치기 요청에 렌더 키→값 예시 (seed 1·2)를 직접 넣음. 비교 9번 "값이 칸의 뜻에 맞다" 추가 — 이것 없이는 구조만 보고 "같다"로 넘어감.
- source 고르기: values.md 종류 표(1~106줄)는 읽게 되돌림 (검색만 시키면 `rule:hs_code`·`rule:incoterms` 를 못 찾고 `rule:note` 로 채움). 메모 글을 내는 `rule:note`·`free_text` 는 메모 칸에만.
- 로고 자리의 기관명 글자는 "지어낸 글자"로 보지 않음.

## 16. 스킬을 새로 짬: 재기는 도구, 읽기는 모델, 쓰기는 도구 (2026-11)

내부망 3회차 결과(압수수색검증영장 팩스 스캔)가 글자는 대체로 맞는데 **표 구조부터 달랐다**: 합친 칸("대상 계좌")이 두 칸으로 나뉨, 줄마다 값 칸 시작 자리가 다름,
첫 열 너비가 덩어리마다 다른 것을 못 따라 항목명이 옆 값을 덮음. 앞 스킬은 표 구조를 **모델이 그림을 보고 html 을 쓰며 한 번에** 정하게 했고,
그것을 맞대 볼 기계 검사도 없었다 (비교 9문항 중 3·4번을 모델 눈으로만). 그림에서 선 자리·합친 칸을 재는 일은 비전 모델이 약한 일이다.

Claude 가 직접 한다면 하는 순서를 그대로 스킬로 옮겼다:

| 순서 | 누가 | 도구 |
|---|---|---|
| 기울기 바로잡기 · 표 선·칸·합친 칸·글자 덩어리 자리 재기 | 코드 | `grid.py` (Pillow 만 — studio 이미지에 numpy·OpenCV 없음) |
| 덩어리마다 잘라 크게 보고 칸 글자 읽기, 값 자리 `{키}` 정하기 | 모델 | `view.py table/crop` (보기 창) |
| 키·항목명·종류·값 만드는 법·설명 | 모델 | `layout.json` 의 `fields` |
| html 쓰기: 표 = 잰 열 너비·행 높이·rowspan/colspan, 표 밖 글자 = 잰 자리, 글자 크기 = 잰 높이 (좁은 글꼴은 가로 줄임) | 코드 | `build.py` |
| 원본·렌더를 같은 도구로 재서 맞대기 (표 선, 칸 글자 있음/없음, 잘린 글자, 글자 덩어리 너비, 값이 칸 밖) | 코드 | `check.py` |
| 같은 자리의 원본·렌더를 잘라 맞대 보며 `layout.json` 고치기 | 모델 | `view.py compare` |

**보기 창**: ReLab 에는 그림을 여는 도구가 없지만, 요청에 `@` 로 붙인 그림을 **단계마다 디스크에서 다시 읽는다** (`coding_loop._pictures`).
중계 서버로 확인: `@img/view.png` 를 붙인 요청에서 1단계에 모델이 명령으로 파일을 덮어쓰자 2단계 요청에는 새 그림이 실렸다 (빨강 200×100 → 파랑 300×150).
그래서 진행기는 `view_1~4.png` 네 장을 늘 붙이고, 모델은 `view.py … --to n` 으로 원하는 곳을 띄운다. 파일은 시작 때 있어야 하고 2MB 이하.

선 찾기 시험 (원본 = 공개 hf011·hf294·hf025, 팩스 흉내 = 0.9배·1.2° 기울임·흑백·티끌·끊김):

| | 깨끗한 원본 | 팩스 흉내 |
|---|---|---|
| 기울기 | 0 | 1.18~1.22° 찾아 바로잡음 |
| hf011 표 4개 | 열 경계·행 경계·합친 칸 원본과 같음 | 같은 구조 (자리 0.9배) |
| hf294 표 9개 (16열 표 포함) | 같음 | 같음 |
| hf025 | 같음 | 표 1개에서 열 경계 1개 더 찾음 |

글자 획을 선으로 잘못 보는 것: 끊김 메우기를 2px 로 작게 + 선 바로 위·아래 줄이 함께 검으면(글자 줄) 버림. 바코드(촘촘한 세로선 무리)는 선 목록에서 빼고 자리만.

hf011 을 이 순서로 직접 만든 결과: 표 선 대조 경고 0 (원본과 렌더의 열·행 경계 3px 안), 남은 경고는 칸 가장자리에 닿은 글자 2칸 · 글자 덩어리 너비 2곳.
글자 크기: 한글 검은 부분 높이 ≈ 글자 크기 × 0.9 (렌더로 맞춤). 원본이 좁은 글꼴이면 같은 높이로는 넓게 그려지므로, 글자 크기를 비율만큼 줄이고 세로만 `scaleY` 로 되돌린다
(가로 `scaleX` 는 칸 너비를 그대로 차지해 정렬이 어긋남).
