/**
 * @file {{FILE_NAME}}
 * @brief {{MODULE_BRIEF}}
 *
 * Template set version: 2.1.0 (ZL501).
 * EPR baseline: {{EPR_VERSION}}.
 * EDI baseline: {{EDI_VERSION}}.
 *
 * Replace every {{...}} placeholder before delivery. Remove optional sections
 * and fields that do not apply. Do not invent target, timing, safety, license,
 * or verification information.
 */

/* {{COPYRIGHT_AND_LICENSE_NOTICE}} */

#ifndef {{HEADER_GUARD}}
#define {{HEADER_GUARD}}

/* Standard Library Includes */
{{STANDARD_LIBRARY_INCLUDES}}

/* Project Includes */
{{PROJECT_INCLUDES}}

/* Public Macros */
{{PUBLIC_MACROS}}

/* Public Constants */
{{PUBLIC_CONSTANTS}}

/* Public Types */
{{PUBLIC_TYPES}}

/* Public Function Declarations */

/**
 * @brief This is a Service Function. {{SERVICE_FUNCTION_BRIEF}}
 * @details Function: {{FILE_STEM}}_{{SERVICE_FUNCTION_NAME}}.
 * @param[in] {{INPUT_PARAMETER}} {{INPUT_PARAMETER_DESCRIPTION}}
 * @param[out] {{OUTPUT_PARAMETER}} {{OUTPUT_PARAMETER_DESCRIPTION}}
 * @return {{RETURN_DESCRIPTION}}
 * @retval {{SUCCESS_VALUE}} {{SUCCESS_DESCRIPTION}}
 * @retval {{FAILURE_VALUE}} {{FAILURE_DESCRIPTION}}
 * @pre {{PRECONDITION}}
 * @post {{POSTCONDITION}}
 * @note 执行上下文：{{EXECUTION_CONTEXT}}
 * @note 重入与同步：{{REENTRANCY_AND_SYNCHRONIZATION}}
 * @note 阻塞与时间：{{BLOCKING_AND_TIMING}}
 * @warning {{WARNING_DESCRIPTION}}
 * @author {{AUTHOR}}
 * @date {{CREATED_DATE}}
 */
{{RETURN_TYPE}} {{FILE_STEM}}_{{SERVICE_FUNCTION_NAME}}(
    {{INPUT_PARAMETER_TYPE}} {{INPUT_PARAMETER}},
    {{OUTPUT_PARAMETER_TYPE}} *{{OUTPUT_PARAMETER}});

#endif /* {{HEADER_GUARD}} */
