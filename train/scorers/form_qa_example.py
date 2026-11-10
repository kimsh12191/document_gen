"""채점 함수 견본: 서식 전용 질문(서식 폴더 qa.py, 과제 form_qa) 중 몇 개만 다르게 채점하고, 나머지는 모두 기본 채점.

서식 폴더에는 질문·정답만 두고, 채점은 여기(train/scorers) 한 곳에서 정한다. 이 파일을 복사해 RULES 를 고친다.
설정 (data.benchmark 의 평가 세트 하나에, 경로는 설정 파일 기준):
  {"id": "syn", "paths": ["<bank 데이터셋>"], "scorer": "../scorers/my_form_qa.py:score"}
이 함수는 그 세트의 평가 점수(보고서·studio)에 쓰인다.
고친 뒤 학습 없이 다시 채점: python -m train report <결과 폴더> --rescore (guide/train/steps.md).

문항에서 쓸 것
  item["meta"]["question"]   "<서식ID>.<qa.py 함수 이름>" (예: "employment_certificate.재직기간")
  item["answer"]             qa.py 가 돌려준 정답 (글·숫자·"예"/"아니오"·JSON)
  item["eval"]["answer_type"]  기본 채점 종류: number · yesno · text · json
꼴·규칙은 train/scorers/kie_default.py 맨 위: score(item, output) -> {"metrics": {이름: 0~1}, "main": 주 지표, "parse_fail"?}
"""
from docgen.bench import evaluate as E
from docgen.bench.metrics import loose_text, strip_answer, to_number


def contains_all(item, output):
    """정답 글의 줄마다 답에 들어 있으면 맞음 (순서·다른 말 허용). 줄글 요약 질문에."""
    lines = [x for x in str(item["answer"]).split("\n") if x.strip()]
    got = loose_text(output or "")
    ok = [loose_text(x) in got for x in lines]
    return {"metrics": {"acc": float(all(ok)), "line_recall": sum(ok) / len(ok) if ok else 1.0}, "main": "acc"}


def near_number(tol):
    """숫자가 tol 안이면 맞음 (예: 개월 수 ±1)."""
    def score(item, output):
        p = to_number(strip_answer(output))
        return {"metrics": {"acc": float(p is not None and abs(p - float(item["answer"])) <= tol)}, "main": "acc",
                "parse_fail": p is None}
    return score


# 질문 → 채점 함수. 여기 없는 질문·과제는 기본 채점 (studio 기본과 같은 점수)
RULES = {
    # "employment_certificate.요약": contains_all,
    # "loan_application.대출기간": near_number(1),
}


def score(item, output):
    rule = RULES.get((item.get("meta") or {}).get("question"))
    if rule is not None:
        return rule(item, output)
    r = E.SCORERS[item["task"]](item, output)
    return {**r, "main": r.get("main") or E.main_metric(item["task"], r["metrics"])}
