import pytesseract 

class OCR:

	@staticmethod
	def getTextFromImage(ocrGray):
		return pytesseract.image_to_string(ocrGray,config="--psm 11")