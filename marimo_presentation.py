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
    layout_file="layouts/marimo_presentation.slides.json",
)


@app.cell
def _():
    import marimo as mo
    import subprocess
    return mo, subprocess


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
    mo.vstack([
        mo.md("""
        # Outline

        Goal of this presentation is to hopefully introduce many new
        tools/techniques but not go into depth on any one of them.
        """),
        mo.accordion({
            "Della": mo.md("""
    - Mental model of how the Della cluster is organized
    - Ssh into della without a password
    - Vscode remotely into della without a password
    - Job and quota monitoring tools
    """),
            "General command line": mo.md("""
    - tmux, ctrl+R tips and tricks
    - uv python runtime and dependency manager
    - claude code AI in the terminal
    """),
            "Github": mo.md("""
    - Mermaid-js diagrams
    - Github actions
    - Copilot on github
    """),
        }, multiple=True),
    ])
    return


@app.cell
def _():
    # Slide 3: Della architecture
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md("# Della cluster architecture"),
        mo.mermaid("""
        graph LR
            subgraph Della [Della compute nodes]
                N1[Node] & N2[Node] & N3[Node] & N4[...]
            end

            Della -->|fast 🐇| scratch["/scratch/gpfs"]
            Della --> home["/home"]

            subgraph Login [Login / access nodes]
                vis1["della-vis1.princeton.edu"]
                mydella["https://mydella.princeton.edu"]
                gpu["della-gpu.princeton.edu"]
                della9["della9.princeton.edu"]
            end

            Login -->|slow 🐢| projects["/projects"]
            Login --> tigerdata["/tigerdata"]
        """),
    ])
    return


@app.cell
def _():
    # Slide 4: Other users on the shared node
    return


@app.cell
def _(mo, subprocess):
    def get_list_of_logged_in_users():
        try:
            result = subprocess.check_output(["who"])
            lines = ["- "+r for r in result.decode().split("\n") if len(r) > 0]
            return "\n".join(lines)
        except OSError:
            return "*Not available in browser mode*"

    users_button = mo.ui.button(
        label="Refresh logged-in users",
        on_click=lambda value: get_list_of_logged_in_users(),
    )
    return (users_button,)


@app.cell
def _(mo, users_button):
    header = mo.md("""
    # On the Della login node you're sharing with other users
    """)

    users_md = mo.md(users_button.value) if users_button.value else mo.md("")

    mo.vstack([header, users_button, users_md])
    return


@app.cell
def _():
    # Slide 5: Top processes
    return


@app.cell
def _(mo, subprocess):
    def get_top_processes():
        try:
            result = subprocess.check_output(
                ["top", "-bn1", "-w", "200"], text=True
            )
        except OSError:
            return "*Not available in browser mode*"
        lines = result.strip().split("\n")
        # Find the header line (starts with PID)
        header_idx = next(
            i for i, l in enumerate(lines) if l.strip().startswith("PID")
        )
        header = lines[header_idx].split()
        rows = []
        for line in lines[header_idx + 1 : header_idx + 21]:
            rows.append(line.split(None, len(header) - 1))
        return [dict(zip(header, row)) for row in rows if len(row) == len(header)]

    top_button = mo.ui.button(
        label="Refresh top",
        on_click=lambda value: get_top_processes(),
    )
    return (top_button,)


@app.cell
def _(mo, top_button):
    top_header = mo.md("""
    # Top processes on the login node
    """)

    if isinstance(top_button.value, list):
        table = mo.ui.table(top_button.value, selection=None)
    elif isinstance(top_button.value, str):
        table = mo.md(top_button.value)
    else:
        table = mo.md("")

    mo.vstack([top_header, top_button, table])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
