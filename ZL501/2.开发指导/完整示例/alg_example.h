/**
 * @file alg_example.h
 * @brief Declares a platform-independent bounded sample processing interface.
 *
 * Description: Declares the bounded sample processing contract.
 * Author: Codex (ZL501 adaptation of Nan.Wang example)
 * Created: 2026-10-21
 * Last editor: Codex
 * Last edited: 2026-10-28T16:17:46+08:00
 * EPR baseline: ZL501 3.0.0.
 * EDI baseline: ZL501 3.0.0.
 * Branch: ZL501
 * Previous commit: f78d11ec4c24450e142d2cb62083f4759e10f8b0
 * It is not a target-DSP validation artifact.
 */

/* Copyright and license strategy: TBD; this teaching example is not a release file. */

#ifndef ALG_EXAMPLE_H
#define ALG_EXAMPLE_H

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
 * @brief Computes and limits the integer average of input samples.
 * @category Service Function
 * @details Function: alg_example_processSamples.
 * @param[in] pSamples Points to a readable array containing sample_count signed samples.
 * @param[in] sample_count Number of valid array elements, from 1 to EXAMPLE_MAX_SAMPLE_COUNT.
 * @param[in] lower_limit Lowest value that may be written to pOutputValue.
 * @param[in] upper_limit Highest value that may be written to pOutputValue.
 * @param[out] pOutputValue Points to a writable result object and must not alias pSamples.
 * @return Status describing whether processing completed.
 * @retval EXAMPLE_STATUS_OK pOutputValue contains the limited integer average.
 * @retval EXAMPLE_STATUS_NULL_POINTER A required pointer was null; pOutputValue is unchanged.
 * @retval EXAMPLE_STATUS_INVALID_COUNT sample_count was invalid; pOutputValue is unchanged.
 * @retval EXAMPLE_STATUS_INVALID_LIMITS The limits were invalid; pOutputValue is unchanged.
 * @pre No module initialization is required.
 * @post On success, pOutputValue is between lower_limit and upper_limit, inclusive.
 * @post On failure, pOutputValue and the input sample array are unchanged.
 * @note 执行上下文：Synchronous platform-independent code;
 *       target ISR suitability is unverified.
 * @note 重入与同步：No shared state is used;
 *       callers protect concurrently shared objects.
 * @note 阻塞与时间：No wait or I/O is used; target execution time has not been measured.
 * @warning This teaching interface has not been validated with the project TI toolchain or DSP.
 * @author Codex (ZL501 adaptation of Nan.Wang example)
 * @date 2026-10-21
 */
EXAMPLE_Status alg_example_processSamples(const int16_t *pSamples,
    size_t sample_count,
    int16_t lower_limit,
    int16_t upper_limit,
    int16_t *pOutputValue);

#endif /* ALG_EXAMPLE_H */
