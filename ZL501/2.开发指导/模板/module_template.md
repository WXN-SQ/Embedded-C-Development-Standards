# {{MODULE_NAME}} 模块资料库

## 1. 模板及基线信息

| 项目 | 内容 |
| --- | --- |
| 模板集版本 | 2.1.0（ZL501） |
| EPR基线 | {{EPR_VERSION}} |
| EDI基线 | {{EDI_VERSION}} |
| 模块名称 | {{MODULE_NAME}} |
| 模块前缀 | {{MODULE_PREFIX}} |
| 文件名词干 | {{FILE_STEM}}（例如 `alg_test`；函数名再加一个下划线及操作名） |
| 函数创建日期 | {{CREATED_DATE}}（YYYY-MM-DD；以真实记录核验） |
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

`{{MODULE_NAME}}` 与 `{{FILE_STEM}}` 均应取项目已登记的文件名词干，例如 `alg_test`；函数操作名不得再含下划线，保证函数名恰有两个下划线。指针名使用 `pXxx`，全局指针使用已裁决的 `pGXxx`。函数头的创建人和日期须从真实记录核验。

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
| `{{FILE_STEM}}_{{SERVICE_FUNCTION_NAME}}` | Service | Public / `static` | {{SERVICE_DEFINITION_LOCATION}} | {{SERVICE_FUNCTION_BRIEF}} | {{SERVICE_PROJECT_CALLS}} | Pending Review | {{SERVICE_REVIEW_RECORD}} |
| `{{FILE_STEM}}_{{COMPOSITE_FUNCTION_NAME}}` | Composite | `static` | {{COMPOSITE_DEFINITION_LOCATION}} | {{COMPOSITE_FUNCTION_BRIEF}} | {{COMPOSITE_PROJECT_CALLS}} | Pending Review | {{COMPOSITE_REVIEW_RECORD}} |
| `{{FILE_STEM}}_{{ATOMIC_FUNCTION_NAME}}` | Atomic | `static` | {{ATOMIC_DEFINITION_LOCATION}} | {{ATOMIC_FUNCTION_BRIEF}} | None | Pending Review | {{ATOMIC_REVIEW_RECORD}} |

## 5. 全局变量与文件作用域对象

| 变量 | 类型 | 链接/可见性 | 定义位置 | 初值 | 含义与单位 | 读者 | 写者 | 生命周期/所有者 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {{FILE_SCOPE_OBJECT_NAME_OR_NONE}} | {{TYPE}} | {{LINKAGE}} | {{LOCATION}} | {{INITIAL_VALUE}} | {{MEANING_AND_UNIT}} | {{READERS}} | {{WRITERS}} | {{LIFETIME_AND_OWNER}} |

## 6. 函数详细资料

### 6.1 `{{FILE_STEM}}_{{SERVICE_FUNCTION_NAME}}`

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

### 6.2 `{{FILE_STEM}}_{{COMPOSITE_FUNCTION_NAME}}`

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

### 6.3 `{{FILE_STEM}}_{{ATOMIC_FUNCTION_NAME}}`

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

## 8. ZL501 功能模块设计资料

| 设计项 | 内容或权威位置 |
| --- | --- |
| 四层归属与 `func/control` 分区 | {{LAYER_AND_FUNCTION_PARTITION}} |
| 主要参数结构体及获取接口 | {{PARAMETER_STRUCTURE_AND_ACCESS}} |
| 相关结构体定义 | {{STRUCTURE_DEFINITION_LINKS}} |
| 接口函数说明 | {{INTERFACE_FUNCTION_LINKS}} |
| 功能设计流程 | {{FUNCTIONAL_FLOW}} |
| 遥控遥测需求（无需求时注明不适用） | {{TELECONTROL_TELEMETRY_MAPPING_OR_NONE}} |
| EMIF 地址及多组读写接口（无需求时注明不适用） | {{EMIF_MAPPING_OR_NONE}} |

以上条目指向源码权威声明与项目需求，不复制第二份公共接口契约；实际硬件地址、时序及目标验证依证据填写。

## 9. 待确认项

| 编号 | 待确认内容 | 影响 | 关闭条件 | 状态 |
| --- | --- | --- | --- | --- |
| {{TBD_ID_OR_NONE}} | {{TBD_DESCRIPTION}} | {{TBD_IMPACT}} | {{TBD_CLOSURE_CONDITION}} | Open / Closed |

## 10. 待集成代码段

| 编号 | 源码位置 | 所属模块 | 相关模块 | 待集成内容 | 影响 | 临时行为 | 关闭条件 | 责任人 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {{PIB_ID_OR_NONE}} | {{PIB_SOURCE_LOCATION}} | {{MODULE_PREFIX}} | {{RELATED_MODULES}} | {{PIB_CONTENT}} | {{PIB_IMPACT}} | {{PIB_TEMPORARY_BEHAVIOR}} | {{PIB_CLOSURE_CONDITION}} | {{PIB_OWNER}} | Open / Ready for Integration / Closed |

> 仅登记有任务、依赖、设计或人工确认依据的 PIB；无 PIB 时填 `None`，不从普通空代码推定。Closed 项保留关闭日期、源码身份和验证证据，且对应源码标记必须删除。

## 11. 同步与人工审核记录

| 日期 | 源码身份 | 核对范围 | AI读取范围 | 人工审核人 | 结论 | 未关闭项 |
| --- | --- | --- | --- | --- | --- | --- |
| {{REVIEW_DATE}} | {{SOURCE_IDENTITY}} | {{REVIEW_SCOPE}} | {{AI_READ_SCOPE}} | {{HUMAN_REVIEWER}} | {{REVIEW_CONCLUSION}} | {{OPEN_ITEMS}} |
