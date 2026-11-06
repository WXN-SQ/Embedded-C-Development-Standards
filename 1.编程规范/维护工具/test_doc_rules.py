"""Focused regression tests for complete-example function documentation checks."""

import importlib.util
from pathlib import Path
import tempfile
import unittest


TOOL = Path(__file__).with_name("coding_rules.py")
loader = importlib.util.spec_from_file_location("coding_rules", TOOL)
rules = importlib.util.module_from_spec(loader)
loader.loader.exec_module(rules)


class FunctionDocTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="doc-check-", dir=TOOL.parent)
        root = Path(self.temp.name)
        self.source = root / "sample.c"
        self.header = root / "sample.h"
        self.module = root / "sample.md"
        self.source.write_text(
            "/**\n * @brief Adds one.\n * @details Uses integer addition.\n"
            " * @param[in] value Input value.\n * @return Increased value.\n"
            " * @author Test Author\n * @date 2026-11-06\n"
            " * @par Change Log\n * - 2026-11-06 | Test Author | Created example.\n"
            " */\nint sample_addOne(int value)\n{\n    return value + 1;\n}\n",
            encoding="utf-8",
        )
        self.header.write_text("int sample_addOne(int value);\n", encoding="utf-8")
        fields = "\n".join(f"| {field} | Reviewed |" for field in rules.EXTENDED_FIELDS)
        self.module.write_text(
            "### 1.1 `sample_addOne`\n\n| 字段 | 内容 |\n| --- | --- |\n"
            + fields + "\n", encoding="utf-8",
        )

    def tearDown(self):
        self.temp.cleanup()

    def errors(self):
        return rules.function_doc_errors(self.source, self.header, self.module)

    def test_valid_structure(self):
        self.assertEqual(self.errors(), [])

    def test_rejects_old_fields_and_header_contract(self):
        text = self.source.read_text(encoding="utf-8").replace(
            " * @details Uses integer addition.", " * @category Atomic Function."
        )
        self.source.write_text(text, encoding="utf-8")
        self.header.write_text("/** @brief Old contract. */\nint sample_addOne(int value);\n", encoding="utf-8")
        errors = self.errors()
        self.assertTrue(any("unapproved" in error for error in errors))
        self.assertTrue(any("header before declaration" in error for error in errors))

    def test_rejects_missing_change_log_and_module_field(self):
        self.source.write_text(
            self.source.read_text(encoding="utf-8").replace(" * @par Change Log\n", ""),
            encoding="utf-8",
        )
        self.module.write_text(
            self.module.read_text(encoding="utf-8").replace("| 前置条件 | Reviewed |\n", ""),
            encoding="utf-8",
        )
        errors = self.errors()
        self.assertTrue(any("Change Log" in error for error in errors))
        self.assertTrue(any("前置条件" in error for error in errors))

    def test_zero_parameter_function_has_no_param_field(self):
        text = self.source.read_text(encoding="utf-8").replace(
            " * @param[in] value Input value.\n", ""
        ).replace("sample_addOne(int value)", "sample_addOne(void)")
        self.source.write_text(text, encoding="utf-8")
        self.assertEqual(self.errors(), [])
        self.source.write_text(
            text.replace(" * @return", " * @param[in] value No explicit parameters.\n * @return"),
            encoding="utf-8",
        )
        self.assertTrue(any("pseudo parameter" in error for error in self.errors()))


if __name__ == "__main__":
    unittest.main()
