import cv2
import numpy as np
from PIL import Image
import argparse
from supporter.textsupport import TextSupporter
from supporter.ocr import OCR
from supporter.filesupport import FileSupport

'''

This class exposes and process API "process()"
which will return a dict of format 
{
    "tableName" : tableId
}

example -> 
{'course': 1434, 'College': 586, 'Student': 582}


'''


class Rectangle:

    def __init__(self,imgPath):
        self.imgPath = imgPath
        self.dict = {
            "rectangle" : [],
        }
        self.tableNameDict = {}
        self.image = cv2.imread(self.imgPath)
        self.imageBW = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)

    def _showImage(self,img):
        cv2.imshow("Output",img)
        cv2.waitKey()

    def _getCharacters(self,tableId):
        ocrImage = cv2.imread("segmentedTables/table{id}/{id}.png".format(id = tableId))
        ocrGray = cv2.cvtColor(ocrImage,cv2.COLOR_BGR2GRAY)
        imgText = OCR.getTextFromImage(ocrGray)
        self.tableNameDict[TextSupporter.trim(imgText)] = tableId
    
    def _detectRectangle(self,c):
        peri=cv2.arcLength(c,True)
        vertices = cv2.approxPolyDP(c, 0.01 * peri, True)
        area = cv2.contourArea(c)
        sides = len(vertices)
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        if (sides == 4):
             self.dict["rectangle"].append({"area":area,"box":np.int0(box),"tableId" : "{}".format(np.int0(box)[0][0])})

    def _saveTableImages(self):
            FileSupport.removeFolders()
            toCropImage = Image.open(self.imgPath)
            for rectangleBox in self.dict['rectangle']:
                if rectangleBox["box"][0][-1] == rectangleBox["box"][1][-1] and rectangleBox["box"][2][-1] == rectangleBox["box"][3][-1]:
                        cv2.drawContours(self.image,[rectangleBox["box"]],-1,(0,255,100),3)
                        x1 = rectangleBox["box"][0][0]
                        y1 = rectangleBox["box"][0][-1]
                        x2 = rectangleBox["box"][2][0]
                        y2 = rectangleBox["box"][2][-1]
                        cropedRect = toCropImage.crop((x1,y1,x2,y2))
                        FileSupport.createDirectory("{}".format(rectangleBox["box"][0][-1]))
                        filename = "segmentedTables/table{name}/{name}.png".format(name = rectangleBox["box"][0][-1])
                        cropedRect.save(filename)
                        self._getCharacters(rectangleBox["box"][0][-1])

    def process(self):
        edged = cv2.Canny(self.imageBW, 170, 255)
        ret,thresh = cv2.threshold(self.imageBW,240,255,cv2.THRESH_BINARY)
        (contours,_) = cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            self._detectRectangle(cnt)
        self._saveTableImages()
        print(self.tableNameDict)
        return self.tableNameDict




ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="path to input image")
#ap.add_argument("-o","--output",type=str,required=True,help="output file name")
args = vars(ap.parse_args())

rectangle = Rectangle(args['image'])
rectangle.process()