from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
import os
from dotenv import load_dotenv
import cv2 as cv
import csv

### Variables
load_dotenv()
storage_account = "ncapdata"
access_key = os.getenv("ACCESS_KEY")
containers = ["montserrat"]
static_path = os.getcwd() + "/edge/static/"
image_list = set()

### Helper functions
def cd_to_container(container):
    os.chdir(static_path + "NCAP")
    if (os.path.isdir(os.getcwd()+ "/" + container)):
        os.chdir(container)
    else:
        os.mkdir(os.getcwd()+ "/" + container)
        os.chdir(container)

def resize(path):
    img = cv.imread(path)
    scale_percent = 10
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv.resize(img, dim, interpolation = cv.INTER_AREA)
    cv.imwrite(path[:-3] + "jpg", resized)
    os.remove(path)

def read_links():
    with open(static_path + "links.csv") as f:
        reader = csv.reader(f)
        next(reader, None) # Skip the headers
        for row in reader:
            blob_name_1 = row[2] + "_" + row[3].zfill(4) + "/" + \
                row[2] + "_" + row[3].zfill(4) + "_" + row[4].zfill(4)
            blob_name_2 = row[2] + "_" + row[5].zfill(4) + "/" + \
                row[2] + "_" + row[5].zfill(4) + "_" + row[6].zfill(4) 
            image_list.add(blob_name_1)
            image_list.add(blob_name_2)

### Downloader
def download_images():
    for container in containers:
        cd_to_container(container)
        block_blob_service = BlockBlobService(account_name=storage_account, account_key=access_key)
        generator = block_blob_service.list_blobs(container)
        for blob in generator:
            if blob.name[:-4] in image_list:
                print("Downloading " + container + "/" + blob.name)
                #check if the path contains a folder structure, create the folder structure
                if "/" in "{}".format(blob.name):
                    #extract the folder path and check if that folder exists locally, and if not create it
                    head, tail = os.path.split("{}".format(blob.name))
                    if (os.path.isdir(os.getcwd()+ "/" + head)):
                        #download the files to this directory
                        block_blob_service.get_blob_to_path(container,blob.name,os.getcwd()+ "/" + head + "/" + tail)
                    else:
                        #create the diretcory and download the file to it
                        os.mkdir(os.getcwd()+ "/" + head)
                        block_blob_service.get_blob_to_path(container,blob.name,os.getcwd()+ "/" + head + "/" + tail)
                else:
                    block_blob_service.get_blob_to_path(container,blob.name,blob.name)
                resize(os.getcwd() + "/" + blob.name)

read_links()
download_images()