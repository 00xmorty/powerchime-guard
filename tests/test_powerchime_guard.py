import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "powerchime-guard"
LOADER = SourceFileLoader("powerchime_guard", str(CLI))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
MODULE = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(MODULE)


class PowerChimeGuardTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(CLI), *args], capture_output=True, text=True, check=False
        )

    def test_normalize_preference(self):
        self.assertEqual(MODULE.normalize_preference(False), "disabled")
        self.assertEqual(MODULE.normalize_preference("1"), "enabled")
        self.assertEqual(MODULE.normalize_preference(None), "default")

    def test_json_fixture_is_read_only(self):
        result = self.run_cli("--input", str(ROOT / "tests/fixture.json"), "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["preference"], "default")
        self.assertFalse(payload["changed"])
        self.assertNotIn("plan", payload)

    def test_disable_plan_is_fixed_and_not_executed(self):
        result = self.run_cli(
            "--input", str(ROOT / "tests/fixture.json"), "--plan-disable"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            "defaults write com.apple.PowerChime ChimeOnAllHardware -bool false",
            result.stdout,
        )
        self.assertIn("PLAN ONLY", result.stdout)

    def test_restore_plan_deletes_only_one_key(self):
        result = self.run_cli(
            "--input", str(ROOT / "tests/fixture.json"), "--plan-restore"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            "defaults delete com.apple.PowerChime ChimeOnAllHardware", result.stdout
        )
        self.assertNotIn("rm ", result.stdout)

    def test_invalid_fixture_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text('{"preference":"maybe"}', encoding="utf-8")
            result = self.run_cli("--input", str(path))
        self.assertEqual(result.returncode, 2)
        self.assertIn("ERROR", result.stderr)


if __name__ == "__main__":
    unittest.main()
