import os
import shutil

class FileSupport:

    @staticmethod
    def createDirectory(id):
        path = os.getcwd()
        try:
            os.makedirs(path+"/segmentedTables"+"/table{tableId}".format(tableId = id))
        except OSError:
            print ("Creation of the directory failed")
        else:
            print ("Successfully created the directory")


    @staticmethod
    def removeFolders():
    	path = os.getcwd()
    	shutil.rmtree(path+"/segmentedTables")