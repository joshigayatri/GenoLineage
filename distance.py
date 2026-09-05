"""
Module 3 - Part 1: Pairwise Genetic Distance Calculation
============================================================
"""


def edit_distance(seq1, seq2):
    """
    Computes minimum edits needed to turn seq1 into seq2.
    Same DP-table idea as Needleman-Wunsch (Module 1).
    Time complexity: O(m * n)
    """
    m, n = len(seq1), len(seq2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],
                    dp[i][j - 1],
                    dp[i - 1][j - 1],
                )

    return dp[m][n]


def build_distance_matrix(sequences):
    names = list(sequences.keys())
    matrix = {}

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            dist = edit_distance(sequences[a], sequences[b])
            matrix[(a, b)] = dist
            matrix[(b, a)] = dist

    return names, matrix


def print_distance_matrix(names, matrix):
    print(f"{'':12s}" + "".join(f"{n:12s}" for n in names))
    for a in names:
        row = f"{a:12s}"
        for b in names:
            d = 0 if a == b else matrix[(a, b)]
            row += f"{d:<12d}"
        print(row)
