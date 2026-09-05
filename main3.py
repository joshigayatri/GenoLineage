"""
Module 3 Demo: Ancestry Clustering via UPGMA
================================================
Run this file directly:   python main3.py
"""

from distance import build_distance_matrix, print_distance_matrix
from upgma import upgma, print_tree


def run_ancestry_demo():
    print("=" * 70)
    print("STEP 1: Sample DNA sequences (simulating different ancestries)")
    print("=" * 70)

    samples = {
        "Sample_A": "ATCGATCGATCGGGCTA",
        "Sample_B": "ATCGATCGATCGGGCTT",
        "Sample_C": "ATCGATCGATGGGGCTA",
        "Sample_D": "GGGGCCCCTTTTAAAAG",
        "Sample_E": "ATCGATCGATCGGGATA",
    }

    for name, seq in samples.items():
        print(f"  {name}: {seq}")
    print()

    print("=" * 70)
    print("STEP 2: Compute pairwise genetic distance (edit distance, DP)")
    print("=" * 70)
    names, dist_matrix = build_distance_matrix(samples)
    print_distance_matrix(names, dist_matrix)
    print()
    print("(Smaller number = more genetically similar = likely closer ancestry)")
    print()

    print("=" * 70)
    print("STEP 3: Run UPGMA clustering to build the ancestry tree")
    print("=" * 70)
    root = upgma(names, dist_matrix)
    print_tree(root)
    print()

    print("=" * 70)
    print("STEP 4: Interpretation")
    print("=" * 70)
    print("Samples that merge together at a LOWER distance are more closely")
    print("related (closer ancestry). Samples that only merge near the root")
    print("of the tree are the most genetically distant from everyone else.")
    print()
    print("Complexity note for your report:")
    print("UPGMA time complexity: O(n^3) for this straightforward implementation")


if __name__ == "__main__":
    run_ancestry_demo()