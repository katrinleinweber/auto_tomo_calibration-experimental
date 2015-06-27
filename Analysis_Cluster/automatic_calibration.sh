# Detector -----------------------------------------------------------------
module load global/cluster
module load python/ana

#cd /dls/tmp/jjl36382/logs

#read -p "enter path " path

#read -p "enter step " step

#qsub -pe smp 2 -j y -t 1-2159:10 -tc 10 python ~/auto_tomo_calibration-experimental/Analysis_Cluster/detector.py $path"recon_%05i.tif" /dls/tmp/jjl36382/results/out%05i.dat

# CHANGE THE RANGE IN ANALYSE.PY. THE RANGE CORRESPONDS TO THE NUMBER OF FILES IN
# Analyse: get centres and radii -------------------------------------------

#python ~/auto_tomo_calibration-experimental/Analysis_Cluster/analyse.py


# Area selector ------------------------------------------------------------

nb_spheres=`cat ~/Documents/auto_tomo_calibration-experimental/Analysis_Cluster/nb_spheres.txt`
centX=`~/Documents/auto_tomo_calibration-experimental/Analysis_Cluster/centresX.txt`
centY=`~/Documents/auto_tomo_calibration-experimental/Analysis_Cluster/centresY.txt`
centZ=`~/Documents/auto_tomo_calibration-experimental/Analysis_Cluster/centresZ.txt`

for i in `seq 1 $nb_spheres`;
do
	X=`awk "NR=="$i ~/Documents/auto_tomo_calibration-experimental/Analysis_Cluster/centresX.txt`
	echo $X
	qsub -pe smp 2 -j y -t $ ~/auto_tomo_calibration-experimental/Analysis_Cluster/run.sh
done


#qsub -pe smp 2 -j y -t 1-7 -tc 10 ~/auto_tomo_calibration-experimental/Analysis_Cluster/run.sh /dls/tmp/jjl36382/spheres/sphere%02i.npy

#python ~/auto_tomo_calibration-experimental/Analysis_Cluster/selector.py -x 456 -y 456 -z 456 -r 380 $@


# Filter whole spheres (numbers 3 to 6 in this data) -----------------------
#qsub -pe smp 2 -j y -t 3-6 -tc 10 ~/auto_tomo_calibration-experimental/Analysis_Cluster/run.sh /dls/tmp/jjl36382/spheres/sphere%02i.npy /dls/tmp/jjl36382/spheres/sphere_f%02i.npy
#python ~/auto_tomo_calibration-experimental/Analysis_Cluster/filter_sphere.py $@


# Get radii according to angles --------------------------------------------
#qsub -pe smp 2 -j y -t 1-360:10 -tc 10 ~/auto_tomo_calibration-experimental/Analysis_Cluster/run.sh /dls/tmp/jjl36382/spheres/sphere_f%02i.npy /dls/tmp/jjl36382/radii/radii%03i.npy

#python ~/auto_tomo_calibration-experimental/Analysis_Cluster/get_radii.py -x 456 -y 456 -z 456 $@


# Plot radii ----------------------------------------------------------------

#python ~/auto_tomo_calibration-experimental/Analysis_Cluster/plot_radii.py
