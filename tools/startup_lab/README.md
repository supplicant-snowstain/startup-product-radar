# Startup Radar — Hypothesis Evaluation Prototype v0.1

Experimental, not production-ready. This is a deterministic audit of supplied evidence metadata; it does not browse the web or prove startup viability.

From repository root:

```bash
PYTHONPATH=tools/startup_lab python -m startup_lab benchmark
PYTHONPATH=tools/startup_lab python -m unittest discover -s tools/startup_lab/tests -v
PYTHONPATH=tools/startup_lab python -m startup_lab evaluate tools/startup_lab/examples/idea.json
```

The benchmarks are **synthetic test fixtures**. example.org URLs are placeholders, not verified observations. The tool detects missing independent need evidence, lack of competitors/counterevidence, invalid metadata, and unsupported inferences from VC investment. It does not verify source authenticity or conduct real user research.

Future modules: evidence acquisition, URL verification, cross-product retrieval, contradiction discovery, and uncertainty calibration. Keep generated inferences separate from curated source evidence.
