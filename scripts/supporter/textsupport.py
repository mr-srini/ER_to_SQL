import re

class TextSupporter:

	@staticmethod
	def trim(text):
	    return re.sub("\n", "", text).strip()

	@staticmethod
	def isPrimaryKey(txt,tableName):
	    if txt.lower() == "id":
	    	return True     
	    if tableName.lower()+"_id" == txt or tableName.lower()+"id" == txt:
	        return True
	    return False

	@staticmethod
	def removeDuplicateKeys(lst,tableName):
		for item in lst:
			if item.lower() == "id":
				return "id"
			elif tableName+"_id" in lst or tableName+"id" in lst:
				return tableName+"_id"

	@staticmethod
	def isForeignKey(txt,tableName):
		if txt == "id":
			return False
		elif tableName.lower()+"_id" == txt or tableName.lower()+"id" == txt:
			return False
		return True







