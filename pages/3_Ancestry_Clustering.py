import streamlit as st
from style import inject_custom_css, hero_banner, stat_card_row
from distance import build_distance_matrix
from upgma import upgma

st.set_page_config(page_title="Ancestry Clustering | GenoLineage", page_icon="🗺️", layout="wide")
inject_custom_css()

with st.sidebar:
    st.markdown("### 🗺️ Module 3")
    st.caption("UPGMA Clustering — Greedy Algorithm")
    st.markdown("---")
    st.markdown("**Concepts used:**\n- Edit distance (DP)\n- Greedy clustering\n- Tree construction")

hero_banner("Ancestry Clustering", "Group DNA samples by genetic similarity to visualize ancestry relationships")

st.markdown("## 1. Sample sequences")

default_samples = {
    "Sample_A": "ATCGATCGATCGGGCTA",
    "Sample_B": "ATCGATCGATCGGGCTT",
    "Sample_C": "ATCGATCGATGGGGCTA",
    "Sample_D": "GGGGCCCCTTTTAAAAG",
    "Sample_E": "ATCGATCGATCGGGATA",
}

use_custom = st.checkbox("Edit sample sequences manually")

samples = {}
if use_custom:
    cols = st.columns(len(default_samples))
    for col, (name, seq) in zip(cols, default_samples.items()):
        with col:
            new_seq = st.text_input(name, value=seq)
            samples[name] = new_seq.upper().strip()
else:
    samples = default_samples
    cols = st.columns(len(samples))
    for col, (name, seq) in zip(cols, samples.items()):
        with col:
            st.markdown(f"**{name}**")
            st.markdown(f'<div class="seq-box">{seq}</div>', unsafe_allow_html=True)

st.markdown("---")

if st.button("🌐 Run Ancestry Clustering"):
    names, dist_matrix = build_distance_matrix(samples)

    st.markdown("## 2. Pairwise genetic distance")
    import pandas as pd
    matrix_rows = []
    for a in names:
        row = {"": a}
        for b in names:
            row[b] = 0 if a == b else dist_matrix[(a, b)]
        matrix_rows.append(row)
    df = pd.DataFrame(matrix_rows).set_index("")
    st.dataframe(df, use_container_width=True)
    st.caption("Lower number = more genetically similar = closer ancestry")

    st.markdown("## 3. Ancestry tree (UPGMA)")
    root = upgma(names, dist_matrix)

    # Build a simple text-based dendrogram for display
    def render_tree_html(node, depth=0):
        indent = "&nbsp;" * (depth * 6)
        if node.is_leaf():
            return f'<div style="color:#5eead4; font-family:monospace;">{indent}🧬 {node.name}</div>'
        html = f'<div style="color:#94a3b8; font-family:monospace;">{indent}⤷ merged at distance {node.height:.2f}</div>'
        html += render_tree_html(node.left, depth + 1)
        html += render_tree_html(node.right, depth + 1)
        return html

    st.markdown(
        f'<div class="seq-box" style="line-height:1.9;">{render_tree_html(root)}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.info(
        "Samples merging at LOWER distances share closer ancestry. Samples that "
        "only join near the root are the most genetically distant — this mirrors "
        "real founder-effect patterns (e.g. why certain mutations concentrate in "
        "specific ancestral populations)."
    )

    stat_card_row([
        (len(samples), "Samples Clustered"),
        ("O(n³)", "UPGMA Complexity"),
        (f"{len(samples)-1}", "Merge Steps"),
        ("Greedy", "Algorithm Type"),
    ])