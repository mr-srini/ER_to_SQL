import re

class DictSupport:

	def __init__(self,lst):
		self.lst = lst


	def getDict(self):
		preProcessList = self._removeNextLineCharacter()
		tableList, attributeList, primaryKeyList= [] ,[], []
		for text in preProcessList:
			returnedTableValue = self._getTableName(text)
			returnedKeyValue = self._getPrimaryKey(text)

			if returnedTableValue is not None:
				tableList.append(returnedTableValue.replace("_T",""))

			if returnedKeyValue is not None:
				primaryKeyList.append(returnedKeyValue)
						

		attributeList = [x.replace("_T","") for x in preProcessList if len(x)>1]
		for item in tableList:
			attributeList.remove(item)
		for item in primaryKeyList:
			if not self._isForeignKey(item,tableList[0].lower()):
				attributeList.remove(item)
		dictKeys = ['tableName', 'primaryKey', 'attributes']
		dictValue = [tableList[0],self._removeDuplicateKeys(primaryKeyList,tableList[0].lower()), attributeList]
		dictResult = dict(zip(dictKeys, dictValue))
		
		return dictResult


	def _removeNextLineCharacter(self):
	    res = []
	    for x in self.lst:
	        a = re.sub("\n", " ", x).strip()
	        if a:
	            res.append(a)
	    return self._removeBlankSpace(res)
	
	def _removeBlankSpace(self,lst):
	    res = []
	    for ele in lst:
	        if ele.strip():
	            res.append(ele)
	    return res

	def _getTableName(self,txt):
	    regex = r"([a-zA-Z]+_T$)"
	    if re.search(regex, txt,re.IGNORECASE):
	        match = re.search(regex, txt,re.IGNORECASE)
	        if match:
	            return match.group()
	
	

	def _getPrimaryKey(self,txt):
	    if txt.lower() == "id":
	    	return txt
	    regex = r"([a-zA-Z]*_ID$)"     
	    if re.search(regex, txt,re.IGNORECASE):
	        match = re.search(regex, txt,re.IGNORECASE)
	        if match:
	            return match.group()


	def _removeDuplicateKeys(self,lst,tableName):
		for item in lst:
			if item.lower() == "id":
				return "id"
			elif tableName+"_id" in lst or tableName+"id" in lst:
				return tableName+"_id"

	def _isForeignKey(self,txt,tableName):
		if txt == "id":
			return False
		elif tableName+"_id" == txt or tableName+"id" == txt:
			return False
		return True







