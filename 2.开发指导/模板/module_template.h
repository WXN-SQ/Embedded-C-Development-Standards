/**
 * @file {{FILE_NAME}}
 * @brief {{MODULE_BRIEF}}
 *
 * Template set version: 2.0.0.
 * EPR baseline: {{EPR_VERSION}}.
 * EDI baseline: {{EDI_VERSION}}.
 * Description: {{FILE_DESCRIPTION}}
 * Author: {{AUTHOR}}
 * Created: {{CREATED_AT}}
 * Last editor: {{LAST_EDITOR}}
 * Last edited: {{LAST_EDITED_AT}}
 * Branch: {{BRANCH}}
 * Previous commit: {{PREVIOUS_COMMIT}}
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
 * @brief {{SERVICE_FUNCTION_BRIEF}}
 * @category Service Function
 * @param[in] {{INPUT_PARAMETER}} {{INPUT_PARAMETER_DESCRIPTION}}
 * @param[out] {{OUTPUT_PARAMETER}} {{OUTPUT_PARAMETER_DESCRIPTION}}
 * @return {{RETURN_DESCRIPTION}}
 * @retval {{SUCCESS_VALUE}} {{SUCCESS_DESCRIPTION}}
 * @retval {{FAILURE_VALUE}} {{FAILURE_DESCRIPTION}}
 * @pre {{PRECONDITION}}
 * @post {{POSTCONDITION}}
 * @note Execution context: {{EXECUTION_CONTEXT}}
 * @note Reentrancy and synchronization: {{REENTRANCY_AND_SYNCHRONIZATION}}
 * @note Blocking and timing: {{BLOCKING_AND_TIMING}}
 * @warning {{WARNING_DESCRIPTION}}
 * @author {{AUTHOR}}
 */
{{RETURN_TYPE}} {{MODULE_PREFIX}}_{{SERVICE_FUNCTION_NAME}}(
    {{INPUT_PARAMETER_TYPE}} {{INPUT_PARAMETER}},
    {{OUTPUT_PARAMETER_TYPE}} *{{OUTPUT_PARAMETER}});

#endif /* {{HEADER_GUARD}} */
