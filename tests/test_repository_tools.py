"""Repository plumbing tests; these do not run an LLM or grade research reasoning."""
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from package_skill import package
from validate_repository import SKILL_NAME, public_files, validate


class RepositoryToolsTests(unittest.TestCase):
    def setUp(self):
        scratch = (ROOT / "work" / "tests").resolve()
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="repo-test-", dir=scratch)
        if not Path(self.temp.name).resolve().is_relative_to(scratch):
            raise RuntimeError("Test directory escaped the intended workspace")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "source"
        for file in public_files(ROOT):
            target = self.root / file.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(file, target)

    def test_clean_package_contains_all_public_files_and_github_config(self):
        self.assertEqual(validate(self.root), [])
        output = self.root / "dist" / "package.zip"
        count = package(self.root, output)
        with zipfile.ZipFile(output) as archive:
            expected = {SKILL_NAME + "/" + p.relative_to(self.root).as_posix() for p in public_files(self.root)}
            self.assertEqual(set(archive.namelist()), expected)
            self.assertEqual(len(archive.namelist()), count)
            self.assertIn(SKILL_NAME + "/.github/workflows/ci.yml", archive.namelist())
            for file in public_files(self.root):
                self.assertEqual(archive.read(SKILL_NAME + "/" + file.relative_to(self.root).as_posix()), file.read_bytes())

    def test_local_research_and_cache_directories_are_excluded(self):
        for folder in ("work", "inputs", "outputs", "private", "__pycache__", ".venv"):
            path = self.root / folder / "private-notes.txt"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Synthetic private fixture. Must never enter the ZIP.", encoding="utf-8")
        output = self.root / "dist" / "package.zip"
        package(self.root, output)
        with zipfile.ZipFile(output) as archive:
            self.assertFalse(any("private-notes.txt" in name for name in archive.namelist()))

    def test_broken_reference_is_detected_and_blocks_packaging(self):
        skill = self.root / "SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "\n[Broken](references/missing.md)\n", encoding="utf-8")
        self.assertTrue(any("Broken local link" in issue for issue in validate(self.root)))
        with self.assertRaises(ValueError):
            package(self.root, self.root / "dist" / "package.zip")

    def test_unfinished_skill_and_wrong_invocation_are_detected(self):
        skill = self.root / "SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "\n[TODO: fill instructions]\n", encoding="utf-8")
        ui = self.root / "agents" / "openai.yaml"
        ui.write_text(ui.read_text(encoding="utf-8").replace("$" + SKILL_NAME, "$wrong-skill"), encoding="utf-8")
        issues = validate(self.root)
        self.assertTrue(any("unfinished scaffold" in issue for issue in issues))
        self.assertTrue(any("Default prompt" in issue for issue in issues))

    def test_environment_file_outside_ignored_dirs_blocks_package(self):
        (self.root / ".env").write_text("DUMMY_SETTING=synthetic-test-only\n", encoding="utf-8")
        output = self.root / "dist" / "package.zip"
        with self.assertRaises(ValueError):
            package(self.root, output)
        self.assertFalse(output.exists())

    def test_parent_relative_archive_target_is_normalized(self):
        output = self.root / ".." / "parent-package.zip"
        package(self.root, output)
        actual = Path(self.temp.name) / "parent-package.zip"
        self.assertTrue(actual.is_file())
        with zipfile.ZipFile(actual) as archive:
            self.assertIn(SKILL_NAME + "/SKILL.md", archive.namelist())


if __name__ == "__main__":
    unittest.main()
