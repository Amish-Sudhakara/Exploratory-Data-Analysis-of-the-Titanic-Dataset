# Exploratory Data Analysis of the Titanic Dataset

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
| Overall survival rate | 38.38% |
| Female survival rate | 74.2% |
| Male survival rate | 18.89% |
| First-class survival rate | 62.96% |
| Third-class survival rate | 24.24% |
| Children survival rate | 57.97% |
| Travelling alone survival rate | 30.35% |
| Travelling with family survival rate | 50.56% |

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
Exploratory Data Analysis of the Titanic Dataset/
├── data/
│   ├── processed/
│   │   └── titanic_cleaned.csv
│   └── raw/
│       └── README.md
├── docs/
│   ├── methodology.md
│   └── project_structure.txt
├── notebooks/
│   └── Titanic_EDA.ipynb
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
cd "Exploratory Data Analysis of the Titanic Dataset"
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
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
notebooks/Titanic_EDA.ipynb
```

## Project Outputs

- Cleaned dataset: `data/processed/titanic_cleaned.csv`
- EDA summary tables: `reports/tables`
- Key findings: `reports/key_findings.txt`
- Visualizations: `reports/figures`

## Author

Add your name, LinkedIn profile, and GitHub profile here before publishing.
