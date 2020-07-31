from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urljoin

url = "http://apps.vedavaapi.org/manuscripts/books/jain-mscripts/Palmleaves%20Manuscripts/Upamiti%20BORI/"

req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
# print(soup.title.text.split('/')[-1].replace(" ","_"))
dir_name = soup.title.text.split('/')[-1].replace(" ","_").lower() # Takes the title of book and replaces space with _ and all upper cases to lower cases
images = "images"
# Directory Creation
if not os.path.exists(dir_name):
    print("Directory with name "+dir_name+" will be created in the present directory")
    os.mkdir(dir_name)
    os.mkdir(dir_name+"/"+images)
else:
    print("Directory could not be created, because direcory with name {} already exists in the current directory.".format(dir_name))
textfile = dir_name+"/"+"img_url_map.txt"
# print(soup)
os.system("touch {}".format(textfile))
imgs = [link.get('href') for link in soup.find_all('a') if link.get('href').split('.')[-1]=='JPG']
print("There are {} images in total".format(len(imgs)))
count = 1
for img in imgs:
    print("Downloading image {} with name {}...".format(count,img))
    file_loc = dir_name+'/'+images+'/'+img
    with open (file_loc,'wb') as f:
        jpg = requests.get(url+"/"+img)
        f.write(jpg.content)
    os.system("echo "+img+" , "+url+"/"+img+" >> {}".format(textfile))
    count+=1



    