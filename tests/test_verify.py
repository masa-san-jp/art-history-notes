import contextlib
import io
import unittest
from unittest import mock

from tools import verify


class VerifySequenceTests(unittest.TestCase):
    def test_stops_at_first_failure_and_returns_exit_code(self):
        failed = mock.Mock(returncode=7)
        with mock.patch.object(verify.subprocess, "run", return_value=failed) as run:
            self.assertEqual(7, verify.main())
        self.assertEqual(1, run.call_count)

    def test_runs_all_steps_in_order_when_successful(self):
        successful = mock.Mock(returncode=0)
        with mock.patch.object(verify.subprocess, "run", return_value=successful) as run:
            self.assertEqual(0, verify.main())

        self.assertEqual(len(verify.steps()), run.call_count)
        commands = [call.args[0] for call in run.call_args_list]
        self.assertEqual(["tools/build_graph.py", "--check"], commands[0][1:])
        self.assertEqual(["tools/audit_source_migration.py", "--check-type", "movement", "--quiet"], commands[2][1:])
        self.assertEqual(["tools/audit_source_migration.py", "--check-type", "context", "--quiet"], commands[3][1:])
        self.assertEqual(["tools/audit_source_migration.py", "--check-type", "person", "--quiet"], commands[4][1:])
        self.assertEqual(["-m", "unittest", "discover", "-s", "tests", "-p", "test*.py"], commands[5][1:])
        self.assertEqual(["git", "diff", "--exit-code", "--", "data/", "overviews/coverage.md"], commands[-1])
        self.assertTrue(all(call.kwargs == {"cwd": verify.ROOT, "check": False}
                             for call in run.call_args_list))

    def test_start_failure_returns_one(self):
        stderr = io.StringIO()
        with mock.patch.object(verify.subprocess, "run", side_effect=OSError("missing")), \
                contextlib.redirect_stderr(stderr):
            self.assertEqual(1, verify.main())
        self.assertIn("command failed to start", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
