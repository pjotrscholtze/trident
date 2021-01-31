#!/bin/bash -e
#SBATCH -t 400:00 -N 1 -n 8 --mem=16000M

echo "run queries"
rm -rf /var/scratch/pse740/test
time ~/trident/build/trident load -i /var/scratch/pse740/test -f /var/scratch/pse740/latest-lexemes.nt.gz
du -h -d0 /var/scratch/pse740/test

~/trident/build/trident benchmark -i /var/scratch/pse740/test --query_file /var/scratch/pse740/queries_for_das.sparql --query_type query --logfile --logfile /var/scratch/pse740/queries.log