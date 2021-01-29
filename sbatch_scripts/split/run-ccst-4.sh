#!/bin/bash -e
#SBATCH -t 75:00 -N 1 -n 8 --mem=16000M

ROUND=4
echo "Round $ROUND (cache clear + skiptables)"
rm -rf /var/scratch/pse740/test-cache-clear-skip-tables-$ROUND
time ~/trident/build/trident load -i /var/scratch/pse740/test-cache-clear-skip-tables-$ROUND -f /var/scratch/pse740/latest-lexemes.nt.gz --skipTables true
du -h -d0 /var/scratch/pse740/test-cache-clear-skip-tables-$ROUND
