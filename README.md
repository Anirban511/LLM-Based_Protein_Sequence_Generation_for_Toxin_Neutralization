# Antivenom_Synthesis_using_Deep_learning
-Fine-tuned transformer-based protein language models (ProtGPT2/ESM2) on curated venom toxin datasets (UniProt) using HuggingFace, achieving low perplexity (~8–12) and strong sequence learning convergence.

-Generated novel protein sequences conditioned on toxin-binding motifs and evaluated structural feasibility via AlphaFold/ColabFold with >80% of candidates showing stable folds (pLDDT > 70).

-Ranked candidates using biochemical heuristics (hydrophobicity, cysteine content, stability indices) and docking simulations (AutoDock/Rosetta), achieving top candidate binding affinity improvements of ~20–30% over baseline sequences
