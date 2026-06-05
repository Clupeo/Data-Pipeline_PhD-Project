# PhD Data Analysis Pipeline - Jupyter Notebook Suite

This interactive Jupyter notebook pipeline analyzes microalgae–bacteria consortia with a specific focus on sinking properties and community composition. The project is part of the doctoral thesis **[Characterization of floc-forming and fast-sedimenting microalgae-bacteria consortia in bioremediation](https://macau.uni-kiel.de/receive/macau_mods_00005694)** by **Dr. Cedric Hering-Peter**, conducted at the Plant Cell Physiology and Biotechnology group, Kiel University (2021–2025).

> **Note on Data Scope:** This repository showcases the full analytical workflow using example data. Due to large file sizes, raw metagenomic sequencing (NGS) data is excluded. However, the complete pipeline structure and additional manual example outputs are included for verification.

---

## Prerequisites

Before you start, ensure you have:

- **Python 3.10+** - Download from [python.org](https://www.python.org/)
- **Git** - For cloning the repository
- **Jupyter Lab or VS Code** - For running notebooks

---

## Quick Start Guide

```bash
# 1. Clone repository
git clone https://github.com/yourusername/phd-data-analysis-pipeline.git
cd phd-data-analysis-pipeline

# 2. Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configure dataset mode
# Edit analysis_config.yaml at the root:
# Set data_mode: "example" for showcase (default) 
# Set data_mode: "full" for complete local dataset (online offline)

# 4. Run the analysis
# Open 02_Data-Analysis/02_Workspace/notebooks/ in Jupyter/VS Code
# Select the 'venv' kernel and execute notebooks in order
# OR
python 02_Data-Analysis/02_Workspace/run_example_pipeline.py

# 5. Done! Check output
ls outputs/  # Example outputs available immediately; Full outputs generated upon execution
```

---

## Project Structure

```bash
phd-data-analysis-pipeline/
│
├── 01_Instrument-Data/             Data layer
│   ├── 00_Example-Data/            Showcase data (in repository)
│   └── [01–16]*/                   Full instrument data (local,gitignored)
│       └── ...                     *Requires local access
│
├── 02_Data-Analysis/               Core Analysis Layer
│   └── 02_Workspace/
│       ├── notebooks/              11 specialized analysis notebooks
│       ├── scripts/                data_helper.py, plot_helper.py, constants.py
│       ├── data/
│       │   └── meta_data.csv       Experiment metadata
│       └── images/                 Generated plots
│
├── 03_Output/                      Results layer
│   ├── 00_Example-Output/          Preview outputs (in repository)
│   └── [generated outputs]         Full pipeline results (local)
│
├── analysis_config.yaml            Configuration switch (Example ↔ Full)
└── requirements.txt                Python dependencies
```

---

## Notebook Modules

The pipeline consists of 11 specialized notebooks, each targeting a specific scientific dimension:

| Module | Purpose | Data Requirement |
|---|---|---|
| **Meta-Data** | Experiment metadata overview & validation | All |
| **Recovery-Rates** | Photometer sedimentation recovery (%) | All |
| **Sinking-Velocities** | FlowCam sinking rates (m/h) distribution | All |
| **Particle-Sizes** | Particle size distribution (µm) analysis | All |
| **Zeta-Potentials** | Surface charge (mV) characterization | All |
| **Suspended-Solids** | TSS/VSS gravimetric analysis | All |
| **Sinking-Properties** | Combined radar plots for multi-variate view | All |
| **Taxa-Distribution** | NGS community heatmaps | **Full Only** |
| **Taxa-Variance** | NGS PCA analysis & variance decomposition | **Full Only** |
| **Data-Statistics** | ANOVA / t-test across measurements | **Full Only** |
| **EPS-Analysis** | Extracellular polymeric substances quantification | **Full Only** |

---

## Common Workflow

### Update Analysis & Republish

```bash
# 1. Update Data
# Place new raw data into 01_Instrument-Data/[Experiment_ID]/
# OR update meta_data.csv with new experiment details

# 2. Re-run Pipeline
# Switch to desired mode in analysis_config.yaml
# Execute notebooks sequentially in 02_Data-Analysis/02_Workspace/notebooks/

# When prompted for missing files, check path configuration

# 3. Export Results
# (Save Notebook as HTML/PDF or export plots manually)

# 4. Republish
# (Push updated example outputs to GitHub for portfolio refresh)
```

---

## Visual & Reporting Style

The pipeline employs a cohesive scientific visualization scheme to ensure clarity and reproducibility across publications and portfolios.

| Category | Visualization Type | Key Metrics |
|----------|-------------------|-------------|
| Physical Properties | Boxplots | Particle Size, Sinking Velocity, Recovery Rate, Zeta Potential |
| Community Dynamics | Heatmaps & PCA | Taxa abundance, Variance explained |
| Process Efficiency | Bar & Line Charts | Suspended Solids |
| Statistical Validation | Table & Error Bars | P-values, Confidence Intervals |

### Usage Guidelines:

Maintain consistent color palettes across all notebooks for cross-referencing.
Include error bars for all quantitative biological measurements.
Ensure axis labels include units (e.g., m/h, µm, %) for immediate readability.

---

## Version Info

- Last Updated: June, 2026
- Status: Released
- Python: 3.10+
- Jupyter: Compatible with Lab & VS Code
- Data: Example (Remote), Full (Local)

---

## License

This project is personal research work. Feel free to adapt for academic or portfolio use.

---