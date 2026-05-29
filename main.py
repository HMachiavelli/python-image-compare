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

    print('Starting image comparison:', len(files), 'images found in the folder.')

    mainImgShape = mainImage.shape[0] * mainImage.shape[1]
    result = []
    for filename in files:
        image = io.imread(os.path.join('images', filename), as_gray=True)
        if(image is None):
            continue

        imgShape = image.shape[0] * image.shape[1]

        if(mainImgShape > imgShape): # We have to resize the main image to the shape of the target one
            mainImage = transform.resize(mainImage, image.shape, preserve_range=True)
        else: # We have to resize the target image to the shape of the main one
            image = transform.resize(image, mainImage.shape, preserve_range=True)

        similarity = compare(mainImage, image, filename)
        if(similarity != False):
            result.append(f'\nImage {filename} is {similarity:.2f}% similar to the main image.')
        
    if(len(result) == 0):
        print('No similar images found.')
    else:
        print('Comparison results:\n')
        for res in result:
            print(res, f'\n')

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
    similarity = metrics.structural_similarity(image1, image2, data_range=1)
    if (similarity < 0):
        similarity *= -1
    similarity = similarity * 100

	# Check if SSIM>threshold to determine if they are similar
    if (similarity >= 50):
        return similarity

    vertical_flip_image = vertical_flip(image2)
    horizontal_flip_image = horizontal_flip(image2)
    vertical_flip_image = vertical_flip_image.astype(np.uint8)
    horizontal_flip_image = horizontal_flip_image.astype(np.uint8)

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

    if(difference1 > 40):
        return similarity1
    elif(difference2 > 40):
        return similarity2
        
    return false

if __name__ == '__main__':
    main()