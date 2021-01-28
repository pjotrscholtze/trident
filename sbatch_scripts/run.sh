#!/bin/bash -e
#SBATCH -t 75:00 -N 1 -n 8 --mem=16000M

echo "Round 1"
rm -rf /var/scratch/pse740/test
time ~/trident/build/trident load -i /var/scratch/pse740/test -f /var/scratch/pse740/latest-lexemes.nt.gz
du -h -d0 /var/scratch/pse740/test

echo "Round 2"
rm -rf /var/scratch/pse740/test
time ~/trident/build/trident load -i /var/scratch/pse740/test -f /var/scratch/pse740/latest-lexemes.nt.gz
du -h -d0 /var/scratch/pse740/test

echo "Round 3"
rm -rf /var/scratch/pse740/test
time ~/trident/build/trident load -i /var/scratch/pse740/test -f /var/scratch/pse740/latest-lexemes.nt.gz
du -h -d0 /var/scratch/pse740/test

echo "Round 4"
rm -rf /var/scratch/pse740/test
time ~/trident/build/trident load -i /var/scratch/pse740/test -f /var/scratch/pse740/latest-lexemes.nt.gz
du -h -d0 /var/scratch/pse740/test

echo "Round 5"
rm -rf /var/scratch/pse740/test
time ~/trident/build/trident load -i /var/scratch/pse740/test -f /var/scratch/pse740/latest-lexemes.nt.gz
du -h -d0 /var/scratch/pse740/test

