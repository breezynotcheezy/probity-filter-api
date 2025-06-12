```bash
pip install fastbackfilter[perf]
python -m fastbackfilter.cli one sample.pdf
```

Common file types such as PNG, MP3, MP4, HTML and GZIP now have dedicated
engines.  Engine detection runs all registered engines in parallel for faster
results.

## Logging

Set `FASTBACK_LOG` to change verbosity. Logs are emitted as pretty JSON, for example:

```bash
FASTBACK_LOG=INFO python -m fastbackfilter.cli one sample.pdf
```
