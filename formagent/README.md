# formagent: 서식 이미지 → docgen 서식 (사내 모델 + ReLab)

서식 이미지를 주면 사내 모델(vLLM)이 ReLab CLI 로 스킬 [`form-from-image`](../.claude/skills/form-from-image/SKILL.md) 를 따라
서식 초안(`fields.md` · `template.html.j2` · `form.json` · 필요하면 `generate.py`)을 만들고, 원본과 비교하며 고친다.
등록은 사람이 결과를 보고 한다 (스킬 7단계). 설계와 시험 기록은 [PLAN.md](PLAN.md).

## 준비

| 무엇 | 어떻게 |
|---|---|
| Python | 3.10~3.13, 리눅스 x86_64 (studio 서버·컨테이너) |
| ReLab | 없으면 `python -m formagent install` (또는 처음 `run` 할 때) 이 이 폴더의 묶음 `relab/wheels` 로 **인터넷 없이** `~/.local/share/relab-cli` 에 설치. 이미 깔린 것은 `RELAB_BIN` · PATH 의 `relab` 순서로 찾음 |
| 모델 | `~/.relab/config.json` 에 `"provider": "vllm"`, `"codingModel": "<served model>"`, `"vllmEndpoint": "http://<host>:<port>/v1"`, `"modelContextWindows": {"<served model>": 1240000}` — 또는 실행할 때 `--provider vllm --endpoint … --model …`. 키가 필요한 서버면 환경 변수 `VLLM_API_KEY` |
| 프로젝트 설정 | 저장소의 `.relab/config.json` (`defaultRules: false` — ReLab 이 `docs/` 문서를 만들지 않게, `planFirst: false` — 새 `.py` 를 계획 승인 없이 쓰게). 커밋되어 있음 |
| 미리보기 | `python -m docgen.preview` 가 되는 곳 (Playwright Chromium. studio 이미지에는 있음) |

## studio 화면

studio 왼쪽 메뉴 **이미지로 서식 만들기** (`studio/api_form_agent.py`, `studio/static/js/form-agent.js`): 그림·ID·원본 종류·추가 요청 → **[시작]**
(ReLab 이 없으면 자동 설치) → **진행**(회차마다 모델의 말·한 일·검사) · **결과**(원본|렌더 나란히, 마지막 검사, 보고) · **파일**(fields.md 표 등) → **이어서 지시** · **[멈추기]**
→ 결과 탭 **[등록]** (공개/비공개 고르고 확인 세 가지에 체크 → 검사·옮기기·카드·formdir check → 서식 다시 읽기 → 서식 › 미리보기/검수).
화면이 띄우는 것도 아래 명령이다 (`go` · `continue`). 모델 설정은 studio `config.json` 의 `"form_agent": {"provider", "endpoint", "model", "max_fix_rounds", "round_minutes", "relab"}`.
화면 설명은 [guide/studio/studio.md](../guide/studio/studio.md#이미지로-서식-만들기). 그림: [화면 흐름](docs/screens.png) · [동작 시나리오](docs/scenario.png) (가짜 모델로 돌린 실제 화면).

## 명령 (저장소 맨 위에서)

```bash
python -m formagent install                                                   # ReLab 확인·설치, 경로 출력
python -m formagent run --image a.png [b.png] --id loan_application --kind blank [--note "현금 행은 계좌 비워"]
                       [--provider vllm --endpoint http://<host>:<port>/v1 --model <name>] [--rounds 3] [--round-minutes 60]
python -m formagent go       --id loan_application                            # (studio 가 씀) 초안을 만든 뒤 회차 돌기
python -m formagent status   --id loan_application                            # 상태·회차·검사 요약
python -m formagent continue --id loan_application --message "계좌번호 칸을 세 칸으로"   # 이어서 지시 (질문에 대한 답도 이것으로)
python -m formagent stop     --id loan_application                            # 멈추기 (다른 터미널에서)
python -m formagent register --id loan_application --to public                # 등록 (사람이 확인한 뒤): public=docgen/forms, private=$DOCGEN_PRIVATE_FORMS
```

- `--kind`: `blank` 빈 서식 · `sample` 견본 · `real` 실서류 (실제 값을 어느 파일에도 옮기지 않게 요청에 적음).
- 종료 코드: 0 끝남 · 3 모델이 질문하고 기다림 (`status` 의 `question` 을 보고 `continue --message <답>`) · 1 멈춤·실패 · 2 시작 못 함 (ID·이미지·ReLab).
- 한 번에 한 건만 돌린다 (같은 저장소에서 미리보기·검사가 겹치지 않게).

## 결과 (`out/form_drafts/<ID>/`, git 에 올라가지 않음)

| 파일 | 누가 | 내용 |
|---|---|---|
| `source.png`, `source_2.png` … | 진행기 | 원본 (2MB 이하로 줄임) |
| `fields.md` · `template.html.j2` · `form.json` · `generate.py` | 모델 | 서식 초안 (스킬 1~3단계) |
| `review.md` · `report.md` | 모델 | 회차별 비교 8문항, 마지막 보고 (스킬 5·6단계) |
| `run.json` | 진행기 | 상태 `running`·`waiting`·`done`·`stopped`·`failed`, 회차마다 요청 문장·종료 코드·검사 요약 |
| `relab_<n>.log` | 진행기 | n회차 ReLab 출력 그대로 (모델의 말 `●`, 한 일 `⎿`) |
| `check_<n>/` · `check_final/` | 진행기 | 회차 뒤 검사 (`check.py`): `check.json`, `side_<쪽>.jpg`(원본·렌더 나란히), `renders.jpg`(렌더 모음) |
| `report.json` | 진행기 | 마지막 검사(모델 말과 따로), 회차 요약, **초안 폴더 밖에서 바뀐 파일** |
| `__init__.py` | 진행기 | ReLab 이 저장소 전체를 프로젝트로 보게 하는 표시 (PLAN.md 13절) |

## 회차

1. **1회차:** 요청 = 원본 그림(`@source.png`) + "SKILL.md 를 읽고 따라라, 0~4단계, 검사 명령 통과". 모델이 칸 표 → 템플릿·form.json(·generate.py) → `python -m pytest .claude/skills/form-from-image/test_draft.py --draft <초안> -q` 통과까지.
2. 진행기가 `check.py` 로 검사해 `check_1/` 에 비교 그림을 만든다.
3. **2회차~:** 요청 = 비교 그림(`@side_0.jpg`, `@renders.jpg`) + 앞 회차 파일 안내 + 검사의 문제·경고 (+ 사람의 지시). 모델이 `review.md` 8문항 → 고침 → 검사 통과 → `report.md`.
4. `report.md` 를 쓰고 검사를 통과하면 끝. 아니면 `--rounds` 만큼 (기본 3) 고치기 회차.

ReLab 은 `-p`(비대화 실행)에서 `-c`(이어 하기)를 보지 않아 **회차마다 새 대화**다. 앞 회차는 초안 폴더의 파일과 요청 문장으로 넘긴다.

## 사람이 볼 것

- `fields.md` 의 키·설명 (데이터셋을 만든 뒤에는 키를 못 바꿈), `check_final/side_*.jpg`, `report.json` 의 `warnings`·`outside_changes`.
- `generate.py` 는 미리보기 때 **실행되는 코드**다. 등록 전에 읽는다.
- 괜찮으면 **[등록]** (또는 `python -m formagent register`) → studio 서식 › 생성 사례 › 미리보기/검수 → 검수 완료. 실서류에서 만든 것은 비공개 폴더에만 (공개는 거부).

## 시험

```bash
python -m pytest formagent/tests -q          # 가짜 relab 으로 회차·질문·이어서·멈추기·초안 밖 변경
```

실제 ReLab 을 가짜 모델 서버로 돌린 시험은 PLAN.md 13절.
