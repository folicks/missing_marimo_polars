# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "polars==1.22.0",
# ]
# ///

import marimo

__generated_with = "0.11.13"
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

        _By Felix Najera._  

        In real‑world datasets, missing values are inevitable. Polars offers a rich set of methods to detect, remove, and impute missing data efficiently. This notebook walks through common patterns and best practices for dealing with nulls in Polars DataFrames.
        """
    )
    return


@app.cell
def _(mo):
    mo.accordion({
        "### TLDR":"""everything works as normal using functions such as [```.is_null```](https://docs.pola.rs/api/python/stable/reference/expressions/api/polars.Expr.is_null.html) to check for missing values, [```fill_null```](https://docs.pola.rs/api/python/stable/reference/expressions/api/polars.Expr.fill_null.html), and [`drop`]() to replace the missing values and to drop them. taking special note of variables with String cases see the Strings notebook for more."""
    })
    return


@app.cell
def _(mo):
    mo.md("""Before that lets do a review of how Polars datatypes work  specifically String objects up until this point""")
    return


@app.cell
def _(mo):
    mo.md("""On the note of the Polars datatype specific features we can mention the null types of Polars of NaN and null.""")
    return


@app.cell
def _():
    return


@app.cell
def _():
    import polars as pl

    df = pl.DataFrame(
        {
            "A": [1, 2, 3, 4, 5],
            "fruits": ["banana", None, "apple", "apple", "banana"],
            "age": [25, None, 37, 29, None],
            "B": [5, 4, 3, 2, 1],
            "score": [85, 92,  None, None, 88],
            "height_cm": [170.0, 165.5, None, 180.2, 175.0],

        }
    )
    df
    return df, pl


@app.cell
def _(mo):
    mo.md("""Where ```null``` is what is used in dataset features of with datatype other floats and ```NaN``` is used in the dataset features witha  datatype of float""")
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.md("""For the purposes of this guide we won't mention all pelicularities that may come from pandas conversions""")
    return


@app.cell
def _(mo):
    data_filler = mo.ui.dropdown(["NaN","None","null"],value="null")
    #the idea is to place the desired missing data types into the spots of the data perforable at random idk what the value would be tbh


    return (data_filler,)


@app.cell
def _(data_filler, mo):
    reps = mo.ui.slider(1,10, label=f"type of missing values {data_filler.value}")
    return (reps,)


@app.cell
def _(data_filler, reps):
    data_filler,reps
    return


app._unparsable_cell(
    r"""
    # make a sliding df with the intention of making it switch thru the null type cases and the variables using the mo.md ui style
    pl.DataFrame(
    """,
    name="_"
)


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
def _(mo):
    mo.md("""Theres also an alternative function ```interpolate``` that can be used to fill missing values in a column with the average of the surrounding values. This is useful when you have a time series or a sequence of values and you want to fill in the gaps with a smooth transition.""")
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
def _(mo):
    mo.md("""###Going Further""")
    return


@app.cell
def _(mo):
    mo.md("""you'll notice I hardly mention the null types of Polars of NaN and null. In practice when applying these functions you'll notice that the null types are not the same as the missing values in pandas. For example, if you have a column with NaN values, and you apply `fill_null(0)`, it will replace the NaN values with 0, but it won't change the dtype of the column. This is different from pandas, where filling NaN values with 0 will change the dtype of the column to int.""")
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


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ## 🔖 References

        - Polars documentation: https://pola.rs/docs  
        - Handling missing data in Polars: https://docs.pola.rs/user-guide/expressions/missing-data/
        """
    )
    return


@app.cell
def _():
    import sys

    if "pyodide" in sys.modules:
        import micropip
        await micropip.install("polars")
            
        import polars as pl
        return (pl,)
    return

@app.cell
async def _():
    import sys

    if "pyodide" in sys.modules:
        import micropip
        await micropip.install("polars")

    import polars as pl
    return (pl,)




if __name__ == "__main__":
    app.run()
