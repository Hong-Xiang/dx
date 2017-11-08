#!/bin/bash
#SBATCH -o %J.out
#SBATCH -e %J.err
source ~/.bashrc
date
{{commands}}
date