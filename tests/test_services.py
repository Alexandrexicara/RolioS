import tempfile
import unittest
from pathlib import Path

from rollos.core import RollCore
from rollos.display import RollDisplay
from rollos.storage import RollStorage


class RollServiceTests(unittest.TestCase):
    def test_core_persists_config_and_event(self):
        with tempfile.TemporaryDirectory() as folder:
            core = RollCore(folder)
            self.assertEqual(core.config.product_name, "RollOS")
            core.log_event("boot", {"source": "test"})
            self.assertTrue((Path(folder) / "events.jsonl").exists())
            self.assertIn('"boot"', (Path(folder) / "events.jsonl").read_text(encoding="utf-8"))

    def test_display_modes(self):
        display = RollDisplay()
        self.assertEqual(display.state_for(0.2).mode, "compact")
        self.assertEqual(display.state_for(0.9).mode, "expanded")
        self.assertEqual(display.state_for(0.9).columns, 2)

    def test_display_clamps_range(self):
        display = RollDisplay()
        self.assertEqual(display.state_for(2).expansion, 1.0)
        self.assertEqual(display.state_for(-1).expansion, 0.0)

    def test_storage_snapshot(self):
        with tempfile.TemporaryDirectory() as folder:
            snapshot = RollStorage().snapshot(folder)
            self.assertGreater(snapshot.total_bytes, 0)
            self.assertGreaterEqual(snapshot.free_bytes, 0)


if __name__ == "__main__":
    unittest.main()
