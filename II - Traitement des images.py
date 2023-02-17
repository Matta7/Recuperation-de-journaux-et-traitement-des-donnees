import cv2
import numpy as np
from scipy import signal
import os
from os import listdir


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def contour(image):
    kernel_LR = np.array([[1, 0, -1],
                          [2, 0, -2],
                          [1, 0, -1]])
    img1 = signal.convolve2d(image, kernel_LR, boundary='symm', mode='same')

    kernel_UD = np.array([[1, 2, 1],
                          [0, 0, 0],
                          [-1, -2, -1]])
    img2 = signal.convolve2d(image, kernel_UD, boundary='symm', mode='same')

    return np.absolute(img1) + np.absolute(img2)
    

def triangle(image):
  image_copy = image.copy()

  for x in range(2, image.shape[0]-2):
    for y in range(2, image.shape[1]-2):

      if image[x, y] == 255 and image[x, y+1] == 255 and image[x+1, y] == 255 and image[x+1, y+1] == 255:
        image_copy[x-1, y] = 255
        image_copy[x-1, y+1] = 255
        image_copy[x, y-1] = 255
        image_copy[x, y+2] = 255
        image_copy[x+1, y-1] = 255
        image_copy[x+1, y+2] = 255
        image_copy[x+2, y] = 255
        image_copy[x+2, y+1] = 255
        
  return image_copy


def remplissage(image):
  image_copy = image.copy()

  for x in range(2, image.shape[0]-2):
    for y in range(2, image.shape[1]-2):

      if image[x-1, y] == 0 and image[x, y+1] == 0 and image[x+1, y] == 0 and image[x, y-1] == 0:
        image_copy[x, y] = 0
        
  return image_copy


dir = 'images'
images = []

for image in os.listdir(dir):
  if image.endswith(".jpg") or image.endswith(".tif") or image.endswith(".jpeg") or image.endswith(".png"):
    images.append(image)


for image in images:

  print(image)
  img_path = dir + '/' + image
  img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
  #img = cv2.imread(dir + '/' + image)
  
  gray = get_grayscale(img)
  
  bilateral = cv2.bilateralFilter(gray, 15, 50, 120)
  edges = contour(bilateral)
  _, thresh = cv2.threshold(gray, 10, 255, 1)
  img = (edges + 1.5*thresh)

  # Image négative
  data = np.full(img.shape, 255) 
  data[img > 180] = 0
  img = data


  img = triangle(img)
  img = remplissage(img)

  imgStringSplit = image.split('.')

  img_save_path = dir + '/' + imgStringSplit[0] + '_traitee' + '.' + imgStringSplit[1]
  cv2.imencode(".jpg", img)[1].tofile(img_save_path)
  #cv2.imwrite(dir + '/' + imgStringSplit[0] + '_traitee' + '.' + imgStringSplit[1], img)
  os.remove(dir + '/' + image)


