/**
 * @file {{FILE_NAME}}
 * @brief Implements {{MODULE_BRIEF_LOWERCASE}}.
 *
 * Template set version: 2.0.0 (ZL501).
 * EPR baseline: {{EPR_VERSION}}.
 * EDI baseline: {{EDI_VERSION}}.
 *
 * Replace every {{...}} placeholder before delivery. Delete unused optional
 * content and empty logical sections. Public interface contracts remain in
 * the matching header and are not duplicated here.
 */

/* {{COPYRIGHT_AND_LICENSE_NOTICE}} */

#include "{{MODULE_NAME}}.h"

/* Standard Library Includes */
{{STANDARD_LIBRARY_INCLUDES}}

/* Project Includes */
{{PROJECT_INCLUDES}}

/* Private Macros */
{{PRIVATE_MACROS}}

/* Private Constants */
{{PRIVATE_CONSTANTS}}

/* Private Types */
{{PRIVATE_TYPES}}

/* Private File-Scope Objects */
{{PRIVATE_FILE_SCOPE_OBJECTS}}

/**
 * @brief This is an Atomic Function. {{ATOMIC_FUNCTION_BRIEF}}
 * @details Function: {{FILE_STEM}}_{{ATOMIC_FUNCTION_NAME}}.
 * @param[in] {{ATOMIC_INPUT_PARAMETER}} {{ATOMIC_INPUT_DESCRIPTION}}
 * @return {{ATOMIC_RETURN_DESCRIPTION}}
 * @author {{AUTHOR}}
 * @date {{CREATED_DATE}}
 */
static {{ATOMIC_RETURN_TYPE}} {{FILE_STEM}}_{{ATOMIC_FUNCTION_NAME}}(
    {{ATOMIC_INPUT_TYPE}} {{ATOMIC_INPUT_PARAMETER}})
{
    /* Local Variables */
    {{ATOMIC_LOCAL_VARIABLES}}

    /* Main Processing */
    {{ATOMIC_MAIN_PROCESSING}}

    /* Cleanup and Return */
    return {{ATOMIC_RETURN_VALUE}};
}

/**
 * @brief This is a Composite Function. {{COMPOSITE_FUNCTION_BRIEF}}
 * @details Function: {{FILE_STEM}}_{{COMPOSITE_FUNCTION_NAME}}.
 * @param[in] {{COMPOSITE_INPUT_PARAMETER}} {{COMPOSITE_INPUT_DESCRIPTION}}
 * @param[out] {{COMPOSITE_OUTPUT_PARAMETER}} {{COMPOSITE_OUTPUT_DESCRIPTION}}
 * @return {{COMPOSITE_RETURN_DESCRIPTION}}
 * @author {{AUTHOR}}
 * @date {{CREATED_DATE}}
 */
static {{COMPOSITE_RETURN_TYPE}} {{FILE_STEM}}_{{COMPOSITE_FUNCTION_NAME}}(
    {{COMPOSITE_INPUT_TYPE}} {{COMPOSITE_INPUT_PARAMETER}},
    {{COMPOSITE_OUTPUT_TYPE}} *{{COMPOSITE_OUTPUT_PARAMETER}})
{
    /* Local Variables */
    {{COMPOSITE_LOCAL_VARIABLES}}

    /* Input Validation */
    {{COMPOSITE_INPUT_VALIDATION}}

    /* Main Processing */
    {{COMPOSITE_MAIN_PROCESSING_USING_ATOMIC_FUNCTIONS}}

    /* Output Assignment */
    {{COMPOSITE_OUTPUT_ASSIGNMENT}}

    /* Cleanup and Return */
    return {{COMPOSITE_RETURN_VALUE}};
}

/*
 * Public contract: see {{MODULE_NAME}}.h.
 * Function classification: Service Function, pending human review until the
 * matching module knowledge base records an Approved result.
 */
{{RETURN_TYPE}} {{FILE_STEM}}_{{SERVICE_FUNCTION_NAME}}(
    {{INPUT_PARAMETER_TYPE}} {{INPUT_PARAMETER}},
    {{OUTPUT_PARAMETER_TYPE}} *{{OUTPUT_PARAMETER}})
{
    /* Local Variables */
    {{SERVICE_LOCAL_VARIABLES}}

    /* Input Validation */
    {{SERVICE_INPUT_VALIDATION}}

    /* External Data Acquisition */
    {{SERVICE_EXTERNAL_DATA_ACQUISITION}}

    /* Main Processing */
    {{SERVICE_MAIN_PROCESSING_USING_COMPOSITE_AND_ATOMIC_FUNCTIONS}}

    /* Output Assignment */
    {{SERVICE_OUTPUT_ASSIGNMENT}}

    /* Debug and Diagnostics */
    {{SERVICE_DEBUG_AND_DIAGNOSTICS}}

    /* Cleanup and Return */
    {{SERVICE_CLEANUP}}
    return {{SERVICE_RETURN_VALUE}};
}
