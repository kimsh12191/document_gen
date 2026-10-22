"""시나리오 예시의 고객 일관성과 프로필 설정별 캐시 분리 (브라우저 없이 검사)."""
import pytest

from docgen import preview
from docgen.bench.build import Builder


@pytest.fixture()
def rendered_profiles(tmp_path, monkeypatch):
    profiles = []

    def render(spec, profile, seed):
        profiles.append((spec.id, profile))
        return "<html></html>", [], {}

    class Renderer:
        def render(self, html, path):
            return {"images": [str(path)], "pages": [{"width": 100, "height": 200}], "overflow": False}

        def __exit__(self, *args):
            pass

    monkeypatch.setattr(preview, "render", render)
    monkeypatch.setattr(preview, "source_hash", lambda doc_id: "source")
    monkeypatch.setattr("docgen.schema.build_fields", lambda raw, info: [])
    pv = preview.Previewer(tmp_path)
    pv._renderer = Renderer()
    yield pv, profiles
    pv.close()


def test_scenario_documents_share_customer_and_bundle_settings(rendered_profiles):
    pv, profiles = rendered_profiles
    expected = Builder.bundle_profile("jeonse_loan", 42)
    for doc_id in ("resident_id_card", "employment_certificate", "loan_application"):
        pv.render(doc_id, seed=42, extra=expected.extra)
    assert len(profiles) == 3
    for doc_id, p in profiles:
        assert p.person == expected.person
        assert p.employment == expected.employment
        assert p.property == expected.property
        assert p.extra == expected.extra


def test_profile_settings_are_part_of_preview_cache(rendered_profiles):
    pv, profiles = rendered_profiles
    jeonse = {"scenario": "jeonse_loan", "loan_kind": "jeonse", "form_bank": "하나은행"}
    a = pv.render("loan_application", seed=42, extra=jeonse)
    again = pv.render("loan_application", seed=42, extra=dict(reversed(list(jeonse.items()))))
    credit = pv.render("loan_application", seed=42, extra={**jeonse, "loan_kind": "credit"})
    plain = pv.render("loan_application", seed=42)
    assert len(profiles) == 3
    assert a["images"] == again["images"]
    assert len({a["images"][0], credit["images"][0], plain["images"][0]}) == 3
    assert profiles[0][1].extra["loan_kind"] == "jeonse"
    assert profiles[1][1].extra["loan_kind"] == "credit"
    assert profiles[2][1].extra == {}


def test_preview_rejects_non_object_profile_settings(rendered_profiles):
    pv, _ = rendered_profiles
    with pytest.raises(ValueError, match="JSON 객체"):
        pv.render("loan_application", extra=["jeonse"])


def test_first_page_returns_early_and_rest_follows_or_yields(tmp_path, monkeypatch):
    """화면 미리보기(first=True): 1쪽만 찍고 돌려준 뒤 남은 쪽을 찍는다. 그 사이 다른 요청이 오면 양보하고, 나중에 complete 가 마저 그린다."""
    import threading
    from pathlib import Path

    gate = threading.Event()
    shots = []

    class Renderer:
        def render(self, html, path, first_only=False):
            paths = [Path(path).with_name(f"page_p{i + 1}.png") for i in range(3)]
            for i, p in enumerate(paths):
                if i == 0 or not first_only:
                    p.write_bytes(b"png")
                    shots.append(p.name)
            info = {"images": [str(p) for p in paths], "pages": [{"width": 100, "height": 200}] * 3, "overflow": False}
            if first_only:
                info["rest"] = [[i, str(p)] for i, p in enumerate(paths) if i]
            return info

        def finish(self, rest, stop=lambda: False):
            for _, p in rest:
                gate.wait(5)
                if stop():
                    return False
                Path(p).write_bytes(b"png")
                shots.append(Path(p).name)
            return True

        def __exit__(self, *args):
            pass

    monkeypatch.setattr(preview, "render", lambda spec, profile, seed: ("<html></html>", [], {}))
    monkeypatch.setattr(preview, "source_hash", lambda doc_id: "source")
    monkeypatch.setattr("docgen.schema.build_fields", lambda raw, info: [])
    pv = preview.Previewer(tmp_path)
    pv._renderer = Renderer()
    label = pv.render("loan_application", seed=1, first=True)   # 남은 쪽은 gate 에서 멈춰 있다
    folder = tmp_path / Path(label["images"][0]).parent
    assert (folder / "pending.json").exists() and pv.finishing(folder) and shots == ["page_p1.png"]
    gate.set()
    pv.call(lambda: None)   # 줄 선 일이 있으면 남은 쪽을 멈춘다 (이미 찍은 쪽까지만)
    assert not pv.finishing(folder)
    full = pv.render("loan_application", seed=1)   # 모든 쪽이 필요하면 마저 그린다
    assert all((tmp_path / p).exists() for p in full["images"]) and not (folder / "pending.json").exists()
    again = pv.render("loan_application", seed=2, first=True)
    import time

    for _ in range(100):
        if not pv.finishing(tmp_path / Path(again["images"][0]).parent):
            break
        time.sleep(0.02)
    assert not (tmp_path / Path(again["images"][0]).parent / "pending.json").exists()   # 줄이 없으면 끝까지
    pv.close()
