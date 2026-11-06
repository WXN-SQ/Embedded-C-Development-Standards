/**
 * @file alg_example.c
 * @brief Implements platform-independent bounded integer sample processing.
 *
 * Description: Demonstrates bounded sample processing without target validation.
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

#include "alg_example.h"

/**
 * @brief Adds a validated array of signed samples.
 * @details Adds each of count validated samples to a 32-bit accumulator.
 * @param[in] pSamples Points to a readable array containing count valid elements.
 * @param[in] count Number of elements to add, from 1 to EXAMPLE_MAX_SAMPLE_COUNT.
 * @return Sum of all input samples represented as int32_t.
 * @author Codex (ZL501 adaptation of Nan.Wang example)
 * @date 2026-10-21
 * @par Change Log
 * - 2026-11-06 | Codex | Moved classification to the module record and revised this header.
 */
static int32_t alg_example_sumSamples(const int16_t *pSamples, size_t count)
{
    int32_t sum = 0;
    size_t index = 0U;

    for (index = 0U; index < count; ++index)
    {
        sum += (int32_t) pSamples[index];
    }

    return sum;
}

/**
 * @brief Divides a validated sum by a positive sample count.
 * @details Divides the validated sum using C99 integer division.
 * @param[in] sum Signed sum to divide.
 * @param[in] divisor Positive divisor representable as int32_t.
 * @return Integer quotient truncated toward zero and representable as int16_t.
 * @author Codex (ZL501 adaptation of Nan.Wang example)
 * @date 2026-10-21
 * @par Change Log
 * - 2026-11-06 | Codex | Clarified division behavior and moved classification to the module record.
 */
static int16_t alg_example_divideSum(int32_t sum, int32_t divisor)
{
    return (int16_t) (sum / divisor);
}

/**
 * @brief Limits a signed value to an inclusive range.
 * @details Returns the nearest bound when value lies outside the inclusive range.
 * @param[in] value Value to limit.
 * @param[in] lower_limit Inclusive lower bound.
 * @param[in] upper_limit Inclusive upper bound, not less than lower_limit.
 * @return Limited value between lower_limit and upper_limit, inclusive.
 * @author Codex (ZL501 adaptation of Nan.Wang example)
 * @date 2026-10-21
 * @par Change Log
 * - 2026-11-06 | Codex | Clarified range behavior and moved classification to the module record.
 */
static int16_t alg_example_limitValue(int16_t value, int16_t lower_limit, int16_t upper_limit)
{
    if (value < lower_limit)
    {
        return lower_limit;
    }

    if (value > upper_limit)
    {
        return upper_limit;
    }

    return value;
}

/**
 * @brief Computes the integer average of validated samples.
 * @details Sums samples and divides by the validated sample count.
 * @param[in] pSamples Points to a validated readable sample array.
 * @param[in] sample_count Valid sample count, from 1 to EXAMPLE_MAX_SAMPLE_COUNT.
 * @return Integer average of the input samples, truncated toward zero.
 * @author Codex (ZL501 adaptation of Nan.Wang example)
 * @date 2026-10-21
 * @par Change Log
 * - 2026-11-06 | Codex | Removed source classification and clarified the average calculation.
 */
static int16_t alg_example_computeAverage(const int16_t *pSamples, size_t sample_count)
{
    /* Local Variables */
    int32_t sum = 0;
    int16_t average = 0;

    /* Main Processing */
    sum = alg_example_sumSamples(pSamples, sample_count);
    average = alg_example_divideSum(sum, (int32_t) sample_count);

    /* Cleanup and Return */
    return average;
}

/**
 * @brief Computes and limits the integer average of input samples.
 * @details Validates pointers, count and limits before calculating the bounded result.
 * @param[in] pSamples Readable array containing sample_count signed samples.
 * @param[in] sample_count Number of valid elements, from 1 to EXAMPLE_MAX_SAMPLE_COUNT.
 * @param[in] lower_limit Lowest value that may be written to pOutputValue.
 * @param[in] upper_limit Highest value that may be written to pOutputValue.
 * @param[out] pOutputValue Writable result object that must not alias pSamples.
 * @return EXAMPLE_STATUS_OK on success; otherwise a pointer, count or limit error.
 * @author Codex (ZL501 adaptation of Nan.Wang example)
 * @date 2026-10-21
 * @par Change Log
 * - 2026-11-06 | Codex | Moved the public function header from the declaration to this definition.
 */
EXAMPLE_Status alg_example_processSamples(const int16_t *pSamples,
    size_t sample_count,
    int16_t lower_limit,
    int16_t upper_limit,
    int16_t *pOutputValue)
{
    /* Local Variables */
    int16_t average = 0;

    /* Input Validation */
    if ((pSamples == NULL) || (pOutputValue == NULL))
    {
        return EXAMPLE_STATUS_NULL_POINTER;
    }

    if ((sample_count == 0U) || (sample_count > EXAMPLE_MAX_SAMPLE_COUNT))
    {
        return EXAMPLE_STATUS_INVALID_COUNT;
    }

    if (lower_limit > upper_limit)
    {
        return EXAMPLE_STATUS_INVALID_LIMITS;
    }

    /* Main Processing */
    average = alg_example_computeAverage(pSamples, sample_count);

    /* Output Assignment */
    *pOutputValue = alg_example_limitValue(average, lower_limit, upper_limit);

    /* Cleanup and Return */
    return EXAMPLE_STATUS_OK;
}
