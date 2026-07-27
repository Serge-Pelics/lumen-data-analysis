# Lumen Data Analysis / DMCA Takedown Visualizer

Exploratory open-source toolkit for studying **DMCA takedown notice patterns**, with a focus on signals that may indicate **abusive or false copyright complaints** submitted against websites and search indexes.

This repository is an early building block for future research into how automated and low-quality DMCA notices appear in public transparency datasets (for example, records collected by the [Lumen Database](https://lumendatabase.org/)).

## Research context

Search engines and platforms receive large volumes of copyright removal requests. Many are legitimate. A smaller but important subset appears to:

- reuse template language across many unrelated domains,
- list improbable “original work” URLs,
- arrive in sudden bursts from rotating sender identities,
- target affiliate, review, or informational pages rather than clear copyrighted media.

The long-term goal of this project is to help researchers, site operators, and journalists **detect and visualize those patterns** from structured notice exports (CSV), before expanding into live API monitoring when research access is available.

> This project does **not** give legal advice and does **not** determine whether any specific notice is lawful or unlawful. It is an analytical aid for transparency research.

## What this repo contains (v0.1)

| Path | Purpose |
|---|---|
| `analyze_dmca.py` | Baseline Python script: load a CSV of notices, summarize counts, and generate simple charts |
| `sample_data/dmca_notices_sample.csv` | Synthetic sample dataset for demos (not production Lumen exports) |
| `requirements.txt` | Python dependencies |
| `output/` | Generated charts (created when you run the script) |

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python analyze_dmca.py --input sample_data/dmca_notices_sample.csv --outdir output
```

The script prints a short console summary and writes PNG charts such as:

- notices over time,
- top sender names,
- sender-country distribution (when present).

## Expected CSV columns

Minimum useful columns:

```text
notice_id,date_received,sender,sender_country,recipient,target_domain,role
```

- `role` may be `original` or `infringing` (how the domain appears in the notice).
- Extra columns are ignored safely.

## Roadmap

- [ ] Connect to Lumen research API exports (when access is granted)
- [ ] Burst / template-similarity detectors for suspicious notice clusters
- [ ] Domain monitoring alerts for newly published notices
- [ ] Richer dashboards (interactive HTML) beyond static matplotlib charts
- [ ] Documentation of methodology for false-positive / false-negative evaluation

## Ethics & responsible use

Use this toolkit only for:

- academic or independent research,
- defending your own sites against abusive removals,
- public-interest transparency work.

Do not use it to harass complainants, evade valid copyright enforcement, or re-publish private contact data.

## Author

Maintained by [Serge-Pelics](https://github.com/Serge-Pelics) as part of ongoing SEO / search-integrity research.

## License

MIT — see `LICENSE`.
