"""
Data utilities: reading reference gene sequences (FASTA format) and
generating synthetic "patient" sequences with mutations for testing,
since real patient genomic data needs ethical clearance.
"""

import random


def read_fasta(filepath):
    sequences = {}
    header = None
    seq_chunks = []

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    sequences[header] = "".join(seq_chunks)
                header = line[1:]
                seq_chunks = []
            else:
                seq_chunks.append(line.upper())

    if header is not None:
        sequences[header] = "".join(seq_chunks)

    return sequences


def generate_mutated_sequence(reference_seq, num_mutations=3, seed=None):
    if seed is not None:
        random.seed(seed)

    bases = ["A", "T", "C", "G"]
    seq_list = list(reference_seq)
    mutation_log = []

    positions = random.sample(range(len(seq_list)), min(num_mutations, len(seq_list)))
    for pos in positions:
        original = seq_list[pos]
        new_base = random.choice([b for b in bases if b != original])
        seq_list[pos] = new_base
        mutation_log.append({
            "position": pos,
            "original_base": original,
            "mutated_base": new_base,
        })

    return "".join(seq_list), mutation_log


def write_fasta(filepath, header, sequence, line_width=70):
    with open(filepath, "w") as f:
        f.write(f">{header}\n")
        for i in range(0, len(sequence), line_width):
            f.write(sequence[i:i + line_width] + "\n")