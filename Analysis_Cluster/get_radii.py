import os
from skimage import io
import numpy as np

import radii_angles

def save_data(filename, data):
    print("Saving data")
    f = open(filename, 'w')
    np.save(f, data)
    f.close()

if __name__ == '__main__' :
    import optparse
    usage = "%prog [options] input_file_template, output_file_template \n" + \
        "  input_file_template  = /location/of/file/filename%02i.npy \n" + \
        "  output_file_template = /location/of/output/filename%02i.dat"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-x", "--xpos", dest="x_pos", help="X position of the centre of the sphere of interest", default=500, type='int')
    parser.add_option("-y", "--ypos", dest="y_pos", help="Y position of the centre of the sphere of interest", default=500, type='int')
    parser.add_option("-z", "--zpos", dest="z_pos", help="Z position of the centre of the sphere of interest", default=500, type='int')
    
    (options, args) = parser.parse_args()
    
    print "x = %i, y = %i, z = %i" % (options.x_pos, options.y_pos, options.z_pos)
    
    (options, args) = parser.parse_args()
    
    x = options.x_pos
    y = options.y_pos
    z = options.z_pos
    
    # get the number of the frame to process
    task_id = int(os.environ['SGE_TASK_ID']) - 1
    
    # make the filename
    input_filename = args[0]
    output_filename = args[1] % task_id
    
    # load the sphere
    print("Loading image %s" % input_filename)
    sphere = np.load(input_filename)
    
    # measure radii
    radii = radii_angles.plot_radii(sphere, (x, y, z), task_id, task_id+10)
    
    # save data
    print("Saving data %s" % output_filename)
    save_data(output_filename, radii)
