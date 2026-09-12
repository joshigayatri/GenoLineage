"""
Maps a gene name to the disease it causes and gene-specific prevention advice.
"""

GENE_DISEASE_INFO = {
    "BRCA1": {
        "disease": "Hereditary Breast & Ovarian Cancer",
        "advice": [
            "Start mammograms/MRI screening earlier than the general population (often from age 25–30).",
            "Consider genetic counseling to discuss preventive surgery options (mastectomy/oophorectomy).",
            "Carrier screening for partner is recommended before planning children.",
        ],
    },
    "CFTR": {
        "disease": "Cystic Fibrosis",
        "advice": [
            "Both partners should undergo carrier screening before pregnancy.",
            "If both are carriers, genetic counseling can explain a 25% risk per pregnancy.",
            "Preimplantation Genetic Diagnosis (PGD) during IVF can select unaffected embryos.",
        ],
    },
    "HBB": {
        "disease": "Sickle Cell Disease / Beta-Thalassemia",
        "advice": [
            "Carrier (trait) screening is recommended, especially if there is family history.",
            "Genetic counseling helps calculate risk if both partners are carriers.",
            "Regular hematology check-ups are advised for confirmed carriers.",
        ],
    },
}


def detect_gene_from_header(header: str):
    """Looks for a known gene name inside the FASTA header text."""
    if not header:
        return None
    header_upper = header.upper()
    for gene in GENE_DISEASE_INFO:
        if gene in header_upper:
            return gene
    return None