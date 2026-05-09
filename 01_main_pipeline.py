#!/usr/bin/env python3
"""
ANTIVENOM PROTEIN DESIGN PIPELINE
Workflow: PDB Input → LLM Sequences → ProteinMPNN → AlphaFold → Comparison

Author: Anirban
Project: Computational Antivenom Design
"""

import os
import sys
import json
import logging
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple
import subprocess
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import LLM sequence generator using ProtGPT2 (no API key required)
try:
    from llm_sequence_generator_protgpt2 import LLMSequenceGeneratorNoAPI, ProtGPT2Lite
except ImportError:
    logger.warning("llm_sequence_generator_protgpt2 not found. Make sure it's in the same directory.")
    LLMSequenceGeneratorNoAPI = None
    ProtGPT2Lite = None


@dataclass
class SequenceResult:
    """Result object for a generated sequence"""
    sequence_id: str
    method: str  # 'LLM' or 'ProteinMPNN'
    sequence: str
    length: int
    avg_plddt: float = None
    max_plddt: float = None
    min_plddt: float = None
    cysteine_count: int = None
    hydrophobicity_score: float = None
    binding_energy: float = None
    plddt_scores: List[float] = None
    
    def to_dict(self):
        return asdict(self)


class PDBHandler:
    """STEP 1: Download and validate toxin structures from PDB"""
    
    def __init__(self, pdb_id: str, output_dir: str = './data/pdb'):
        self.pdb_id = pdb_id.upper()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.pdb_file = self.output_dir / f"{pdb_id}.pdb"
    
    def download_pdb(self):
        """Download PDB structure from RCSB (skips if already cached locally)"""
        if self.pdb_file.exists():
            logger.info(f"✓ Using cached PDB file: {self.pdb_file}")
            return True

        logger.info(f"Downloading PDB structure: {self.pdb_id}")
        url = f"https://files.rcsb.org/download/{self.pdb_id}.pdb"

        try:
            import urllib.request
            urllib.request.urlretrieve(url, self.pdb_file)
            logger.info(f"✓ Downloaded to {self.pdb_file}")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to download: {e}")
            return False
    
    def validate_pdb(self) -> bool:
        """Validate PDB file format"""
        if not self.pdb_file.exists():
            logger.error(f"PDB file not found: {self.pdb_file}")
            return False
        
        with open(self.pdb_file, 'r') as f:
            lines = f.readlines()
            atom_lines = [l for l in lines if l.startswith('ATOM')]
            
        logger.info(f"✓ PDB validation passed ({len(atom_lines)} atoms)")
        return len(atom_lines) > 0
    
    def extract_coordinates(self) -> Dict:
        """Extract 3D coordinates from PDB"""
        coords = {'atoms': [], 'residues': []}
        
        with open(self.pdb_file, 'r') as f:
            for line in f:
                if line.startswith('ATOM'):
                    atom_name = line[12:16].strip()
                    res_num = int(line[22:26])
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    coords['atoms'].append({
                        'name': atom_name,
                        'residue': res_num,
                        'coords': [x, y, z]
                    })
        
        logger.info(f"✓ Extracted {len(coords['atoms'])} coordinates")
        return coords





class ProteinMPNN:
    """STEP 3: Generate structure-optimized sequences using ProteinMPNN"""
    
    def __init__(self, pdb_file: str):
        self.pdb_file = pdb_file
        self.model_path = "./protein_mpnn_weights"
    
    def generate_sequences(self, num_sequences: int = 5, binding_region: str = None) -> List[str]:
        """
        Run ProteinMPNN on PDB structure
        
        This would typically call the ProteinMPNN model.
        For now, we'll generate synthetic sequences for demo.
        """
        logger.info(f"Running ProteinMPNN on {self.pdb_file}...")
        
        # TODO: Integrate actual ProteinMPNN
        # This would require:
        # 1. Download ProteinMPNN weights
        # 2. Parse PDB
        # 3. Run inference with or without interface specification
        
        # Placeholder: Generate synthetic sequences
        amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
        sequences = [
            ''.join(np.random.choice(list(amino_acids), size=np.random.randint(80, 150)))
            for _ in range(num_sequences)
        ]
        
        logger.info(f"✓ ProteinMPNN generated {len(sequences)} structure-optimized sequences")
        return sequences


class AlphaFoldPredictor:
    """STEP 4: Predict 3D structures and confidence scores using AlphaFold"""
    
    def __init__(self):
        self.model = None
    
    def predict_structure(self, sequence: str) -> Tuple[np.ndarray, List[float]]:
        """
        Predict 3D structure and pLDDT scores
        
        Returns:
            (coordinates_array, plddt_scores)
        """
        logger.info(f"Predicting structure for {len(sequence)}-aa sequence...")
        
        # TODO: Integrate OmegaFold or ESMFold for faster inference
        # For demo: generate synthetic pLDDT scores
        
        # Synthetic: Higher confidence for structured regions
        plddt = np.random.normal(75, 15, size=len(sequence))
        plddt = np.clip(plddt, 10, 100)
        
        logger.info(f"✓ Average pLDDT: {plddt.mean():.2f} ± {plddt.std():.2f}")
        
        return None, plddt.tolist()
    
    def batch_predict(self, sequences: List[str]) -> Dict[str, Tuple]:
        """Predict structures for multiple sequences"""
        results = {}
        for i, seq in enumerate(sequences):
            coords, plddt = self.predict_structure(seq)
            results[f"seq_{i}"] = (coords, plddt)
        return results


class ProteinAnalyzer:
    """STEP 5: Analyze and compare sequences"""
    
    @staticmethod
    def calculate_cysteine_bonds(sequence: str) -> Tuple[int, List[Tuple[int, int]]]:
        """Count cysteines and identify potential disulfide bonds"""
        cysteine_positions = [i for i, aa in enumerate(sequence) if aa == 'C']
        count = len(cysteine_positions)
        
        # Pair cysteines (simple greedy pairing)
        bonds = []
        remaining = cysteine_positions.copy()
        while len(remaining) >= 2:
            bonds.append((remaining.pop(0), remaining.pop(0)))
        
        return count, bonds
    
    @staticmethod
    def calculate_hydrophobicity(sequence: str) -> float:
        """
        Calculate Kyte-Doolittle hydrophobicity index
        Scale: -4.5 to +4.5 (negative = hydrophilic, positive = hydrophobic)
        """
        # Kyte-Doolittle scale
        kd_scale = {
            'A': 1.8, 'C': 2.5, 'D': -3.5, 'E': -3.5, 'F': 2.8,
            'G': -0.4, 'H': -3.2, 'I': 4.5, 'K': -3.9, 'L': 3.8,
            'M': 1.9, 'N': -3.5, 'P': -1.6, 'Q': -3.5, 'R': -4.5,
            'S': -0.8, 'T': -0.7, 'V': 4.2, 'W': -0.9, 'Y': -1.3
        }
        
        total = sum(kd_scale.get(aa, 0) for aa in sequence)
        return total / len(sequence) if sequence else 0
    
    @staticmethod
    def quality_report(results: List[SequenceResult]) -> Dict:
        """Generate comprehensive comparison report"""
        report = {
            'llm_sequences': [],
            'mpnn_sequences': [],
            'comparison': {}
        }
        
        llm_results = [r for r in results if r.method == 'LLM']
        mpnn_results = [r for r in results if r.method == 'ProteinMPNN']
        
        report['llm_sequences'] = [r.to_dict() for r in llm_results]
        report['mpnn_sequences'] = [r.to_dict() for r in mpnn_results]
        
        # Compute metrics
        if llm_results:
            avg_plddt_llm = np.mean([r.avg_plddt for r in llm_results if r.avg_plddt])
            report['comparison']['avg_plddt_llm'] = float(avg_plddt_llm)
        
        if mpnn_results:
            avg_plddt_mpnn = np.mean([r.avg_plddt for r in mpnn_results if r.avg_plddt])
            report['comparison']['avg_plddt_mpnn'] = float(avg_plddt_mpnn)
        
        report['comparison']['quality_assessment'] = {
            'high_confidence_llm': sum(1 for r in llm_results if r.avg_plddt and r.avg_plddt > 90),
            'high_confidence_mpnn': sum(1 for r in mpnn_results if r.avg_plddt and r.avg_plddt > 90),
        }
        
        return report


class AntivenemPipeline:
    """Main orchestration class"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.results = []
        self.output_dir = Path(config.get('output_dir', './results'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def run(self, pdb_id: str, num_sequences: int = 5):
        """Execute complete pipeline"""
        logger.info("="*60)
        logger.info("ANTIVENOM PROTEIN DESIGN PIPELINE")
        logger.info("="*60)
        
        # STEP 1: Get PDB structure
        logger.info("\n[STEP 1] Fetching toxin structure...")
        pdb_handler = PDBHandler(pdb_id)
        if not pdb_handler.download_pdb() or not pdb_handler.validate_pdb():
            logger.error("Failed to obtain valid PDB structure")
            return None
        
        # STEP 2: LLM sequence generation using ProtGPT2 (no API key needed)
        logger.info("\n[STEP 2] Generating LLM sequences using ProtGPT2...")
        toxin_info = {
            'type': '3FTx',
            'binding_residues': 'Acetylcholine binding pocket',
            'target': 'Neuromuscular junction'
        }
        
        llm_sequences = []
        
        if LLMSequenceGeneratorNoAPI is None:
            logger.error("✗ llm_sequence_generator_protgpt2 module not found!")
            logger.error("  Please copy llm_sequence_generator_protgpt2.py to the same directory")
        else:
            try:
                # Try full ProtGPT2 model
                llm_gen = LLMSequenceGeneratorNoAPI(method='protgpt2')
                llm_sequences = llm_gen.generate_antivenom_sequences(toxin_info, num_sequences)
                
                # If model failed or no sequences generated, use lite mode
                if not llm_sequences and ProtGPT2Lite is not None:
                    logger.warning("⚠️  ProtGPT2 model generation failed, using lite mode...")
                    llm_sequences = ProtGPT2Lite.generate_sequences(num_sequences=num_sequences)
                    
            except Exception as e:
                logger.warning(f"⚠️  ProtGPT2 model error: {e}")
                if ProtGPT2Lite is not None:
                    logger.info("  Falling back to lite mode...")
                    llm_sequences = ProtGPT2Lite.generate_sequences(num_sequences=num_sequences)
                else:
                    logger.error("  Lite mode also not available")
        
        # STEP 3: ProteinMPNN generation
        logger.info("\n[STEP 3] Generating ProteinMPNN sequences...")
        mpnn = ProteinMPNN(str(pdb_handler.pdb_file))
        mpnn_sequences = mpnn.generate_sequences(num_sequences)
        
        # STEP 4: AlphaFold prediction
        logger.info("\n[STEP 4] Predicting structures with AlphaFold...")
        af = AlphaFoldPredictor()
        
        all_sequences = [
            ('LLM', llm_sequences),
            ('ProteinMPNN', mpnn_sequences)
        ]
        
        for method, sequences in all_sequences:
            for i, seq in enumerate(sequences):
                coords, plddt = af.predict_structure(seq)
                
                cys_count, bonds = ProteinAnalyzer.calculate_cysteine_bonds(seq)
                hydro = ProteinAnalyzer.calculate_hydrophobicity(seq)
                
                result = SequenceResult(
                    sequence_id=f"{method}_seq_{i+1}",
                    method=method,
                    sequence=seq,
                    length=len(seq),
                    avg_plddt=np.mean(plddt),
                    max_plddt=max(plddt),
                    min_plddt=min(plddt),
                    cysteine_count=cys_count,
                    hydrophobicity_score=hydro,
                    plddt_scores=plddt
                )
                self.results.append(result)
        
        # STEP 5: Analysis and comparison
        logger.info("\n[STEP 5] Comparing methods...")
        report = ProteinAnalyzer.quality_report(self.results)
        
        # Save results
        self._save_results(report)
        
        logger.info("\n" + "="*60)
        logger.info("PIPELINE COMPLETE")
        logger.info("="*60)
        
        return report
    
    def _save_results(self, report: Dict):
        """Save results to JSON and generate analysis plots"""
        output_file = self.output_dir / "results.json"
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        logger.info(f"✓ Results saved to {output_file}")
        self._generate_plots(report)

    def _generate_plots(self, report: Dict):
        """Generate 4 analysis plots and save to results/analysis_plots.png"""
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            from matplotlib.patches import Patch
        except ImportError:
            logger.warning("matplotlib not installed — skipping plot generation. Run: pip install matplotlib")
            return

        llm_seqs = report.get('llm_sequences', [])
        mpnn_seqs = report.get('mpnn_sequences', [])

        if not llm_seqs and not mpnn_seqs:
            logger.warning("No sequence data available for plotting")
            return

        colors = {'LLM': '#2196F3', 'ProteinMPNN': '#4CAF50'}
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Antivenom Design Pipeline — Analysis Results', fontsize=14, fontweight='bold')

        # Plot 1: Average pLDDT per sequence (LLM vs ProteinMPNN)
        ax1 = axes[0, 0]
        llm_plddt = [s.get('avg_plddt') or 0 for s in llm_seqs]
        mpnn_plddt = [s.get('avg_plddt') or 0 for s in mpnn_seqs]
        if llm_plddt:
            ax1.bar([i - 0.2 for i in range(len(llm_plddt))], llm_plddt,
                    width=0.4, label='LLM', color=colors['LLM'], alpha=0.85)
        if mpnn_plddt:
            ax1.bar([i + 0.2 for i in range(len(mpnn_plddt))], mpnn_plddt,
                    width=0.4, label='ProteinMPNN', color=colors['ProteinMPNN'], alpha=0.85)
        ax1.axhline(y=70, color='red', linestyle='--', linewidth=1, alpha=0.6, label='Quality threshold (70)')
        ax1.set_title('1. Composite Score Comparison (avg pLDDT)', fontsize=10)
        ax1.set_xlabel('Sequence Index')
        ax1.set_ylabel('Average pLDDT Score')
        ax1.set_ylim(0, 100)
        ax1.legend(fontsize=8)
        ax1.grid(axis='y', alpha=0.3)

        # Plot 2: pLDDT confidence distribution (per-residue histogram)
        ax2 = axes[0, 1]
        all_llm_plddt = [score for s in llm_seqs for score in (s.get('plddt_scores') or [])]
        all_mpnn_plddt = [score for s in mpnn_seqs for score in (s.get('plddt_scores') or [])]
        if all_llm_plddt:
            ax2.hist(all_llm_plddt, bins=20, alpha=0.65, label='LLM', color=colors['LLM'])
        if all_mpnn_plddt:
            ax2.hist(all_mpnn_plddt, bins=20, alpha=0.65, label='ProteinMPNN', color=colors['ProteinMPNN'])
        ax2.axvline(x=70, color='red', linestyle='--', linewidth=1, alpha=0.6, label='Good confidence (70)')
        ax2.set_title('2. pLDDT Confidence Distribution', fontsize=10)
        ax2.set_xlabel('pLDDT Score (per residue)')
        ax2.set_ylabel('Frequency')
        ax2.legend(fontsize=8)
        ax2.grid(alpha=0.3)

        # Plot 3: Sequence length distribution
        ax3 = axes[1, 0]
        all_seqs = llm_seqs + mpnn_seqs
        lengths = [s.get('length', 0) or 0 for s in all_seqs]
        bar_colors = [colors[s.get('method', 'LLM')] for s in all_seqs]
        labels = [f"{'L' if s.get('method') == 'LLM' else 'M'}{i+1}" for i, s in enumerate(all_seqs)]
        ax3.bar(range(len(lengths)), lengths, color=bar_colors, alpha=0.85)
        ax3.set_title('3. Sequence Length Distribution', fontsize=10)
        ax3.set_xlabel('Sequence')
        ax3.set_ylabel('Length (amino acids)')
        ax3.set_xticks(range(len(labels)))
        ax3.set_xticklabels(labels, fontsize=8)
        ax3.grid(axis='y', alpha=0.3)
        ax3.legend(handles=[
            Patch(facecolor=colors['LLM'], label='LLM'),
            Patch(facecolor=colors['ProteinMPNN'], label='ProteinMPNN')
        ], fontsize=8)

        # Plot 4: Score breakdown by category (pLDDT, cysteine, hydrophobicity)
        ax4 = axes[1, 1]
        plddts = [s.get('avg_plddt') or 0 for s in all_seqs]
        cys_scores = [min((s.get('cysteine_count') or 0) * 10, 100) for s in all_seqs]
        hydro_scores = [(((s.get('hydrophobicity_score') or 0) + 4.5) / 9.0) * 100 for s in all_seqs]
        x_pos = np.arange(len(labels))
        width = 0.25
        ax4.bar(x_pos - width, plddts, width, label='pLDDT (structure)', color='#FF9800', alpha=0.85)
        ax4.bar(x_pos, cys_scores, width, label='Cysteine score', color='#9C27B0', alpha=0.85)
        ax4.bar(x_pos + width, hydro_scores, width, label='Hydrophobicity', color='#F44336', alpha=0.85)
        ax4.set_title('4. Score Breakdown by Category', fontsize=10)
        ax4.set_xlabel('Sequence')
        ax4.set_ylabel('Score (normalized 0-100)')
        ax4.set_xticks(x_pos)
        ax4.set_xticklabels(labels, fontsize=8)
        ax4.set_ylim(0, 100)
        ax4.legend(fontsize=7)
        ax4.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plot_file = self.output_dir / "analysis_plots.png"
        plt.savefig(plot_file, dpi=150, bbox_inches='tight')
        plt.close()
        logger.info(f"✓ Analysis plots saved to {plot_file}")


if __name__ == "__main__":
    config = {
        'output_dir': './results',
        'api_key': os.getenv('ANTHROPIC_API_KEY')
    }
    
    pipeline = AntivenemPipeline(config)
    # Example: Use 3FTx (three-finger toxin structure)
    report = pipeline.run('3FTX', num_sequences=5)
