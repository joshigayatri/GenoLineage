"""
Module 2 Demo: Pedigree Tree + Inheritance Probability
==========================================================
Run this file directly:   python main2.py
"""

from pedigree import build_sample_family, naive_inheritance_probability, \
    memoized_inheritance_probability, print_family_risk_report
from recursion_demo import benchmark_comparison, print_benchmark_table


def run_pedigree_demo():
    print("=" * 70)
    print("PART A: Family Pedigree Risk Calculation")
    print("=" * 70)

    people = build_sample_family()

    print("\nFamily tree built with the following members:")
    for name in people:
        print(f"  - {name}")

    print("\n--- Risk report (using MEMOIZED calculation) ---")
    print_family_risk_report(people, lambda p: memoized_inheritance_probability(p))

    print("\nNote: Grandpa_A is a KNOWN carrier (mutation_status=True).")
    print("Notice how the risk probability HALVES with each generation")
    print("moving away from Grandpa_A -- this matches real Mendelian")
    print("dilution of a dominant-style trait across generations.\n")


def run_complexity_demo():
    print("=" * 70)
    print("PART B: Naive Recursion vs Memoized Recursion (Complexity Analysis)")
    print("=" * 70)
    print("\nSimulating inheritance-probability calculation across increasing")
    print("numbers of generations back, comparing naive vs memoized recursion.\n")

    small_values = [5, 10, 15, 20]
    results = benchmark_comparison(small_values)
    print_benchmark_table(results)

    print("\nNow pushing further to show the naive version's exponential blowup:")
    print("(this will get noticeably slower for naive -- that's the point!)\n")

    larger_values = [25, 28, 30]
    results2 = benchmark_comparison(larger_values)
    print_benchmark_table(results2)

    print("\n--- Complexity summary for your report ---")
    print("Naive recursion:    O(2^n) time  -- calls roughly DOUBLE per generation")
    print("Memoized recursion: O(n) time    -- each generation computed exactly once")
    print("Space (memoized):   O(n)         -- one dictionary entry per generation")


if __name__ == "__main__":
    run_pedigree_demo()
    run_complexity_demo()