from azure.storage.blob import BlobServiceClient
from azure.storage.blob import PublicAccess
import os
from dotenv import load_dotenv
import cv2 as cv
import csv
import numpy as np

### Variables
load_dotenv()
storage_account = "https://portal.azure.com/#@aerialhistoryprojectoutlook.onmicrosoft.com/resource/subscriptions/10bd7236-339f-4730-8042-e6200e7e76f4/resourceGroups/Historical_Remote_Sensing/providers/Microsoft.Storage/storageAccounts/ncapdata/overview" #"ncapdata"
access_key = os.getenv("ACCESS_KEY")
connect_str = os.getenv("CONNECT_STR")
containers = ["jamaica"] # "dominica", "montserrat","jamaica", "stlucia"
static_path = os.getcwd() + "/edge/static/"
link_path = "human_links_01232021.csv"
no_image_path = "no_image_01232021.csv"
image_list = set()
no_image_list = []
scale_factor = 10

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
    width = int(img.shape[1] * scale_factor / 100)
    height = int(img.shape[0] * scale_factor / 100)
    dim = (width, height)
    resized = cv.resize(img, dim, interpolation = cv.INTER_AREA)
    cv.imwrite(path[:-3] + "jpg", resized)
    if (path[-3:] == "tif"):
        os.remove(path)

def read_links():
    with open(static_path + link_path) as f:
        reader = csv.reader(f)
        next(reader, None) # Skip the headers
        for row in reader:
            blob_name_1 = row[1] + "_" + row[2].zfill(4) + "/" + \
                row[1] + "_" + row[2].zfill(4) + "_" + row[3].zfill(4)
            blob_name_2 = row[1] + "_" + row[4].zfill(4) + "/" + \
                row[1] + "_" + row[4].zfill(4) + "_" + row[5].zfill(4)
            image_list.add(blob_name_1)
            image_list.add(blob_name_2)
    no_image_list_np = np.asarray(no_image_list)
    np.savetxt(static_path + no_image_path, no_image_list_np, delimiter=",", fmt='%s')

### Downloader
def download_images():
    for container in containers:
        cd_to_container(container)
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_client = blob_service_client.get_container_client(container)
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            if blob.name[:-4] in image_list:
                print("Downloading " + container + "/" + blob.name)
                if os.path.exists(os.getcwd() + "/" + blob.name):
                    print("Already downloaded.")
                    continue
                #check if the path contains a folder structure, create the folder structure
                if "/" in "{}".format(blob.name):
                    #extract the folder path and check if that folder exists locally, and if not create it
                    head, tail = os.path.split("{}".format(blob.name))
                    if (os.path.isdir(os.getcwd()+ "/" + head)):
                        #download the files to this directory
                        # blob_service_client.get_blob_to_path(container,blob.name,os.getcwd()+ "/" + head + "/" + tail)
                        download_file_path = os.getcwd()+ "/" + head + "/" + tail
                        with open(download_file_path, "wb") as download_file:
                            download_file.write(container_client.download_blob(blob.name).readall())
                    else:
                        #create the diretcory and download the file to it
                        os.mkdir(os.getcwd()+ "/" + head)
                        # blob_service_client.get_blob_to_path(container,blob.name,os.getcwd()+ "/" + head + "/" + tail)
                        download_file_path = os.getcwd()+ "/" + head + "/" + tail
                        with open(download_file_path, "wb") as download_file:
                            download_file.write(container_client.download_blob(blob.name).readall())
                else:
                    # blob_service_client.get_blob_to_path(container,blob.name,blob.name)
                    download_file_path = blob.name
                    with open(download_file_path, "wb") as download_file:
                        download_file.write(container_client.download_blob(blob.name).readall())

                resize(os.getcwd() + "/" + blob.name)

def check():
    def check_image(image, row):
        if not os.path.isfile(image_path + "/" + image + ".jpg") and not row in no_image_list:
            no_image_list.append(row)
        return
    os.chdir(static_path + "NCAP")
    image_path = os.getcwd()
    with open(static_path + link_path) as f:
        reader = csv.reader(f)
        next(reader, None) # Skip the headers
        for row in reader:
            blob_name_1 = row[1] + "_" + row[2].zfill(4) + "/" + \
                row[1] + "_" + row[2].zfill(4) + "_" + row[3].zfill(4)
            blob_name_2 = row[1] + "_" + row[4].zfill(4) + "/" + \
                row[1] + "_" + row[4].zfill(4) + "_" + row[5].zfill(4)
            check_image(row[0] + "/" + blob_name_1, row)
            check_image(row[0] + "/" + blob_name_2, row)
    no_image_list_np = np.asarray(no_image_list)
    np.savetxt(static_path + no_image_path, no_image_list_np, delimiter=",", fmt='%s')
    no_image_list.sort()
    combined_string = ""
    for no_image in no_image_list:
        combined_string += str(no_image) + "\n"
    print(combined_string)

### Main
# read_links()
# download_images()
# check()


### KIV 
# if __name__ == "__main__":
#     main()

