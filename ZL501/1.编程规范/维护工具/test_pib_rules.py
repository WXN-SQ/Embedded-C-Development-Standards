"""Focused PIB checks without optional format-validation dependencies."""

import importlib.util
from pathlib import Path
import tempfile
import unittest


TOOL = Path(__file__).with_name("coding_rules.py")
loader = importlib.util.spec_from_file_location("coding_rules", TOOL)
rules = importlib.util.module_from_spec(loader)
loader.loader.exec_module(rules)


class PIBChecks(unittest.TestCase):
    def test_single_marker_and_registry(self):
        with tempfile.TemporaryDirectory(prefix="pib-test-", dir=TOOL.parent) as folder:
            source = Path(folder) / "motion.c"
            registry = Path(folder) / "motion.md"
            source.write_text(
                "/* PIB: PIB-MOTION-001\n"
                " * Related modules: COMM, STATE\n"
                " * Content: Integrate the confirmed state interfaces.\n"
                " */\n", encoding="utf-8")
            registry.write_text(
                "| PIB-MOTION-001 | motion.c | MOTION | COMM, STATE | Work | "
                "Unavailable | Return not ready | Interfaces frozen | Owner | Open |\n",
                encoding="utf-8")
            self.assertEqual(rules.pib_errors([source], [registry]), [])
            registry.write_text(registry.read_text(encoding="utf-8").replace("Open", "Closed"),
                                encoding="utf-8")
            self.assertTrue(any("Closed" in item for item in rules.pib_errors([source], [registry])))

    def test_range_pair_and_fields(self):
        with tempfile.TemporaryDirectory(prefix="pib-test-", dir=TOOL.parent) as folder:
            source = Path(folder) / "motion.c"
            registry = Path(folder) / "motion.md"
            source.write_text("/* PIB-BEGIN: PIB-MOTION-002 */\n", encoding="utf-8")
            registry.write_text("| PIB-MOTION-002 | motion.c | MOTION | COMM | Work | X | X | X | X | Open |\n",
                                encoding="utf-8")
            errors = rules.pib_errors([source], [registry])
            self.assertTrue(any("PIB-END" in item for item in errors))
            self.assertTrue(any("Related modules" in item for item in errors))

    def test_duplicate_registry_and_orphan_open_item(self):
        with tempfile.TemporaryDirectory(prefix="pib-test-", dir=TOOL.parent) as folder:
            first = Path(folder) / "first.md"
            second = Path(folder) / "second.md"
            row = "| PIB-MOTION-003 | motion.c | MOTION | COMM | Work | X | X | X | X | Open |\n"
            first.write_text(row, encoding="utf-8")
            second.write_text(row, encoding="utf-8")
            errors = rules.pib_errors([], [first, second])
            self.assertTrue(any("registry entry is not unique" in item for item in errors))
            self.assertTrue(any("open registry item has no source marker" in item for item in errors))

    def test_empty_code_does_not_create_pib(self):
        with tempfile.TemporaryDirectory(prefix="pib-test-", dir=TOOL.parent) as folder:
            source = Path(folder) / "empty.c"
            source.write_text("void motion_wait(void) { }\n", encoding="utf-8")
            self.assertEqual(rules.pib_errors([source], []), [])


if __name__ == "__main__":
    unittest.main()
