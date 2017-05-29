#importing some useful packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

import math


def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)


def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def region_of_interest(img, vertices):
    """
    Applies an image mask.

    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    # defining a blank mask to start with
    mask = np.zeros_like(img)

    # defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    # filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    # returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    """
    NOTE: this is the function you might want to use as a starting point once you want to
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).

    Think about things like separating line segments by their
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of
    the lines and extrapolate to the top and bottom of the lane.

    This function draws `lines` with `color` and `thickness`.
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)
            
            
def separete_lines(lines):
    for l in lines:
        print(l)
        print(l[0][2])
        print(l[0][0])

        dir = np.array([l[0][2] - l[0][0], l[0][3] - l[0][1]])
        print("dir")
        print(dir.dtype)
        print(len(dir))
        print(dir)
        print("come")
        print(dir)
        if l[0][0] < l[0][2]:
            dir[0], dir[1] = dir[1], dir[0]
        print(np.inner(dir, [0,1]))


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.

    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)

    separete_lines(lines)
    print(lines)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines, [255, 0, 0], 10)
    return line_img


# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., λ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.

    `initial_img` should be the image before any processing.

    The result image is computed as follows:

    initial_img * α + img * β + λ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, λ)

import os
# TODO: Build your pipeline that will draw lane lines on the test_images
# then save them to the test_images directory.
import glob


def debug_show(img):
    pass
    # plt.imshow(img, cmap='gray')
    # plt.show()


def roi_vertices(img):
    '''return vertices of region of interest'''
    img_shape = img.shape
    tl = (470, 300)
    bl = (20, img_shape[0])
    br = (img_shape[1] - 20, img_shape[0])
    tr = (470, 300)
    return np.array([[tl, bl, br, tr]], dtype=np.int32)


def find_lines(img):
    '''detect all lines'''

    # convert to gray scale
    gray = grayscale(img)

    # GaussianBlur
    blur_gray = gaussian_blur(gray, 5)

    debug_show(region_of_interest(blur_gray, roi_vertices(img)))

    # canny edge
    edges = canny(blur_gray, 50, 150)
    debug_show(edges)

    # image mask
    masked_img = region_of_interest(edges, roi_vertices(edges))

    # Hough
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 80  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 100  # maximum gap in pixels between connectable line segments
    lines_img = hough_lines(masked_img, rho, theta, threshold, min_line_length, max_line_gap)

    debug_show(lines_img)

    img_result = weighted_img(img, lines_img)
    debug_show(img_result)


for img in glob.glob("test_images/*.jpg"):
    image = mpimg.imread(img)
    plt.imshow(image)
    plt.show()
    find_lines(image)
