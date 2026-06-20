import json
from pathlib import Path

from app.models import ProcessingReport


def write_json_file(path: str, data: dict) -> str:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(output_path)


def write_text_file(path: str, data: str) -> str:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(data, encoding="utf-8")
    return str(output_path)


def write_processing_report(report: ProcessingReport) -> str:
    return write_json_file("output/processing_report.json", report.to_dict())
