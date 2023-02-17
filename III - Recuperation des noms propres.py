import pytesseract
from pytesseract import Output
import cv2
from skimage import io
import numpy as np
import sys
from matplotlib import pyplot as plt
from matplotlib import image as mpimage
from autocorrect import Speller
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import json
import os


tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner")
model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner")

nlp = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")


def camembert(texte):

  res = nlp(texte)

  per = []
  for i in range(len(res)):
    if res[i]:
      if res[i]['entity_group'] == 'PER' and res[i]['score'] >= 0.75:
        per.append(res[i]['word'])

  return per


def segmentationH(img):

  img = img[10:-10, 10:-10] # remove the border, it confuses contour detection
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  thresholded = cv2.adaptiveThreshold(
                  gray, 255,
                  cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,
                  25,
                  15
              )

  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (500, 1))
  closing = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel)

  contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  imgc = []
  for i in range(len(contours)):
    x, y, w, h = cv2.boundingRect(contours[i])
    
    if w * h > 11000:
      imgc.append(img[y:y+h, x:x+w])

  imgc.reverse()
  return imgc


def segmentationV(imgc):
  imgd = []
  for i in range(len(imgc)):
    img2 = imgc[i]

    img2 = img2[10:-10, 10:-10] # remove the border, it confuses contour detection

    if(img2.shape[0] > 10 and img2.shape[1] > 10):
      gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)


      thresholded = cv2.adaptiveThreshold(
                      gray, 255,
                      cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,
                      25,
                      15
                  )

      kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 100))
      closing = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel)

      contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      
      for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        
        if w * h > 10000:
          imgd.append(img2[y:y+h, x:x+w])

  imgd.reverse()
  return imgd


def segmentation(img):
  return segmentationV(segmentationH(img))


def ocr(img):
  imgString = ''
  imgString += pytesseract.image_to_string(img, lang='fra')
  imgString += '\n'

  imgStringCopy = imgString.replace('-\n', '').replace('\n', ' ').replace('  ','\n')

  return imgStringCopy


def correction(texte):

  spell = Speller(lang='fr')
  correction = spell(texte)
    
  return correction



nomsDict = {}

dir = 'images'
images = []

for image in os.listdir(dir):
  if image.endswith(".jpg") or image.endswith(".tif") or image.endswith(".jpeg") or image.endswith(".png"):
    images.append(image)


for image in images:


  img_path = dir + '/' + image
  img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
  #img = cv2.imread(dir + '/' + image)
  segmentationImage = segmentation(img)

  valueInfos = image.split('_')

  for i in range(len(segmentationImage)):
    keyName = image + '_paragraphe_' + str(i+1)

    text = ocr(segmentationImage[i])

    if not text == "":
      print(text)
      try:
        correction = correction(text)
      except:
        correction = text
      noms = camembert(correction)

      if not noms == []:

        d = {
            "nom": noms,
            "date": valueInfos[1],
            "page": valueInfos[3],
            "paragraphe": i+1
        }

        nomsDict[keyName] = d

    else:
      if i != 0:
        i-=1


with open('result/noms.json', 'w') as f:
  json_object = json.dumps(nomsDict, indent=4, ensure_ascii=False)
  f.write(json_object)
