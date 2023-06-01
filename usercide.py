import gzip
import shutil
import requests as req
import io
import os
from zipfile import ZipFile
import socket
import sys
import os

### Client Side ###

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432     # The port used by the server
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
    
    def save_zip_file(self, zip_file, path, zip_file_name="sec.gz"):
        #check if the path exists
        if not os.path.exists(path):
            os.makedirs(path)
        #save the zip_file bytes to a file in the path
        with open(path + zip_file_name, "wb") as f:
            f.write(zip_file)
        
        return True 

    def unzip_file(self, zip_file, path):
        #check if the path exists
        if not os.path.exists(path):
            os.makedirs(path)
        #unzip the file
        zip_file.extractall(path)

        return True

if __name__ == '__main__':
    f_type = "typo"
    name = "brookfield asset management inc."
    year = "2016"
    quarter = "2"

    request = f"{f_type},{name},{year},{quarter}"
    
    ez = EzSecReq("YOUR_API_KEY")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(request.encode())
        response = b''
        while True:
            data = s.recv(1024)
            print(f"Received {len(data)} bytes")
            print(f"Data: {data}")
            response += data
            if len(data) < 1024:
                break
    
    path = "./test/"
    saved_file = ez.save_zip_file(response, path)
            

    print('Received:', saved_file)

    