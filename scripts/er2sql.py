from PIL import Image
import pytesseract
import argparse
import cv2
import numpy as np
import os, errno
import re
from dictsupport import DictSupport



#python er2sql.py --image {image path} --output {output file name} without extention (.sql)


#DiverClass
class ErToSQL:

	def __init__(self,output):
		self.output = output



	def _removeLines(self,imgPath):
		image = cv2.imread(imgPath)
		mask = np.ones(image.shape, dtype=np.uint8) * 255
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
		kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
		dilate = cv2.dilate(thresh, kernel, iterations=3)

		cnts = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if len(cnts) == 2 else cnts[1]
		for c in cnts:
		    area = cv2.contourArea(c)
		    if area < 15000:
		        x,y,w,h = cv2.boundingRect(c)
		        mask[y:y+h, x:x+w] = image[y:y+h, x:x+w]

		cv2.imshow("mask",mask)
		cv2.waitKey()
		gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
  		# Getting words from image 
		lst = self._getCharacters(gray)
		return lst


	def _getCharacters(self,gray):
		imgText = pytesseract.image_to_string(gray,config="--psm 11")
		lst = imgText.split("\n\n")
		return lst


	def _getDict(self,lst):
		createDict = DictSupport(lst)
		dictResult = createDict.getDict()
		return dictResult

	def _write(self,dict):
		commandString = "CREATE TABLE %s("%dict['tableName']
		primaryKeyString = "%s varchar PRIMARY KEY,"%dict['primaryKey']
		attributeString = ""
		for index in range(0,len(dict['attributes'])-1):
			attributeString+="%s varchar,\n"%dict["attributes"][index]
		attributeString+="%s varchar\n);"%dict['attributes'][-1]
		
		print(commandString + "\n" + primaryKeyString + "\n" + attributeString)
		f = open("generatedSQL/%s.sql"%self.output, "w")
		f.write(commandString + "\n" + primaryKeyString + "\n" + attributeString)
		f.close()


	def getSQLFile(self,imgPath):
		lst = self._removeLines(imgPath)
		dictResult = self._getDict(lst)
		self._write(dictResult)
		print(dictResult)





ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="path to input image")
ap.add_argument("-o","--output",type=str,required=True,help="output file name")
args = vars(ap.parse_args())


er = ErToSQL(args['output'])
er.getSQLFile(args['image'])

#python er2sql.py --image images/college_table.png --output collegeTable
#['id', 'location', 'name', 'College_T']
#{'tableName': 'College', 'primaryKey': 'id', 'attributes': ['location', 'name']}






