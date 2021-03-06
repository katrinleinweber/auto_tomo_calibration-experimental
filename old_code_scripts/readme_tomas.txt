# Task IDs: "start-stop:step"

# You can find below all the necessary commands to run my program.
# To use the cluster:
# Run the single file "submit.sh" after having modified the names of the files you want to run in this same file and in "run.sh".
# The file called "monitor.sh" is used to display the job array running on the cluster.
# qstat -u '*' shows all of the jobs on the cluster
# qstat shows your jobs on the cluster
# watch qstat shows a live feed of the jobs in the queue

# qdel - removes all your jobs

# Detector -----------------------------------------------------------------
module load global/cluster
cd /dls/tmp/jjl36382/logs
qsub -pe smp 2 -j y -t 1:2159:10 -tc 20 ~/auto_tomo_calibration-experimental/Analysis_Cluster/run.sh /dls/science/groups/das/ExampleData/SphereTestData/38644/recon_%05i.tif /dls/tmp/jjl36382/results/out%05i.dat
# In run.sh
module load python/ana
python ~/auto_tomo_calibration-experimental/Analysis_Cluster/detector.py $@


# CHANGE THE RANGE IN ANALYSE.PY. THE RANGE CORRESPONDS TO THE NUMBER OF FILES IN
# Analyse: get centres and radii -------------------------------------------
module load python/ana
cd /dls/tmp/jjl36382/logs
python ~/auto_tomo_calibration-experimental/Analysis_Cluster/analyse.py


# Area selector ------------------------------------------------------------
module load global/cluster
cd /dls/tmp/jjl36382/logs
qsub -pe smp 2 -j y -t 1 -tc 10 ~/auto_tomo_calibration-experimental/Analysis_Cluster/run.sh /dls/tmp/jjl36382/spheres/sphere%02i.npy
# In run.sh
module load python/ana
python ~/auto_tomo_calibration-experimental/Analysis_Cluster/selector.py -x 1105 -y 1002 -z 1470 -r 380 $@


# Filter whole spheres (numbers 3 to 6 in this data) -----------------------
module load global/cluster
cd /dls/tmp/jjl36382/logs
qsub -pe smp 2 -j y -t 1 -tc 10 ~/auto_tomo_calibration-experimental/Analysis_Cluster/run.sh /dls/tmp/jjl36382/spheres/sphere%02i.npy /dls/tmp/jjl36382/spheres/sphere_f%02i.npy
# In run.sh
module load python/ana
python ~/auto_tomo_calibration-experimental/Analysis_Cluster/filter_sphere.py $@


# Get radii according to angles --------------------------------------------
module load global/cluster
cd /dls/tmp/jjl36382/logs
qsub -pe smp 2 -j y -t 1-360:10 -tc 20 ~/auto_tomo_calibration-experimental/Analysis_Cluster/run.sh /dls/tmp/jjl36382/spheres/sphere_f%02i.npy /dls/tmp/jjl36382/radii/radii%03i.npy
# In run.sh
module load python/ana
python ~/auto_tomo_calibration-experimental/Analysis_Cluster/get_radii.py -x 1105 -y 1002 -z 1470 $@


# Plot radii ----------------------------------------------------------------
# Not sure if matplotlib works without Dawn - otherwise run with Dawn
module load python/ana
cd /dls/tmp/jjl36382/logs
python ~/auto_tomo_calibration-experimental/Analysis_Cluster/plot_radii.py
