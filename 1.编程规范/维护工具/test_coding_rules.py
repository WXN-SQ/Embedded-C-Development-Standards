"""Regression checks for configuration behavior and release binding failures."""

import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "1.编程规范/维护工具"
loader = importlib.util.spec_from_file_location("coding_rules", TOOL_DIR / "coding_rules.py")
rules = importlib.util.module_from_spec(loader)
loader.loader.exec_module(rules)
sys.path.insert(0, str(ROOT / ".tools/format-validation"))
import editorconfig


class BundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text, cls.version, cls.profile = rules.document()
        cls.clang = rules.clang_tool(None, cls.profile)
        cls.temp = tempfile.TemporaryDirectory(prefix="rule-check-", dir=TOOL_DIR)
        cls.scratch = Path(cls.temp.name)
        cls.config = cls.scratch / ".clang-format"
        cls.config.write_bytes(rules.rendered(cls.text, cls.version, cls.profile)[".clang-format"].encode())

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def formatted(self, text, filename="probe.c"):
        return subprocess.run(
            [self.clang, "--style=file:" + str(self.config), "--assume-filename=" + filename],
            input=text.encode(), check=True, capture_output=True,
        ).stdout.decode()

    def test_allman_macro_pointer_and_cast_sample(self):
        source = (TOOL_DIR / "probe.input.txt").read_text(encoding="utf-8")
        expected = (TOOL_DIR / "probe.expected.txt").read_text(encoding="utf-8")
        actual = self.formatted(source)
        self.assertEqual(actual, expected)  # Expected output was independently reviewed.
        self.assertEqual(self.formatted(actual), actual)
        self.assertIn("int *ptr;", actual)
        self.assertIn("return (int) first;", actual)
        self.assertIn("    }\n    while (first > 0U);", actual)
        self.assertIn("void SRV_empty(void)\n{\n}\n", actual)
        self.assertIn("#include <stdint.h>\n#include <string.h>", actual)

    def test_long_arguments_binary_breaks_and_initializer(self):
        first = "first_argument_with_a_long_descriptive_name"
        second = "second_argument_with_a_long_descriptive_name"
        third = "third_argument_with_a_long_descriptive_name"
        source = (
            f"void SRV_call(unsigned int {first}, unsigned int {second}, unsigned int {third});\n"
            "void SRV_probe(void) {\n"
            f"    unsigned int result = {first} + {second} + {third};\n"
            "    SRV_Obj candidate = { .first = 1U, .second = 2U, .third = 3U, };\n"
            "}\n"
        )
        actual = self.formatted(source)
        self.assertRegex(actual, r"\n    unsigned int " + second)
        self.assertRegex(actual, r"\n        [+=] ")
        self.assertIn(".first = 1U,\n", actual)
        self.assertIn(".second = 2U,\n", actual)
        self.assertEqual(self.formatted(actual), actual)
        self.assertTrue(all(len(line) <= 100 for line in actual.splitlines()))

    def test_preprocessor_data_comments_and_no_brace_insertion(self):
        source = (
            "/**\n * @brief Preserve the documented contract.\n * @param[in] input value.\n */\n"
            "#if defined(SRV_FEATURE)\n"
            "const char *label = \"do not alter this string\\t\";\n"
            "#endif // SRV_FEATURE\n"
            "void SRV_probe(unsigned int value) { if(value) return; }\n"
        )
        actual = self.formatted(source)
        self.assertIn("/**\n * @brief Preserve the documented contract.\n * @param[in] input value.\n */", actual)
        self.assertIn('"do not alter this string\\t"', actual)
        self.assertIn("#if defined(SRV_FEATURE)", actual)
        self.assertIn("#endif // SRV_FEATURE", actual)
        self.assertRegex(actual, r"if \(value\)\n        return;")
        self.assertEqual(self.formatted(actual), actual)

    def test_complete_chapter18_files_are_stable(self):
        section = self.text.split("## 18 综合模块封装示例", 1)[1].split("## 19 附录与版本管理", 1)[0]
        blocks = re.findall(r"```c\n(.*?)\n```", section, re.S)
        self.assertEqual(len(blocks), 5)
        # 18.6 prelude, then 18.4 lifecycle, then 18.5 update implementation.
        implementation = "\n\n".join([blocks[3], blocks[1], blocks[2]]) + "\n"
        for filename, code in [("motangcomp.h", blocks[0] + "\n"),
                               ("motangcomp.c", implementation),
                               ("test_motangcomp.c", blocks[4] + "\n")]:
            with self.subTest(filename=filename):
                actual = self.formatted(code, filename)
                self.assertEqual(actual, code)
                self.assertEqual(rules.source_errors(filename, actual.encode()), [])

    def test_unicode_width_and_file_bytes(self):
        accepted = ("//" + "中" * 98 + "\n").encode()
        self.assertEqual(rules.source_errors("sample.c", accepted), [])
        rejected = ("//" + "中" * 99 + "\n").encode()
        self.assertTrue(any("EPR-FMT-006" in item for item in rules.source_errors("sample.c", rejected)))
        for raw, expected in [
            (b"\xef\xbb\xbfint value;\n", "010"), (b"\xff\n", "010"),
            (b"int value;\r\n", "011"), (b"int value; \n", "012"),
            (b"int value;\n\n", "013"), (b"int value;", "013"),
            (b"", "013"), (b"\tint value;\n", "001"),
        ]:
            with self.subTest(raw=raw):
                self.assertTrue(any("EPR-FMT-" + expected in item for item in rules.source_errors("sample.c", raw)))

    def test_editorconfig_matching_and_non_c_scope(self):
        editor_root = self.scratch / "editor"
        editor_root.mkdir(exist_ok=True)
        config = rules.rendered(self.text, self.version, self.profile)[".editorconfig"]
        (editor_root / ".editorconfig").write_bytes(config.encode())
        expected = self.profile["editorconfig"]["properties"]
        for filename in ["sample.c", "sample.h", "src/nested/sample.c", "tests/sample.h"]:
            self.assertEqual(editorconfig.get_properties(str(editor_root / filename)), expected)
        for filename in ["README.md", "helper.py", "src/sample.cpp"]:
            self.assertEqual(editorconfig.get_properties(str(editor_root / filename)), {})
        # The core reports unset; supporting editor plugins remove those effects.
        for filename in [".tools/sample.c", ".tools/a/sample.h"]:
            self.assertEqual(editorconfig.get_properties(str(editor_root / filename)),
                             {key: "unset" for key in expected})

    def cloned_release(self, label):
        clone = self.scratch / label
        (clone / rules.TOOL_DIR).mkdir(parents=True)
        (clone / rules.SPEC.parent).mkdir(parents=True, exist_ok=True)
        shutil.copyfile(TOOL_DIR / "coding_rules.py", clone / rules.TOOL_DIR / "coding_rules.py")
        text = self.text
        text = re.sub(r"^- 正式版本：\S+$", "- 正式版本：1.0.0", text, flags=re.M)
        begin, rest = text.split(rules.LOG_BEGIN, 1)
        log, end = rest.split(rules.LOG_END, 1)
        log = "\n".join(line for line in log.splitlines() if not re.match(r"\| \d+\.\d+\.\d+ \|", line)) + "\n"
        (clone / rules.SPEC).write_bytes((begin + rules.LOG_BEGIN + log + rules.LOG_END + end).encode())
        result = self.command(clone, "sync", "--kind", "initial", "--change", "initial test fixture",
                              "--rules", "ALL", "--profile-reviewed", "test fixture review")
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        return clone

    def command(self, clone, *args):
        arguments = [sys.executable, str(clone / rules.TOOL_DIR / "coding_rules.py"), *args]
        if args[0] == "sync":
            arguments.extend(["--clang-format", self.clang])
        return subprocess.run(arguments, capture_output=True)

    def test_stale_spec_and_manually_modified_config_fail(self):
        clone = self.cloned_release("tampering")
        self.assertEqual(self.command(clone, "check").returncode, 0)
        spec_path = clone / rules.SPEC
        original = spec_path.read_bytes()
        spec_path.write_bytes(original + b"\n")
        self.assertNotEqual(self.command(clone, "check").returncode, 0)
        spec_path.write_bytes(original)
        config = clone / ".clang-format"
        config.write_bytes(config.read_bytes().replace(b'ColumnLimit: 100', b'ColumnLimit: 80'))
        self.assertNotEqual(self.command(clone, "check").returncode, 0)

    def test_patch_minor_major_regenerate_both_configs(self):
        clone = self.cloned_release("upgrades")
        for kind, expected in [("patch", "1.0.1"), ("minor", "1.1.0"), ("major", "2.0.0")]:
            spec_path = clone / rules.SPEC
            spec_path.write_bytes(spec_path.read_bytes() + ("\n<!-- " + kind + " fixture edit -->\n").encode())
            self.assertNotEqual(self.command(clone, "check").returncode, 0)
            result = self.command(clone, "sync", "--kind", kind, "--change", kind + " test fixture",
                                  "--rules", "EPR-GOV-012", "--profile-reviewed", "test fixture review")
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            self.assertEqual(self.command(clone, "check").returncode, 0)
            for filename in [".clang-format", ".editorconfig"]:
                self.assertIn("# Normative-Version: " + expected,
                              (clone / filename).read_text(encoding="utf-8"))
            manifest = json.loads((clone / rules.MANIFEST).read_text(encoding="utf-8"))
            self.assertEqual(manifest["normative_version"], expected)
        self.assertEqual(len(manifest["releases"]), 4)

    def test_invalid_profile_does_not_change_published_bundle(self):
        clone = self.cloned_release("invalid-option")
        spec_path = clone / rules.SPEC
        edited = spec_path.read_text(encoding="utf-8").replace('"IndentWidth": 4,', '"UnknownFormatOptionForTest": true,\n    "IndentWidth": 4,')
        spec_path.write_bytes(edited.encode())
        paths = [rules.SPEC, rules.MANIFEST, Path(".clang-format"), Path(".editorconfig")]
        before = {path: (clone / path).read_bytes() for path in paths}
        result = self.command(clone, "sync", "--kind", "patch", "--change", "invalid fixture",
                              "--rules", "ALL", "--profile-reviewed", "test fixture review")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(before, {path: (clone / path).read_bytes() for path in paths})


if __name__ == "__main__":
    unittest.main(verbosity=2)
