"""Validate repository metadata and links, not an agent's scientific reasoning."""
import argparse
import ast
import os
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "grill-my-research-skill"
EXCLUDE_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", "work", "inputs", "outputs", "private", "dist", "build", ".idea", ".vscode"}
LOCAL_SUFFIXES = {".pyc", ".pyo", ".pdf", ".pptx", ".docx", ".xlsx", ".zip", ".pem", ".key", ".log"}


def canonical(path):
    # Normalize lexical parent segments even with filesystem providers whose
    # resolve() result retains them for nonexistent output files.
    return Path(os.path.normpath(str(Path(path).resolve())))


def public_files(root):
    root = canonical(root)
    files = []
    for folder, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDE_DIRS)
        for directory in dirs:
            if (Path(folder) / directory).is_symlink():
                raise ValueError("Do not distribute symbolic-link directories")
        for name in sorted(names):
            path = Path(folder) / name
            if path.is_symlink():
                raise ValueError(f"Do not distribute symbolic links: {path.relative_to(root)}")
            files.append(path)
    return sorted(files)


def yaml_data(text):
    try:
        import yaml
    except ImportError as exc:
        raise ValueError("Install development helpers: python -m pip install -r requirements-dev.txt") from exc
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML: {exc}") from exc


def validate(root=ROOT):
    root = canonical(root)
    issues = []
    required = ["SKILL.md", "README.md", "README.en.md", "LICENSE", "CONTRIBUTING.md", "CHANGELOG.md",
                ".gitignore", ".gitattributes", "requirements-dev.txt", "agents/openai.yaml",
                ".github/workflows/ci.yml", "evals/cases.yaml", "evals/README.md"]
    for name in required:
        if not (root / name).is_file():
            issues.append(f"Missing required repository file: {name}")
    if issues:
        return issues
    skill = (root / "SKILL.md").read_text(encoding="utf-8-sig")
    match = re.match(r"\A---\n(.*?)\n---\n", skill, re.S)
    if not match:
        return ["SKILL.md must begin with YAML frontmatter"]
    metadata = yaml_data(match.group(1))
    if not isinstance(metadata, dict) or metadata.get("name") != SKILL_NAME or not metadata.get("description"):
        issues.append("Skill name or description is invalid")
    if re.search(r"(?m)^\[TODO:[^\n]*\]\s*$", skill):
        issues.append("SKILL.md contains an unfinished scaffold")
    ui = yaml_data((root / "agents/openai.yaml").read_text(encoding="utf-8-sig"))
    interface = ui.get("interface", {}) if isinstance(ui, dict) else {}
    if "$" + SKILL_NAME not in str(interface.get("default_prompt", "")):
        issues.append("Default prompt must explicitly invoke $" + SKILL_NAME)
    if not 25 <= len(str(interface.get("short_description", ""))) <= 64:
        issues.append("UI short description must have 25–64 characters")
    cases = yaml_data((root / "evals/cases.yaml").read_text(encoding="utf-8-sig"))
    entries = cases.get("cases", []) if isinstance(cases, dict) else []
    if not entries:
        issues.append("Behavioral cases must not be empty")
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict) or not all(entry.get(k) for k in ("id", "mode", "input", "accept", "fail")):
            issues.append("Every evaluation case needs id, mode, input, acceptance and failure criteria")
            continue
        if entry["id"] in seen:
            issues.append("Duplicate evaluation case: " + entry["id"])
        seen.add(entry["id"])
        if not isinstance(entry["accept"], list) or not isinstance(entry["fail"], list):
            issues.append("Evaluation acceptance/failure criteria must be lists")
    for file in public_files(root):
        relative = file.relative_to(root)
        if file.name.startswith(".env") or file.suffix.lower() in LOCAL_SUFFIXES:
            issues.append(f"Local/private/generated file must not enter source package: {relative}")
            continue
        if file.suffix == ".py":
            ast.parse(file.read_text(encoding="utf-8-sig"), filename=str(relative))
        if file.suffix in (".yaml", ".yml"):
            yaml_data(file.read_text(encoding="utf-8-sig"))
        if file.suffix == ".md":
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", file.read_text(encoding="utf-8-sig")):
                target = target.split(' "', 1)[0].strip("<>")
                url = urlsplit(target)
                if url.scheme or target.startswith("#"):
                    continue
                if not (file.parent / unquote(url.path)).exists():
                    issues.append(f"Broken local link in {relative}: {target}")
    return issues


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    args = ap.parse_args()
    try:
        issues = validate(args.root)
    except (ValueError, OSError, SyntaxError) as exc:
        print(f"ERROR: {exc}")
        return 2
    print("\n".join(issues) if issues else "PASS: metadata, syntax, local links, evaluation-case structure and public file scope")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
