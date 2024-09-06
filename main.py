import numpy as np
from scipy import misc
from skimage import io, metrics, transform
import sys
import math
import os

def main():
    files = os.listdir('images')
    if(len(files) == 0):
        print('Folder images does not exist or is empty!')
        exit()

    mainImage = io.imread('main.jpeg', as_gray=True)
    if(mainImage is None):
        print('Main image does not exist or is invalid!')
        exit()

    mainImgShape = mainImage.shape[0] * mainImage.shape[1]
    for filename in files:
        image = io.imread(os.path.join('images', filename), as_gray=True)
        if(image is None):
            continue

        imgShape = image.shape[0] * image.shape[1]

        if(mainImgShape > imgShape): # We have to resize the main image to the shape of the target one
            mainImage = transform.resize(mainImage, image.shape, preserve_range=True)
        else: # We have to resize the target image to the shape of the main one
            image = transform.resize(image, mainImage.shape, preserve_range=True)

        compare(mainImage, image, filename)

# Horizontal Flip Function
def horizontal_flip(image):
    row = image.shape[0]
    column = image.shape[1]
    flip_img = np.zeros((image.shape[0], image.shape[1]))
    for r in range(row):
        for c in range(column):
            flip_img[r][column-c-1] = image[r][c]
    return flip_img

# Vertical Flip Function
def vertical_flip(image):
    row = image.shape[0]
    column = image.shape[1]
    flip_img = np.zeros((image.shape[0], image.shape[1]))
    for r in range(row):
        for c in range(column):
            flip_img[row-1-r][c] = image[r][c]
    return flip_img

# Comparison Function
def compare(image1, image2, filename):
    # Calculate Structural Similarity Index
    print('\nComparing Images (main x ', filename, '):')
    similarity = metrics.structural_similarity(image1, image2, data_range=1)
    if (similarity < 0):
        print("\nSecond Image maybe an Inverted version of the first")
        similarity *= -1
    similarity = similarity * 100
    print('\nSimilarity --> ', similarity, '%')

	# Check if SSIM>threshold to determine if they are similar
    if (similarity == 100):
        print('\nThe Images are Same.')
    elif (similarity >= 90):
        print('\nThe Images are Identical.')
    elif (similarity >= 75):
        print('\nThe Images are Similar.')
    elif (similarity >= 50):
        print('\nThe Images are Vaguely Similar.')
    elif (similarity >= 25):
        print('\nThe Images are Slightly Different.')
    elif (similarity >= 1):
        print('\nThe Images are Dissimilar.')
    else:
        print('\nThe Images are Distinct.')
    vertical_flip_image = vertical_flip(image2)
    horizontal_flip_image = horizontal_flip(image2)
    vertical_flip_image = vertical_flip_image.astype(np.uint8)
    horizontal_flip_image = horizontal_flip_image.astype(np.uint8)

    # Uncomment the following lines to save flipped images to disk.
	# misc.imsave('HorizontalFlip.jpg', horizontal_flip_image)
	# misc.imsave('VerticalFlip.jpg', vertical_flip_image)

    similarity1 = metrics.structural_similarity(horizontal_flip_image, image1, data_range=1)
    if (similarity1 < 0):
        similarity1 *= -1
    similarity1 = similarity1 * 100
    similarity2 = metrics.structural_similarity(vertical_flip_image, image1, data_range=1)
    if (similarity2 < 0):
        similarity2 *= -1
    similarity2 = similarity2 * 100

    difference1 = similarity1 - similarity
    difference2 = similarity2 - similarity

    if(difference1 >40):
        print('\nThe Images are most likely Horizontally Flipped.')
        print('\nHorizontal Flip Similarity --> ', similarity1, '%')
    if(difference2 >40):
        print('\nThe Images are most likely Vertically Flipped.')
        print('\nVertical Flip Similarity --> ',similarity2, '%')

if __name__ == '__main__':
    main()