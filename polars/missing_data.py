# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "polars==1.22.0",
# ]
# ///

import marimo

__generated_with = "0.12.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        # Handling Missing Data in Polars

        _By [Your Name]._  

        In real‑world datasets, missing values are inevitable. Polars offers a rich set of methods to detect, remove, and impute missing data efficiently. This notebook walks through common patterns and best practices for dealing with nulls in Polars DataFrames.
        """
    )
    return


@app.cell
def _():
    import polars as pl

    # Create a DataFrame with various kinds of missing data
    df = pl.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "age": [25, None, 37, 29, None],
        "height_cm": [170.0, 165.5, None, 180.2, 175.0],
        "score": [85, 92,  None, None, 88]
    })
    df
    return df, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 1. Detecting Nulls

        Use `is_null` or `null_count` to find missing values.
        """
    )
    return


@app.cell
def _(df, pl):
    # Show where nulls are
    mask = df.select([pl.col(c).is_null().alias(f"{c}_is_null") for c in df.columns])
    counts = df.null_count()
    mask, counts
    return counts, mask


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 2. Dropping Nulls

        - `drop_nulls()` removes any row containing nulls  
        - You can target specific columns with `subset=`
        """
    )
    return


@app.cell
def _(df):
    # drop any row with a null
    dropped_all = df.drop_nulls()
    # drop rows with nulls only in 'score'
    dropped_score = df.drop_nulls(subset=["score"])
    dropped_all, dropped_score
    return dropped_all, dropped_score


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 3. Filling Nulls

        - `fill_null(value)` replaces all nulls with a scalar  
        - `fill_null(strategy="forward")` uses previous non-null value  
        - `fill_null(strategy="backward")` uses next non-null value
        """
    )
    return


@app.cell
def _(df):
    filled_constant = df.fill_null(0)
    filled_ffill = df.fill_null(strategy="forward")
    filled_bfill = df.fill_null(strategy="backward")
    filled_constant, filled_ffill, filled_bfill
    return filled_bfill, filled_constant, filled_ffill


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 4. Imputing with Expressions

        Leverage Polars expressions for conditional imputation.  
        Example: fill missing `age` with the average age.
        """
    )
    return


@app.cell
def _(df, pl):
    mean_age = df.select(pl.col("age").mean()).item()
    imputed = df.with_column(
        pl.col("age").fill_null(mean_age).alias("age_imputed")
    )
    mean_age, imputed
    return imputed, mean_age


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 5. Lazy Execution for Large Datasets

        For big data, use the lazy API to defer computation and optimize the pipeline.
        """
    )
    return


@app.cell
def _(pl):
    # assume large CSV with missing values
    lazy_df = pl.scan_csv("large_with_nulls.csv")
    result = (
        lazy_df
        .filter(pl.col("age").is_not_null())
        .with_column(pl.col("score").fill_null(0))
        .select(["id", "age", "score"])
        .collect()
    )
    lazy_df, result
    return lazy_df, result


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ## 🔖 References

        - Polars documentation: https://pola.rs/docs  
        - Handling missing data in Polars: https://pola.rs/docs/reference/expressions#nulls
        """
    )
    return


if __name__ == "__main__":
    app.run()
