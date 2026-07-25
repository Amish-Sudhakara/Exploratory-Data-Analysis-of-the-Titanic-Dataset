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
