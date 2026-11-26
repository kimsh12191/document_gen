# formagent 진행 계획: 서식 이미지 → 서식 추가 에이전트 (ReLab + studio 탭)

상태: **진행기·검사 완료, studio 탭 전** — `python -m formagent` (사용법 [README.md](README.md)), 스킬 `check.py`·`test_draft.py`. 남은 것: studio 탭(11절 4), 등록 버튼(5), 내부망 실제 모델 시험(6).

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
| 4 | studio API·탭 | 가짜 relab 로 띄워 화면 캡처 |
| 5 | (2차) `register.py`·[등록] | 임시 비공개 폴더로 등록 → `card`·미리보기 |
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
| 요청에 적힌 파일 | 그 회차에서 읽지 않으면 `finish` 를 한 번 거절 ("the request names …"). 2회차 요청은 SKILL.md·초안 파일을 먼저 읽으라고 적는다 |

## 14. 열린 질문

- [등록] 을 첫 판에 넣을지 (지금 계획: 2차).
- ReLab 설치 위치: studio 도커 이미지에 넣을지(`docker/`), 서버에 따로 설치하고 경로만 적을지.
- `generate.py` 가 있는 html 서식에서 `python -m docgen.formdir check` 가 `KeyError: 'items'` 로 멈추는 엔진 문제를 고칠지 (등록 확인에 필요).
