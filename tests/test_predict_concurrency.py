import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch
from bank_ocr.data import write_jsonl, read_jsonl
from bank_ocr.inference import predict

class ConcurrentPredictTests(unittest.TestCase):
    def test_parallel_cache_and_resume(self):
        barrier = threading.Barrier(2)
        def respond(request, timeout):
            barrier.wait(timeout=5)
            class Response:
                def __enter__(self): return self
                def __exit__(self, *args): pass
                def read(self):
                    return json.dumps({"choices": [{"message": {"content": "ok"}, "finish_reason": "stop"}]}).encode()
            return Response()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            image = root / "page.png"
            image.write_bytes(b"image")
            tasks = root / "tasks.jsonl"
            output = root / "predictions.jsonl"
            write_jsonl(tasks, [{"id": str(i), "messages": [{"content": "<image>read"}], "images": [str(image)]} for i in range(4)])
            with patch("bank_ocr.inference.urlopen", side_effect=respond) as http, patch("bank_ocr.inference.base64.b64encode", wraps=__import__("base64").b64encode) as encode:
                predict(tasks, output, "http://localhost:8000/v1", "model", "run", concurrency=2)
                self.assertEqual(http.call_count, 4)
                self.assertEqual(encode.call_count, 1)
                self.assertEqual({r["id"] for r in read_jsonl(output)}, {"0", "1", "2", "3"})
                predict(tasks, output, "http://localhost:8000/v1", "model", "run", concurrency=1)
                self.assertEqual(http.call_count, 4)
    def test_invalid_concurrency(self):
        for value in (0, -1, True, 1.5):
            with self.assertRaisesRegex(ValueError, "concurrency"):
                predict("missing", "missing", "http://localhost", "model", "run", concurrency=value)
