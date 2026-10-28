"""사내 OCR 어댑터. Studio와 학습 준비에서 같은 함수를 사용한다."""
import json
import mimetypes
import os
import uuid
from pathlib import Path
from urllib.request import Request, urlopen
# OCR API 서버 엔드포인트 설정
BASE_URL = os.getenv("INTERNAL_OCR_BASE_URL", "http://localhost:30107")

# 주요 엔드포인트
HEALTH_URL = f"{BASE_URL}/health"
STATS_URL = f"{BASE_URL}/stats"
OCR_URL = f"{BASE_URL}/ocr"
OCR_JSON_URL = f"{BASE_URL}/api/v1/ocr"
CHAT_URL = f"{BASE_URL}/v1/chat/completions"
def ocr_from_file(image_path: str, *, base_url: str | None = None) -> dict:
    """
    이미지 파일을 OCR API 로 전송

    Args:
        image_path: OCR 을 수행할 이미지 파일 경로

    Returns:
        OCR 결과 딕셔너리
    """
    image = Path(image_path)
    boundary = uuid.uuid4().hex
    mime = mimetypes.guess_type(image.name)[0] or "image/png"
    # 캐시 파일은 보통 픽셀 해시 이름이다. 원본 이름의 헤더 문자도 제거한다.
    filename = image.name.replace('"', '_').replace('\r', '_').replace('\n', '_')
    header = (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{filename}"\r\n'
              f'Content-Type: {mime}\r\n\r\n').encode("utf-8")
    body = header + image.read_bytes() + f'\r\n--{boundary}--\r\n'.encode()
    endpoint = (base_url or os.getenv("INTERNAL_OCR_BASE_URL", BASE_URL)).rstrip("/") + "/ocr"
    req = Request(endpoint, data=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urlopen(req, timeout=300) as response:
        return json.loads(response.read())
