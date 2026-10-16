/**
 * @file example_module.h
 * @brief Declares a platform-independent bounded sample processing interface.
 *
 * This file is a teaching example for EPR 1.0.1 and EDI 1.0.1.
 * It is not a target-DSP validation artifact.
 */

/* Copyright and license strategy: TBD; this teaching example is not a release file. */

#ifndef EDI_COMPLETE_EXAMPLE_EXAMPLE_MODULE_H
#define EDI_COMPLETE_EXAMPLE_EXAMPLE_MODULE_H

#include <stddef.h>
#include <stdint.h>

/** Maximum supported number of samples in one call. */
#define EXAMPLE_MAX_SAMPLE_COUNT (16U)

/** Status values returned by the example module. */
typedef enum
{
    EXAMPLE_STATUS_OK = 0, /**< Processing completed successfully. */
    EXAMPLE_STATUS_NULL_POINTER, /**< A required pointer was null. */
    EXAMPLE_STATUS_INVALID_COUNT, /**< The sample count was outside the supported range. */
    EXAMPLE_STATUS_INVALID_LIMITS /**< The lower limit was greater than the upper limit. */
} EXAMPLE_Status;

/**
 * @brief This is a Service Function. Computes and limits the integer average of input samples.
 * @param[in] samples Points to a readable array containing sample_count signed samples.
 * @param[in] sample_count Number of valid array elements, from 1 to EXAMPLE_MAX_SAMPLE_COUNT.
 * @param[in] lower_limit Lowest value that may be written to output_value.
 * @param[in] upper_limit Highest value that may be written to output_value.
 * @param[out] output_value Points to a writable result object and must not alias samples.
 * @return Status describing whether processing completed.
 * @retval EXAMPLE_STATUS_OK output_value contains the limited integer average.
 * @retval EXAMPLE_STATUS_NULL_POINTER A required pointer was null; output_value is unchanged.
 * @retval EXAMPLE_STATUS_INVALID_COUNT sample_count was invalid; output_value is unchanged.
 * @retval EXAMPLE_STATUS_INVALID_LIMITS The limits were invalid; output_value is unchanged.
 * @pre No module initialization is required.
 * @post On success, output_value is between lower_limit and upper_limit, inclusive.
 * @post On failure, output_value and the input sample array are unchanged.
 * @note 执行上下文：Synchronous platform-independent code; target ISR suitability is unverified.
 * @note 重入与同步：No shared state is used; callers protect concurrently shared objects.
 * @note 阻塞与时间：No wait or I/O is used; target execution time has not been measured.
 * @warning This teaching interface has not been validated with the project TI toolchain or DSP.
 * @author Nan.Wang
 */
EXAMPLE_Status EXAMPLE_process_samples(const int16_t *samples,
    size_t sample_count,
    int16_t lower_limit,
    int16_t upper_limit,
    int16_t *output_value);

#endif /* EDI_COMPLETE_EXAMPLE_EXAMPLE_MODULE_H */
