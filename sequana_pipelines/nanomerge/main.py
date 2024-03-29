#
#  This file is part of Sequana software
#
#  Copyright (c) 2016-2021 - Sequana Dev Team (https://sequana.readthedocs.io)
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  Website:       https://github.com/sequana/sequana
#  Documentation: http://sequana.readthedocs.io
#  Contributors:  https://github.com/sequana/sequana/graphs/contributors
##############################################################################
import sys
import os
import subprocess
import shutil
from pathlib import Path

import rich_click as click
import click_completion

click_completion.init()

from sequana_pipetools.options import *
from sequana_pipetools import SequanaManager


NAME = "nanomerge"

help = init_click(
    NAME,
    groups={
        "Pipeline Specific": [
            "--promethion",
            "--summary",
            "--summary-percentage",
            "--summary-max-gb",
            "--sample-sheet",
            "--update-taxonomy",
        ],
    },
)


@click.command(context_settings=help)
@include_options_from(ClickSnakemakeOptions, working_directory=NAME)
@include_options_from(ClickSlurmOptions)
@include_options_from(ClickInputOptions, add_input_readtag=False)
@include_options_from(ClickGeneralOptions)
@click.option(
    "--sample-sheet",
    "samplesheet",
    required=True,
    default="SampleSheet.csv",
    show_default=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="""a CSV with 3 columns named project,sample,barcode """,
)
@click.option(
    "--summary",
    "summary",
    default=None,
    type=click.Path(file_okay=True, dir_okay=False),
    help="a summary file generated by albacore or guppy. if provided, pyqoQC is used to generate a HTML report. ",
)
@click.option(
    "--summary-percentage",
    "summary_percentage",
    default=None,
    type=click.INT,
    show_default=True,
    help="percentage of the sequencing summary file to process. Use this option if you have memory issue typically with promethium runs). If unset, nanomerge will set this value automatically so that the final file to process do not exceed 16Go. This value can be changed with --summary-max--gb",
)
@click.option(
    "--summary-max-gb",
    "summary_max_gb",
    help="max size of the summary file before performing sub sampling automatically. Use this option if you have memory issue.",
    default=16,
    type=click.FLOAT,
    show_default=True,
)
@click.option("--promethion", is_flag="store_true", help="set summary_percentage to 10%%")
def main(**options):
    # the real stuff is here
    manager = SequanaManager(options, NAME)
    manager.setup()


    # aliases
    options = manager.options
    cfg = manager.config.config

    # fills input_data, input_directory, input_readtag
    # needs an update of sequana_pipetools to exclude readtag
    #manager.fill_data_options(no_readtag=True)

    def fill_input_directory():
        cfg.input_directory = os.path.abspath(options.input_directory)

    def fill_input_pattern():
        cfg.input_pattern = options.input_pattern

    def fill_samplesheet():
        if os.path.exists(options.samplesheet):
            shutil.copy(options.samplesheet, manager.workdir)
            cfg.samplesheet = Path(options.samplesheet).name
        else:
            raise IOError(f"{options.samplesheet} not found. Requested to perfom the merge of FastQ files")

    def fill_summary():
        if options.summary:
            if os.path.exists(options.summary):
                shutil.copy(options.summary, manager.workdir)
                cfg.summary = Path(options.summary).name
            elif not os.path.exists(options.summary):
                raise IOError(f"{options.summary} not found. Check your input filename")

            # if the sequencing summary file is large (larger than 16gb by default) we sub sample the data
            # The percentage is set automatically to have a final file of 16Gb (by default)

            if options.summary_percentage is None:
                cfg.sub_sample_summary.percentage = options.summary_max_gb / (
                    os.stat(options.summary).st_size / 1024 / 1024 / 1024
                )
                cfg.sub_sample_summary.percentage = int(cfg.sub_sample_summary.percentage * 100)
                if cfg.sub_sample_summary.percentage > 100:
                    cfg.sub_sample_summary.percentage = 100
                if cfg.sub_sample_summary.percentage < 100:
                    size = os.stat(options.summary).st_size / 1024 / 1024 / 1024
                    logger.warning(
                        f"Input file size is {size}Gb , which is larger than {options.summary_max_gb}Gb. Will use {cfg.sub_sample_summary.percentage}% of the data"
                    )
            else:  # user sets the value himself, so nothing to do
                cfg.sub_sample_summary.percentage = options.summary_percentage

            # if --promethion was used, set percentage to 10 whatsover
            if options.promethion:
                cfg.sub_sample_summary.percentage = 10
        else:
            cfg.summary = None


    if options['from_project']:
        if '--sample-sheet' in sys.argv:
            fill_samplesheet()
        if "--summary" in sys.argv:
            fill_summary()
        if "--input-directory" in sys.argv:
            fill_input_directory()
        if "--input-pattern" in sys.argv:
            fill_input_pattern()
    else:
        fill_input_directory()
        fill_input_pattern()
        fill_samplesheet()
        fill_summary()

    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()



if __name__ == "__main__":
    main()
