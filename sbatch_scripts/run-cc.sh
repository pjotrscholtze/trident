#!/bin/bash -e
#SBATCH -t 75:00 -N 1 -n 8 --mem=16000M

echo "Round 1 (cache clear)"
rm -rf /var/scratch/pse740/test-cache-clear
sync; echo 3 > /proc/sys/vm/drop_caches; swapoff -a && swapon -a
time ~/trident/build/trident load -i /var/scratch/pse740/test-cache-clear -f /var/scratch/pse740/latest-lexemes.nt.gz
du -h -d0 /var/scratch/pse740/test-cache-clear

echo "Round 2 (cache clear)"
rm -rf /var/scratch/pse740/test-cache-clear
sync; echo 3 > /proc/sys/vm/drop_caches; swapoff -a && swapon -a
time ~/trident/build/trident load -i /var/scratch/pse740/test-cache-clear -f /var/scratch/pse740/latest-lexemes.nt.gz
du -h -d0 /var/scratch/pse740/test-cache-clear

echo "Round 3 (cache clear)"
rm -rf /var/scratch/pse740/test-cache-clear
sync; echo 3 > /proc/sys/vm/drop_caches; swapoff -a && swapon -a
time ~/trident/build/trident load -i /var/scratch/pse740/test-cache-clear -f /var/scratch/pse740/latest-lexemes.nt.gz
du -h -d0 /var/scratch/pse740/test-cache-clear

echo "Round 4 (cache clear)"
rm -rf /var/scratch/pse740/test-cache-clear
sync; echo 3 > /proc/sys/vm/drop_caches; swapoff -a && swapon -a
time ~/trident/build/trident load -i /var/scratch/pse740/test-cache-clear -f /var/scratch/pse740/latest-lexemes.nt.gz
du -h -d0 /var/scratch/pse740/test-cache-clear

echo "Round 5 (cache clear)"
rm -rf /var/scratch/pse740/test-cache-clear
sync; echo 3 > /proc/sys/vm/drop_caches; swapoff -a && swapon -a
time ~/trident/build/trident load -i /var/scratch/pse740/test-cache-clear -f /var/scratch/pse740/latest-lexemes.nt.gz
du -h -d0 /var/scratch/pse740/test-cache-clear

