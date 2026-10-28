# alg_example 模块资料库

## 1. 基本信息

| 项目 | 内容 |
| --- | --- |
| 模块名称 | `alg_example` |
| 模块职责 | 对一组有界整数样本求整数平均值，并把结果限制在调用方给定范围内 |
| 模块非职责 | 不采集硬件数据，不管理任务或中断，不执行浮点滤波，不保存跨调用状态 |
| EPR基线 | ZL501 EPR 3.0.2 |
| EDI基线 | ZL501 EDI 3.0.2 |
| 模板集版本 | 3.0.2 |
| 源码身份 | 工作区教学示例；C/H文件SHA-256见第10.1节 |
| C语言基线 | 面向ISO C99；项目TI编译器支持情况尚未验证 |
| 编译器 | TBD：项目TI编译器名称和完整版本未知 |
| DSP型号 | TBD |
| 项目版整理 | Codex；基于通用版 Nan.Wang 教学示例改写；分类与发布批准单独记录 |
| 维护状态 | Approved；五个函数的职责与调用关系未变，3.0.0 文档格式已由 Nan.Wang 评审通过 |
| 最近核对 | 2026-10-28，3.0.2 仅更新文件头版本与目录位置；源码身份见第10.1节 |

## 2. 文件映射

| 文件 | 属性 | 职责 |
| --- | --- | --- |
| `alg_example.h` | Public Header | 声明状态类型、样本数量上限和公共Service接口 |
| `alg_example.c` | Implementation | 实现一个Service、一个Composite和三个Atomic函数 |
| `alg_example.md` | Knowledge Base | 汇总分类、变量、输入输出、依赖和审核状态 |

## 3. 设计假设

- `int16_t`和`int32_t`由目标C实现提供。
- `EXAMPLE_MAX_SAMPLE_COUNT`为16，最坏求和范围可由`int32_t`表示。
- 整数平均采用C99有符号整数除法规则，结果向零截断。
- 该示例不使用共享可变状态、动态内存、HAL、RTOS、DMA或厂商扩展。
- TI编译器、DSP、ABI、执行时间和栈使用尚未验证。

## 4. 函数清单与分类审核

| 函数 | 分类 | 可见性 | 主要职责 | 直接项目调用 | 审核状态 |
| --- | --- | --- | --- | --- | --- |
| `alg_example_processSamples` | Service | Public | 校验接口输入，计算平均值并限制输出 | `alg_example_computeAverage`, `alg_example_limitValue` | Approved |
| `alg_example_computeAverage` | Composite | `static` | 组合求和与除法步骤以计算平均值 | `alg_example_sumSamples`, `alg_example_divideSum` | Approved |
| `alg_example_sumSamples` | Atomic | `static` | 对已校验样本进行有界求和 | None | Approved |
| `alg_example_divideSum` | Atomic | `static` | 用正整数样本数量计算整数商 | None | Approved |
| `alg_example_limitValue` | Atomic | `static` | 将值限制到有效闭区间 | None | Approved |

### 4.1 调用关系

```text
alg_example_processSamples [Service]
├── alg_example_computeAverage [Composite]
│   ├── alg_example_sumSamples [Atomic]
│   └── alg_example_divideSum [Atomic]
└── alg_example_limitValue [Atomic]
```

静态阅读未发现直接、间接或隐蔽递归。五个函数分类已由 Nan.Wang 于 2026-10-21 审核批准，绑定第10.1节 C/H 摘要。

## 5. 全局变量与文件作用域对象

None。`EXAMPLE_MAX_SAMPLE_COUNT`是公共宏常量，不是变量或对象。

## 6. 函数详细资料

### 6.1 `alg_example_processSamples`

| 项目 | 内容 |
| --- | --- |
| 分类 | Service Function |
| 可见性 | Public |
| 分类依据 | 向调用方提供完整的校验、平均计算和范围限制服务 |
| 审核状态 | Approved；Nan.Wang，2026-10-21；源码身份见第10.1节 |

#### 输入、输出与返回

| 名称 | 类型 | 方向 | 含义与单位 | 关键条件 |
| --- | --- | --- | --- | --- |
| `pSamples` | `const int16_t *` | Input | 无量纲整数样本数组 | 非空；至少含sample_count个可读元素；不得与pOutputValue重叠 |
| `sample_count` | `size_t` | Input | 有效样本数 | 1至16 |
| `lower_limit` | `int16_t` | Input | 输出闭区间下限 | 不大于upper_limit |
| `upper_limit` | `int16_t` | Input | 输出闭区间上限 | 不小于lower_limit |
| `pOutputValue` | `int16_t *` | Output | 受限整数平均值 | 非空；仅成功时写入 |
| Return | `EXAMPLE_Status` | Return | 处理状态 | 失败时pOutputValue保持不变 |

#### 局部变量

| 局部变量 | 类型 | 作用域 | 初值/来源 | 含义与单位 | 用途 |
| --- | --- | --- | --- | --- | --- |
| `Average` | `int16_t` | Function | `0` | 无量纲整数平均值 | 保存Composite计算结果，供范围限制使用 |

### 6.2 `alg_example_computeAverage`

| 项目 | 内容 |
| --- | --- |
| 分类 | Composite Function |
| 可见性 | `static` |
| 分类依据 | 组合两个Atomic步骤完成内部平均计算 |
| 审核状态 | Approved；Nan.Wang，2026-10-21；源码身份见第10.1节 |

#### 输入、输出与返回

| 名称 | 类型 | 方向 | 含义与单位 | 关键条件 |
| --- | --- | --- | --- | --- |
| `pSamples` | `const int16_t *` | Input | 已校验的整数样本数组 | 非空且至少含sample_count个元素 |
| `sample_count` | `size_t` | Input | 已校验的样本数 | 1至16 |
| Return | `int16_t` | Return | 向零截断的整数平均值 | 可由int16_t表示 |

#### 局部变量

| 局部变量 | 类型 | 作用域 | 初值/来源 | 含义与单位 | 用途 |
| --- | --- | --- | --- | --- | --- |
| `Sum` | `int32_t` | Function | `0` | 样本总和 | 保存Atomic求和结果 |
| `Average` | `int16_t` | Function | `0` | 整数平均值 | 保存Atomic除法结果 |

### 6.3 `alg_example_sumSamples`

| 项目 | 内容 |
| --- | --- |
| 分类 | Atomic Function |
| 可见性 | `static` |
| 分类依据 | 只执行一个有界求和操作，不调用项目函数 |
| 审核状态 | Approved；Nan.Wang，2026-10-21；源码身份见第10.1节 |

#### 输入、输出与返回

| 名称 | 类型 | 方向 | 含义与单位 | 关键条件 |
| --- | --- | --- | --- | --- |
| `pSamples` | `const int16_t *` | Input | 已校验的整数样本数组 | 非空且至少含count个元素 |
| `count` | `size_t` | Input | 求和元素数 | 1至16 |
| Return | `int32_t` | Return | 样本总和 | 在int32_t范围内 |

#### 局部变量

| 局部变量 | 类型 | 作用域 | 初值/来源 | 含义与单位 | 用途 |
| --- | --- | --- | --- | --- | --- |
| `Sum` | `int32_t` | Function | `0` | 样本总和 | 累积输入样本 |
| `Index` | `size_t` | Function | `0U` | 数组索引 | 控制有界循环 |

### 6.4 `alg_example_divideSum`

| 项目 | 内容 |
| --- | --- |
| 分类 | Atomic Function |
| 可见性 | `static` |
| 分类依据 | 只执行一次已校验的整数除法，不调用项目函数 |
| 审核状态 | Approved；Nan.Wang，2026-10-21；源码身份见第10.1节 |

#### 输入、输出与返回

| 名称 | 类型 | 方向 | 含义与单位 | 关键条件 |
| --- | --- | --- | --- | --- |
| `Sum` | `int32_t` | Input | 已验证范围的样本总和 | 来自最多16个int16_t样本 |
| `Divisor` | `int32_t` | Input | 正整数除数 | 1至16 |
| Return | `int16_t` | Return | 向零截断的整数商 | 在int16_t范围内 |

#### 局部变量

None。

### 6.5 `alg_example_limitValue`

| 项目 | 内容 |
| --- | --- |
| 分类 | Atomic Function |
| 可见性 | `static` |
| 分类依据 | 只执行一个闭区间限制操作，不调用项目函数 |
| 审核状态 | Approved；Nan.Wang，2026-10-21；源码身份见第10.1节 |

#### 输入、输出与返回

| 名称 | 类型 | 方向 | 含义与单位 | 关键条件 |
| --- | --- | --- | --- | --- |
| `Value` | `int16_t` | Input | 待限制整数值 | 任意int16_t值 |
| `lower_limit` | `int16_t` | Input | 闭区间下限 | 不大于upper_limit |
| `upper_limit` | `int16_t` | Input | 闭区间上限 | 不小于lower_limit |
| Return | `int16_t` | Return | 限制后的值 | 位于闭区间内 |

#### 局部变量

None。

## 7. 直接依赖与使用注意事项

| 类别 | 内容 |
| --- | --- |
| 项目模块依赖 | None |
| 标准库依赖 | `<stddef.h>`提供`size_t`和`NULL`；`<stdint.h>`提供固定宽度整数类型 |
| HAL/芯片库依赖 | None |
| RTOS依赖 | None |
| 厂商扩展 | None |
| 配置依赖 | C99优先；需要目标实现提供int16_t和int32_t |
| 初始化依赖 | None |
| 使用注意事项 | 整数平均向零截断；输出仅在成功时写入；本示例未经目标DSP验证 |

## 8. 待确认项

| 编号 | 待确认内容 | 影响 | 关闭条件 | 状态 |
| --- | --- | --- | --- | --- |
| EX-TBD-001 | 项目TI编译器和C99模式 | 无法证明目标编译兼容 | 使用真实编译器和项目选项完成构建 | Open |
| EX-TBD-002 | DSP型号、ABI和数据模型 | 无法证明目标类型及执行行为 | 核对器件、ABI、编译器资料和目标结果 | Open |
| EX-TBD-003 | 函数三级分类人工审核 | 分类结论必须绑定当前源码身份 | Nan.Wang逐函数审核并批准 | Closed，2026-10-21；绑定第10.1节摘要 |
| EX-TBD-004 | 版权与许可证策略 | 示例不能作为正式发布文件 | 项目提供并批准标注策略 | Open |

## 9. 待集成代码段
+
None。当前教学示例无跨模块待集成依赖，不创建无事实依据的 PIB 记录；格式和生命周期要求见 EPR 16.8、17.11 与 EDI 3.8、8.12、9.8、12.8。

## 10. 验证与同步记录

| 检查 | 状态 | 结果与限制 |
| --- | --- | --- |
| 文件映射及占位符 | 已执行 | 三个同名文件存在；未发现双花括号占位符 |
| UTF-8、LF、Tab、尾随空白和C行宽 | 已执行 | ZL501 3.0.2 `format-check` 通过；示例 C/H 执行格式与字节检查，参数化模板仅执行字节检查 |
| EPR clang-format基线 | 已执行 | clang-format 21.1.0 与 ZL501 EPR 3.0.2 的 `check`、`format-check` 通过 |
| 静态调用关系与递归 | 已执行 | 静态阅读与第4.1节调用图一致；不构成目标环境验证 |
| 主机C99语法与告警检查 | 已执行 | clang 21.1.0 `-std=c99 -Wall -Wextra -Werror -fsyntax-only` 通过；不构成目标编译或运行验证 |
| TI编译器构建 | 未执行 | TI编译器名称、版本和工程配置未知 |
| 目标DSP运行 | 未执行 | DSP型号和目标环境未知 |
| PIB 显式标记检查 | 已执行 | `pib-check` 在当前教学示例发现 0 个源码标记；不能据此推断产品不存在未识别集成缺口 |
| 人工分类审核 | 已通过 | Nan.Wang 于 2026-10-21 确认五个函数分类，2026-10-28 评审通过本次 `@category` 表达与源码身份变化；函数实现、职责、调用关系及可见性未改 |

### 10.1 C/H文件摘要

| 文件 | SHA-256 |
| --- | --- |
| `alg_example.h` | `E6B107E13905AA35A2F84ABCB8E7015DA2A2C8EBD390863E55272E48E0EC59B4` |
| `alg_example.c` | `D493949C18F2465AAB2C344B1D01A92F503C12977AC148BC82DB1B3924B17C10` |

人工审核时的 C/H 摘要分别为 `35F32F1536C223931D4DCC753D1A2CA00F9A3387311009313ED7AAE8EE9B3050` 和 `46CCF58E2174024DF89ACEF96359322629F1617AFE955E5E040108886CE96B6A`。3.0.0 更新了文件头、保护宏与函数文档字段；3.0.1 和 3.0.2 仅更新版本、路径及上一提交身份。函数实现、职责、调用关系或可见性未修改；上表为 3.0.2 当前文件摘要。

这些结果仅覆盖表中列明的文件和静态检查，不证明TI工具链、目标DSP、实时性或全部EPR规则已经通过。
