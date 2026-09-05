import streamlit as st
from style import inject_custom_css, hero_banner, stat_card_row
from alignment import needleman_wunsch, smith_waterman, find_mutation_positions
from data_utils import read_fasta, generate_mutated_sequence

st.set_page_config(page_title="Mutation Detection | GenoLineage", page_icon="🧫", layout="wide")
inject_custom_css()

with st.sidebar:
    st.markdown("### 🧫 Module 1")
    st.caption("Sequence Alignment — Dynamic Programming")
    st.markdown("---")
    st.markdown("**Algorithms used:**\n- Needleman-Wunsch (global)\n- Smith-Waterman (local)")

hero_banner("Mutation Detection", "Align a patient DNA sample against a reference gene to locate disease-linked mutations")

# ---------------- Input section ----------------
st.markdown("## 1. Choose input")

input_mode = st.radio(
    "How would you like to provide the reference sequence?",
    ["Use built-in sample", "Upload a FASTA file", "Paste sequence manually"],
    horizontal=True,
)

reference_seq = None
header = "Manual input"

if input_mode == "Use built-in sample":
    try:
        sequences = read_fasta("sample_reference.fasta")
        header, reference_seq = list(sequences.items())[0]
        st.success(f"Loaded: {header}")
    except FileNotFoundError:
        st.error("sample_reference.fasta not found in this folder.")

elif input_mode == "Upload a FASTA file":
    uploaded = st.file_uploader("Upload reference FASTA file", type=["fasta", "fa", "txt"])
    if uploaded is not None:
        content = uploaded.read().decode("utf-8")
        lines = content.strip().split("\n")
        header = lines[0].lstrip(">")
        reference_seq = "".join(lines[1:]).upper()
        st.success(f"Loaded: {header} ({len(reference_seq)} bases)")

else:
    manual_seq = st.text_area("Paste reference DNA sequence (A, T, C, G only)", height=120)
    if manual_seq.strip():
        reference_seq = "".join(manual_seq.split()).upper()
        header = "Manual sequence"

st.markdown("## 2. Patient sample")

patient_mode = st.radio(
    "Patient sequence source",
    ["Auto-generate synthetic patient (for demo)", "Paste patient sequence manually"],
    horizontal=True,
)

patient_seq = None
num_mutations = 3

if patient_mode == "Auto-generate synthetic patient (for demo)":
    num_mutations = st.slider("Number of mutations to inject", 1, 10, 3)
else:
    manual_patient = st.text_area("Paste patient DNA sequence", height=120)
    if manual_patient.strip():
        patient_seq = "".join(manual_patient.split()).upper()

st.markdown("---")

run = st.button("🔬 Run Alignment", use_container_width=False)

if run:
    if not reference_seq:
        st.error("Please provide a reference sequence first.")
        st.stop()

    if patient_mode == "Auto-generate synthetic patient (for demo)":
        patient_seq, true_mutations = generate_mutated_sequence(reference_seq, num_mutations=num_mutations, seed=None)
        with st.expander("Ground-truth mutations injected (for verification)"):
            for m in true_mutations:
                st.write(f"Position {m['position']}: {m['original_base']} → {m['mutated_base']}")

    if not patient_seq:
        st.error("Please provide a patient sequence.")
        st.stop()

    import time
    start = time.perf_counter()
    aligned_ref, aligned_patient, score, dp = needleman_wunsch(reference_seq, patient_seq)
    elapsed = time.perf_counter() - start

    detected = find_mutation_positions(aligned_ref, aligned_patient)

    st.markdown("## 3. Results")

    stat_card_row([
        (score, "Alignment Score"),
        (len(detected), "Mutations Found"),
        (f"{elapsed*1000:.2f} ms", "Runtime"),
        (f"{(len(reference_seq)+1)*(len(patient_seq)+1):,}", "DP Cells"),
    ])

    st.markdown("")
    st.markdown("### Detected mutations")
    if detected:
        st.table([
            {"Position": m["position"], "Reference": m["reference_base"], "Patient": m["patient_base"]}
            for m in detected
        ])
    else:
        st.success("No mutations detected — sequences match.")

    with st.expander("View full aligned sequences"):
        st.markdown("**Reference (aligned):**")
        st.markdown(f'<div class="seq-box">{aligned_ref}</div>', unsafe_allow_html=True)
        st.markdown("**Patient (aligned):**")
        st.markdown(f'<div class="seq-box">{aligned_patient}</div>', unsafe_allow_html=True)

    st.markdown("### Local alignment demo (Smith-Waterman)")
    motif_len = min(15, len(reference_seq))
    default_motif = reference_seq[10:10+motif_len] if len(reference_seq) > 25 else reference_seq[:motif_len]
    motif = st.text_input("Motif to search for inside the reference sequence", value=default_motif)
    if motif:
        aligned_seq, aligned_motif, sw_score, _ = smith_waterman(reference_seq, motif)
        c1, c2 = st.columns(2)
        c1.metric("Best local match score", sw_score)
        c2.markdown(f"**Matched region:**\n<div class='seq-box'>{aligned_seq}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        f"**Complexity note:** Needleman-Wunsch builds a DP matrix of size "
        f"({len(reference_seq)+1} × {len(patient_seq)+1}), giving **O(m·n)** time "
        f"and space complexity."
    )