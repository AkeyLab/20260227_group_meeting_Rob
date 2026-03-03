# Akey Group Meeting — February 27, 2026

Interactive presentation covering Princeton's Della HPC cluster, command-line productivity tools, and AI-assisted development. Built with [marimo](https://marimo.io) notebooks and deployed automatically via GitHub Actions.

## Live notebooks

- **[Presentation](https://akeylab.github.io/20260227_group_meeting_Rob/)** — interactive WASM version of the slides
- **[Marimo example notebook](https://akeylab.github.io/20260227_group_meeting_Rob/example/)** — showcases marimo features (reactive cells, UI widgets, plotting)
- **[PDF](presentation.pdf)** — static PDF of the presentation

## Topics covered

- **Della cluster** — architecture overview, SSH key setup, filesystem quotas, compute node specs
- **Job monitoring** — `checkquota`, `squeue`/`sacct`, `jobstats`, `reportseff`
- **Command-line tools** — tmux, Ctrl+R history search, uv (Python runtime/package manager)
- **AI tools** — Claude Code, GitHub Copilot
- **GitHub features** — Mermaid diagrams in Markdown, GitHub Actions CI/CD

## Project structure

```
├── marimo_presentation.py      # Main presentation notebook (slides)
├── marimo_example.py           # Example notebook demonstrating marimo features
├── layouts/                    # Slide layout configs
├── data/                       # Sample command outputs for browser/WASM mode
├── examples/
│   ├── slurm_job_monitoring/   # SLURM sbatch scripts and demo outputs
│   ├── tmux/                   # tmux live demo scripts
│   └── uv/                     # uv tutorial notes
├── .github/workflows/          # CI: build HTML/WASM/PDF, deploy to GitHub Pages
└── presentation.pdf            # Auto-generated PDF (committed by CI)
```

## Running locally

```bash
# Run the presentation (slides mode)
uvx marimo edit marimo_presentation.py --sandbox

# Run the example notebook
uvx marimo edit marimo_example.py --sandbox
```

The `--sandbox` flag tells uv to automatically install dependencies from the inline script metadata — no manual setup required.
