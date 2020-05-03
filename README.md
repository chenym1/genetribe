# genetribe

Multiple-level homolog-identification pipeline.

[Our homepage]()

Authors | Email
------------ | -------------
Chen, Yongming | chen_yongming@126.com
Guo, Weilong | guoweilong@126.com

## Dependencies

The GeneTribe is implemented in `python3`, and three external command-line tools, which are executable on your `PATH`,  are needed:
- [blast](https://blast.ncbi.nlm.nih.gov/Blast.cgi?)     `conda install blast -c bioconda`
- [MCscan](https://github.com/tanghaibao/jcvi/)    `pip install jcvi`
- [bedtools](https://bedtools.readthedocs.io/en/latest/)  `conda install bedtools -c bioconda`

## Installation

- The easy way to install:
```sh
git clone git@github.com:chenym1/genetribe.git
cd genetribe
./install.sh
```

## Command
```sh
genetribe -h
```
```sh
# Program: genetribe (tools for homologoues inference)
# Version: 0.1.0

# Usage: genetribe <command> [options]

# Subcommands include:

# [ pipeline ]
#      core           The core workflow of genetribe
#      sameassembly   The Homolog inference for same assembly

# [  tools ]
#      RBH            Obtain Reciprocal Best Hits(RBH)
#      CBS            Calculate Collinearity Block Score(CBS)
#      longestcds     Extract the longest protein sequence from protein fasta

# Author: Chen,Yongming; chen_yongming@126.com
```

For more **details**, check [our tutorial]()
