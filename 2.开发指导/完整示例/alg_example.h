/**
 * @file alg_example.h
 * @brief Declares a platform-independent bounded sample processing interface.
 *
 * Description: Declares the bounded sample processing contract.
 * Author: Codex (ZL501 adaptation of Nan.Wang example)
 * Created: 2026-10-21
 * Last editor: Codex
 * Last edited: 2026-11-06T11:54:28+08:00
 * EPR baseline: ZL501 4.0.0.
 * EDI baseline: ZL501 4.0.0.
 * Branch: ZL501
 * Previous commit: 3d9741a765ac43090dabe7c1b05972d96dcbe16f
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

EXAMPLE_Status alg_example_processSamples(const int16_t *pSamples,
    size_t sample_count,
    int16_t lower_limit,
    int16_t upper_limit,
    int16_t *pOutputValue);

#endif /* ALG_EXAMPLE_H */
