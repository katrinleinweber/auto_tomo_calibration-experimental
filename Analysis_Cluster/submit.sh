module load global/cluster
cd /dls/tmp/jjl36382/logs
qsub -pe smp 2 -j y -t 1-360:10 -tc 10 ~/auto_tomo_calibration-experimental/Analysis_Cluster/run.sh /dls/tmp/jjl36382/spheres/sphere01.npy /dls/tmp/jjl36382/radii/radii%03i.npy
