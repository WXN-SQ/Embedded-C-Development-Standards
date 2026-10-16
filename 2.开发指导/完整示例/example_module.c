/**
 * @file example_module.c
 * @brief Implements platform-independent bounded integer sample processing.
 *
 * This file is a teaching example for EPR 1.0.1 and EDI 1.0.1.
 * It is not a target-DSP validation artifact.
 */

/* Copyright and license strategy: TBD; this teaching example is not a release file. */

#include "example_module.h"

/**
 * @brief This is an Atomic Function. Adds a validated array of signed samples.
 * @param[in] samples Points to a readable array containing count valid elements.
 * @param[in] count Number of elements to add, from 1 to EXAMPLE_MAX_SAMPLE_COUNT.
 * @return Sum of all input samples represented as int32_t.
 * @author Nan.Wang
 */
static int32_t EXAMPLE_sum_samples(const int16_t *samples, size_t count)
{
    int32_t sum = 0;
    size_t index = 0U;

    for (index = 0U; index < count; ++index)
    {
        sum += (int32_t) samples[index];
    }

    return sum;
}

/**
 * @brief This is an Atomic Function. Divides a validated sum by a positive sample count.
 * @param[in] sum Signed sum to divide.
 * @param[in] divisor Positive divisor representable as int32_t.
 * @return Integer quotient truncated toward zero and representable as int16_t.
 * @author Nan.Wang
 */
static int16_t EXAMPLE_divide_sum(int32_t sum, int32_t divisor)
{
    return (int16_t) (sum / divisor);
}

/**
 * @brief This is an Atomic Function. Limits a signed value to an inclusive range.
 * @param[in] value Value to limit.
 * @param[in] lower_limit Inclusive lower bound.
 * @param[in] upper_limit Inclusive upper bound, not less than lower_limit.
 * @return Limited value between lower_limit and upper_limit, inclusive.
 * @author Nan.Wang
 */
static int16_t EXAMPLE_limit_value(int16_t value, int16_t lower_limit, int16_t upper_limit)
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
 * @param[in] samples Points to a validated readable sample array.
 * @param[in] sample_count Valid sample count, from 1 to EXAMPLE_MAX_SAMPLE_COUNT.
 * @return Integer average of the input samples, truncated toward zero.
 * @author Nan.Wang
 */
static int16_t EXAMPLE_compute_average(const int16_t *samples, size_t sample_count)
{
    /* Local Variables */
    int32_t sum = 0;
    int16_t average = 0;

    /* Main Processing */
    sum = EXAMPLE_sum_samples(samples, sample_count);
    average = EXAMPLE_divide_sum(sum, (int32_t) sample_count);

    /* Cleanup and Return */
    return average;
}

/*
 * Public contract: see example_module.h.
 * Classification: Service Function; human review status is Approved.
 */
EXAMPLE_Status EXAMPLE_process_samples(const int16_t *samples,
    size_t sample_count,
    int16_t lower_limit,
    int16_t upper_limit,
    int16_t *output_value)
{
    /* Local Variables */
    int16_t average = 0;

    /* Input Validation */
    if ((samples == NULL) || (output_value == NULL))
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
    average = EXAMPLE_compute_average(samples, sample_count);

    /* Output Assignment */
    *output_value = EXAMPLE_limit_value(average, lower_limit, upper_limit);

    /* Cleanup and Return */
    return EXAMPLE_STATUS_OK;
}
