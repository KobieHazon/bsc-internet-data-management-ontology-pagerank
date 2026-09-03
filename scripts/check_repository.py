#!/usr/bin/env python3
from pathlib import Path
import ast
import sys

ROOT = Path(__file__).resolve().parents[1]
required_files = ['assignment/HW2_2018.pdf', 'question3a.py', 'question3b.py', 'football_ontology.py', 'ontology_queries.py', 'ontology.nt', 'question2c.txt', 'question3c.txt']
missing = [name for name in required_files if not (ROOT / name).exists()]
if missing:
    print("Missing required files: " + ", ".join(missing), file=sys.stderr)
    sys.exit(1)

for path in ROOT.rglob("*"):
    rel = path.relative_to(ROOT).as_posix()
    if any(part.startswith("._") for part in path.parts):
        print(f"Apple metadata file is tracked candidate: {rel}", file=sys.stderr)
        sys.exit(1)
    if path.suffix in {".pyc", ".zip", ".docx"}:
        print(f"Forbidden wrapper/generated artifact: {rel}", file=sys.stderr)
        sys.exit(1)

for path in ROOT.glob("*.py"):
    try:
        ast.parse(path.read_text(encoding="utf-8", errors="ignore"), filename=str(path))
    except SyntaxError as exc:
        print(f"Python syntax check failed in {path.name}: {exc}", file=sys.stderr)
        sys.exit(1)

text_files = [p for p in ROOT.rglob("*") if p.is_file() and p.suffix.lower() in {".py", ".md", ".csv", ".txt", ".xml", ".html", ".dtd", ".nt", ""}]
combined = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in text_files)
markers = ["".join(["208", "234", "161"]), "/" + "Users" + "/", "/" + "home" + "/"]
if any(marker in combined for marker in markers):
    print("Privacy or machine-path marker found in tracked text", file=sys.stderr)
    sys.exit(1)

required_markers = ['rdflib', 'crawler', 'pr_calculator', 'ontology_prefix']
missing_markers = [marker for marker in required_markers if marker not in combined]
if missing_markers:
    print("Missing expected project markers: " + ", ".join(missing_markers), file=sys.stderr)
    sys.exit(1)

print("Repository static checks passed.")
