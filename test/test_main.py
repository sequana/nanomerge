import os
import subprocess
import sys

import sequana_pipelines.nanomerge.main as m
from . import test_dir

def test_standalone_subprocess(tmpdir):
    input_dir = os.sep.join((test_dir, 'resources'))
    cmd = ["test", "--input-directory", input_dir, "--working-directory", str(tmpdir), "--force"]
    subprocess.call(cmd)


def test_standalone_script(tmpdir):
    input_dir = os.sep.join((test_dir, 'data', "barcoded"))
    samplesheet = os.sep.join((test_dir, 'data',  "samplesheet.csv"))
    summary = os.sep.join((test_dir, 'data', "sequence_summary.txt"))
    sys.argv = ["test", "--input-directory", input_dir, "--working-directory", str(tmpdir), "--force", 
        "--input-pattern", "*/*fastq.gz", "--samplesheet", samplesheet, "--summary", summary]
    m.main()


def test_standalone_script2(tmpdir):
    input_dir = os.sep.join((test_dir, 'data', "unbarcoded"))
    samplesheet = os.sep.join((test_dir, 'data',  "samplesheet_unbarcoded.csv"))
    summary = os.sep.join((test_dir, 'data',  "sequence_summary.txt"))
    sys.argv = ["test", "--input-directory", input_dir, "--working-directory", str(tmpdir), "--force", 
        "--input-pattern", "*fastq.gz", "--samplesheet", samplesheet, "--summary", summary]
    m.main()


def test_version():
    cmd = ["sequana_nanomerge", "--version"]
    subprocess.call(cmd)

