"""
Batch resume extraction.

Usage:
    python batch_resume.py --input data/ --output output/resumes/
"""

import argparse
import json
import traceback
from pathlib import Path

from src.graph.workflow import build_graph

SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def run(input_folder: str, output_folder: str):
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    files = sorted(f for f in input_path.iterdir() if f.suffix.lower() in SUPPORTED_EXTENSIONS)

    if not files:
        print(f"No PDF/DOCX files found in: {input_path.resolve()}")
        return

    print(f"Input  : {input_path.resolve()}")
    print(f"Output : {output_path.resolve()}")
    print(f"Files  : {len(files)}")
    print("-" * 60)

    graph = build_graph()
    passed, failed, errored = 0, 0, 0

    for i, file in enumerate(files, 1):
        output_file = output_path / f"{file.stem}.json"
        print(f"[{i:>3}/{len(files)}] {file.name:<50}", end="", flush=True)

        try:
            result = graph.invoke({
                "mode": "resume_only",
                "reflection_loop": 0,
                "resume_file_path": str(file),
                "jd_file_path": None,
                "resume_markdown": None,
                "jd_markdown": None,
                "resume_data": None,
                "jd_data": None,
                "judge_results": [],
            })

            output = {
                "resume_data": result["resume_data"].model_dump(),
                "judge_results": result.get("judge_results", []),
                "reflection_loop": result.get("reflection_loop", 0),
            }

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=4, ensure_ascii=False)

            grades = [jr["grade"].upper() for jr in output["judge_results"]]
            verdict = "PASS" if grades and all(g == "PASS" for g in grades) else "FAIL"
            retried = output["reflection_loop"] > 1
            print(f"  {verdict}" + (" (retried)" if retried else ""))

            if verdict == "PASS":
                passed += 1
            else:
                failed += 1

        except Exception as e:
            print(f"  ERROR: {e}")
            with open(output_path / f"{file.stem}.error.json", "w", encoding="utf-8") as f:
                json.dump({"file": str(file), "error": str(e), "traceback": traceback.format_exc()}, f, indent=4)
            errored += 1

    print("-" * 60)
    print(f"Total: {len(files)}  |  PASS: {passed}  |  FAIL: {failed}  |  ERROR: {errored}")
    print(f"Output saved to: {output_path.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch resume extraction.")
    parser.add_argument("--input", required=True, help="Folder containing resume PDFs/DOCXs")
    parser.add_argument("--output", required=True, help="Folder to save extracted JSON results")
    args = parser.parse_args()

    run(args.input, args.output)
