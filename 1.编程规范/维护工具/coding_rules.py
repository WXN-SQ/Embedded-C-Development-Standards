"""Generate and verify the version-bound coding-rule configuration bundle.

The normative document owns the JSON tool profile. This program does not infer
formatting requirements from natural language or certify semantic compliance.
"""

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
SPEC = Path("1.编程规范/嵌入式编程规则手册.md")
MANIFEST = Path("1.编程规范/编程规则版本绑定.json")
TOOL_DIR = Path("1.编程规范/维护工具")
PARAMETERIZED_TEMPLATE_DIR = Path("2.开发指导/模板")
PROFILE_BEGIN = "<!-- EPR-TOOL-PROFILE-BEGIN -->"
PROFILE_END = "<!-- EPR-TOOL-PROFILE-END -->"
LOG_BEGIN = "<!-- EPR-CHANGELOG-BEGIN -->"
LOG_END = "<!-- EPR-CHANGELOG-END -->"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write(path, text):
    (ROOT / path).write_bytes(text.encode("utf-8"))


def version_tuple(version):
    if not re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)", version):
        raise ValueError("版本号必须为主版本.次版本.修订版本")
    return tuple(map(int, version.split(".")))


def document():
    text = (ROOT / SPEC).read_bytes().decode("utf-8")
    matches = re.findall(r"^- 正式版本：(\S+)$", text, re.M)
    if len(matches) != 1:
        raise ValueError("正式版本元数据必须唯一")
    version_tuple(matches[0])
    if "- 文档状态：正式发布" not in text:
        raise ValueError("只有正式发布文档可同步配置")
    pattern = re.escape(PROFILE_BEGIN) + r"\s*```json\n(.*?)\n```\s*" + re.escape(PROFILE_END)
    profiles = re.findall(pattern, text, re.S)
    if len(profiles) != 1:
        raise ValueError("工具配置JSON基线必须唯一并带有规定标记")
    profile = json.loads(profiles[0])
    if profile["schema_version"] != 1:
        raise ValueError("不支持的工具配置基线格式")
    ids = re.findall(r"^#### (EPR-[A-Z]+-\d{3}) ", text, re.M)
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("规则编号缺失或重复")
    fields = ["约束等级", "适用范围", "检查方式", "工具映射", "依据", "偏离条件"]
    sections = ["规则正文", "理由", "正例", "反例", "检查判据"]
    for match in re.finditer(r"^#### (EPR-[A-Z]+-\d{3}) .*?\n(.*?)(?=^#### |^## |\Z)", text, re.M | re.S):
        body = match[2]
        actual_fields = re.findall(r"^- (" + "|".join(fields) + r")：", body, re.M)
        actual_sections = re.findall(r"^##### (.+)$", body, re.M)
        level = re.search(r"^- 约束等级：(\w+)$", body, re.M)
        if actual_fields != fields or actual_sections != sections or not level or level[1] not in ("REQUIRED", "RECOMMENDED", "OPTIONAL"):
            raise ValueError("规则结构或等级无效：" + match[1])
        if any(verdict + "：" not in body for verdict in ["符合", "违规", "不适用", "无法判断"]):
            raise ValueError("规则检查判据缺失：" + match[1])
    referenced = set(re.findall(r"EPR-[A-Z]+-\d{3}", text))
    if referenced - set(ids):
        raise ValueError("文档存在未定义规则编号")
    for group in profile["rule_groups"].values():
        if not set(group) <= set(ids):
            raise ValueError("工具映射存在未定义规则编号")
    for directory in profile["excluded_directories"]:
        candidate = Path(directory)
        if candidate.is_absolute() or ".." in candidate.parts or not candidate.parts:
            raise ValueError("排除目录必须为项目内相对目录")
    if text.count(LOG_BEGIN) != 1 or text.count(LOG_END) != 1:
        raise ValueError("正式变更记录标记缺失或重复")
    return text, matches[0], profile


def yaml_lines(value, indent=0):
    """Emit the JSON-compatible subset of YAML without a YAML dependency."""
    prefix = " " * indent
    lines = []
    for key, item in value.items():
        if isinstance(item, dict):
            lines.append(f"{prefix}{key}:")
            lines.extend(yaml_lines(item, indent + 2))
        elif isinstance(item, list):
            lines.append(f"{prefix}{key}:")
            for entry in item:
                lines.append(prefix + "  - " + json.dumps(entry, ensure_ascii=False))
        else:
            lines.append(f"{prefix}{key}: " + json.dumps(item, ensure_ascii=False))
    return lines


def rendered(text, version, profile):
    header = (
        "# Generated from the embedded coding rules; edit the document's tool profile.\n"
        f"# Normative-Version: {version}\n"
        f"# Normative-Source: {SPEC.as_posix()}\n"
        f"# Normative-SHA256: {digest(text.encode('utf-8'))}\n"
        f"# Binding-Manifest: {MANIFEST.as_posix()}\n"
    )
    clang = header + f"# clang-format baseline: {profile['clang_format_version']}\n"
    clang += "# Allman blocks are expressed as Custom to also wrap do/while.\n"
    clang += "# Scope: owned .c/.h files; use 1.编程规范/维护工具/coding_rules.py format-check.\n"
    clang += "# Rule mappings and supplemental checks: spec section 19.4.\n"
    clang += "---\n" + "\n".join(yaml_lines(profile["clang_format"])) + "\n"
    editor = header + "# This profile intentionally has no wildcard section for other file types.\n"
    editor += "root = true\n\n[" + profile["editorconfig"]["pattern"] + "]\n"
    editor += "\n".join(f"{key} = {value}" for key, value in profile["editorconfig"]["properties"].items()) + "\n"
    for directory in profile["excluded_directories"]:
        editor += "\n[" + Path(directory).as_posix().rstrip("/") + "/**.{c,h}]\n"
        editor += "\n".join(f"{key} = unset" for key in profile["editorconfig"]["properties"]) + "\n"
    return {".clang-format": clang, ".editorconfig": editor}


def clang_tool(argument, profile):
    local = ROOT / ".tools/format-validation/clang_format/data/bin/clang-format.exe"
    executable = argument or (str(local) if local.is_file() else shutil.which("clang-format"))
    if not executable:
        raise ValueError("未找到clang-format；请使用--clang-format指定工具路径")
    actual = subprocess.run([executable, "--version"], check=True, capture_output=True, text=True).stdout
    found = re.search(r"clang-format version (\d+\.\d+\.\d+)", actual)
    if not found or found[1] != profile["clang_format_version"]:
        raise ValueError("clang-format版本与文档工具基线不一致：" + actual.strip())
    return executable


def validate_config(executable, config):
    subprocess.run(
        [executable, "--style=file:" + str(config), "--assume-filename=probe.c", "--dump-config"],
        check=True, capture_output=True, text=True,
    )


def check():
    text, version, profile = document()
    manifest = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
    if manifest["schema_version"] != 1 or manifest["normative_version"] != version:
        raise ValueError("规范与绑定记录版本不一致")
    if manifest["source"] != SPEC.as_posix():
        raise ValueError("绑定记录规范路径不一致")
    for key in ["clang_format_version", "editorconfig_core_version"]:
        if manifest[key] != profile[key]:
            raise ValueError("绑定记录工具版本不一致：" + key)
    expected = rendered(text, version, profile)
    for path in [SPEC.as_posix(), *expected]:
        actual = (ROOT / path).read_bytes()
        if digest(actual) != manifest["artifacts"][path]["sha256"]:
            raise ValueError("文件摘要不一致，必须评估版本并同步配置：" + path)
        if path in expected and actual != expected[path].encode("utf-8"):
            raise ValueError("配置未从现行规范基线生成：" + path)
    if not manifest["releases"] or manifest["releases"][-1]["version"] != version:
        raise ValueError("绑定发布记录缺少当前版本")
    if manifest["releases"][-1]["artifacts"] != manifest["artifacts"]:
        raise ValueError("当前发布记录与绑定摘要不一致")
    log = text.split(LOG_BEGIN, 1)[1].split(LOG_END, 1)[0]
    if f"| {version} |" not in log:
        raise ValueError("正式变更记录缺少当前版本")
    return text, version, profile, manifest


def sync(args):
    text, current, profile = document()
    previous = None
    if (ROOT / MANIFEST).exists():
        previous = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
        if args.kind == "initial":
            raise ValueError("已有绑定基线，不能重复发布初版")
        major, minor, patch = version_tuple(previous["normative_version"])
        new_version = {
            "major": f"{major + 1}.0.0",
            "minor": f"{major}.{minor + 1}.0",
            "patch": f"{major}.{minor}.{patch + 1}",
        }[args.kind]
        if current not in (previous["normative_version"], new_version):
            raise ValueError("文档版本与指定变更类型的预期版本不一致")
    else:
        if args.kind != "initial" or current != "1.0.0":
            raise ValueError("首次同步必须为initial且规范版本为1.0.0")
        new_version = current
    known_ids = set(re.findall(r"^#### (EPR-[A-Z]+-\d{3}) ", text, re.M))
    affected = [item.strip() for item in args.rules.split(",")]
    if affected != ["ALL"] and not set(affected) <= known_ids:
        raise ValueError("涉及规则应为现行规则编号列表或ALL")
    if not args.profile_reviewed:
        raise ValueError("必须先审查正文与工具基线一致，再用--profile-reviewed记录审查责任")
    today = date.today().isoformat()
    text = re.sub(r"^- 正式版本：\S+$", "- 正式版本：" + new_version, text, count=1, flags=re.M)
    text = re.sub(r'("formal_version"\s*:\s*)"\d+\.\d+\.\d+"', r'\g<1>"' + new_version + '"', text)
    # The release-date metadata denotes the current release, not the first release.
    text = re.sub(r"^- 发布日期：\S+$", "- 发布日期：" + today, text, count=1, flags=re.M)
    clean = lambda item: item.replace("|", "\\|").replace("\n", " ").replace("\r", " ")
    row = f"| {new_version} | {today} | {args.kind} | {clean(args.rules)} | {clean(args.change)} | 同步生成两份配置、关联版本与摘要；工具覆盖范围见19.4 | 用户授权范围内执行；配置基线审查：{clean(args.profile_reviewed)} |\n"
    log = text.split(LOG_BEGIN, 1)[1].split(LOG_END, 1)[0]
    if f"| {new_version} |" in log:
        raise ValueError("变更记录已存在目标版本，拒绝重复追加")
    text = text.replace(LOG_END, row + LOG_END, 1)
    expected = rendered(text, new_version, profile)
    executable = clang_tool(args.clang_format, profile)
    # Validate before changing any published artifact; remove only our own temp file.
    temporary = ROOT / TOOL_DIR / ".coding-rules-config.tmp"
    if temporary.exists():
        raise ValueError("配置验证临时文件已存在，拒绝覆盖")
    try:
        temporary.write_bytes(expected[".clang-format"].encode("utf-8"))
        validate_config(executable, temporary)
    finally:
        if temporary.exists():
            temporary.unlink()
    artifacts = {SPEC.as_posix(): {"sha256": digest(text.encode("utf-8"))}}
    artifacts.update({path: {"sha256": digest(content.encode("utf-8"))} for path, content in expected.items()})
    release = {"version": new_version, "date": today, "kind": args.kind, "change": args.change,
               "affected_rules": affected, "profile_reviewed_by": args.profile_reviewed, "artifacts": artifacts}
    manifest = {"schema_version": 1, "normative_version": new_version,
                "source": SPEC.as_posix(), "artifacts": artifacts,
                "clang_format_version": profile["clang_format_version"],
                "editorconfig_core_version": profile["editorconfig_core_version"],
                "releases": (previous["releases"] if previous else []) + [release]}
    write(SPEC, text)
    for path, content in expected.items():
        write(path, content)
    write(MANIFEST, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    check()
    print("已同步发布规范及两份配置：" + new_version)


def source_errors(path, raw):
    errors = []
    if raw.startswith(b"\xef\xbb\xbf"):
        errors.append("EPR-FMT-010: UTF-8 BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return ["EPR-FMT-010: invalid UTF-8"]
    if b"\r" in raw:
        errors.append("EPR-FMT-011: non-LF line ending")
    if not raw or not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
        errors.append("EPR-FMT-013: require nonempty file and exactly one final LF")
    for number, line in enumerate(text.split("\n"), 1):
        if "\t" in line:
            errors.append(f"{number}: EPR-FMT-001: actual Tab; review any semantic exception")
        if len(line) > 100:
            errors.append(f"{number}: EPR-FMT-006: {len(line)} Unicode code points")
        if line.endswith((" ", "\t")):
            errors.append(f"{number}: EPR-FMT-012: trailing whitespace")
    return [f"{path}: {error}" for error in errors]


def format_check(args):
    _, _, profile, _ = check()
    executable = clang_tool(args.clang_format, profile)
    validate_config(executable, ROOT / ".clang-format")
    files = []
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if path.is_file() and path.suffix in profile["source_extensions"]:
            if any(relative.is_relative_to(Path(directory)) for directory in profile["excluded_directories"]):
                continue
            files.append(path)
    errors = []
    parameterized_templates = 0
    for path in sorted(files):
        relative = path.relative_to(ROOT)
        raw = path.read_bytes()
        errors.extend(source_errors(relative.as_posix(), raw))
        if relative.is_relative_to(PARAMETERIZED_TEMPLATE_DIR):
            parameterized_templates += 1
            continue
        result = subprocess.run([executable, "--style=file:" + str(ROOT / ".clang-format"),
                                 "--dry-run", "--Werror", str(path)], capture_output=True)
        if result.returncode:
            errors.append(result.stderr.decode("utf-8", errors="replace").strip())
    if errors:
        raise ValueError("\n".join(errors))
    formatted = len(files) - parameterized_templates
    print(f"格式与补充字节检查完成：{formatted}个可解析.c/.h文件；"
          f"{parameterized_templates}个参数化模板仅执行字节检查；语义规则未由此验证")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="action", required=True)
    actions.add_parser("check", help="check version, generation output and SHA-256 binding")
    release = actions.add_parser("sync", help="release a new version and regenerate both configurations")
    release.add_argument("--kind", choices=["initial", "major", "minor", "patch"], required=True)
    release.add_argument("--change", required=True)
    release.add_argument("--rules", required=True, help="comma-separated rule IDs, or ALL")
    release.add_argument("--profile-reviewed", required=True, help="AI or human who reviewed profile vs prose")
    release.add_argument("--clang-format")
    formatter = actions.add_parser("format-check", help="read-only owned C source checks")
    formatter.add_argument("--clang-format")
    args = parser.parse_args()
    try:
        if args.action == "check":
            _, version, _, _ = check()
            print("版本、生成内容及SHA-256绑定一致：" + version)
        elif args.action == "sync":
            sync(args)
        else:
            format_check(args)
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        print("检查失败：" + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
