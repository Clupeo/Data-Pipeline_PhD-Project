# PhD Data Analysis Pipeline: Microbial Ecology Research

A comprehensive data analysis pipeline for PhD research on how environmental factors (light, temperature, salinity, pH, antibiotics) affect microorganisms and their physical properties.

## Project Overview

This project analyzes experimental data from microbial ecology studies, investigating the effects of various environmental conditions on microorganism behavior and physical properties. The pipeline is built with **Jupyter notebooks** for interactive analysis and **Python helper scripts** for reusable utilities. All analysis outputs are publication-ready visualizations and statistical results.

## Project Structure

```
.
├── notebooks/              # 12 Jupyter notebooks organized by analysis type
├── scripts/                # Reusable Python helper modules
├── data/                   # Input data files (CSV/TSV)
├── statistics/             # Statistical analysis outputs (Prism files)
├── requirements.txt        # Python dependencies
└── Data-Science.code-workspace  # VS Code workspace configuration
```

## Notebooks Guide

### Physical Properties Analysis
- **Sinking-Velocities.ipynb** — Analysis of particle sinking rates (m/h) under different conditions
- **Particle-Sizes.ipynb** — Distribution and analysis of particle sizes (μm)
- **Zeta-Potentials.ipynb** — Surface charge analysis (mV) affecting colloidal stability
- **Suspended-Solids.ipynb** — Total suspended solids (TSS/VSS) analysis (g/L, %)
- **Recovery-Rates.ipynb** — Recovery efficiency analysis (%)

### Biological Analysis
- **Taxa-Distribution.ipynb** — Microbial community composition and taxonomic distribution (NGS sequencing)
- **Taxa-Variance.ipynb** — Variance and diversity analysis of microbial taxa

### Meta-Analysis
- **Data-Statistics.ipynb** — Comprehensive statistical overview and analysis of all measurements
- **EPS-Analysis.ipynb** — Extracellular polymeric substances analysis
- **Meta-Data.ipynb** — Metadata exploration and experiment structure overview

## Data

### Format
- **CSV/TSV files** containing experimental measurements and metadata
- **Data files**: `meta_data.csv`, `backup.csv`

### Metadata Structure
Experiments are identified by:
- `EXP_ABBR` — Experiment abbreviation
- `BIO_REP` — Biological replicate number
- `TEC_REP` — Technical replicate number

### Measurements
- Recovery rates (%)
- Sinking velocities (m/h)
- Particle sizes (μm)
- Total suspended solids (g/L, %)
- Zeta potentials (mV)
- Microbial taxonomy (NGS sequencing data)

## Scripts

### `scripts/data_helper.py`
Utilities for data loading and preprocessing:
- File discovery and filtering (e.g., "CH" experiments)
- Data type conversion
- Time-series filtering
- Control value duplication for analysis

### `scripts/plot_helper.py`
Publication-quality visualization functions:
- Boxplots and statistical plots
- Custom styling (Arial font, grayscale palette)
- Legend and axis formatting
- Reusable plotting templates

## Setup & Installation

### Prerequisites
- Python 3.11 or later
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/[YOUR_USERNAME]/[REPO_NAME].git
   cd [REPO_NAME]
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Open the workspace in VS Code**:
   ```bash
   code Data-Science.code-workspace
   ```

## Usage

### Running Notebooks

1. Open any notebook in `notebooks/` folder
2. Select the Python kernel from the virtual environment
3. Run cells sequentially or use "Run All" for complete analysis

### Development Workflow

1. Start with **Meta-Data.ipynb** to understand the experiment structure
2. Review **Data-Statistics.ipynb** for comprehensive statistical overview
3. Run specific analysis notebooks based on your research question
4. Use `scripts/plot_helper.py` for consistent visualization across notebooks

## Output

- **Visualizations**: Generated within notebooks and exported as figures
- **Statistical Results**: Saved to `statistics/` folder, including Prism files for additional analysis
- **Processed Data**: Intermediate results stored in notebook outputs

## Project Status

- **Active development** for PhD thesis/disputation
- Well-organized with reusable helper modules
- Ready for refactoring and optimization

## Future Improvements

- Extract hardcoded paths to configuration file
- Modularize notebook code into reusable functions
- Add comprehensive docstrings to helper modules
- Implement automated testing for data processing functions
- Create data processing pipeline documentation

## Author

Conducted as part of PhD research at CAU Kiel

## License

[Add appropriate license]

---

For questions or contributions, please contact the project maintainer.
