```bash
pip install fastbackfilter[perf]
python -m fastbackfilter.cli one sample.pdf
```

Common file types such as PNG, MP3, MP4, HTML, GZIP, JSON, CSV, TAR and WAV now
have dedicated engines. Engine detection runs all registered engines in parallel
for faster results. Use ``--only`` to limit scanning to particular engines.

Use the ``--only`` option to restrict detection to specific engines for faster
scans, for example:

```bash
python -m fastbackfilter.cli one sample.wav --only wav
```

## Logging

Set `FASTBACK_LOG` to change verbosity. Logs are emitted as pretty JSON, for example:

```bash
FASTBACK_LOG=INFO python -m fastbackfilter.cli one sample.pdf
```
