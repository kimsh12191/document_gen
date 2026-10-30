"""Convert per-document image/qa JSON files to ms-swift JSONL (stdlib only)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def records(document: dict, image_root: Path | None = None):
    if not isinstance(document, dict):
        raise ValueError("document must be a JSON object")
    image, qa = document.get("image"), document.get("qa")
    if not isinstance(image, str) or not image.strip():
        raise ValueError("image must be a nonempty path string")
    if not isinstance(qa, list) or not qa:
        raise ValueError("qa must be a nonempty list")
    if image_root is not None:
        image = str((image_root / image).resolve())
    for index, pair in enumerate(qa, 1):
        if not isinstance(pair, dict) or "answer" not in pair:
            raise ValueError(f"qa[{index}]: question and answer are required")
        question = pair.get("question")
        if not isinstance(question, str) or not question.strip():
            raise ValueError(f"qa[{index}]: question must be a nonempty string")
        tags = question.count("<image>")
        if tags > 1:
            raise ValueError(f"qa[{index}]: only one <image> is allowed")
        answer = pair["answer"]
        if not isinstance(answer, str):
            answer = json.dumps(answer, ensure_ascii=False, allow_nan=False)
        yield {
            "messages": [
                {"role": "user", "content": question if tags else "<image>" + question},
                {"role": "assistant", "content": answer},
            ],
            "images": [image],
        }


def convert(source: Path, output: Path, *, image_root: Path | None = None,
            recursive: bool = False, check_images: bool = False) -> tuple[int, int]:
    source, output = Path(source), Path(output)
    if not source.is_dir():
        raise ValueError(f"input folder does not exist: {source}")
    if output.suffix.lower() != ".jsonl":
        raise ValueError("output must use the .jsonl extension")
    files = sorted(source.rglob("*.json") if recursive else source.glob("*.json"))
    if not files:
        raise ValueError(f"no .json files in {source}")
    count = 0
    # Exclusive creation prevents accidental overwrites, including concurrent runs.
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        try:
            for path in files:
                try:
                    document = json.loads(path.read_text(encoding="utf-8-sig"))
                    for record in records(document, image_root):
                        if check_images:
                            image = Path(record["images"][0])
                            if not image.is_absolute():
                                image = output.parent / image
                            if not image.is_file():
                                raise ValueError(f"image does not exist: {image}")
                        stream.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
                        count += 1
                except (ValueError, OSError) as exc:
                    raise ValueError(f"{path}: {exc}") from exc
        except BaseException:
            # Remove only this run's incomplete output; preserve all source files.
            stream.close()
            output.unlink()
            raise
    return len(files), count


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="folder containing image/qa JSON files")
    parser.add_argument("output", type=Path, help="new output .jsonl file (must not exist)")
    parser.add_argument("--image-root", type=Path,
                        help="base folder to resolve relative image paths against")
    parser.add_argument("--recursive", action="store_true", help="include subfolders")
    parser.add_argument("--check-images", action="store_true", help="require image files to exist")
    args = parser.parse_args(argv)
    try:
        documents, samples = convert(args.source, args.output, image_root=args.image_root,
                                     recursive=args.recursive, check_images=args.check_images)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    print(f"Converted {documents} documents -> {samples} samples: {args.output}")


if __name__ == "__main__":
    main()
