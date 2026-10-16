# VS Code C 代码格式化配置指南

## 1. 目标与适用范围

本文说明如何以项目根目录的 `.clang-format` 为唯一格式基线，在 Windows、VS Code 和 LLVM 环境中实现：

- 手动格式化当前文件；
- 保存时自动格式化；
- 一键格式化整个工程中的受控 C 源文件；
- 提交代码前只读检查格式；
- 通过 Git Hook 或 CI 阻止不符合格式要求的代码进入仓库。

当前项目的正式格式工具版本为 clang-format 21.1.0，受控源文件扩展名为 `.c` 和 `.h`。格式化只改变源代码排版，不替代 TI CCS 编译器、静态分析、测试或代码评审。

## 2. 环境前提

### 2.1 必需软件

- Visual Studio Code；
- Microsoft C/C++ 扩展 `ms-vscode.cpptools`；
- LLVM clang-format 21.1.0；
- 执行项目检查脚本时，需要 Python 3.10 或更高版本；
- 使用提交前检查时，需要项目处于 Git 仓库中。

### 2.2 验证 clang-format 版本

在 PowerShell 中执行：

```powershell
& "C:\Program Files\LLVM\bin\clang-format.exe" --version
```

期望输出包含：

```text
clang-format version 21.1.0
```

clang-format 的版本应与 `.clang-format` 文件头部登记的版本完全一致。旧版本可能无法识别新配置项，或者产生不同的格式化结果。

### 2.3 `.clang-format` 的查找规则

当格式风格设置为 `file` 时，clang-format 会从当前源文件所在目录开始，逐级向父目录查找 `.clang-format`。

例如：

```text
Project/
├── .clang-format
└── src/
    └── module/
        └── motor.c
```

格式化 `motor.c` 时可以找到项目根目录中的 `.clang-format`。

如果配置文件位于与源码无父子关系的其他目录，clang-format 不会自动找到它。建议始终把 `.clang-format` 放在项目根目录，并在 VS Code 中通过“打开文件夹”打开项目根目录。

## 3. VS Code 基础配置

项目级配置文件为 `.vscode/settings.json`。推荐内容如下：

```json
{
    "[c]": {
        "editor.defaultFormatter": "ms-vscode.cpptools",
        "editor.formatOnSave": false
    },
    "[cpp]": {
        "editor.defaultFormatter": "ms-vscode.cpptools",
        "editor.formatOnSave": false
    },
    "C_Cpp.clang_format_path": "C:\\Program Files\\LLVM\\bin\\clang-format.exe",
    "C_Cpp.clang_format_style": "file",
    "C_Cpp.clang_format_fallbackStyle": "none"
}
```

各配置项的作用：

- `editor.defaultFormatter`：指定 Microsoft C/C++ 扩展负责 C/C++ 格式化；
- `editor.formatOnSave`：控制保存时是否自动格式化；
- `C_Cpp.clang_format_path`：指定 clang-format 21.1.0 的可执行文件；
- `C_Cpp.clang_format_style`：使用文件中的格式规则；
- `C_Cpp.clang_format_fallbackStyle`：找不到 `.clang-format` 时不使用其他备用风格。

设置 `fallbackStyle` 为 `none` 可以避免在配置文件缺失时意外套用 Visual Studio、LLVM 或其他默认风格。

修改配置后如果没有立即生效，可执行：

```text
Ctrl + Shift + P
→ Developer: Reload Window
```

## 4. 手动格式化当前文件

打开一个 `.c` 或 `.h` 文件，然后使用以下任意方式：

- 按 `Shift + Alt + F`；
- 在编辑器中右键，选择“格式化文档”；
- 按 `Ctrl + Shift + P`，执行 `Format Document`。

如果 VS Code 第一次使用时要求选择格式化程序：

1. 选择“配置默认格式化程序”；
2. 选择 Microsoft C/C++ 扩展；
3. 再次执行“格式化文档”。

该操作只修改当前打开的文件。

## 5. 保存时自动格式化

确认手动格式化结果符合预期后，可将 `.vscode/settings.json` 中 C 和 C++ 的配置改为：

```json
"[c]": {
    "editor.defaultFormatter": "ms-vscode.cpptools",
    "editor.formatOnSave": true
},
"[cpp]": {
    "editor.defaultFormatter": "ms-vscode.cpptools",
    "editor.formatOnSave": true
}
```

启用后，每次保存 C/C++ 文件都会自动格式化当前文件。

如果暂时不希望保存时改变排版，将 `editor.formatOnSave` 改回 `false`。建议在旧工程中先保持关闭，确认规则及差异规模后再启用。

## 6. 命令行格式化单个文件

### 6.1 预览格式化结果

不使用 `-i` 时，格式化结果只输出到终端，不修改源文件：

```powershell
& "C:\Program Files\LLVM\bin\clang-format.exe" `
    -style=file `
    "C:\path\to\source.c"
```

### 6.2 直接修改源文件

```powershell
& "C:\Program Files\LLVM\bin\clang-format.exe" `
    -style=file `
    -i `
    "C:\path\to\source.c"
```

其中：

- `-style=file` 表示读取 `.clang-format`；
- `-i` 表示直接改写文件。

## 7. 一键格式化整个工程

全工程格式化会直接修改范围内的全部文件，因此应与只读检查分开。可以在 `.vscode/tasks.json` 中添加以下任务：

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "格式化全部自有 C 代码",
            "type": "shell",
            "command": "$ErrorActionPreference = 'Stop'; Get-ChildItem -LiteralPath '${workspaceFolder}' -Recurse -File | Where-Object { ($_.Extension -eq '.c' -or $_.Extension -eq '.h') -and -not $_.FullName.StartsWith((Join-Path '${workspaceFolder}' '.tools')) } | ForEach-Object { & 'C:\\Program Files\\LLVM\\bin\\clang-format.exe' -i -style=file $_.FullName; if ($LASTEXITCODE -ne 0) { throw \"格式化失败：$($_.FullName)\" } }",
            "options": {
                "shell": {
                    "executable": "powershell.exe",
                    "args": [
                        "-NoProfile",
                        "-ExecutionPolicy",
                        "Bypass",
                        "-Command"
                    ]
                }
            },
            "problemMatcher": []
        }
    ]
}
```

执行任务：

```text
Ctrl + Shift + P
→ Tasks: Run Task
→ 格式化全部自有 C 代码
```

执行前建议确认工作区状态，执行后审查全部差异。不要在不了解文件归属的情况下对历史工程直接进行全量格式化。

### 7.1 排除目录原则

当前正式工具基线只排除 `.tools`。当前尚未正式排除以下常见目录：

```text
third_party
generated
build
Debug
Release
```

当工程引入第三方代码、生成代码或构建输出时，应先在正式规范的工具基线中登记目录范围，再按项目维护流程同步生成 `.clang-format`、`.editorconfig` 和版本绑定记录。

不应只修改 VS Code Task 的排除列表，否则全工程格式化与正式格式检查可能使用不同范围。

## 8. 提交前只读格式检查

项目已有检查入口：

```powershell
python "1.编程规范/维护工具/coding_rules.py" format-check `
    --clang-format "C:\Program Files\LLVM\bin\clang-format.exe"
```

该命令不会修改源码，主要检查：

- clang-format 版本是否为项目登记版本；
- `.clang-format` 是否能被正确解析；
- 正式规范、生成配置和版本绑定摘要是否一致；
- 受控 `.c/.h` 文件是否符合格式；
- 文件是否为 UTF-8 且无 BOM；
- 是否使用 LF 换行；
- 是否含有实际 Tab 或行尾空格；
- 是否超过100个 Unicode 码点；
- 文件末尾是否恰好保留一个换行。

检查失败时命令返回非零退出码，可供 Git Hook 和 CI 阻止提交或合并。

### 8.1 当前 Python 环境注意事项

本文创建时，本机命令 `python` 指向 Windows Store 占位程序，无法执行项目脚本，且 `py` 启动器不可用。因此需要先安装 Python 3.10 或更高版本，并确认：

```powershell
python --version
```

可以输出真实 Python 版本，然后再运行 `coding_rules.py`。

## 9. VS Code 格式检查任务

可以在 `.vscode/tasks.json` 的 `tasks` 数组中添加：

```json
{
    "label": "检查 C 代码格式",
    "type": "process",
    "command": "python",
    "args": [
        "1.编程规范/维护工具/coding_rules.py",
        "format-check",
        "--clang-format",
        "C:\\Program Files\\LLVM\\bin\\clang-format.exe"
    ],
    "options": {
        "cwd": "${workspaceFolder}"
    },
    "problemMatcher": []
}
```

执行方式：

```text
Ctrl + Shift + P
→ Tasks: Run Task
→ 检查 C 代码格式
```

格式化任务会修改文件；格式检查任务只检查并报告问题。二者不能混为一谈。

## 10. Git 提交前自动检查

建议将 Hook 放在版本化目录中，而不是仅写入本机 `.git/hooks`。在实际 Git 仓库中创建 `.githooks/pre-commit`：

```sh
#!/bin/sh

python "1.编程规范/维护工具/coding_rules.py" format-check \
    --clang-format "C:/Program Files/LLVM/bin/clang-format.exe"

status=$?

if [ "$status" -ne 0 ]; then
    echo "提交已终止：请先修正 C 代码格式。"
    exit "$status"
fi
```

在仓库根目录执行一次：

```powershell
git config core.hooksPath .githooks
```

之后每次执行 `git commit` 时：

- 检查通过：允许提交；
- 检查失败：拒绝提交，但不修改源文件。

不要在 `pre-commit` 中静默执行全工程格式化。Hook 在提交过程中修改文件时，修改后的内容可能没有进入暂存区，容易造成提交内容与工作区不一致。

本规范仓库已使用Git管理；上述Hook仍属于可选部署方案，未作为本次基线的一部分启用。

## 11. CI 检查思路

CI 应调用与本地相同的只读检查命令：

```powershell
python "1.编程规范/维护工具/coding_rules.py" check
python "1.编程规范/维护工具/coding_rules.py" format-check `
    --clang-format "<CI环境中的clang-format 21.1.0路径>"
```

CI 环境必须固定 clang-format 21.1.0，不能使用随运行环境变化的未锁定版本。检查失败时应使流水线返回失败，而不是在 CI 中自动格式化并提交代码。

不同代码托管平台的流水线语法不同，应在确定使用 GitHub Actions、GitLab CI、Jenkins 或其他平台后再创建对应配置。

## 12. 推荐日常工作流

```text
编辑 C 源文件
    ↓
Shift + Alt + F 手动格式化当前文件
    ↓
确认稳定后，可开启保存时自动格式化
    ↓
提交前运行 format-check
    ↓
检查成功后执行 git commit
    ↓
CI 使用相同版本和命令再次检查
```

对于大范围旧代码整理：

1. 单独创建格式化变更；
2. 一键格式化受控文件；
3. 审查完整差异；
4. 重新编译并执行必要测试；
5. 不要把功能修改和全量格式化混在同一个提交中。

## 13. 常见问题排查

### 13.1 执行“格式化文档”后没有变化

依次检查：

1. 当前文件语言模式是否为 C 或 C++；
2. Microsoft C/C++ 扩展是否已启用；
3. `editor.defaultFormatter` 是否为 `ms-vscode.cpptools`；
4. clang-format 路径是否正确；
5. `.clang-format` 是否位于当前文件目录或其父目录；
6. 执行 `Developer: Reload Window` 后重试。

### 13.2 提示找不到样式文件

检查 `.clang-format` 的位置，并确保使用 VS Code 打开了正确的项目根目录。由于备用风格设置为 `none`，找不到配置文件时不会自动使用其他风格。

### 13.3 提示未知配置项或配置值无效

首先执行：

```powershell
& "C:\Program Files\LLVM\bin\clang-format.exe" --version
```

确认实际版本为 21.1.0。不要通过删除正式配置项来迁就旧版本工具。

### 13.4 VS Code 与 CCS 格式化结果不同

CCS 5.5 和 CCS 12.7 使用 Eclipse/CDT Formatter，不能直接等同于 clang-format。CCS 20.x 的格式化能力还取决于其内置 clangd 版本。正式代码应以外部 clang-format 21.1.0 和项目根目录 `.clang-format` 的结果为准。

### 13.5 为什么检查通过仍不能证明代码完全符合编程规范

clang-format 只处理排版。`format-check` 还检查部分编码和文本约束，但不能证明命名语义、类型安全、并发安全、ISR/DMA约束、目标 ABI、实时性或功能行为正确。这些内容仍需编译器诊断、静态分析、测试和代码评审提供证据。
