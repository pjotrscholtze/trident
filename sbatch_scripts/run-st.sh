#!/bin/bash -e
#SBATCH -t 75:00 -N 1 -n 8 --mem=16000M

echo "Round 1 (skiptables)"
rm -rf /var/scratch/pse740/test-skip-tables
time ~/trident/build/trident load -i /var/scratch/pse740/test-skip-tables -f /var/scratch/pse740/latest-lexemes.nt.gz --skipTables true
du -h -d0 /var/scratch/pse740/test-skiptables

echo "Round 2 (skiptables)"
rm -rf /var/scratch/pse740/test-skip-tables
time ~/trident/build/trident load -i /var/scratch/pse740/test-skip-tables -f /var/scratch/pse740/latest-lexemes.nt.gz --skipTables true
du -h -d0 /var/scratch/pse740/test-skiptables

echo "Round 3 (skiptables)"
rm -rf /var/scratch/pse740/test-skip-tables
time ~/trident/build/trident load -i /var/scratch/pse740/test-skip-tables -f /var/scratch/pse740/latest-lexemes.nt.gz --skipTables true
du -h -d0 /var/scratch/pse740/test-skiptables

echo "Round 4 (skiptables)"
rm -rf /var/scratch/pse740/test-skip-tables
time ~/trident/build/trident load -i /var/scratch/pse740/test-skip-tables -f /var/scratch/pse740/latest-lexemes.nt.gz --skipTables true
du -h -d0 /var/scratch/pse740/test-skiptables

echo "Round 5 (skiptables)"
rm -rf /var/scratch/pse740/test-skip-tables
time ~/trident/build/trident load -i /var/scratch/pse740/test-skip-tables -f /var/scratch/pse740/latest-lexemes.nt.gz --skipTables true
du -h -d0 /var/scratch/pse740/test-skiptables

