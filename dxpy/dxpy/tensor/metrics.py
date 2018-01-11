import numpy as np


def rmse(label, target):
    err = target - label
    value = np.sqrt(np.sum(np.square(err)) / label.size)
    # base = np.sqrt(np.sum(np.square(target)) / label.size)
    # return value / base
    return value

def mean_absolute_error(label, target):
    err = target - label
    return np.mean(np.abs(err))

def bias(label, target):
    return np.mean(label - target)


def variance(label, target):
    return np.std(label - target)


def psnr(label, target):
    minv = np.min(label)
    maxv = np.max(label)
    sca = 255.0 / (maxv - minv)
    ln = (label - minv) * sca
    tn = (target - minv) * sca
    rmv = rmse(ln, tn)
    value = 10 * np.log((255.0**2) / (rmv**2)) / np.log(10)
    return value


'''
The function to compute SSIM
@param param: img_mat_1 1st 2D matrix
@param param: img_mat_2 2nd 2D matrix
'''


def ssim(label, target):
    minv = np.min(label)
    maxv = np.max(label)
    sca = 255.0 / (maxv - minv)
    img_mat_1 = (label - minv) * sca
    img_mat_2 = (target - minv) * sca
    import numpy
    import scipy.ndimage
    from numpy.ma.core import exp
    from scipy.constants.constants import pi
    # Variables for Gaussian kernel definition
    gaussian_kernel_sigma = 1.5
    gaussian_kernel_width = 11
    gaussian_kernel = numpy.zeros(
        (gaussian_kernel_width, gaussian_kernel_width))

    # Fill Gaussian kernel
    for i in range(gaussian_kernel_width):
        for j in range(gaussian_kernel_width):
            gaussian_kernel[i, j] =\
                (1 / (2 * pi * (gaussian_kernel_sigma**2))) *\
                exp(-(((i - 5)**2) + ((j - 5)**2)) /
                    (2 * (gaussian_kernel_sigma**2)))

    # Convert image matrices to double precision (like in the Matlab version)
    img_mat_1 = img_mat_1.astype(numpy.float)
    img_mat_2 = img_mat_2.astype(numpy.float)

    # Squares of input matrices
    img_mat_1_sq = img_mat_1**2
    img_mat_2_sq = img_mat_2**2
    img_mat_12 = img_mat_1 * img_mat_2

    # Means obtained by Gaussian filtering of inputs
    img_mat_mu_1 = scipy.ndimage.filters.convolve(img_mat_1, gaussian_kernel)
    img_mat_mu_2 = scipy.ndimage.filters.convolve(img_mat_2, gaussian_kernel)

    # Squares of means
    img_mat_mu_1_sq = img_mat_mu_1**2
    img_mat_mu_2_sq = img_mat_mu_2**2
    img_mat_mu_12 = img_mat_mu_1 * img_mat_mu_2

    # Variances obtained by Gaussian filtering of inputs' squares
    img_mat_sigma_1_sq = scipy.ndimage.filters.convolve(
        img_mat_1_sq, gaussian_kernel)
    img_mat_sigma_2_sq = scipy.ndimage.filters.convolve(
        img_mat_2_sq, gaussian_kernel)

    # Covariance
    img_mat_sigma_12 = scipy.ndimage.filters.convolve(
        img_mat_12, gaussian_kernel)

    # Centered squares of variances
    img_mat_sigma_1_sq = img_mat_sigma_1_sq - img_mat_mu_1_sq
    img_mat_sigma_2_sq = img_mat_sigma_2_sq - img_mat_mu_2_sq
    img_mat_sigma_12 = img_mat_sigma_12 - img_mat_mu_12

    # c1/c2 constants
    # First use: manual fitting
    c_1 = 6.5025
    c_2 = 58.5225

    # Second use: change k1,k2 & c1,c2 depend on L (width of color map)
    l = 255
    k_1 = 0.01
    c_1 = (k_1 * l)**2
    k_2 = 0.03
    c_2 = (k_2 * l)**2

    # Numerator of SSIM
    num_ssim = (2 * img_mat_mu_12 + c_1) * (2 * img_mat_sigma_12 + c_2)
    # Denominator of SSIM
    den_ssim = (img_mat_mu_1_sq + img_mat_mu_2_sq + c_1) *\
        (img_mat_sigma_1_sq + img_mat_sigma_2_sq + c_2)
    # SSIM
    ssim_map = num_ssim / den_ssim
    index = numpy.average(ssim_map)

    return index


# def msssim(img1, img2):
#     """This function implements Multi-Scale Structural Similarity (MSSSIM) Image
#     Quality Assessment according to Z. Wang's "Multi-scale structural similarity
#     for image quality assessment" Invited Paper, IEEE Asilomar Conference on
#     Signals, Systems and Computers, Nov. 2003

#     Author's MATLAB implementation:-
#     http://www.cns.nyu.edu/~lcv/ssim/msssim.zip
#     """
#     from scipy import ndimage
#     import numpy
#     level = 5
#     weight = numpy.array([0.0448, 0.2856, 0.3001, 0.2363, 0.1333])
#     downsample_filter = numpy.ones((2, 2)) / 4.0
#     im1 = img1.astype(numpy.float64)
#     im2 = img2.astype(numpy.float64)
#     mssim = numpy.array([])
#     mcs = numpy.array([])
#     for l in range(level):
#         ssim_map, cs_map = ssim(im1, im2, cs_map=True)
#         mssim = numpy.append(mssim, ssim_map.mean())
#         mcs = numpy.append(mcs, cs_map.mean())
#         filtered_im1 = ndimage.filters.convolve(im1, downsample_filter,
#                                                 mode='reflect')
#         filtered_im2 = ndimage.filters.convolve(im2, downsample_filter,
#                                                 mode='reflect')
#         im1 = filtered_im1[::2, ::2]
#         im2 = filtered_im2[::2, ::2]
#     return (numpy.prod(mcs[0:level - 1]**weight[0:level - 1]) *
#             (mssim[level - 1]**weight[level - 1]))


# def ssim(img1, img2, cs_map=False):
#     """Return the Structural Similarity Map corresponding to input images img1
#     and img2 (images are assumed to be uint8)

#     This function attempts to mimic precisely the functionality of ssim.m a
#     MATLAB provided by the author's of SSIM
#     https://ece.uwaterloo.ca/~z70wang/research/ssim/ssim_index.m
#     """
#     img1 = img1.astype(numpy.float64)
#     img2 = img2.astype(numpy.float64)
#     size = 11
#     sigma = 1.5
#     window = gauss.fspecial_gauss(size, sigma)
#     K1 = 0.01
#     K2 = 0.03
#     L = 255 #bitdepth of image
#     C1 = (K1*L)**2
#     C2 = (K2*L)**2
#     mu1 = signal.fftconvolve(window, img1, mode='valid')
#     mu2 = signal.fftconvolve(window, img2, mode='valid')
#     mu1_sq = mu1*mu1
#     mu2_sq = mu2*mu2
#     mu1_mu2 = mu1*mu2
#     sigma1_sq = signal.fftconvolve(window, img1*img1, mode='valid') - mu1_sq
#     sigma2_sq = signal.fftconvolve(window, img2*img2, mode='valid') - mu2_sq
#     sigma12 = signal.fftconvolve(window, img1*img2, mode='valid') - mu1_mu2
#     if cs_map:
#         return (((2*mu1_mu2 + C1)*(2*sigma12 + C2))/((mu1_sq + mu2_sq + C1)*
#                     (sigma1_sq + sigma2_sq + C2)),
#                 (2.0*sigma12 + C2)/(sigma1_sq + sigma2_sq + C2))
#     else:
#         return ((2*mu1_mu2 + C1)*(2*sigma12 + C2))/((mu1_sq + mu2_sq + C1)*
#                     (sigma1_sq + sigma2_sq + C2))
