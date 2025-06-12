*************************************************************
pip install fastbackfilter
python -m fastbackfilter.cli one sample.pdf
*************************************************************



Set `FASTBACK_LOG` to change verbosity. Logs are emitted as pretty JSON, for example:

*************************************************************
FASTBACK_LOG=INFO python -m fastbackfilter.cli one sample.pdf
*************************************************************
