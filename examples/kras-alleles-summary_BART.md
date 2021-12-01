# The origins and genetic interactions of KRAS mutations are allele- and tissue-specific

summarization method: BART

## Introduction

Located at a critical signaling junction between extracellular growth receptors and pro-growth pathways, KRAS is one of the most commonly mutated genes in cancer. It is frequently mutated in only a handful of cancers, with the highest frequencies in colorectal adenocarcinoma. Activating KRAS mutations result in elevated engagement of downstream pathways.

## Results

### KRAS alleles are non-uniformly distributed across cancers

This study utilized publicly available sequencing data from COAD, LUAD, MM, and PAAD. KRAS was most frequently mutated in PAAD (86%), followed by COAD (41%), LUAD (35%), and MM (22%) At the allele level, most mutations by single-nucleotide substitutions occurred at one of four “hotspot” codons: 12, 13, 61, and 146.

### The KRAS alleles have different mutagenic origins

One potential explanation for the distinct allelic frequencies across cancer types is that tissue-specific mutational processes determine the frequency distribution. To explore this hypothesis, we used mutational signatures to map the mutational spectrum in tumor samples. The most common in COAD, MM, and PAAD, were the “clock-like” single base substitution (SBS) signatsures SBS1 and SBS5. LUAD was uniquely enriched for a mutational signature of exogenous cause, tobacco smoke carcinogens.

### The frequency of most KRAS alleles cannot be solely attributed to the prevalence of detected mutagens

The frequencies of the KRAS alleles were best predicted in MM, with an exception for the most frequent allele, Q61H, which was dramatically underestimated. In PAAD, the G12R mutation is expected to occur in 5.2% of PAAD tumors, which is far below the actual frequency of 16.7%. The Pearson correlations between the observed and predicted KRAS allele frequencies for each cancer ranged from 0.4 to 0.6 (or 0.7–0.9 when restricted to just G12) In most cases, tumors samples with a specific KRAS allele did not, on average, have a higher probability of obtaining that mutation than other tumors of the same cancer type. This was not true for KRAS G12V in COAD and KRas G12C in LUAD (Wilcoxon rank-sum test, FDR-adjusted p value < 0.05). Interestingly, the KRASG12V

### The KRAS alleles have distinct comutation networks

KRAS G12V had an increased rate of comutation with TCF7L2, which encodes TCF4, a regulator of Wnt signaling often dysregulated in COAD, specifically the R488C mutation. Several KRAS alleles had reduced comutations with NRAS and BRAF, and increased comutations with APC and PIK3CA. The comutation network of the G13D allele was enriched in genes implicated in apoptosis and senescence. The KRAS allele-specific comutation network uncovered in LUAD was far larger than that of COAD (Supplementary Fig. 5a) This was likely caused by the higher mutation frequency in this cancer, increasing the statistical power to detect both increased and reduced comutation interactions. There were several intriguing cellular processes enriched in the LUAD networks for each allele.

### KRAS allele-specific genetic dependencies reveal potential synthetic lethal vulnerabilities

KRAS alleles have measurably different signaling behaviors and genetic interactions. We used data from a genome-wide, CRISPR/Cas9 knockout screen of cancer cell lines to identify genes with KRAS allele-specific genetic dependencies. KRAS alleles with a sufficient number of cell lines were G12D, G12R, and G12V. GSEA revealed substantial differences in the dependencies of critical cellular pathways. In these cell lines, 130 individual genes demonstrated KRAS allele-specific genetic dependency.

## Discussion

Study addresses the genetic complexity of cancer through a genetic interaction analysis of oncogenic KRAS alleles in COAD, LUAD, MM, and PAAD. Measuring the levels of mutational signatures revealed that the cancer-specific distributions of KRAS mutations were influenced, but not determined, by the active mutational processes in the tumor samples. This study has broad implications for the understanding of oncogene biology and for cancer therapy. Whether a targeted therapy directly inhibits the activated oncoprotein or not, it is important to understand
