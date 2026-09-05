import streamlit as st
from style import inject_custom_css, hero_banner, stat_card_row

st.set_page_config(
    page_title="GenoLineage | Hereditary Disease Analyzer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()

# ---------------- Sidebar branding ----------------
with st.sidebar:
    st.markdown("### 🧬 GenoLineage")
    st.caption("DNA-Based Hereditary Disease\nPrediction & Prevention System")
    st.markdown("---")
    st.markdown("**Use the pages above** to navigate through each module.")
    st.markdown("---")
    st.caption("Design & Analysis of Algorithms\nProject · B.Tech ENTC")

# ---------------- Hero ----------------
hero_banner(
    "GenoLineage",
    "Detecting hereditary disease mutations, predicting inheritance risk, "
    "and mapping ancestry — powered by classical Dynamic Programming, "
    "Recursion, and Greedy algorithms."
)

st.markdown("")

# ---------------- Top stats ----------------
stat_card_row([
    ("3", "Core Modules"),
    ("O(mn)", "Alignment Complexity"),
    ("O(n)", "Memoized Recursion"),
    ("O(n³)", "UPGMA Clustering"),
])

st.markdown("")
st.markdown("## How this system works")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="stat-card" style="text-align:left; height:230px;">
            <span class="badge badge-dp">Dynamic Programming</span>
            <h3 style="margin-top:14px;">🧫 Mutation Detection</h3>
            <p style="color:#94a3b8; font-size:14px;">
            Aligns a DNA sample against known disease-gene references using
            Needleman-Wunsch and Smith-Waterman to pinpoint exact mutation
            positions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="stat-card" style="text-align:left; height:230px;">
            <span class="badge badge-rec">Recursion + Memoization</span>
            <h3 style="margin-top:14px;">🌳 Family Risk</h3>
            <p style="color:#94a3b8; font-size:14px;">
            Builds a pedigree tree and calculates the probability that a
            known mutation is passed down to children and grandchildren,
            following Mendelian inheritance rules.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="stat-card" style="text-align:left; height:230px;">
            <span class="badge badge-greedy">Greedy Clustering</span>
            <h3 style="margin-top:14px;">🗺️ Ancestry Mapping</h3>
            <p style="color:#94a3b8; font-size:14px;">
            Groups DNA samples by genetic similarity using UPGMA, showing
            which ancestries are closely related and explaining why some
            diseases cluster in specific populations.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("")
st.markdown("---")
st.markdown(
    """
    ### Why this matters
    Disease-causing mutations are inherited through fixed chromosomal patterns —
    autosomal dominant, autosomal recessive, X-linked, or mitochondrial. Certain
    mutations also concentrate within specific ancestral populations through
    founder effects (e.g. sickle cell trait in West African ancestry, Tay-Sachs
    in Ashkenazi Jewish ancestry). This system detects, predicts, and explains
    that risk — then points toward real prevention pathways such as carrier
    screening, genetic counseling, and preimplantation genetic diagnosis (PGD).

    **👈 Use the sidebar to explore each module.**
    """
)

st.info("⚠️ This tool is for academic demonstration only and does not provide medical advice.")