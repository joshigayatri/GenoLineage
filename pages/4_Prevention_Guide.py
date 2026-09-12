import streamlit as st
from style import inject_custom_css, hero_banner
from gene_info import GENE_DISEASE_INFO

st.set_page_config(page_title="Prevention Guide | GenoLineage", page_icon="🛡️", layout="wide")
inject_custom_css()

with st.sidebar:
    st.markdown("### 🛡️ Prevention Guide")
    st.caption("Real-world pathways to reduce transmission risk")

hero_banner("Prevention Pathways", "Once a mutation and inheritance risk are identified, these are the real, established medical routes to reduce transmission")

st.warning("⚠️ This page is for academic/informational purposes only. It is not medical advice — always consult a certified genetic counselor or physician.")

# ---------------- Disease-specific recommendation block ----------------
detected_gene = st.session_state.get("detected_gene")
detected_mutations = st.session_state.get("detected_mutations")

if detected_gene and detected_mutations:
    info = GENE_DISEASE_INFO[detected_gene]
    st.markdown(
        f"""
        <div class="hero-banner" style="margin-top:10px;">
            <h3 style="margin-bottom:6px;">🧬 Based on your result: {detected_gene} — {info['disease']}</h3>
            <p style="color:#94a3b8;">{len(detected_mutations)} mutation(s) detected in this gene.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("#### Specific recommendations")
    for point in info["advice"]:
        st.markdown(f"- {point}")
    st.markdown("---")
    st.markdown("#### General pathways (still applicable)")
elif detected_mutations is not None:
    st.info("No specific gene match found for detected mutations — showing general prevention pathways below.")
else:
    st.info("Run **Mutation Detection** first to see disease-specific recommendations here. General pathways are shown below.")

# ---------------- General pathways (existing content) ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="stat-card" style="text-align:left; height:260px;">
            <h3>🧪 Carrier Screening</h3>
            <p style="color:#94a3b8; font-size:14px;">
            A test done before or during early pregnancy to check if both
            partners carry the same recessive mutation. If both are carriers,
            genetic counseling can outline the exact risk to future children.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="stat-card" style="text-align:left; height:260px;">
            <h3>👩‍⚕️ Genetic Counseling</h3>
            <p style="color:#94a3b8; font-size:14px;">
            A specialist reviews family history and test results to calculate
            precise probability trees for a couple's children, and explains
            all available options in plain language.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="stat-card" style="text-align:left; height:260px;">
            <h3>🔬 PGD (Preimplantation Genetic Diagnosis)</h3>
            <p style="color:#94a3b8; font-size:14px;">
            During IVF, embryos are tested for the specific mutation before
            implantation, allowing only unaffected embryos to be selected —
            an established clinical method for monogenic disorders.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown(
    """
    ### Why prevention ≠ DNA editing
    This project does not modify DNA. Editing inherited (germline) DNA in humans
    remains experimental and ethically restricted. Instead, real prevention works
    by **informed reproductive choices** — knowing the risk in advance through
    screening, and choosing a path (natural conception with counseling, PGD, or
    donor options) that avoids passing on a known, serious mutation.
    """
)