"""초안 서식 검사를 pytest 로 (check.py 와 같은 검사).

    python -m pytest .claude/skills/form-from-image/test_draft.py --draft out/form_drafts/<ID> -q

ReLab 같은 에이전트는 바뀐 파일을 "테스트 실행기"가 덮어야 일이 끝났다고 본다. 그래서 같은 검사를 pytest 로도 부른다.
--draft 가 없으면 건너뛴다 (저장소 전체 pytest 는 pytest.ini 의 testpaths 라 이 파일을 모으지 않는다).
"""
import json

import check


def test_draft(draft):
    result = check.run(draft)
    print(json.dumps(check.summary(result), ensure_ascii=False, indent=1))
    assert result["passed"], "\n".join(["검사를 통과하지 못했습니다:", *result["problems"]])
