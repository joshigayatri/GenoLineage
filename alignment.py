"""
Module 1: Sequence Alignment (Dynamic Programming)
=====================================================
Implements Needleman-Wunsch (GLOBAL alignment) and Smith-Waterman (LOCAL alignment)
completely from scratch, using a 2D Dynamic Programming matrix + traceback.
"""

MATCH_SCORE = 1
MISMATCH_PENALTY = -1
GAP_PENALTY = -2


def _score(a, b):
    return MATCH_SCORE if a == b else MISMATCH_PENALTY


def needleman_wunsch(seq1, seq2):
    m, n = len(seq1), len(seq2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        dp[i][0] = dp[i - 1][0] + GAP_PENALTY
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j - 1] + GAP_PENALTY

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            diagonal = dp[i - 1][j - 1] + _score(seq1[i - 1], seq2[j - 1])
            up = dp[i - 1][j] + GAP_PENALTY
            left = dp[i][j - 1] + GAP_PENALTY
            dp[i][j] = max(diagonal, up, left)

    aligned1, aligned2 = [], []
    i, j = m, n
    while i > 0 and j > 0:
        current = dp[i][j]
        diagonal = dp[i - 1][j - 1] + _score(seq1[i - 1], seq2[j - 1])
        up = dp[i - 1][j] + GAP_PENALTY

        if current == diagonal:
            aligned1.append(seq1[i - 1])
            aligned2.append(seq2[j - 1])
            i -= 1
            j -= 1
        elif current == up:
            aligned1.append(seq1[i - 1])
            aligned2.append('-')
            i -= 1
        else:
            aligned1.append('-')
            aligned2.append(seq2[j - 1])
            j -= 1

    while i > 0:
        aligned1.append(seq1[i - 1])
        aligned2.append('-')
        i -= 1
    while j > 0:
        aligned1.append('-')
        aligned2.append(seq2[j - 1])
        j -= 1

    aligned1.reverse()
    aligned2.reverse()

    return ''.join(aligned1), ''.join(aligned2), dp[m][n], dp


def smith_waterman(seq1, seq2):
    m, n = len(seq1), len(seq2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    best_score = 0
    best_pos = (0, 0)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            diagonal = dp[i - 1][j - 1] + _score(seq1[i - 1], seq2[j - 1])
            up = dp[i - 1][j] + GAP_PENALTY
            left = dp[i][j - 1] + GAP_PENALTY
            dp[i][j] = max(0, diagonal, up, left)

            if dp[i][j] > best_score:
                best_score = dp[i][j]
                best_pos = (i, j)

    aligned1, aligned2 = [], []
    i, j = best_pos
    while i > 0 and j > 0 and dp[i][j] != 0:
        current = dp[i][j]
        diagonal = dp[i - 1][j - 1] + _score(seq1[i - 1], seq2[j - 1])
        up = dp[i - 1][j] + GAP_PENALTY

        if current == diagonal:
            aligned1.append(seq1[i - 1])
            aligned2.append(seq2[j - 1])
            i -= 1
            j -= 1
        elif current == up:
            aligned1.append(seq1[i - 1])
            aligned2.append('-')
            i -= 1
        else:
            aligned1.append('-')
            aligned2.append(seq2[j - 1])
            j -= 1

    aligned1.reverse()
    aligned2.reverse()

    return ''.join(aligned1), ''.join(aligned2), best_score, dp


def find_mutation_positions(aligned_ref, aligned_patient):
    mutations = []
    for idx, (r, p) in enumerate(zip(aligned_ref, aligned_patient)):
        if r != p:
            mutations.append({
                "position": idx,
                "reference_base": r,
                "patient_base": p,
            })
    return mutations


def print_dp_matrix(seq1, seq2, dp):
    header = "     " + "   ".join(['-'] + list(seq2))
    print(header)
    for i, row in enumerate(dp):
        label = '-' if i == 0 else seq1[i - 1]
        print(f"{label}  " + "  ".join(f"{val:3d}" for val in row))