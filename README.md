# COMPLETE SETUP & EXECUTION GUIDE
## Antivenom Protein Design Pipeline (ProtGPT2-Based)
## 📋 TABLE OF CONTENTS

1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [File Organization](#file-organization)
4. [Automatic Downloads (What You Don't Need to Do)](#automatic-downloads)
5. [Configuration](#configuration)
6. [Running the Pipeline](#running-the-pipeline)
7. [Understanding the Output](#understanding-the-output)
8. [Troubleshooting](#troubleshooting)

---

## 🖥️ SYSTEM REQUIREMENTS

### Hardware
- **CPU**: Intel/AMD processor (4 cores minimum)
- **RAM**: 8 GB minimum (16 GB recommended)
- **Storage**: 20 GB free space (for models & results)
- **GPU**: Optional but 10x faster (NVIDIA CUDA recommended)

### Software
- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Internet**: Required for first run (downloads models & PDB files)

---

## 💾 INSTALLATION STEPS

### STEP 1: Install Python

**Windows:**
1. Download Python from https://www.python.org/downloads/
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"

**macOS/Linux:**
```bash
# Already installed, verify:
python3 --version
# Should show Python 3.8+
```

### STEP 2: Create Working Directory

```bash
# Create folder for your project
mkdir antivenom_pipeline
cd antivenom_pipeline
```

### STEP 3: Download All Files

Download these files and place them in your `antivenom_pipeline` folder:

**Core Pipeline Code:**
- `01_main_pipeline.py`
- `llm_sequence_generator_protgpt2.py`
- `02_docking_analysis.py`
- `03_metrics_analysis.py`
- `04_results_dashboard.html`

**Configuration:**
- `requirements_protgpt2.txt`
- `config.yaml`

**Optional (for reference):**
- `PROTGPT2_SETUP.md`
- `PIPELINE_VISUALIZATION.html`
- `PIPELINE_VISUALIZATION_INTERACTIVE.html`

### STEP 4: Set Up Virtual Environment (Recommended)

```bash
# Navigate to your folder
cd antivenom_pipeline

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# You should see (venv) at the start of your terminal
```

### STEP 5: Install Dependencies

```bash
# Install all required packages
pip install -r requirements_protgpt2.txt
```

**Installation takes:** 5-10 minutes (first time)

### STEP 6: Verify Installation

```bash
# Check Python packages installed
pip list

# Should show:
# - transformers
# - torch
# - numpy
# - scipy
# - etc.
```

### STEP 7: For GPU Support (Optional but Recommended)

If you have NVIDIA GPU:

```bash
# Install GPU version of PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify GPU:
python -c "import torch; print(torch.cuda.is_available())"
# Should print: True
```

**Result:** 10x faster sequence generation!

---

## 📁 FILE ORGANIZATION

Your folder structure should look like:

```
antivenom_pipeline/
├── venv/                              (Created by step 4)
├── data/                              (Auto-created on first run)
│   └── pdb/                           (Auto-downloads PDB files here)
├── results/                           (Auto-created on first run)
│   ├── results.json                   (Generated after running)
│   └── analysis_plots.png             (Generated after running)
├── 01_main_pipeline.py                (Download this)
├── llm_sequence_generator_protgpt2.py (Download this)
├── 02_docking_analysis.py             (Download this)
├── 03_metrics_analysis.py             (Download this)
├── 04_results_dashboard.html          (Download this)
├── requirements_protgpt2.txt          (Download this)
├── config.yaml                        (Download this)
├── PROTGPT2_SETUP.md                  (Optional reference)
├── PIPELINE_VISUALIZATION.html        (Optional, for viewing diagram)
└── PIPELINE_VISUALIZATION_INTERACTIVE.html (Optional, interactive diagram)
```

---

## ⚙️ AUTOMATIC DOWNLOADS

### You DON'T Need to Manually Download These:

#### 1. ProtGPT2 Model
**What it is:** Language model trained on protein sequences (1.2 GB)

**Automatic Download:**
```
✅ Happens automatically on first run
✅ Downloaded to: ~/.cache/huggingface/models/
✅ Takes: 2-5 minutes (first time only)
✅ Subsequent runs: Instant (uses cached model)
```

**How it works:**
- First time you run the pipeline, it downloads from Hugging Face
- Stores in cache folder
- All future runs use the cached version

#### 2. PDB Files (Toxin Structures)
**What it is:** 3D structure of venom toxins

**Automatic Download:**
```
✅ Happens automatically on first run
✅ Downloaded to: ./data/pdb/
✅ Takes: 1-5 seconds per file
✅ Example: 3FTX.pdb (snake toxin structure)
```

**How it works:**
- Pipeline automatically downloads from RCSB PDB
- Stores in your local `data/pdb/` folder
- You can use any valid PDB ID

---

## ⚙️ CONFIGURATION

### Edit config.yaml (Optional)

The `config.yaml` file has default settings. Only edit if you want to change:

```yaml
# Default settings (no changes needed for first run):

pipeline:
  pdb_id: "3FTX"              # Toxin ID (can change to 1BTX, 2BQQ, etc.)
  num_sequences: 5            # Number of sequences to generate
  output_dir: "./results"     # Where to save results

alphafold:
  use_gpu: true               # Set to false if no GPU available
  model_name: "esm_fold"      # Fast model
```

### You Don't Need to Change Anything!

The defaults are perfect for first run. Just leave it as is.

---

## 🚀 RUNNING THE PIPELINE

### Method 1: Simple Command Line (Recommended)

```bash
# Make sure you're in the antivenom_pipeline folder
cd antivenom_pipeline

# Activate virtual environment (if created)
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Run the pipeline
python 01_main_pipeline.py
```

### Expected Output:

```
============================================================
ANTIVENOM PROTEIN DESIGN PIPELINE
============================================================

[STEP 1] Fetching toxin structure...
Downloading PDB structure: 3FTX
✓ Downloaded to ./data/pdb/3FTX.pdb
✓ PDB validation passed (1234 atoms)

[STEP 2] Generating LLM sequences using ProtGPT2...
Loading ProtGPT2 model from nferruz/ProtGPT2...
Using device: cuda (GPU detected!)
✓ ProtGPT2 model loaded successfully
Generating 5 antivenom sequences using ProtGPT2...
  Sequence 1: MKTLCCGRT... (45 aa)
  Sequence 2: MLSCAVQKP... (42 aa)
  Sequence 3: MVSTGCSVQ... (38 aa)
  Sequence 4: MKTLVFVVW... (51 aa)
  Sequence 5: MCCCGGNLL... (40 aa)
✓ Generated 5 valid sequences

[STEP 3] Generating ProteinMPNN sequences...
✓ ProteinMPNN generated 5 structure-optimized sequences

[STEP 4] Predicting structures with AlphaFold...
Predicting structure for 45-aa sequence...
✓ Average pLDDT: 78.5 ± 3.2
... (continues for all 10 sequences)

[STEP 5] Comparing methods...
✓ Results saved to ./results/results.json

============================================================
PIPELINE COMPLETE
============================================================
```

### Execution Time:

| Mode | Time | Speed |
|------|------|-------|
| **GPU** | 10-15 minutes | ⚡ Fastest |
| **CPU** | 25-35 minutes | 🐢 Medium |
| **CPU (no model)** | 5-10 minutes | ⚡ Fast (lite mode) |

### Method 2: Step-by-Step in Python

If you want more control:

```python
# Open a Python terminal
python

# Then run:
from main_pipeline import AntivenemPipeline

config = {
    'output_dir': './results',
    'api_key': None  # No API key needed!
}

pipeline = AntivenemPipeline(config)

# Run with default toxin (3FTX)
report = pipeline.run('3FTX', num_sequences=5)

# Or use different toxin:
# report = pipeline.run('1BTX', num_sequences=5)
# report = pipeline.run('2BQQ', num_sequences=5)
```

---

## 📊 UNDERSTANDING THE OUTPUT

### Generated Files:

#### 1. results/results.json
**What it is:** Complete data in JSON format

**Contains:**
```json
{
  "llm_sequences": [
    {
      "sequence_id": "LLM_seq_1",
      "sequence": "MKTLCCGRT...",
      "length": 45,
      "avg_plddt": 78.5,
      "composite_score": 69.9,
      ...
    }
  ],
  "mpnn_sequences": [...],
  "comparison": {
    "avg_plddt_llm": 78.3,
    "avg_plddt_mpnn": 85.0,
    "quality_assessment": {...}
  }
}
```

**Use:** Import into Excel, Python, or other tools

#### 2. results/analysis_plots.png
**What it is:** Visualization charts showing comparison

**Contains:** 4 plots
- Composite score comparison
- pLDDT confidence distribution
- Sequence length distribution
- Score breakdown by category

#### 3. 04_results_dashboard.html
**What it is:** Interactive web visualization

**How to use:**
```bash
# Open in web browser
# Windows: Double-click 04_results_dashboard.html
# macOS/Linux: open 04_results_dashboard.html

# Or in browser: File → Open → Select the file
```

**Features:**
- 6 interactive tabs
- Real-time charts
- Method comparison
- Sequence details
- Export functionality

### Interpreting Results:

**Composite Score (0-100):**
- 80-100: Excellent candidate
- 70-80: Good candidate
- 60-70: Acceptable
- <60: Poor candidate

**pLDDT Scores (0-100):**
- >90: Very high confidence
- 70-90: Good confidence
- <70: Low confidence (unreliable)

**Winner:**
- ProteinMPNN usually wins (structure-optimized)
- LLM offers diversity
- Compare and choose based on your needs

---

## 🔧 TROUBLESHOOTING

### Issue 1: "No module named 'transformers'"

**Solution:**
```bash
pip install transformers
```

### Issue 2: "No module named 'torch'"

**Solution (CPU only):**
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

**Solution (GPU):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Issue 3: "PDB Download Failed"

**Solution:**
```
- Check internet connection
- Wait 30 seconds and try again
- Verify PDB ID is valid (e.g., 3FTX, 1BTX, 2BQQ)
- Use VPN if behind firewall
```

### Issue 4: "Model Download Failed"

**Solution:**
```
- First run downloads ~1.2 GB (5-10 minutes)
- Check disk space (need 20 GB free)
- Try again later if slow internet
- Lite mode auto-activates if model fails
```

### Issue 5: "CUDA Error" or "GPU Not Found"

**Solution:**
```bash
# The code automatically falls back to CPU
# Just wait for CPU processing (slower)
# Or check GPU installation:
python -c "import torch; print(torch.cuda.is_available())"
```

### Issue 6: Out of Memory (RAM)

**Solution:**
```bash
# Reduce number of sequences:
# Change in 01_main_pipeline.py:
# report = pipeline.run('3FTX', num_sequences=3)  # Instead of 5
```

### Issue 7: "AttributeError" or Code Errors

**Solution:**
```bash
# Make sure ALL files are in the same folder:
ls -la
# Should show:
# - 01_main_pipeline.py
# - llm_sequence_generator_protgpt2.py
# - 02_docking_analysis.py
# - 03_metrics_analysis.py
# - config.yaml
# - requirements_protgpt2.txt
```

---

## 📝 STEP-BY-STEP CHECKLIST

### Before Running:

- [ ] Python 3.8+ installed
- [ ] Created folder `antivenom_pipeline`
- [ ] Downloaded all 6 code files
- [ ] Downloaded config files
- [ ] Created virtual environment (venv)
- [ ] Activated virtual environment
- [ ] Installed dependencies: `pip install -r requirements_protgpt2.txt`
- [ ] Verified installation: `pip list`
- [ ] (Optional) Installed GPU support

### First Run:

- [ ] Navigate to folder: `cd antivenom_pipeline`
- [ ] Activate venv
- [ ] Run pipeline: `python 01_main_pipeline.py`
- [ ] Wait for completion (10-35 minutes)
- [ ] Check results in `results/` folder
- [ ] Open `04_results_dashboard.html` in browser

### After First Run:

- [ ] View results/results.json
- [ ] Open dashboard (much faster - no downloads)
- [ ] Try different toxin: `python 01_main_pipeline.py` (modify pdb_id)
- [ ] Generate more sequences: Increase `num_sequences` in code
- [ ] Export results for analysis

---

## 🎯 COMMON QUESTIONS

### Q: Do I need to download ProtGPT2?
**A:** NO. It downloads automatically on first run.

### Q: Do I need to download the PDB file?
**A:** NO. It downloads automatically on first run.

### Q: Do I need an API key?
**A:** NO. ProtGPT2 is completely local.

### Q: Can I use a different toxin?
**A:** YES. Change `'3FTX'` to any valid PDB ID (e.g., `'1BTX'`, `'2BQQ'`).

### Q: How long does it take?
**A:** 10-15 min (GPU) or 25-35 min (CPU). First run downloads models, subsequent runs are faster.

### Q: Can I run without GPU?
**A:** YES. Works on CPU but is 10x slower.

### Q: What if internet fails during download?
**A:** Pipeline automatically retries. If it fails, lite mode (patterns-based) activates.

### Q: Can I run multiple times?
**A:** YES. Subsequent runs are much faster (no re-downloads).

### Q: How much disk space needed?
**A:** 20 GB free (models + results).

### Q: Windows, macOS, or Linux?
**A:** All supported. Same process, just different activation commands.

---

## ✅ SUMMARY: WHAT YOU NEED TO DO

### MANUAL TASKS:
1. ✅ Install Python
2. ✅ Create working folder
3. ✅ Download 6 code files
4. ✅ Install dependencies: `pip install -r requirements_protgpt2.txt`
5. ✅ Run: `python 01_main_pipeline.py`

### AUTOMATIC TASKS (Pipeline Handles):
1. ✅ Download ProtGPT2 model (auto)
2. ✅ Download PDB file (3FTX) (auto)
3. ✅ Load models into memory (auto)
4. ✅ Generate sequences (auto)
5. ✅ Predict structures (auto)
6. ✅ Compute metrics (auto)
7. ✅ Create results (auto)

### RESULT:
- ✅ results.json (all metrics)
- ✅ analysis_plots.png (visualizations)
- ✅ 04_results_dashboard.html (interactive dashboard)

---

## 🚀 READY TO START?

Follow this order:

```
1. Install Python
   ↓
2. Create folder & download files
   ↓
3. Create virtual environment
   ↓
4. pip install -r requirements_protgpt2.txt
   ↓
5. python 01_main_pipeline.py
   ↓
6. Wait 10-35 minutes
   ↓
7. Check results/ folder
   ↓
8. Open dashboard in browser
   ↓
9. Done! ✅
```

---

## 📞 STILL STUCK?

Check these files for more details:
- `PROTGPT2_SETUP.md` - Detailed setup guide
- `README.md` - Full documentation
- `PIPELINE_VISUALIZATION_INTERACTIVE.html` - See pipeline diagram

---

**You're ready to design antivenoms!** 🧬🐍🚀

