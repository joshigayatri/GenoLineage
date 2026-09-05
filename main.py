"""
Module 1 Demo: Sequence Alignment for Mutation Detection
============================================================
"""

import time
from alignment import needleman_wunsch, smith_waterman, find_mutation_positions, print_dp_matrix
from data_utils import read_fasta, generate_mutated_sequence, write_fasta


def run_demo():
    print("=" * 70)
    print("STEP 1: Load reference sequence from FASTA")
    print("=" * 70)
    sequences = read_fasta("brca1_real.fasta")
    header, reference_seq = list(sequences.items())[0]
    print(f"Header: {header}")
    print(f"Reference sequence ({len(reference_seq)} bases):\n{reference_seq}\n")

    print("=" * 70)
    print("STEP 2: Generate a synthetic 'patient' sequence with mutations")
    print("=" * 70)
    patient_seq, true_mutations = generate_mutated_sequence(
        reference_seq, num_mutations=3, seed=42
    )
    print(f"Patient sequence  ({len(patient_seq)} bases):\n{patient_seq}\n")
    print("Ground-truth mutations we introduced (for verification):")
    for mut in true_mutations:
        print(f"  Position {mut['position']}: "
              f"{mut['original_base']} -> {mut['mutated_base']}")
    print()

    print("=" * 70)
    print("STEP 3: Run Needleman-Wunsch (global alignment)")
    print("=" * 70)
    start = time.perf_counter()
    aligned_ref, aligned_patient, score, dp = needleman_wunsch(reference_seq, patient_seq)
    elapsed = time.perf_counter() - start

    print(f"Alignment score : {score}")
    print(f"Time taken      : {elapsed:.6f} seconds")
    print(f"Reference : {aligned_ref}")
    print(f"Patient   : {aligned_patient}")
    print()

    print("=" * 70)
    print("STEP 4: Detect mutation positions from the alignment")
    print("=" * 70)
    detected = find_mutation_positions(aligned_ref, aligned_patient)
    print(f"Detected {len(detected)} mutation(s):")
    for mut in detected:
        print(f"  Position {mut['position']}: "
              f"reference={mut['reference_base']}  patient={mut['patient_base']}")
    print()

    print("=" * 70)
    print("STEP 5: Smith-Waterman demo (local alignment / motif search)")
    print("=" * 70)
    motif = "GGAAAAGGCCAGC"
    aligned_seq, aligned_motif, sw_score, _ = smith_waterman(reference_seq, motif)
    print(f"Searching for motif: {motif}")
    print(f"Best local match score: {sw_score}")
    print(f"Matched region in reference : {aligned_seq}")
    print(f"Motif alignment              : {aligned_motif}")
    print()

    print("=" * 70)
    print("STEP 6: Complexity note for your report")
    print("=" * 70)
    m, n = len(reference_seq), len(patient_seq)
    print(f"Needleman-Wunsch DP matrix size: {m+1} x {n+1} = {(m+1)*(n+1)} cells")
    print("Time complexity: O(m * n)   |   Space complexity: O(m * n)")
    print()

    write_fasta("sample_patient.fasta", "Synthetic_patient_1", patient_seq)
    print("Saved synthetic patient sequence to sample_patient.fasta")


if __name__ == "__main__":
    run_demo()