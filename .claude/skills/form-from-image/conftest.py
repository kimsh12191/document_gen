"""test_draft.py 의 --draft 옵션 (검사할 초안 폴더)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def pytest_addoption(parser):
    parser.addoption("--draft", action="store", default=None, help="검사할 초안 폴더 (out/form_drafts/<ID>)")


@pytest.fixture
def draft(request):
    path = request.config.getoption("--draft")
    if not path:
        pytest.skip("--draft <초안 폴더> 가 없어서 건너뜀")
    return Path(path)
