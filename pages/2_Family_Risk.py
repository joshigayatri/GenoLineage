import streamlit as st
from style import inject_custom_css, hero_banner, stat_card_row, risk_tag
from pedigree import build_sample_family, memoized_inheritance_probability
from recursion_demo import benchmark_comparison

st.set_page_config(page_title="Family Risk | GenoLineage", page_icon="🌳", layout="wide")
inject_custom_css()

with st.sidebar:
    st.markdown("### 🌳 Module 2")
    st.caption("Pedigree Tree — Recursion + Memoization")
    st.markdown("---")
    st.markdown("**Concepts used:**\n- Tree data structure\n- Recursive Mendelian probability\n- Memoization (DP)")

hero_banner("Family Inheritance Risk", "Build a pedigree and calculate how a known mutation propagates through generations")

st.markdown("## 1. Family pedigree")

people = build_sample_family()

st.markdown(
    """
    <div class="seq-box" style="font-size:14px; line-height:2;">
    Grandpa_A (carrier) ─┬─ Grandma_A (clean)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    Grandpa_B (clean) ─┬─ Grandma_B (clean)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Parent_1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Parent_2<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──────┬──────┘<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Child_1 ── Spouse (clean)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Child_2<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Grandchild_1
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("## 2. Calculated risk per family member")

rows = []
for name, person in people.items():
    if person.mutation_status is not None:
        pct = 100.0 if person.mutation_status else 0.0
        label = "Known carrier" if person.mutation_status else "Known clean"
    else:
        pct = memoized_inheritance_probability(person) * 100
        label = "Calculated"
    rows.append((name, pct, label))

cols = st.columns(5)
for i, (name, pct, label) in enumerate(rows):
    with cols[i % 5]:
        st.markdown(
            f"""
            <div class="stat-card" style="margin-bottom:12px;">
                <div style="font-size:13px; color:#94a3b8;">{name}</div>
                <div style="margin-top:6px;">{risk_tag(pct)}</div>
                <div style="font-size:11px; color:#64748b; margin-top:4px;">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("")
st.info("Notice how risk approximately halves with each generation moving away from the known carrier (Grandpa_A) — this reflects real Mendelian dilution across generations.")

st.markdown("---")
st.markdown("## 3. Naive Recursion vs Memoization — Complexity Proof")
st.caption("This is the core algorithmic argument of Module 2: memoization turns an exponential-time calculation into a linear-time one.")

gen_choice = st.select_slider(
    "Compare naive vs memoized recursion up to how many generations back?",
    options=[10, 15, 20, 25, 28, 30],
    value=25,
)

if st.button("⚡ Run complexity benchmark"):
    with st.spinner("Running naive recursion (this may take a few seconds at higher values)..."):
        results = benchmark_comparison([10, 15, 20, gen_choice])

    naive_times = [r["naive_time_sec"] * 1000 for r in results]
    memo_times = [r["memoized_time_sec"] * 1000 for r in results]
    labels = [str(r["generations"]) for r in results]

    st.markdown("### Runtime comparison (milliseconds)")
    chart_data = {
        "Generations": labels,
        "Naive (ms)": naive_times,
        "Memoized (ms)": memo_times,
    }
    import pandas as pd
    df = pd.DataFrame(chart_data).set_index("Generations")
    st.bar_chart(df)

    last = results[-1]
    speedup = last["naive_time_sec"] / last["memoized_time_sec"] if last["memoized_time_sec"] > 0 else float("inf")
    stat_card_row([
        (f"{last['generations']}", "Generations"),
        (f"{last['naive_function_calls']:,}", "Naive Function Calls"),
        (f"{last['naive_time_sec']*1000:.2f} ms", "Naive Time"),
        (f"{speedup:,.0f}×", "Memoized Speedup"),
    ])