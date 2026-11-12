"""Build a clean source ZIP. No research data, model API or external upload."""
import argparse
import zipfile
from pathlib import Path

from validate_repository import EXCLUDE_DIRS, ROOT, SKILL_NAME, canonical, public_files, validate


def package(root, output):
    root, output = canonical(root), canonical(output)
    if output.is_relative_to(root) and not any(p in EXCLUDE_DIRS for p in output.relative_to(root).parts[:-1]):
        raise ValueError("Place an archive outside public source files, for example under dist/")
    issues = validate(root)
    if issues:
        raise ValueError("Repository validation failed: " + "; ".join(issues))
    files = public_files(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file in files:
            archive.write(file, SKILL_NAME + "/" + file.relative_to(root).as_posix())
    return len(files)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, default=ROOT / "dist" / (SKILL_NAME + ".zip"))
    args = ap.parse_args()
    try:
        count = package(ROOT, args.output)
    except (ValueError, OSError, SyntaxError) as exc:
        print(f"ERROR: {exc}")
        return 2
    print(f"Packaged {count} public source files: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
