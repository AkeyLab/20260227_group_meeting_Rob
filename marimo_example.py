# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.19.6",
#     "pandas",
#     "seaborn",
# ]
# ///

import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    # marimo as a jupyter alternative

    ### Key differences from Jupyter

    | | Jupyter | marimo |
    |---|---|---|
    | **File format** | JSON (`.ipynb`) | Pure Python (`.py`) |
    | **Execution** | Can run cells in any order | Between cell dependencies automatically managed |
    | **Variable scoping** | Any cell can redefine anything | Each variable defined in exactly one cell |
    | **Version control** | Messy diffs on JSON | Clean diffs on `.py` |
    | **Cell structore** | Results below code | Results above code (configurable) |
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 1. Reactive dependencies

    marimo builds a **dependency graph** (DAG) of your cells. When you change
    a value, every downstream cell re-executes automatically.

    Try dragging the slider below — the dependent cells update instantly.
    """)
    return


@app.cell
def _(mo):
    x = mo.ui.slider(1, 20, value=5, label="x")
    x
    return (x,)


@app.cell
def _(x):
    y = x.value ** 2
    y
    return (y,)


@app.cell
def _(mo, x, y):
    mo.md(f"""
    With **x = {x.value}**, we get **y = x² = {y}**.

    Change the slider above and watch this cell update automatically.
    No "Run" button needed!
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 2. No variable redefinition

    In Jupyter, you can define `x = 1` in cell 3 and `x = 99` in cell 7, then
    run them in any order. This can cause reproducibility issues.

    **marimo prevents this entirely.** Each variable can only be defined in one
    cell. If you try to define it again, marimo shows an error *before* running
    anything.

    This means your notebook is always reproducible — there's no hidden state.
    """)
    return


@app.cell
def _():
    var1 = 20
    return (var1,)


@app.cell
def _(var1):
    print(var1)
    return


@app.cell
def _():
    # leaving this in to illustrate a point about marimo
    var1 = 10
    return (var1,)


@app.cell
def _(mo):
    mo.md("""
    ## 3. Interactive UI elements

    marimo has neat `mo.ui` components. Each element's `.value`
    is reactive — downstream cells update when the user interacts.
    """)
    return


@app.cell
def _(mo):
    slider = mo.ui.slider(0, 100, value=50, label="Slider")
    dropdown = mo.ui.dropdown(["Red", "Green", "Blue"], value="Green", label="Color")
    text_input = mo.ui.text(value="hello", label="Text")
    switch = mo.ui.switch(value=True, label="Toggle me")

    mo.vstack([slider, dropdown, text_input, switch])
    return dropdown, slider, switch, text_input


@app.cell
def _(dropdown, mo, slider, switch, text_input):
    mo.md(f"""
    ### Current values

    | Widget | Value |
    |--------|-------|
    | Slider | `{slider.value}` |
    | Dropdown | `{dropdown.value}` |
    | Text | `{text_input.value}` |
    | Switch | `{switch.value}` |
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 4. Tables and plots

    Marimo turns pandas/polars tables into an interactive table.
    """)
    return


@app.cell
def _():
    import pandas as pd
    import itertools
    import random

    organisms = ["Modern Human", "Altai", "Vindija", "Chag", "Deni"]
    genotypes = ["0/0", "0/1", "1/1"]
    chroms = [f"chr{i+1}" for i in range(22)]
    nloci_per_chrom = 10_000

    data = []
    for organism, chrom in  itertools.product(organisms, chroms):
        for pos in range(nloci_per_chrom):
            data.append({
                "chrom": chrom,
                "pos": pos+1,
                "organism": organism,
                "genotype": random.choice(genotypes),
            })
        


    df = pd.DataFrame(data)
    df
    return (df,)


@app.cell
def _(df):
    genotypes_per_organism_df = df.groupby("organism")["genotype"].value_counts().reset_index()
    genotypes_per_organism_df
    return


@app.cell
def _(df):
    import seaborn as sns

    sns.countplot(df, x="organism", hue="genotype")
    return


@app.cell
def _(mo):
    mo.md("""
    ## 8. Summary: Jupyter vs marimo

    | Feature | Jupyter | marimo |
    |---|---|---|
    | File format | JSON `.ipynb` | Python `.py` |
    | Variable redefinition | Allowed (source of bugs) | Prevented at parse time |
    | Git diffs | Noisy JSON | Clean Python |
    | UI widgets | `ipywidgets` (separate install) | Built-in `mo.ui` |
    | Reproducibility | Requires "Restart & Run All" | Guaranteed |
    | Deployment | Voila / nbconvert | `marimo run` (zero config) |

    Overall I find it easier to do work in Jupyter and not worry about
    the fancy UI that marimo provides, or the guarentees about outputs
    always being "fresh". Also marimo can be annoying if you have a slow computation.

    Also jupyter notebooks render very nicely in github, whereas marimo
    notebooks are just .py files and not treated separately.

    I might be convinced to use Marimo for "polished" notebooks, but even then
    I'm not so sure.

    ### Getting started

    mydella.princeton.edu let's you launch a marimo notebook server instead of jupyter notebook

    ```bash
    # Install
    pip install marimo

    # Edit this notebook
    marimo edit marimo_example.py

    # Or run it as a read-only app
    marimo run marimo_example.py
    ```
    """)
    return


if __name__ == "__main__":
    app.run()
