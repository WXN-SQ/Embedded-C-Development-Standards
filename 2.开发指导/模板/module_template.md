# {{MODULE_NAME}} 模块资料库

## 1. 模板及基线信息

| 项目 | 内容 |
| --- | --- |
| 模板集版本 | 1.0.2 |
| EPR基线 | {{EPR_VERSION}} |
| EDI基线 | {{EDI_VERSION}} |
| 模块名称 | {{MODULE_NAME}} |
| 模块前缀 | {{MODULE_PREFIX}} |
| 默认作者 | {{AUTHOR}} |
| 源码身份 | {{SOURCE_IDENTITY}} |
| C语言基线 | {{C_STANDARD}} |
| 编译器 | {{COMPILER_VERSION}} |
| DSP型号 | {{DSP_MODEL}} |
| 维护状态 | {{REVIEW_STATUS}} |
| 最近核对 | {{LAST_REVIEW_RECORD}} |

> 实例化说明：替换全部 `{{...}}` 占位符；不适用内容明确写
> `None`；未知事实转为具有影响说明的 `TBD`。不得预填虚假的
> `Approved`、测试通过或目标验证结论。

## 2. 模块职责与边界

### 2.1 模块职责

{{MODULE_RESPONSIBILITIES}}

### 2.2 模块非职责

{{MODULE_NON_RESPONSIBILITIES}}

## 3. 文件映射

| 文件 | 路径 | 属性 | 职责 |
| --- | --- | --- | --- |
| `{{MODULE_NAME}}.h` | {{HEADER_PATH}} | Public Header | {{HEADER_RESPONSIBILITY}} |
| `{{MODULE_NAME}}.c` | {{SOURCE_PATH}} | Implementation | {{SOURCE_RESPONSIBILITY}} |
| `{{MODULE_NAME}}.md` | {{KNOWLEDGE_BASE_PATH}} | Knowledge Base | Module summary and review state |

## 4. 函数清单与分类审核

| 函数 | 分类 | 可见性 | 定义位置 | 主要职责 | 直接项目调用 | 审核状态 | 审核记录 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `{{MODULE_PREFIX}}_{{SERVICE_FUNCTION_NAME}}` | Service | Public / `static` | {{SERVICE_DEFINITION_LOCATION}} | {{SERVICE_FUNCTION_BRIEF}} | {{SERVICE_PROJECT_CALLS}} | Pending Review | {{SERVICE_REVIEW_RECORD}} |
| `{{MODULE_PREFIX}}_{{COMPOSITE_FUNCTION_NAME}}` | Composite | `static` | {{COMPOSITE_DEFINITION_LOCATION}} | {{COMPOSITE_FUNCTION_BRIEF}} | {{COMPOSITE_PROJECT_CALLS}} | Pending Review | {{COMPOSITE_REVIEW_RECORD}} |
| `{{MODULE_PREFIX}}_{{ATOMIC_FUNCTION_NAME}}` | Atomic | `static` | {{ATOMIC_DEFINITION_LOCATION}} | {{ATOMIC_FUNCTION_BRIEF}} | None | Pending Review | {{ATOMIC_REVIEW_RECORD}} |

## 5. 全局变量与文件作用域对象

| 变量 | 类型 | 链接/可见性 | 定义位置 | 初值 | 含义与单位 | 读者 | 写者 | 生命周期/所有者 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {{FILE_SCOPE_OBJECT_NAME_OR_NONE}} | {{TYPE}} | {{LINKAGE}} | {{LOCATION}} | {{INITIAL_VALUE}} | {{MEANING_AND_UNIT}} | {{READERS}} | {{WRITERS}} | {{LIFETIME_AND_OWNER}} |

## 6. 函数详细资料

### 6.1 `{{MODULE_PREFIX}}_{{SERVICE_FUNCTION_NAME}}`

#### 基本信息

| 项目 | 内容 |
| --- | --- |
| 分类 | Service Function |
| 可见性 | {{SERVICE_VISIBILITY}} |
| 分类依据 | {{SERVICE_CLASSIFICATION_RATIONALE}} |
| 审核状态 | Pending Review |

#### 输入、输出与返回

| 名称 | 类别 | 类型 | 方向 | 含义与单位 | 关键条件 |
| --- | --- | --- | --- | --- | --- |
| `{{INPUT_PARAMETER}}` | Parameter | `{{INPUT_PARAMETER_TYPE}}` | Input | {{INPUT_PARAMETER_DESCRIPTION}} | {{INPUT_PARAMETER_CONDITIONS}} |
| `{{OUTPUT_PARAMETER}}` | Parameter | `{{OUTPUT_PARAMETER_TYPE}} *` | Output | {{OUTPUT_PARAMETER_DESCRIPTION}} | {{OUTPUT_PARAMETER_CONDITIONS}} |
| Return | Return | `{{RETURN_TYPE}}` | Return | {{RETURN_DESCRIPTION}} | {{RETURN_CONDITIONS}} |

#### 局部变量

| 局部变量 | 类型 | 作用域 | 初值/来源 | 含义与单位 | 用途 |
| --- | --- | --- | --- | --- | --- |
| {{SERVICE_LOCAL_NAME_OR_NONE}} | {{TYPE}} | {{SCOPE}} | {{INITIAL_VALUE_OR_SOURCE}} | {{MEANING_AND_UNIT}} | {{PURPOSE}} |

### 6.2 `{{MODULE_PREFIX}}_{{COMPOSITE_FUNCTION_NAME}}`

#### 基本信息

| 项目 | 内容 |
| --- | --- |
| 分类 | Composite Function |
| 可见性 | `static` |
| 分类依据 | {{COMPOSITE_CLASSIFICATION_RATIONALE}} |
| 审核状态 | Pending Review |

#### 输入、输出与返回

| 名称 | 类别 | 类型 | 方向 | 含义与单位 | 关键条件 |
| --- | --- | --- | --- | --- | --- |
| `{{COMPOSITE_INPUT_PARAMETER}}` | Parameter | `{{COMPOSITE_INPUT_TYPE}}` | Input | {{COMPOSITE_INPUT_DESCRIPTION}} | {{COMPOSITE_INPUT_CONDITIONS}} |
| `{{COMPOSITE_OUTPUT_PARAMETER}}` | Parameter | `{{COMPOSITE_OUTPUT_TYPE}} *` | Output | {{COMPOSITE_OUTPUT_DESCRIPTION}} | {{COMPOSITE_OUTPUT_CONDITIONS}} |
| Return | Return | `{{COMPOSITE_RETURN_TYPE}}` | Return | {{COMPOSITE_RETURN_DESCRIPTION}} | {{COMPOSITE_RETURN_CONDITIONS}} |

#### 局部变量

| 局部变量 | 类型 | 作用域 | 初值/来源 | 含义与单位 | 用途 |
| --- | --- | --- | --- | --- | --- |
| {{COMPOSITE_LOCAL_NAME_OR_NONE}} | {{TYPE}} | {{SCOPE}} | {{INITIAL_VALUE_OR_SOURCE}} | {{MEANING_AND_UNIT}} | {{PURPOSE}} |

### 6.3 `{{MODULE_PREFIX}}_{{ATOMIC_FUNCTION_NAME}}`

#### 基本信息

| 项目 | 内容 |
| --- | --- |
| 分类 | Atomic Function |
| 可见性 | `static` |
| 分类依据 | {{ATOMIC_CLASSIFICATION_RATIONALE}} |
| 审核状态 | Pending Review |

#### 输入、输出与返回

| 名称 | 类别 | 类型 | 方向 | 含义与单位 | 关键条件 |
| --- | --- | --- | --- | --- | --- |
| `{{ATOMIC_INPUT_PARAMETER}}` | Parameter | `{{ATOMIC_INPUT_TYPE}}` | Input | {{ATOMIC_INPUT_DESCRIPTION}} | {{ATOMIC_INPUT_CONDITIONS}} |
| Return | Return | `{{ATOMIC_RETURN_TYPE}}` | Return | {{ATOMIC_RETURN_DESCRIPTION}} | {{ATOMIC_RETURN_CONDITIONS}} |

#### 局部变量

| 局部变量 | 类型 | 作用域 | 初值/来源 | 含义与单位 | 用途 |
| --- | --- | --- | --- | --- | --- |
| {{ATOMIC_LOCAL_NAME_OR_NONE}} | {{TYPE}} | {{SCOPE}} | {{INITIAL_VALUE_OR_SOURCE}} | {{MEANING_AND_UNIT}} | {{PURPOSE}} |

## 7. 直接依赖与使用注意事项

| 类别 | 内容 |
| --- | --- |
| 项目模块依赖 | {{PROJECT_MODULE_DEPENDENCIES}} |
| 标准库依赖 | {{STANDARD_LIBRARY_DEPENDENCIES}} |
| HAL/芯片库依赖 | {{HAL_DEPENDENCIES}} |
| RTOS依赖 | {{RTOS_DEPENDENCIES}} |
| 厂商扩展 | {{VENDOR_EXTENSIONS}} |
| 配置依赖 | {{CONFIGURATION_DEPENDENCIES}} |
| 初始化依赖 | {{INITIALIZATION_DEPENDENCIES}} |
| 使用注意事项 | {{USAGE_NOTES}} |

## 8. 待确认项

| 编号 | 待确认内容 | 影响 | 关闭条件 | 状态 |
| --- | --- | --- | --- | --- |
| {{TBD_ID_OR_NONE}} | {{TBD_DESCRIPTION}} | {{TBD_IMPACT}} | {{TBD_CLOSURE_CONDITION}} | Open / Closed |

## 9. 同步与人工审核记录

| 日期 | 源码身份 | 核对范围 | AI读取范围 | 人工审核人 | 结论 | 未关闭项 |
| --- | --- | --- | --- | --- | --- | --- |
| {{REVIEW_DATE}} | {{SOURCE_IDENTITY}} | {{REVIEW_SCOPE}} | {{AI_READ_SCOPE}} | {{HUMAN_REVIEWER}} | {{REVIEW_CONCLUSION}} | {{OPEN_ITEMS}} |
