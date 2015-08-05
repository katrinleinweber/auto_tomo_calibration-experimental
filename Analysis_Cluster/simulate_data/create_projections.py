import numpy as np
import pylab as pl
from scipy.fftpack import fftshift, fft, ifftshift, ifft2
from scipy.ndimage.interpolation import rotate


def add_noise(np_image, amount):
    """
    Adds random noise to the image
    """
    noise = np.random.randn(np_image.shape[0],np_image.shape[1],np_image.shape[2])
    norm_noise = noise/np.max(noise)
    np_image = np_image + norm_noise*np.max(np_image)*amount
    
    return np_image


def get_projections_2D(image):
    """
    Obtain the Radon transform
    """
    
    # Project the sinogram
    sinogram = np.array([
            # Sum along one axis
            np.sum(
                # Rotate image
                rotate(image, theta, order=3, reshape=False, mode='constant', cval=0.0)
                ,axis=0) for theta in xrange(180)])
    
    pl.imshow(sinogram)
    pl.gray()
    pl.show()
    
    from PIL import Image # Import the library
    im = Image.fromarray(image) # Convert 2D array to image object
    im.save("numerical.tif") # Save the image object as tif format

    return sinogram



def elipse2(A1, B1, C1, value1, A2, B2, C2, value2, size):
    
    xc1, yc1 = C1
    xc2, yc2 = C2
     
    step = 1. / (size / 2.)
    Y, X = np.meshgrid(np.arange(-1, 1 + step, step), np.arange(1, -1 - step, -step))

     
    mask1 = (((X - xc1)**2 / A1**2 + (Y - yc1)**2 / B1**2) <= 1)
    mask2 = (((X - xc2)**2 / A2**2 + (Y - yc2)**2 / B2**2) <= 1)

    
    image = np.zeros((size, size))
    image[mask1] = value1
    image[mask2] = value2 
    
    
    from PIL import Image # Import the library
    im = Image.fromarray(image) # Convert 2D array to image object
    im.save("projection.tif") # Save the image object as tif format
    
    return image


def sphere(R1, R2, C1, C2, value1, value2, size):
    
    sphere = np.zeros((size, size, size))

    Xc1, Yc1, Zc1 = C1
    Xc2, Yc2, Zc2 = C2
    
    step = 1. / (size / 2.)
    X, Y, Z = np.meshgrid(np.arange(-1, 1 + step, step), np.arange(1, -1 - step, -step), np.arange(-1, 1 + step, step))
    mask1 = (((X - Xc1)**2 + (Y - Yc1)**2 + (Z - Zc1)**2) < R1**2)
    mask2 = (((X - Xc2)**2 + (Y - Yc2)**2 + (Z - Zc2)**2) < R2**2)
    
    sphere[mask1] = value1
    sphere[mask2] = value2
    
    return sphere


def alpha(A, B, theta):
    return np.sqrt((A**2) * (np.cos(theta))**2 + (B**2) * (np.sin(theta))**2)

    

def projection_shifted(A, B, C, theta, value, t):
    """
    Analytical projections for an elliptical phantom
    """
    xc, yc = C
    
    alph = alpha(A, B, theta)
    try:
        gamma = np.arctan(yc / xc)
    except:
        # arctan at infinity is 90 degrees
        gamma = np.radians(90)
        
    s = np.sqrt(xc**2 + yc**2)
    
    correction = t - s * np.cos(gamma - theta)
    
    if abs(correction) <= alph:
        return ((2 * value * A * B) / (alph**2) * np.sqrt(alph**2 - correction**2))
    else:
        return 0


def analytical(A1, B1, C1, value1, A2, B2, C2, value2, size):
    """
    Get projections at every angle
    """
    sinogram = np.empty([180, size])

    for theta in range(180):
    
        angle = np.radians(theta)
        step = 1. / (size / 2.)
        
        projection = []
        counter = 0

        for t in np.arange(-1.0, 1.0 + step, step):
            
            if counter < size:
                proj1 = projection_shifted(B1, A1, C1, angle, value1, t)
                proj2 = projection_shifted(B2, A2, C2, angle, value2, t)
                proj = proj1 + proj2
                projection.append(proj)
                counter += 1

        if projection:
            sinogram[theta, :] = projection
            
    from PIL import Image # Import the library
    im = Image.fromarray(sinogram) # Convert 2D array to image object
    im.save("analytical.tif") # Save the image object as tif format    
     
    return sinogram


def analytical_3D(R1, C1, value1, R2, C2, value2, size):
    """
    Get projections at every angle
    """
    
    step = 1. / (size / 2.)
    for z in np.arange(-1.0, 1.0 + step, step):
                
        sinogram = np.empty([180, size])
        
        h1 = abs(z - abs(C1[2]))
        new_r1 = np.sqrt(R1**2 - h1**2)
        h2 = abs(z - abs(C2[2]))
        new_r2 = np.sqrt(R2**2 - h2**2)
        
        for theta in range(180):
        
            angle = np.radians(theta)
            projection = []
            counter = 0
            
            for t in np.arange(-1.0, 1.0 + step, step):
                
                if counter < size:
                    
                    proj1 = 0
                    proj2 = 0
                    
                    if R1 >= h1:
                        proj1 = projection_shifted(new_r1, new_r1, (C1[0], C1[1]), angle, value1, t)
                        
                    if R2 >= h2:
                        proj2 = projection_shifted(new_r2, new_r2, (C2[0], C2[1]), angle, value2, t)
                        
                    proj = proj1 + proj2
                    projection.append(proj)
                    counter += 1
    
            sinogram[theta, :] = projection
            
        from PIL import Image # Import the library
        recon = reconstruct(sinogram)
        im = Image.fromarray(recon) # Convert 2D array to image object
        im.save("analytical%i.tif" % ((z+1)/step)) # Save the image object as tif format    
     
    return sinogram


def reconstruct(sinogram):
    
    from skimage.transform import iradon
    sinogram = sinogram.T
    reconstruction_fbp = iradon(sinogram)#, circle=True)
    return reconstruction_fbp
    
# These are diameters
A1 = 0.3
B1 = 0.3
C1 = (0., 0.)
A2 = 0.3
B2 = 0.3
C2 = (0., 0.6)
  
scale = 100
# image = elipse2(A1, B1, C1, 2., A2, B2, C2, -1, scale)
# fig = pl.figure()
# pl.imshow(image)
# pl.gray()
# pl.show()
#  
# sino = analytical(A1, B1, C1, 2., A2, B2, C2, -1, scale)
# pl.imshow(sino)
# pl.gray()
# pl.show()
#   
# numer = get_projections_2D(image)
# 
# reconstruct(sino)
# reconstruct(numer)


# ### Sphere analytical ###
R1 = 0.2
R2 = 0.2
C1 = (0., 0., 0.)
C2 = (0., 0.4, 0.)
size = 256
analytical_3D(R1, C1, 1., R2, C2, 1.5, size)
