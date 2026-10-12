# 필요한 라이브러리 임포트
import requests
import base64
import json
from PIL import Image
import matplotlib.pyplot as plt
import io
import os
# OCR API 서버 엔드포인트 설정
BASE_URL = os.getenv("INTERNAL_OCR_BASE_URL", "http://localhost:30107")

# 주요 엔드포인트
HEALTH_URL = f"{BASE_URL}/health"
STATS_URL = f"{BASE_URL}/stats"
OCR_URL = f"{BASE_URL}/ocr"
OCR_JSON_URL = f"{BASE_URL}/api/v1/ocr"
CHAT_URL = f"{BASE_URL}/v1/chat/completions"
def ocr_from_file(image_path: str) -> dict:
    """
    이미지 파일을 OCR API 로 전송

    Args:
        image_path: OCR 을 수행할 이미지 파일 경로

    Returns:
        OCR 결과 딕셔너리
    """
    with open(image_path, 'rb') as f:
        files = {'file': (image_path.split('/')[-1], f, 'image/png')}
        response = requests.post(OCR_URL, files=files)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
