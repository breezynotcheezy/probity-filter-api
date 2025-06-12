```bash
pip install fastbackfilter[perf]
python -m fastbackfilter.cli one sample.pdf
```

Common file types such as PNG, MP3, MP4, HTML, GZIP, JSON, CSV, TAR, WAV, EXE,
BAT and SH now have dedicated engines. Additional engines cover Python, Java,
JavaScript, C and Git ``.rev`` index files. Engine detection runs all registered
engines concurrently for faster results. Use ``--only`` to limit scanning to
particular engines.

Confidence scores are now computed from weighted heuristics for more accurate
results without adding overhead.

Use the ``--only`` option to restrict detection to specific engines for faster
scans, for example:

```bash
python -m fastbackfilter.cli one sample.wav --only wav
```

You can also restrict directory scans to specific file extensions using
``--ext``:

```bash
python -m fastbackfilter.cli all mydir --ext exe sh
```

## Logging

Set `FASTBACK_LOG` to change verbosity. Logs are emitted as pretty JSON, for example:

```bash
FASTBACK_LOG=INFO python -m fastbackfilter.cli one sample.pdf
```
