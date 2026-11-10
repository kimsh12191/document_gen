"""사용 가이드 화면의 문서 목록: 화면 쓰는 법만, 목록 밖 경로는 읽지 않는다."""
import pytest

from studio import guidebook as G


def test_document_allowlist():
    assert set(G.DOCUMENTS) == {"studio.md", "new-forms.md", "keys.md", "generators.md"}
    for name in G.DOCUMENTS:
        assert G.document(name).startswith("# ")
    for bad in ("training.md", "data.md", "../studio/config.json"):
        with pytest.raises(KeyError):
            G.document(bad)
