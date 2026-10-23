/**
 * @file alg_example.c
 * @brief Implements platform-independent bounded integer sample processing.
 *
 * This file is a teaching example for ZL501 EPR 2.1.0 and EDI 2.1.0.
 * It is not a target-DSP validation artifact.
 */

/* Copyright and license strategy: TBD; this teaching example is not a release file. */

#include "alg_example.h"

/**
 * @brief This is an Atomic Function. Adds a validated array of signed samples.
 * @details Function: alg_example_sumSamples.
 * @param[in] pSamples Points to a readable array containing count valid elements.
 * @param[in] count Number of elements to add, from 1 to EXAMPLE_MAX_SAMPLE_COUNT.
 * @return Sum of all input samples represented as int32_t.
 * @author Codex (ZL501 adaptation of Nan.Wang example)
 * @date 2026-10-21
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
 * @brief This is an Atomic Function. Divides a validated sum by a positive sample count.
 * @details Function: alg_example_divideSum.
 * @param[in] sum Signed sum to divide.
 * @param[in] divisor Positive divisor representable as int32_t.
 * @return Integer quotient truncated toward zero and representable as int16_t.
 * @author Codex (ZL501 adaptation of Nan.Wang example)
 * @date 2026-10-21
 */
static int16_t alg_example_divideSum(int32_t sum, int32_t divisor)
{
    return (int16_t) (sum / divisor);
}

/**
 * @brief This is an Atomic Function. Limits a signed value to an inclusive range.
 * @details Function: alg_example_limitValue.
 * @param[in] value Value to limit.
 * @param[in] lower_limit Inclusive lower bound.
 * @param[in] upper_limit Inclusive upper bound, not less than lower_limit.
 * @return Limited value between lower_limit and upper_limit, inclusive.
 * @author Codex (ZL501 adaptation of Nan.Wang example)
 * @date 2026-10-21
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
 * @brief This is a Composite Function. Computes an average using two Atomic Functions.
 * @details Function: alg_example_computeAverage.
 * @param[in] pSamples Points to a validated readable sample array.
 * @param[in] sample_count Valid sample count, from 1 to EXAMPLE_MAX_SAMPLE_COUNT.
 * @return Integer average of the input samples, truncated toward zero.
 * @author Codex (ZL501 adaptation of Nan.Wang example)
 * @date 2026-10-21
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

/*
 * Public contract: see alg_example.h.
 * Classification: Service Function; approved by Nan.Wang on 2026-10-21.
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
