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
