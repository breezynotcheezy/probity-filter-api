```bash
pip install fastbackfilter[perf]
python -m fastbackfilter.cli one sample.pdf
```

## Logging

Set `FASTBACK_LOG` to change verbosity. Logs are emitted as pretty JSON, for example:

```bash
FASTBACK_LOG=INFO python -m fastbackfilter.cli one sample.pdf
```
