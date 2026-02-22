# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.19.6",
# ]
# ///

import marimo

__generated_with = "0.19.6"
app = marimo.App(
    width="medium",
    layout_file="layouts/20260227_group_meeting.slides.json",
)


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    # Slide 1: Title slide
    return


@app.cell
def _(mo):
    rocket_slider = mo.ui.slider(steps=[1, 2, 3, 4, 5])
    return (rocket_slider,)


@app.cell
def _(mo, rocket_slider):
    rocket = mo.icon("lucide:rocket", size=20)
    rockets = [rocket]*rocket_slider.value

    slider_md = mo.md(f"""
    # Linux tips and tricks. And AI

    February 27th 2026, Rob

    {rocket_slider}
    """)

    rockets_md = mo.hstack(rockets, justify="start")

    mo.vstack([slider_md, rockets_md])
    return


@app.cell
def _():
    # Slide 2: Outline
    return


@app.cell
def _(mo):
    mo.md("""
    # Outline

    * Della
        * Mental model of how the Della cluster is organized
        * Ssh into della without a password
        * Vscode remotely into della without a password
        * Job and quota monitoring tools


    * General command line
        * tmux, ctrl+R tips and tricks
        * uv python runtime and dependency manager
        * claude code AI in the terminal


    * Github
        * Mermaid-js diagrams
        * Github actions
        * Copilot on github
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
