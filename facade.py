import requests as req
import json
import io
import os
from zipfile import ZipFile


url = "http://localhost:5000"


class EzSecReq:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = url
        self.headers = {'x-api-key': self.api_key}
    
    def get_filling_by_CIK(self, cik):
        url = self.base_url + "/secfiles/" + cik
        response = req.request("GET", url, headers=self.headers)
        zippy = ZipFile(io.BytesIO(response.content))
        return zippy

    
    def unzip_file(self, zip_file, path):
        #check if the path exists
        if not os.path.exists(path):
            os.makedirs(path)
        #unzip the file
        zip_file.extractall(path)
        return True
    
    

if __name__ == '__main__':
    # Create an instance of the class
    EzSecReqInstance =  EzSecReq("YOUR_API_KEY")
    # Get all filings for a given company CIK
    reqFile = EzSecReqInstance.get_filling_by_CIK("1000032")
    #print the type of the response
    print(type(reqFile))
    # save the file to a local directory
    EzSecReqInstance.unzip_file(reqFile, "./test/")


    