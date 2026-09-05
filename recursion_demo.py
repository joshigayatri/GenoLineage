"""
Complexity Demonstration: Naive Recursion vs Memoized Recursion
==================================================================
This simulates asking "what is the probability of inheriting a mutation
after N generations back, combining both parental lineage contributions
at every step" -- the number of inheritance paths to check DOUBLES with
every generation (2^N paths total), which is why naive recursion blows
up exponentially while memoization keeps it linear.
"""

import time


def naive_recursive(n):
    """
    NAIVE: recomputes everything from scratch. Time complexity: O(2^n)
    """
    if n <= 1:
        return 0.5
    return 0.5 * naive_recursive(n - 1) + 0.5 * naive_recursive(n - 2)


def memoized_recursive(n, memo=None):
    """
    MEMOIZED: stores each generation's result the first time it's computed.
    Time complexity: O(n)
    """
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        result = 0.5
    else:
        result = 0.5 * memoized_recursive(n - 1, memo) + 0.5 * memoized_recursive(n - 2, memo)
    memo[n] = result
    return result


def count_naive_calls(n):
    """Counts exactly how many recursive calls naive_recursive(n) makes internally."""
    counter = {"calls": 0}

    def helper(k):
        counter["calls"] += 1
        if k <= 1:
            return 0.5
        return 0.5 * helper(k - 1) + 0.5 * helper(k - 2)

    helper(n)
    return counter["calls"]


def benchmark_comparison(generation_values):
    """
    Runs both versions across increasing generation depths and times them.
    """
    results = []

    for n in generation_values:
        start = time.perf_counter()
        naive_result = naive_recursive(n)
        naive_time = time.perf_counter() - start

        start = time.perf_counter()
        memo_result = memoized_recursive(n)
        memo_time = time.perf_counter() - start

        calls = count_naive_calls(n)

        results.append({
            "generations": n,
            "naive_time_sec": naive_time,
            "memoized_time_sec": memo_time,
            "naive_function_calls": calls,
            "result": round(naive_result, 6),
        })

    return results


def print_benchmark_table(results):
    print(f"{'Generations':<12} {'Naive Time (s)':<18} {'Memoized Time (s)':<20} {'Naive Calls':<15}")
    print("-" * 68)
    for r in results:
        print(f"{r['generations']:<12} {r['naive_time_sec']:<18.6f} "
              f"{r['memoized_time_sec']:<20.8f} {r['naive_function_calls']:<15,}")