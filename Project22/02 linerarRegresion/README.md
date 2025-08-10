# Linear Regression: Experience → Salary

A small, end-to-end notebook project that trains and evaluates a simple linear regression model to predict annual salary (in thousands) from work experience.

## Project structure

- `02 linerarRegresion.ipynb` — main notebook with data exploration, feature engineering, model training, evaluation, and diagnostics
- `Experience-Salary.csv` — dataset with monthly experience and salary
- `requirements.txt` — Python dependencies

## Data

- Columns:
  - `exp(in months)`: total work experience in months
  - `salary(in thousands)`: monthly salary measured in thousands
- Engineered features (in-notebook):
  - `exp(in years)` = `exp(in months)` / 12
  - `annualSalary(in thousands)` = `salary(in thousands)` × 12

## Run the notebook

- Open `02 linerarRegresion.ipynb` in VS Code or Jupyter.
- Select a Python kernel with the installed packages.
- Run all cells from top to bottom.

## What the notebook does

1. Load and preview the dataset
2. Explore types and summary statistics
3. Feature engineering: months → years; monthly → annual
4. Visualize relationships (scatter, regression line)
5. Train/test split
6. Fit `LinearRegression` (OLS)
7. Inspect parameters (slope/intercept) and R²
8. Evaluate with MAE, MSE, RMSE
9. Check residual diagnostics (histogram, Q–Q plot)

## Typical results (from a sample run)

- R² (test): ≈ 0.62
- MAE: ≈ 49 (thousands)
- RMSE: ≈ 62.6 (thousands)

Interpretation: the model explains ~62% of variance, but errors are large relative to the mean annual salary, indicating a basic univariate model underfits this problem.

## Limitations

- Single feature (experience) ignores important drivers: role, location, industry, company size, education/skills, etc.
- Linear form may miss thresholds or diminishing returns.
- Annualizing magnifies noise; outliers increase MAE/RMSE.

## Suggested next steps

- Add richer features and domain context
- Allow nonlinearity (polynomial/spline terms; tree-based models/boosting)
- Predict log(salary) to stabilize variance
- Use robust regression or handle outliers explicitly
- Adopt k-fold cross-validation and consider scale-free metrics (e.g., MAPE)

