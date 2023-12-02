import os
import subprocess
import sys


from sequana_pipelines.nanomerge.main import main
from . import test_dir
from click.testing import CliRunner

def test_standalone_subprocess(tmpdir):
    input_dir = os.sep.join((test_dir, 'resources'))
    cmd = ["test", "--input-directory", input_dir, "--working-directory", str(tmpdir), "--force"]
    subprocess.call(cmd)


def test_standalone_script(tmpdir):
    input_dir = os.sep.join((test_dir, 'data', "barcoded"))
    samplesheet = os.sep.join((test_dir, 'data',  "samplesheet.csv"))
    summary = os.sep.join((test_dir, 'data', "sequence_summary.txt"))

    runner = CliRunner()
    results = runner.invoke(main, ["--input-directory", input_dir, "--working-directory", str(tmpdir), "--force",
"--input-pattern", "*/*fastq.gz", "--sample-sheet", samplesheet, "--summary", summary])
    assert results.exit_code == 0


def test_standalone_script2(tmpdir):
    input_dir = os.sep.join((test_dir, 'data', "unbarcoded"))
    samplesheet = os.sep.join((test_dir, 'data',  "samplesheet_unbarcoded.csv"))
    summary = os.sep.join((test_dir, 'data',  "sequence_summary.txt"))

    runner = CliRunner()
    results = runner.invoke(main, ["--input-directory", input_dir, "--working-directory", str(tmpdir), "--force",
"--input-pattern", "*fastq.gz", "--sample-sheet", samplesheet, "--summary", summary])
    assert results.exit_code == 0



def test_version():
    cmd = ["sequana_nanomerge", "--version"]
    subprocess.call(cmd)

