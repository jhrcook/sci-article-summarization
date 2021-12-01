# The origins and genetic interactions of KRAS mutations are allele- and tissue-specific

summarization method: TEXTRANK

## Introduction

Importantly, the activating alleles found in KRAS vary substantially across cancers, indicating possible differences in signaling behavior of the mutant proteins that exploit the environment of the specific cellular context,.
Likely as a consequence of their distinct properties, associations have been uncovered between the specific KRAS mutation status and therapeutic responses and clinical outcomes of cancer patients,.
Thus far, the hypothesis has been that the different biological properties of the mutant KRAS alleles are the cause of these clinical distinctions.
Here, we study the origins of KRAS mutations to assess the extent to which tissue-specific mutational processes determined the allelic distribution.

## Results

Across all the alleles, KRAS was most frequently mutated in PAAD (86%), followed by COAD (41%), LUAD (35%), and MM (22%; Fig. 1a).
Within each cancer type, the relative abundance of the mutational signatures was generally consistent across tumor samples, regardless of the KRAS allele (Fig. 1c).
Some instances of differential mutational signature composition between tumor samples with different KRAS alleles were identified, though they tended to be differences in magnitude of the signatures, not their presence or absence (Supplementary Fig. 2).
Thus, for each cancer, the allelic frequency of KRAS was not caused primarily by distinct compositions of mutational processes in individual tumors.
To discern if specific mutagenic processes were more likely to have caused particular KRAS alleles, the trinucleotide context of the KRAS mutation and the relative activity of the mutational signature in that tumor were used to calculate the probability that the allele in an individual tumor was caused by any detectable mutational process (Fig. 1d).
In LUAD, the KRAS G12A/C/V mutations were primarily attributable to mutations caused by tobacco smoke, whereas KRAS G12D mutations were most likely attributable to clock-like mutations (Fig. 1d and Supplementary Fig. 3b).
The extent to which mutational signatures represent the mechanism driving KRAS allelic diversity was further analyzed by calculating the predicted frequency of each allele based on the frequency of mutations in the same trinucleotide context throughout the exome or genome (Fig. 2a and Supplementary Data 6).
The null hypothesis tested was that, assuming the cancer would acquire a KRAS mutation and one of the common alleles (found in >3% of the tumor samples for a given cancer) was sufficient, the frequency of the KRAS alleles would be determined by the mutational processes alone.
Another approach to examine the impact of mutagenic processes on allele specificity was to compare the probability of obtaining a certain KRAS mutation between tumor samples with the specific mutation, a different KRAS mutation, or WT KRAS (Fig. 2b).
In most cases, tumors samples with a specific KRAS allele did not, on average, have a higher probability of obtaining that mutation than other tumors of the same cancer type.
Interestingly, the KRAS G12V mutation in COAD is likely to be caused by mutational signature SBS8 (Fig. 1d, and Supplementary Figs.
The increased probability of a KRAS G12C mutation in tumor samples that did obtain the allele compared to KRAS WT LUAD tumor samples is likely due to the strong association between this mutation and signature SBS4 induced by carcinogens in tobacco smoke.
The comutation interactions between each KRAS allele and every other mutated gene were investigated using a one-sided Fisher’s exact test of association to identify increased rates of comutation and a test for mutual exclusivity proposed by Leiserson et al.
The result of the comutation analysis on COAD tumors was a weakly connected network of the KRAS alleles with only a few genes linking the alleles together (Fig. 3a).
Contrary to a common assumption, while KRAS and TP53 were frequently found mutated in the same tumor, there was a detectable reduction in comutation between TP53 with KRAS G12D and G13D compared to the rest of the alleles (Fig. 3b).
However, specifically testing for comutation between KRAS alleles, and the most common PIK3CA mutations did not reveal any strong preferences for particular activating PIK3CA mutations.
The KRAS allele-specific comutation network uncovered in LUAD was far larger than that of COAD (Supplementary Fig. 5a).
As in the network derived from COAD, many of these genes were involved in integral KRAS signaling pathways, including an increased comutation interaction between KRAS G12A and MAP2K3, a reduced comutation interaction between KRAS G12D and ERBB4, and a very strong increased rate of comutation between KRAS G12C and STK11 (Supplementary Fig. 5b).
From this limited scope, it was discovered that NRAS had reduced comutation with KRAS G12D, Q61L, and Q61R, but one of the highest rates of comutation (18.5%) with KRAS Q61H, the most common KRAS mutation in MM (Supplementary Fig. 6).
Interestingly, this was just below the rate of NRAS mutation in KRAS WT tumors (23.6%), suggesting that the signaling of the Q61H allele is fundamentally different from the other KRAS mutations in MM, especially G12D.
The KRAS allele comutation network found in the PAAD tumor samples demonstrated that many genes had detectable comutation interactions with multiple alleles, primarily of reduced comutation (Supplementary Fig. 7a).
There were many notable cellular functions and processes enriched in the comutation networks of the KRAS alleles (Fig. 3c), including the protein–protein interaction networks (PPIN) of SMAD1-3 and TGF-\(\beta\) signaling.
While these SMAD gene sets were related, the underlying comutation interactions that drove the enrichment were different for each KRAS allele (Fig. 3f).
It is important to note that many of the comutation interactions identified from this allele-specific analysis were not identified from a gene-level analysis that disregards the KRAS allele information (Supplementary Data 9).
The analysis was restricted to KRAS alleles for which there were at least three different cell lines with the mutation, limiting the following investigation to only COAD and PAAD cell lines.
For example, genes involved in ERBB4 signaling tended to have a weaker lethal effect when knocked out in cell lines with KRAS G12V mutations than in KRAS G12D, G13D, or WT cell lines (Fig. 4b).
Similarly, the cell lines with KRAS G12V mutations were less sensitive to the knockout of genes implicated in cellular senescence (Supplementary Fig. 9d).
In these cell lines, 130 individual genes demonstrated KRAS allele-specific genetic dependency (Supplementary Fig. 10a and Supplementary Data 11).
To address this hypothesis, we constructed linear models for the dependency score of each gene with allele-specific dependency that included a coefficient for the previously linked KRAS allele and a coefficient for the mutation of each gene in its comutation network.
If TP53 mutations induce a stronger dependency on STARD9, the reduced frequency of comutation between TP53 and KRAS G12D would cause the opposite effect to be ascribed to the G12D allele.
Because of the reduced comutation interaction between KRAS G12D and SMAD4 in PAAD, the effects of knocking out these genes can be ascribed to an allele-specific effect or to the SMAD4 mutation.

## Discussion

To investigate allele-specific genetic properties, we conducted statistical tests to identify patterns of comutating genes and genetic dependencies for each KRAS allele in each cancer.
However, allele-specific genetic interactions were not consistent between tissues, demonstrating the complex relationship between the tissue-of-origin, KRAS function, and cooperating genetic events.
The KRAS allele-specific comutation analysis indicates that the various KRAS mutations act within distinct genetic environments.
The principle of this phenomenon was demonstrated by the analysis of the CRISPR-Cas9 screen, when the comutation events were included as explanatory covariates: in several instances, the allele-specific dependency originally assigned to a specific KRAS mutation could instead be attributed to an allele-specific co-mutant gene.
Thus, we provide evidence that not only do the biological properties of the KRAS alleles contribute to their effect on the tumor, but so too do their unique genetic interactions.
