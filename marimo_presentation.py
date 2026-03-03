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
    from pathlib import Path

    _sample_dir = Path("data")
    return mo, subprocess


@app.cell
def _(mo):
    mo.md(f"""
    # Akey Group Meeting February 27th 2026

    Topics

    * Command line tools (tmux, ctrl+R, aliases, tree, pipe to vi)
    * Della
    * Shiny "new" software tools (marimo, uv)
    * Claude code AI in the terminal
    * Github

    This presentation is available on [github](https://github.com/AkeyLab/20260227_group_meeting_Rob/tree/main)

    **Note to Rob:** Record this presentation in zoom
    """)
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md("""
        # Outline

        Goal of this presentation is to hopefully introduce many new
        tools/techniques but not go into depth on any one of them.

        Feel free to follow along and interrupt whenever
        """),
        mo.accordion({
            "Command line tools": mo.md("""
    - tmux, ctrl+R tips and tricks
    """),
            "Della": mo.md("""
    - Mental model of how the Della cluster is organized
    - Ssh into della without a password
    - Vscode remotely into della without a password
    - Job and quota monitoring tools
    """),
            "Shiny new tools": mo.md("""
    - Marimo notebooks as alternatives to python jupyter notebooks
    - uv python version and package manager
    """),
            "Claude code": mo.md("""
    - Interacting with an LLM directly on Della
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
def _(mo):
    mo.center(
        mo.vstack([
            mo.md("# Command line tools"),
            mo.md("(switch to terminal for interactive portion and cd into examples/tmux )"),
        ])
    )
    return


@app.cell
def _(mo):
    mo.center(
        mo.md("# Della")
    )
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md("# Della cluster architecture overview"),
        mo.mermaid("""
        graph TD
            subgraph Local
                Laptop
            end

            subgraph FileSystems
                projects["/projects"]
                tigerdata["/tigerdata"]
                scratch["/scratch/gpfs"]
                home["/home"]
            end

            subgraph Login [Login / access nodes]
                direction TB
                della9["della9.princeton.edu"]
                vis1["della-vis1.princeton.edu"]
                mydella["https://mydella.princeton.edu"]
                gpu["della-gpu.princeton.edu"]
            end

            subgraph Compute [Della compute nodes]
                N1[Node] & N2[Node] & N3[Node] & N4[...]
            end

            Local -->|ssh/web-browser | Login
            Login -->|sbatch | Compute

            Login --> FileSystems
            Compute --> FileSystems
        """),
    ])
    return


@app.cell
def _(mo):
    rocket_slider = mo.ui.slider(steps=[1, 2, 3, 4, 5])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md("# Overview of important notes about Della organization"),
        mo.accordion({
            "Terminology": mo.md("""
    - A "node" is a computer and has multiple CPUs (or cores)
    - A "filesystem" is "mounted" onto each node to allow consistent file access
    - "SLURM" is the "scheduler" on Della and you ask it to schedule your jobs
    """),
            "Login nodes": mo.md("""
    - When you are interactively working with della you're likely on a "login node"
    - Login nodes have internet access
    - You're one of many users sharing the login node
    - Programs requiring lots of time, memory, or compute should not be run on the login node
    """),
            "File systems": mo.md("""
    - On our personal laptops the compute resources are 1:1 tied to the storage resources
    - However on Della the same filesystems are mounted to all login and compute nodes
    - Kind of like accessing the same google document on different computers
    """),
            "Compute nodes": mo.md("""
    - Most of the nodes (99%) composing Della are compute nodes
    - You cannot directly access compute nodes, instead you petition the SLURM scheduler to run a job for you
    - Compute nodes do NOT have internet access
    - This means you can't submit a job that tries to download data or packages from the internet
    """),
            "Vis nodes": mo.md("""
    - These are two special login nodes that aren't hidden behind the scheduler
    - They are powerful shared computers and it's a "free for all" like the "wild west"
    - They DO have internet access
    """),
        }, multiple=True),
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md("""
        # SSH into Della without a password

        **Presentor Note:** Show `della` alias and VScode remote access


        Setting up SSH keys means no more typing your password every time.
        This also enables **VSCode Remote-SSH** to connect seamlessly.

        There are a few steps to follow, but it only needs to be setup once.

        After setup: `ssh della` just works — no password prompt.
        """),
        mo.md("""
        **Full guide with all the details and other helpful suggestions:**
        https://github.com/PrincetonUniversity/removing_tedium
        """),
    ])
    return


@app.cell
def _(mo, subprocess):
    def get_list_of_logged_in_users():
        try:
            result = subprocess.check_output(["who"]).decode()
        except OSError:
            sample = _sample_dir / "sample_who.txt"
            result = sample.read_text() if sample.exists() else ""
            lines = ["- " + r for r in result.strip().split("\n") if len(r) > 0]
            return "*Sample data (actual command not runnable in browser mode):*\n\n" + "\n".join(lines) if lines else "*Not available in browser mode*"
        lines = ["- " + r for r in result.strip().split("\n") if len(r) > 0]
        return "\n".join(lines)

    users_button = mo.ui.button(
        label="Run `who`",
        on_click=lambda value: get_list_of_logged_in_users(),
    )

    def _parse_top_output(text):
        lines = text.strip().split("\n")
        header_idx = next(
            i for i, l in enumerate(lines) if l.strip().startswith("PID")
        )
        header = lines[header_idx].split()
        rows = []
        for line in lines[header_idx + 1 : header_idx + 21]:
            rows.append(line.split(None, len(header) - 1))
        return [dict(zip(header, row)) for row in rows if len(row) == len(header)]

    def get_top_processes():
        try:
            result = subprocess.check_output(
                ["top", "-bn1", "-w", "200"], text=True
            )
        except OSError:
            sample = _sample_dir / "sample_top.txt"
            if sample.exists():
                return ("*Sample data (not available in browser mode):*", _parse_top_output(sample.read_text()))
            return "*Not available in browser mode*"
        return _parse_top_output(result)

    top_button = mo.ui.button(
        label="Run `top`",
        on_click=lambda value: get_top_processes(),
    )
    return top_button, users_button


@app.cell
def _(mo, top_button, users_button):
    users_md = mo.md(users_button.value) if users_button.value else mo.md("")
    if isinstance(top_button.value, tuple):
        warning, data = top_button.value
        table = mo.vstack([mo.md(warning), mo.ui.table(data, selection=None)])
    elif isinstance(top_button.value, list):
        table = mo.ui.table(top_button.value, selection=None)
    elif isinstance(top_button.value, str):
        table = mo.md(top_button.value)
    else:
        table = mo.md("")

    mo.vstack([
        mo.md("# Now that you're on the login node"), 
        mo.md("## On the Della login node you're sharing with other users"), 
        users_button,
        users_md,
        mo.md("## Top processes on the login node"),
        top_button,
        table,
    ])
    return


@app.cell
def _(mo, subprocess):
    import re
    import time

    def _parse_checkquota(text):
        """Parse checkquota output into storage and files tables."""
        storage_rows = []
        files_rows = []
        current = None
        headers = None
        for line in text.strip().split("\n"):
            stripped = line.strip()
            if "Storage/size" in stripped:
                current = "storage"
                continue
            elif "Number of files" in stripped:
                current = "files"
                continue
            if not stripped or stripped.startswith("--"):
                continue
            if stripped.startswith("Filesystem"):
                headers = re.split(r"\s{2,}", stripped)
                continue
            if headers and current:
                parts = re.split(r"\s{2,}", stripped)
                if len(parts) >= 3:
                    row = dict(zip(headers, parts))
                    if current == "storage":
                        storage_rows.append(row)
                    else:
                        files_rows.append(row)
        return storage_rows, files_rows

    def run_checkquota():
        sample_prefix = ""
        try:
            result = subprocess.check_output(["checkquota"], text=True)
        except OSError:
            sample = _sample_dir / "sample_checkquota.txt"
            if sample.exists():
                result = sample.read_text()
                sample_prefix = "*Sample data (not available in browser mode):*"
            else:
                return (None, None, "*Not available in browser mode*")
        storage, files = _parse_checkquota(result)
        return (storage, files, sample_prefix)

    checkquota_button = mo.ui.button(
        label="`checkquota`",
        on_click=lambda value: run_checkquota(),
    )

    def write_large_file():
        projects_f_path = "/projects/AKEY/akey_vol2/rbierman/large_file.txt"
        scratch_f_path = "/scratch/gpfs/AKEY/rbierman/large_file.txt"
        n_lines = 200_000_000
        cmd = f"yes | head -n {n_lines}"

        try:
            start = time.time()
            subprocess.run(f"{cmd} > {projects_f_path}", shell=True, check=True)
            projects_time = time.time() - start

            start = time.time()
            subprocess.run(f"{cmd} > {scratch_f_path}", shell=True, check=True)
            scratch_time = time.time() - start

            # Clean up
            subprocess.run(f"rm -f {projects_f_path} {scratch_f_path}", shell=True)

            return (
                f"Writing {n_lines:,} lines:\n\n"
                f"- `/projects`: {projects_time:.2f}s\n"
                f"- `/scratch`:  {scratch_time:.2f}s"
            )
        except (OSError, subprocess.CalledProcessError) as e:
            return f"*Not available in browser mode:* {e}"

    write_to_projects_button = mo.ui.button(
        label="Write large file (projects vs scratch)",
        on_click=lambda value: write_large_file(),
    )
    return checkquota_button, write_to_projects_button


@app.cell
def _(checkquota_button, mo, write_to_projects_button):
    _quota_elements = []
    if isinstance(checkquota_button.value, tuple):
        storage, files, prefix = checkquota_button.value
        if prefix:
            _quota_elements.append(mo.md(prefix))
        if storage:
            _quota_elements.append(mo.md("### Storage/size quota"))
            _quota_elements.append(mo.ui.table(storage, selection=None))
        if files:
            _quota_elements.append(mo.md("### Number of files quota"))
            _quota_elements.append(mo.ui.table(files, selection=None))
        if not storage and not files and not prefix:
            _quota_elements.append(mo.md("*No quota data available*"))
    elif isinstance(checkquota_button.value, str):
        _quota_elements.append(mo.md(checkquota_button.value))

    _write_result = mo.md("")
    if isinstance(write_to_projects_button.value, str):
        _write_result = mo.md(write_to_projects_button.value)

    mo.vstack([
        mo.md("""
        # Filesystems on Della

        * `/home` is your personal directory and has ~50GB limit
        * `/scratch` is fast parallel storage that is not backed up
        * `/projects` is backed up but slower
        * `/tigerdata` is cold storage backup for infrequently accessed data
        """),
        checkquota_button,
        *_quota_elements,
        write_to_projects_button,
        _write_result,
    ])
    return


@app.cell
def _(mo):
    nodes_info_table = mo.ui.table(
        [
            {"Processor": "2.4 GHz AMD EPYC 9654", "Nodes": 55, "Cores/Node": 192, "Memory/Node": "1500 GB", "GPUs/Node": "N/A"},
            {"Processor": "2.8 GHz Intel Cascade Lake", "Nodes": 64, "Cores/Node": 32, "Memory/Node": "190 GB", "GPUs/Node": "N/A"},
            {"Processor": "3.1 GHz Intel Cascade Lake", "Nodes": 24, "Cores/Node": 40, "Memory/Node": "380 GB", "GPUs/Node": "N/A"},
            {"Processor": "2.6 GHz AMD EPYC Rome", "Nodes": 20, "Cores/Node": 128, "Memory/Node": "768 GB", "GPUs/Node": "2 (A100)"},
            {"Processor": "2.8 GHz Intel Ice Lake", "Nodes": 59, "Cores/Node": 48, "Memory/Node": "1000 GB", "GPUs/Node": "4 (A100)"},
            {"Processor": "2.8 GHz Intel Ice Lake", "Nodes": 10, "Cores/Node": 48, "Memory/Node": "1000 GB", "GPUs/Node": "8 (MIG A100)"},
            {"Processor": "2.8 GHz Intel Ice Lake", "Nodes": 2, "Cores/Node": 48, "Memory/Node": "1000 GB", "GPUs/Node": "28 (MIG A100)"},
            {"Processor": "2.8 ARM Neoverse-V2", "Nodes": 1, "Cores/Node": 72, "Memory/Node": "575 GB", "GPUs/Node": "1 (GH200)"},
            {"Processor": "2.1 GHz Intel Sapphire Rapids", "Nodes": 42, "Cores/Node": 96, "Memory/Node": "1000 GB", "GPUs/Node": "8 (H100)"},
            {"Processor": "2.5 GHz Intel Emerald Rapids", "Nodes": 18, "Cores/Node": 64, "Memory/Node": "1500 GB", "GPUs/Node": "8 (H200)"},
        ],
        selection=None,
    )

    mo.vstack([
        mo.md("# Della compute nodes have lots of resources"),
        nodes_info_table,
        mo.md("If you submit a job asking for 16G of RAM and 1 CPU then you'll get part of a node."),
        mo.md("Not always up to date: https://researchcomputing.princeton.edu/systems/della")
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md("# Job and quota monitoring tools"),
        mo.accordion({
            "checkquota": mo.md("""
    Check your storage usage and quotas on `/home`, `/scratch`, and `/projects`:
    ```bash
    checkquota
    ```
    """),
            "squeue / sacct": mo.md("""
    Monitor your running and recent jobs:
    ```bash
    # Your currently running/pending jobs
    squeue -u $USER

    # Historical job info (last 7 days)
    sacct -u $USER --starttime=$(date -d '7 days ago' +%Y-%m-%d) --format=JobID,JobName,State,Elapsed,MaxRSS
    ```
    """),
            "jobstats": mo.md("""
    Get detailed resource utilization for a completed job:
    ```bash
    jobstats <job_id>
    ```
    """),
            "reportseff": mo.md("""
    A nicer way to see job efficiency — shows CPU, memory, and time efficiency at a glance:
    ```bash
    # Install with uv
    uvx reportseff

    # Check your recent jobs
    reportseff -u $USER
    ```
    [troycomi/reportseff](https://github.com/troycomi/reportseff)
    """),
        }, multiple=True),
    ])
    return


@app.cell
def _(mo, subprocess):
    def get_tmux_sessions():
        try:
            result = subprocess.check_output(
                ["tmux", "list-sessions"], text=True, stderr=subprocess.STDOUT
            )
            return result.strip()
        except (OSError, subprocess.CalledProcessError):
            sample = _sample_dir / "sample_tmux_sessions.txt"
            if sample.exists():
                return "*Sample data (not available in browser mode):*\n\n" + sample.read_text().strip()
            return "No tmux sessions running (or not available in browser mode)"

    tmux_button = mo.ui.button(
        label="List tmux sessions",
        on_click=lambda value: get_tmux_sessions(),
    )
    return (tmux_button,)


@app.cell
def _(mo, tmux_button):
    mo.vstack([
        mo.md("""
        # tmux — persistent terminal sessions

        **Presentor note:** Work through example/tmux

        Your SSH session dies if your connection drops. tmux keeps your work alive.

        | Action | Shortcut |
        |--------|----------|
        | New session | `tmux new -s name` |
        | Detach | `Ctrl+b` then `d` |
        | Reattach | `tmux attach -t name` |
        | Split horizontal | `Ctrl+b` then `"` |
        | Split vertical | `Ctrl+b` then `%` |
        | Switch panes | `Ctrl+b` then arrow keys |
        | List sessions | `tmux ls` |
        """),
        tmux_button,
        mo.md(f"```\n{tmux_button.value}\n```") if isinstance(tmux_button.value, str) and tmux_button.value else mo.md(""),
    ])
    return


@app.cell
def _(mo, subprocess):
    def get_recent_history():
        try:
            result = subprocess.check_output(
                ["bash", "-c", "HISTFILE=~/.bash_history; set -o history; history 20"],
                text=True, stderr=subprocess.STDOUT
            )
            return result.strip() if result.strip() else "No history available"
        except (OSError, subprocess.CalledProcessError):
            return "Not available in browser mode"

    history_button = mo.ui.button(
        label="Show recent history",
        on_click=lambda value: get_recent_history(),
    )
    return (history_button,)


@app.cell
def _(history_button, mo):
    mo.vstack([
        mo.md("""
        # Ctrl+R — reverse history search

        Stop retyping long commands. Press **Ctrl+R** and start typing to search
        through your command history.

        | Action | Key |
        |--------|-----|
        | Start search | `Ctrl+R` |
        | Next match | `Ctrl+R` (again) |
        | Accept & run | `Enter` |
        | Accept & edit | `Right arrow` or `Esc` |
        | Cancel | `Ctrl+C` |

        **Pro tip:** The more you type, the more specific the match.
        Try searching for `squeue` or `sbatch` — it finds your last invocation instantly.
        """),
        history_button,
        mo.md(f"```\n{history_button.value}\n```") if isinstance(history_button.value, str) and history_button.value else mo.md(""),
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md("""
        # uv — fast Python runtime and package manager

        [uv](https://docs.astral.sh/uv/) replaces pip, venv, pyenv, and pipx in a single tool.
        It's written in Rust and is 10-100x faster than pip.

        ```bash
        # Install uv (one line)
        curl -LsSf https://astral.sh/uv/install.sh | sh

        # Run a script with inline dependencies (no venv needed!)
        uv run my_script.py

        # Run a tool without installing it globally
        uvx ruff check .

        # Create a project with managed dependencies
        uv init my_project && cd my_project
        uv add numpy pandas
        ```
        """),
        mo.md("""
        **This very presentation** uses uv's inline script metadata:
        ```python
        # /// script
        # requires-python = ">=3.12"
        # dependencies = [
        #     "marimo>=0.19.6",
        # ]
        # ///
        ```
        Run it with `uvx marimo edit marimo_presentation.py --sandbox` and uv
        handles the rest.
        """),
    ])
    return


@app.cell
def _():
    # Slide 11: Claude Code
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md("""
        # Claude Code — AI in the terminal

        [Claude Code](https://docs.anthropic.com/en/docs/claude-code) is an agentic
        coding tool that lives in your terminal. It can read, write, and run code.

        ```bash
        # Install
        npm install -g @anthropic-ai/claude-code

        # Start a session in any repo
        cd my_project && claude
        ```

        **What it can do:**
        - Read and understand entire codebases
        - Write and edit files across multiple files at once
        - Run commands, tests, and debug errors
        - Create commits and pull requests
        - Search the web for documentation
        """),
        mo.callout(
            mo.md("""
            **This presentation was built collaboratively with Claude Code** —
            the mermaid diagram, the interactive `who`/`top` cells,
            the GitHub Actions workflow, and these slides were all
            created through conversation in the terminal.
            """),
            kind="info",
        ),
    ])
    return


@app.cell
def _(mo):
    mermaid_source = '''
    graph TD
        Yeast -->|Sequencing| DNA
        Yeast -->|Experiment| Growth-Kinetics
        DNA --> Analysis
        Growth-Kinetics --> Analysis
    '''

    mo.vstack([
        mo.md("""
        # Mermaid diagrams in GitHub Markdown

        GitHub natively renders mermaid-js in any Markdown file, issue, or PR.
        Just wrap your diagram in a `mermaid` code fence:
        """),
        mo.hstack([
            mo.md(f"""
    **Source (in any .md file like README.md):**

    ````
    ```mermaid
    {mermaid_source}
    ```
    ````
    """),
            mo.vstack([
                mo.md("**Rendered by GitHub and other tools:**"),
                mo.mermaid(f"""{mermaid_source}"""),
            ]),
        ], widths=[1, 1]),
        mo.md("Lots of different diagrams/plots with examples: https://mermaid.js.org/intro/")
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md("""
        # GitHub Actions — automate everything

        This presentation is automatically built and deployed on every push to `main`:

        ```yaml
        # .github/workflows/build-presentation.yml
        on:
          push:
            branches: [main]

        jobs:
          build:
            steps:
              - uses: actions/checkout@v4
              - uses: astral-sh/setup-uv@v5

              # Export static HTML
              - run: uvx marimo export html marimo_presentation.py -o presentation.html

              # Export interactive WASM version
              - run: uvx marimo export html-wasm marimo_presentation.py -o _site

              # Convert HTML to PDF with Playwright
              - run: uvx playwright install --with-deps chromium
              - run: uv run --with playwright python html_to_pdf.py

          deploy:  # Deploy WASM version to GitHub Pages
            uses: actions/deploy-pages@v4
        ```
        """),
        mo.callout(
            mo.md("""
            **Live right now:**
            [GitHub Pages](https://akeylab.github.io/20260227_group_meeting_Rob/)
            (interactive WASM version) |
            PDF and HTML available as
            [workflow artifacts](https://github.com/AkeyLab/20260227_group_meeting_Rob/actions)
            """),
            kind="success",
        ),
    ])
    return


@app.cell
def _():
    # Slide 14: Copilot on GitHub
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md("""
        # GitHub Copilot — AI on github.com

        GitHub Copilot isn't just for IDEs. On github.com it can:

        - **Summarize pull requests** — auto-generate PR descriptions from diffs
        - **Review code** — request a Copilot review alongside human reviewers
        - **Explain code** — highlight any code and ask "what does this do?"
        - **Search with Copilot Chat** — ask questions about a repo in natural language

        Available with a free tier for public repos and educational accounts.
        """),
        mo.callout(
            mo.md("""
            **Try it:** Go to any PR on GitHub and click
            **"Copilot" > "Summary"** to generate a PR description,
            or request a **Copilot code review** from the reviewers dropdown.
            """),
            kind="info",
        ),
    ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
