
.. image:: https://badge.fury.io/py/sequana-nanomerge.svg
     :target: https://pypi.python.org/pypi/sequana_nanomerge

.. image:: http://joss.theoj.org/papers/10.21105/joss.00352/status.svg
    :target: http://joss.theoj.org/papers/10.21105/joss.00352
    :alt: JOSS (journal of open source software) DOI

.. image:: https://github.com/sequana/nanomerge/actions/workflows/main.yml/badge.svg
   :target: https://github.com/sequana/nanomerge/actions/workflows    




This is is the **nanomerge** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ project

:Overview: TODO 
:Input: TODO
:Output: TODO
:Status: draft
:Citation: Cokelaer et al, (2017), ‘Sequana’: a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI doi:10.21105/joss.00352


Installation
~~~~~~~~~~~~

If you already have all requirements, you can install the packages using pip::

    pip install sequana_nanomerge --upgrade

Otherwise, you can create a *sequana_nanomerge* conda environment executing::

    conda env create -f environment.yml

and later activate the environment::

  conda activate sequana_nanomerge

A third option is to install the pipeline with pip method (see above) and use singularity as explained afterwards.


Usage
~~~~~

::

    sequana_pipelines_nanomerge --help
    sequana_pipelines_nanomerge --input-directory DATAPATH 

This creates a directory with the pipeline and configuration file. You will then need 
to execute the pipeline::

    cd nanomerge
    sh nanomerge.sh  # for a local run

This launch a snakemake pipeline. If you are familiar with snakemake, you can 
retrieve the pipeline itself and its configuration files and then execute the pipeline yourself with specific parameters::

    snakemake -s nanomerge.rules -c config.yaml --cores 4 --stats stats.txt

Or use `sequanix <https://sequana.readthedocs.io/en/master/sequanix.html>`_ interface.


Usage with singularity::
~~~~~~~~~~~~~~~~~~~~~~~~~

With singularity, initiate the working directory as follows::

    sequana_nanomerge --use-singularity

Images are downloaded in the working directory but you can store then in a directory globally (e.g.)::

    sequana_nanomerge --use-singularity --singularity-prefix ~/.sequana/apptainers

and then::

    cd nanomerge
    sh nanomerge.sh

if you decide to use snakemake manually, do not forget to add singularity options::

    snakemake -s nanomerge.rules -c config.yaml --cores 4 --stats stats.txt --use-singularity --singularity-prefix ~/.sequana/apptainers --singularity-args "-B /home:/home"

    
Requirements
~~~~~~~~~~~~

This pipelines requires the following executable(s):

- TODO

.. image:: https://raw.githubusercontent.com/sequana/sequana_nanomerge/master/sequana_pipelines/nanomerge/dag.png


Details
~~~~~~~~~

This pipeline runs **nanomerge** in parallel on the input fastq files (paired or not). 
A brief sequana summary report is also produced.


Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/sequana_nanomerge/master/sequana_pipelines/nanomerge/config.yaml>`_
to be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file. 

Changelog
~~~~~~~~~

========= ====================================================================
Version   Description
========= ====================================================================
0.0.1     **First release.**
========= ====================================================================


