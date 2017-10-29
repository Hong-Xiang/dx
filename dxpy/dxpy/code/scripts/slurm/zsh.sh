#!/usr/bin/env zsh
#SBATCH -o %J.out
#SBATCH -e %J.err
source ~/.zshrc
date
{{commands}}
date
