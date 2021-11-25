#!/usr/bin/env python3

"""Entrypoint to summarization functions."""

from enum import Enum
from typing import Any, Callable, Optional

from typer import Typer

from src.bart_summarization import summarize as bart_summarize
from src.pagerank_summarization import summarize as pagerange_summarize

app = Typer()


class SummarizationMethod(Enum):
    """Available summarization method."""

    TEXTRANK = "TEXTRANK"
    BART = "BART"
    GPT3 = "GPT3"


summarization_callable = Callable[[str, dict[str, Any]], str]

summarization_callables: dict[SummarizationMethod, summarization_callable] = {
    SummarizationMethod.TEXTRANK: pagerange_summarize,
    SummarizationMethod.BART: bart_summarize,
}


def summarize(
    method: SummarizationMethod, text: str, **kwargs: Optional[dict[str, Any]]
) -> str:
    """Summarize text with a specific method.

    Args:
        method (SummarizationMethod): Summarization method.
        text (str): Text to summarize.

    Raises:
        NotImplementedError: Method not yet implemented.

    Returns:
        str: Summary.
    """
    fxn = summarization_callables.get(method)
    if fxn is None:
        raise NotImplementedError(method.value)
    return fxn(text, kwargs)


test_text = """
Located at a critical signaling junction between extracellular growth receptors and
pro-growth pathways, KRAS is one of the most commonly mutated genes in cancer1,2.
However, it is frequently mutated in only a handful of cancers, with the highest
frequencies in colorectal adenocarcinoma (COAD), lung adenocarcinoma (LUAD), multiple
myeloma (MM), and pancreatic adenocarcinoma (PAAD). Importantly, the activating alleles
found in KRAS vary substantially across cancers, indicating possible differences in
signaling behavior of the mutant proteins that exploit the environment of the specific
cellular context3,4.
When mutated at one of its four hotspot codons—12, 13, 61, or 146—activated KRAS protein
hyperactivates many downstream effector pathways, such as the MAPK and PI3K-AKT
signaling pathways1. Previous studies have documented substantial differences in the
biochemical and signaling properties of the common KRAS variants (reviewed by Miller et
al.5 and Li et al.6). KRAS normally operates as a molecular switch, activating
downstream pathways when GTP-bound, but inactive when GDP-bound following the hydrolysis
of the 𝛾
γ-phosphate. This reaction is catalyzed by GTPase-activating proteins (GAPs), while the
exchange of the GDP for a new GTP is facilitated by guanine nucleotide exchange factors
(GEFs)7. Activating KRAS mutations result in elevated engagement of downstream pathways
by increasing the steady-state levels of GTP-bound KRAS. Specifically, mutations to
codons 12, 13, and 61 reduce the rate of intrinsic and/or GAP-mediated hydrolysis, and
mutations at 13 and 61, but not 12, also enhance the rate of nucleotide exchange8,9.
Alternatively, 146 mutations do not alter the rate of GTP hydrolysis, but cause
hyperactivation through an increased rate of GDP exchange4,10,11,12. Additional
biochemical, structural, and signaling distinctions have been identified between
different mutant alleles, including between those at the same amino acid position4,8,13,
14,15,16,17,18,19,20.
Likely as a consequence of their distinct properties, associations have been uncovered
between the specific KRAS mutation status and therapeutic responses and clinical
outcomes of cancer patients3,6. For instance, a retrospective meta-analysis suggested
that COAD tumors with a KRAS G13D allele were sensitive to anti-EGFR therapies, a
treatment generally discouraged for KRAS-mutant tumors21. It has recently been proposed,
via computational and experimental means, that differential interaction kinetics between
KRAS G13D and the Ras GAP NF-1 explain this effect22,23,24. Another example is that the
KRAS G12D allele is associated with worse overall survival in advanced PAAD, when
compared to patients with WT KRAS, KRAS G12R, or KRAS G12V25. Thus far, the hypothesis
has been that the different biological properties of the mutant KRAS alleles are the
cause of these clinical distinctions. However, it is also possible that allele-specific
genetic interactions drive the varying clinical outcomes.
"""


@app.command()
def main() -> None:
    """Run the summarization methods."""
    for method in SummarizationMethod:
        method_msg = f"Summarization method: '{method.value}'"
        print(method_msg)
        print("-" * len(method_msg))
        res = summarize(method=method, text=test_text)
        print(res)
        print("-" * 80 + "\n")
    return None


if __name__ == "__main__":
    app()
