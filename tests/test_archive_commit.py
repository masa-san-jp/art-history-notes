from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from tools import agent_support


class ArchiveCommitTests(unittest.TestCase):
    def make_archive(self, marker: str = "a" * 40) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / ".archive-commit").write_text(marker + "\n", encoding="ascii")
        (root / "payload.txt").write_text("before\n", encoding="utf-8")
        return temporary, root

    def test_archive_commit_is_used_without_git(self) -> None:
        temporary, root = self.make_archive()
        self.addCleanup(temporary.cleanup)
        commit = agent_support.resolve_code_commit(root)
        self.assertEqual("a" * 40, commit)
        self.assertTrue(agent_support.is_immutable_archive(root))
        self.assertTrue(agent_support.revision_exists(commit, root))

    def test_archive_file_states_detect_mutations_without_git(self) -> None:
        temporary, root = self.make_archive()
        self.addCleanup(temporary.cleanup)
        baseline = agent_support.file_states(root)
        (root / "payload.txt").write_text("after\n", encoding="utf-8")
        (root / "new.txt").write_text("new\n", encoding="utf-8")
        current = agent_support.file_states(root, base_sha="a" * 40)
        changed = {
            path for path in set(baseline) | set(current)
            if baseline.get(path) != current.get(path)
        }
        self.assertEqual({"payload.txt", "new.txt"}, changed)

    def test_unsubstituted_or_missing_archive_commit_fails_closed(self) -> None:
        for marker in ("$Format:%H$", None):
            with self.subTest(marker=marker):
                temporary, root = self.make_archive(marker or "a" * 40)
                self.addCleanup(temporary.cleanup)
                if marker is None:
                    (root / ".archive-commit").unlink()
                with self.assertRaisesRegex(RuntimeError, "cannot resolve code commit"):
                    agent_support.resolve_code_commit(root)


if __name__ == "__main__":
    unittest.main()
