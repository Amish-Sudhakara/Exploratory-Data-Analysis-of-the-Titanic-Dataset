from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Iterable


# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT_TITLE = "Exploratory Data Analysis of the Titanic Dataset"
NOTEBOOK_TARGET_NAME = "Titanic_EDA.ipynb"

# Keep this False if you want to run Git commands manually.
INITIALIZE_LOCAL_GIT_REPOSITORY = False


# =============================================================================
# PROJECT PATHS
# =============================================================================

def get_project_root() -> Path:
    """Use the folder containing this script as the project root."""
    try:
        return Path(__file__).resolve().parent
    except NameError:
        return Path.cwd().resolve()


ROOT = get_project_root()

NOTEBOOKS_DIR = ROOT / "notebooks"
DATA_DIR = ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REPORTS_DIR = ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
TABLES_DIR = REPORTS_DIR / "tables"
DOCS_DIR = ROOT / "docs"


# =============================================================================
# GENERAL HELPERS
# =============================================================================

def ensure_directories() -> None:
    """Create the final GitHub project directories."""
    for directory in [
        NOTEBOOKS_DIR,
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        FIGURES_DIR,
        TABLES_DIR,
        DOCS_DIR,
    ]:
        directory.mkdir(parents=True, exist_ok=True)


def is_inside(path: Path, directory: Path) -> bool:
    """Return True when path is inside directory."""
    try:
        path.resolve().relative_to(directory.resolve())
        return True
    except ValueError:
        return False


def find_files(filename: str) -> list[Path]:
    """Find matching files anywhere inside the project."""
    return [
        path
        for path in ROOT.rglob(filename)
        if path.is_file() and ".git" not in path.parts
    ]


def select_source(
    candidates: Iterable[Path],
    target: Path,
) -> Path | None:
    """
    Select the most suitable source file.

    Files outside the final destination are preferred. This makes the script
    safe to run again after the project has already been organized.
    """
    valid_candidates = [
        path for path in candidates
        if path.exists() and path.is_file()
    ]

    if not valid_candidates:
        return None

    outside_target = [
        path for path in valid_candidates
        if path.resolve() != target.resolve()
    ]

    if outside_target:
        return sorted(
            outside_target,
            key=lambda path: (
                len(path.relative_to(ROOT).parts),
                str(path).lower(),
            ),
        )[0]

    return target if target.exists() else None


def move_file(source: Path | None, target: Path) -> bool:
    """Move a file without overwriting an existing final file."""
    if source is None or not source.exists():
        return False

    target.parent.mkdir(parents=True, exist_ok=True)

    if source.resolve() == target.resolve():
        return True

    if target.exists():
        print(f"[KEEP] Existing file: {target.relative_to(ROOT)}")
        return True

    shutil.move(str(source), str(target))

    print(
        f"[MOVE] {source.relative_to(ROOT)} "
        f"-> {target.relative_to(ROOT)}"
    )

    return True


def write_text_file(
    path: Path,
    content: str,
    overwrite: bool = True,
) -> None:
    """Create or replace a UTF-8 text file."""
    if path.exists() and not overwrite:
        print(f"[KEEP] Existing file: {path.relative_to(ROOT)}")
        return

    path.write_text(
        content.strip() + "\n",
        encoding="utf-8",
    )

    print(f"[WRITE] {path.relative_to(ROOT)}")


def read_summary_metrics(summary_path: Path) -> dict[str, str]:
    """Read Metric and Value columns from eda_summary.csv."""
    metrics: dict[str, str] = {}

    if not summary_path.exists():
        return metrics

    try:
        with summary_path.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as file:
            for row in csv.DictReader(file):
                metric_name = str(row.get("Metric", "")).strip()
                metric_value = str(row.get("Value", "")).strip()

                if metric_name:
                    metrics[metric_name] = metric_value

    except Exception as error:
        print(f"[WARN] Could not read EDA summary: {error}")

    return metrics


def get_metric(
    metrics: dict[str, str],
    name: str,
    fallback: str = "N/A",
) -> str:
    return metrics.get(name, fallback)


# =============================================================================
# MOVE AND ORGANIZE PROJECT OUTPUTS
# =============================================================================

def organize_notebook() -> None:
    target = NOTEBOOKS_DIR / NOTEBOOK_TARGET_NAME

    candidates = [
        path
        for path in ROOT.rglob("*.ipynb")
        if ".git" not in path.parts
        and ".ipynb_checkpoints" not in path.parts
    ]

    candidates.sort(
        key=lambda path: (
            0 if "titanic" in path.name.lower() else 1,
            0 if "eda" in path.name.lower() else 1,
            len(path.relative_to(ROOT).parts),
            path.name.lower(),
        )
    )

    source = select_source(candidates, target)

    if not move_file(source, target):
        print(
            "[WARN] No notebook was found. Put the .ipynb file in this "
            "project folder and run the script again."
        )


def organize_csv_outputs() -> None:
    file_map = {
        "titanic_cleaned.csv":
            PROCESSED_DATA_DIR / "titanic_cleaned.csv",

        "eda_summary.csv":
            TABLES_DIR / "eda_summary.csv",

        "missing_values_before_cleaning.csv":
            TABLES_DIR / "missing_values_before_cleaning.csv",

        "missing_values_after_cleaning.csv":
            TABLES_DIR / "missing_values_after_cleaning.csv",
    }

    for filename, target in file_map.items():
        source = select_source(
            find_files(filename),
            target,
        )

        if not move_file(source, target):
            print(f"[WARN] Optional output not found: {filename}")


def organize_text_outputs() -> None:
    target = REPORTS_DIR / "key_findings.txt"

    source = select_source(
        find_files("key_findings.txt"),
        target,
    )

    if not move_file(source, target):
        print("[WARN] Optional output not found: key_findings.txt")


def organize_figures() -> None:
    supported_extensions = {
        ".png",
        ".jpg",
        ".jpeg",
        ".svg",
        ".webp",
    }

    candidates: list[Path] = []

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue

        if path.suffix.lower() not in supported_extensions:
            continue

        if ".git" in path.parts:
            continue

        if is_inside(path, FIGURES_DIR):
            continue

        candidates.append(path)

    for source in sorted(candidates):
        target = FIGURES_DIR / source.name

        if target.exists():
            stem = target.stem
            suffix = target.suffix
            counter = 2

            while target.exists():
                target = FIGURES_DIR / f"{stem}_{counter}{suffix}"
                counter += 1

        move_file(source, target)

    if not any(FIGURES_DIR.iterdir()):
        print("[WARN] No generated figure files were found.")


def remove_empty_leftover_directories() -> None:
    """
    Remove only empty leftover folders.

    Folders containing files are never deleted.
    """
    protected_directories = {
        NOTEBOOKS_DIR.resolve(),
        DATA_DIR.resolve(),
        RAW_DATA_DIR.resolve(),
        PROCESSED_DATA_DIR.resolve(),
        REPORTS_DIR.resolve(),
        FIGURES_DIR.resolve(),
        TABLES_DIR.resolve(),
        DOCS_DIR.resolve(),
    }

    directories = sorted(
        [
            path for path in ROOT.rglob("*")
            if path.is_dir()
        ],
        key=lambda path: len(path.parts),
        reverse=True,
    )

    for directory in directories:
        if directory.resolve() in protected_directories:
            continue

        if ".git" in directory.parts:
            continue

        try:
            if not any(directory.iterdir()):
                directory.rmdir()
                print(
                    f"[REMOVE] Empty folder: "
                    f"{directory.relative_to(ROOT)}"
                )
        except OSError:
            pass


# =============================================================================
# CREATE GITHUB PROJECT FILES
# =============================================================================

def create_requirements() -> None:
    content = """
pandas>=2.0
numpy>=1.24
matplotlib>=3.7
seaborn>=0.13
jupyter>=1.0
nbformat>=5.9
"""

    write_text_file(
        ROOT / "requirements.txt",
        content,
    )


def create_gitignore() -> None:
    content = """
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd

# Virtual environments
.venv/
venv/
env/
ENV/

# Jupyter
.ipynb_checkpoints/

# Editors
.vscode/
.idea/

# Environment variables
.env
.env.*

# Operating-system files
.DS_Store
Thumbs.db
desktop.ini

# Kaggle and temporary outputs
*.zip
kaggle.json

# Do not commit raw competition data
data/raw/*.csv
!data/raw/README.md

# Logs and temporary files
*.log
*.tmp
*.temp
"""

    write_text_file(
        ROOT / ".gitignore",
        content,
    )


def create_raw_data_readme() -> None:
    content = f"""
# Raw Data

The raw Titanic competition files are intentionally not included in this
repository.

Download the Titanic competition dataset from Kaggle and place the following
files in this directory when running the notebook locally:

- `train.csv`
- `test.csv`
- `gender_submission.csv`

The original Kaggle notebook uses:

```text
/kaggle/input/competitions/titanic
```

The project notebook is stored at:

```text
notebooks/{NOTEBOOK_TARGET_NAME}
```
"""

    write_text_file(
        RAW_DATA_DIR / "README.md",
        content,
    )


def create_methodology_document() -> None:
    content = """
# Methodology

## 1. Data Inspection

The training dataset was examined for:

- Shape and columns
- Data types
- Numerical and categorical summaries
- Missing values
- Duplicate records
- Category distributions

## 2. Data Cleaning

The following treatments were used:

- Exact duplicate records were removed.
- Missing `Age` values were filled using the median within each gender and
  passenger-class group.
- Missing `Embarked` values were filled using the mode.
- Missing `Fare` values were filled using the median.
- Missing cabin values were represented as `Unknown`.

## 3. Feature Engineering

The notebook creates:

- `HasCabin`
- `Deck`
- `Title`
- `FamilySize`
- `IsAlone`
- `AgeGroup`
- `FareGroup`

## 4. Exploratory Data Analysis

Survival relationships were explored through:

- Count plots
- Bar plots
- Histograms
- Box plots
- Cross-tabulations
- Correlation analysis
- A correlation heatmap

The analysis studies gender, class, age, fare, family size, solo travel,
embarkation port, cabin availability, and passenger title.

## 5. Interpretation

The results describe associations in the Titanic dataset. They should not be
treated as evidence that a particular feature directly caused survival.
"""

    write_text_file(
        DOCS_DIR / "methodology.md",
        content,
    )


def create_readme() -> None:
    metrics = read_summary_metrics(
        TABLES_DIR / "eda_summary.csv"
    )

    overall_survival = get_metric(
        metrics,
        "Overall survival rate (%)",
    )

    female_survival = get_metric(
        metrics,
        "Female survival rate (%)",
    )

    male_survival = get_metric(
        metrics,
        "Male survival rate (%)",
    )

    first_class_survival = get_metric(
        metrics,
        "First-class survival rate (%)",
    )

    third_class_survival = get_metric(
        metrics,
        "Third-class survival rate (%)",
    )

    child_survival = get_metric(
        metrics,
        "Children survival rate (%)",
    )

    alone_survival = get_metric(
        metrics,
        "Travelling alone survival rate (%)",
    )

    family_survival = get_metric(
        metrics,
        "Travelling with family survival rate (%)",
    )

    content = f"""
# {PROJECT_TITLE}

A complete data-cleaning and exploratory data analysis project using the
Kaggle Titanic dataset.

The project examines how passenger characteristics such as gender, passenger
class, age, fare, family size, embarkation port, cabin availability, and title
were associated with survival.

## Project Objective

The objective is to transform the raw Titanic passenger data into a clean,
analysis-ready dataset and identify meaningful patterns through statistical
summaries and visualizations.

## Key Results

| Metric | Result |
|---|---:|
| Overall survival rate | {overall_survival}% |
| Female survival rate | {female_survival}% |
| Male survival rate | {male_survival}% |
| First-class survival rate | {first_class_survival}% |
| Third-class survival rate | {third_class_survival}% |
| Children survival rate | {child_survival}% |
| Travelling alone survival rate | {alone_survival}% |
| Travelling with family survival rate | {family_survival}% |

Gender and passenger class showed some of the clearest relationships with
survival. Fare, age group, family structure, cabin availability, passenger
title, and embarkation port also showed meaningful patterns.

> These findings represent association, not causation.

## Data Cleaning Performed

- Inspected data types, missing values, duplicates, and category distributions.
- Removed exact duplicate records.
- Filled missing `Age` values using grouped medians based on `Sex` and
  `Pclass`.
- Filled missing `Embarked` values using the mode.
- Filled missing `Fare` values using the median.
- Replaced missing cabin information with `Unknown`.

## Feature Engineering

The following features were created:

- `HasCabin`
- `Deck`
- `Title`
- `FamilySize`
- `IsAlone`
- `AgeGroup`
- `FareGroup`

## Exploratory Analysis

The notebook includes:

- Overall survival distribution
- Survival by gender
- Survival by passenger class
- Gender and class interaction
- Age distribution and age groups
- Fare distribution and fare groups
- Family size and solo travel
- Embarkation port analysis
- Cabin availability analysis
- Passenger title analysis
- Numerical correlation analysis

Generated charts are stored in
[`reports/figures`](reports/figures).

## Repository Structure

```text
{ROOT.name}/
├── data/
│   ├── processed/
│   │   └── titanic_cleaned.csv
│   └── raw/
│       └── README.md
├── docs/
│   ├── methodology.md
│   └── project_structure.txt
├── notebooks/
│   └── {NOTEBOOK_TARGET_NAME}
├── reports/
│   ├── figures/
│   ├── tables/
│   │   ├── eda_summary.csv
│   │   ├── missing_values_after_cleaning.csv
│   │   └── missing_values_before_cleaning.csv
│   └── key_findings.txt
├── .gitignore
├── README.md
└── requirements.txt
```

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook
- Kaggle

## Dataset

This project uses the Titanic dataset from the Kaggle Titanic competition.

Raw competition files are not committed to this repository. On Kaggle, the
notebook expects the dataset at:

```text
/kaggle/input/competitions/titanic
```

For local execution, download the dataset and place the files in `data/raw`.

## Run Locally

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd "{ROOT.name}"
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\\Scripts\\activate
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Jupyter Notebook

```bash
jupyter notebook
```

Open:

```text
notebooks/{NOTEBOOK_TARGET_NAME}
```

## Project Outputs

- Cleaned dataset: `data/processed/titanic_cleaned.csv`
- EDA summary tables: `reports/tables`
- Key findings: `reports/key_findings.txt`
- Visualizations: `reports/figures`

## Author

Add your name, LinkedIn profile, and GitHub profile here before publishing.
"""

    write_text_file(
        ROOT / "README.md",
        content,
    )


def create_tree_text() -> str:
    excluded_names = {
        ".git",
        "__pycache__",
        ".ipynb_checkpoints",
    }

    try:
        script_name = Path(__file__).name
    except NameError:
        script_name = ""

    lines = [ROOT.name + "/"]

    def add_directory(
        directory: Path,
        prefix: str = "",
    ) -> None:
        entries = sorted(
            [
                entry
                for entry in directory.iterdir()
                if entry.name not in excluded_names
                and entry.name != script_name
            ],
            key=lambda entry: (
                entry.is_file(),
                entry.name.lower(),
            ),
        )

        for index, entry in enumerate(entries):
            is_last = index == len(entries) - 1
            connector = "└── " if is_last else "├── "

            lines.append(
                prefix + connector + entry.name
            )

            if entry.is_dir():
                extension = "    " if is_last else "│   "

                add_directory(
                    entry,
                    prefix + extension,
                )

    add_directory(ROOT)

    return "\n".join(lines)


def create_project_structure_file() -> None:
    write_text_file(
        DOCS_DIR / "project_structure.txt",
        create_tree_text(),
    )


def initialize_git_repository() -> None:
    if not INITIALIZE_LOCAL_GIT_REPOSITORY:
        return

    if (ROOT / ".git").exists():
        print("[KEEP] Git repository already exists.")
        return

    if shutil.which("git") is None:
        print(
            "[WARN] Git is not installed or is not available in PATH."
        )
        return

    try:
        subprocess.run(
            ["git", "init"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

        print("[GIT] Local Git repository initialized.")

    except subprocess.CalledProcessError as error:
        print(f"[WARN] Git initialization failed: {error}")


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    print("=" * 78)
    print("PREPARING TITANIC EDA PROJECT FOR GITHUB")
    print("=" * 78)
    print("Project root:", ROOT)
    print()

    ensure_directories()

    organize_notebook()
    organize_csv_outputs()
    organize_text_outputs()
    organize_figures()
    remove_empty_leftover_directories()

    create_requirements()
    create_gitignore()
    create_raw_data_readme()
    create_methodology_document()
    create_readme()
    create_project_structure_file()

    initialize_git_repository()

    print()
    print("=" * 78)
    print("PROJECT REFACTOR COMPLETED")
    print("=" * 78)
    print(create_tree_text())

    print()
    print(
        "Before uploading, edit the Author section in README.md."
    )

    print()
    print("Recommended Git commands:")
    print("  git init")
    print("  git add .")
    print(
        '  git commit -m '
        '"Add Titanic data cleaning and EDA project"'
    )
    print("  git branch -M main")
    print(
        "  git remote add origin "
        "<YOUR_GITHUB_REPOSITORY_URL>"
    )
    print("  git push -u origin main")


if __name__ == "__main__":
    main()