from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urljoin
import re

url = "http://apps.vedavaapi.org/manuscripts/books/jain-mscripts/%e0%a4%ac%e0%a5%87%e0%a4%82%e0%a4%97%e0%a4%b2%e0%a5%8b%e0%a4%b0%20SoftWere%20Manu/%e0%a4%9a%e0%a4%be%e0%a4%82%e0%a4%a6%e0%a5%80%e0%a4%ac%e0%a4%9d%e0%a4%be%e0%a4%b0/"

req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
# print(soup.title.text.split('/')[-1].replace(" ","_"))
# dir_name = soup.title.text.split('/')[-1].replace(" ","_").lower() # Takes the title of book and replaces space with _ and all upper cases to lower cases
dir_name = "chandibajar"
print(dir_name)
images = "images"
# # Directory Creation
if not os.path.exists(dir_name):
    print("Directory with name "+dir_name+" will be created in the present directory")
    os.mkdir(dir_name)
else:
    print("Directory could not be created, because direcory with name {} already exists in the current directory.".format(dir_name))
sub_dirs = [link.get('href') for link in soup.find_all('a') if re.search(r'[\d]+[/]',link.get('href'))]
print(sub_dirs)
print("You have {} subdirectories".format(len(sub_dirs)))
dir_count = 1
for subdir in sub_dirs:
    sub_dir = dir_name+'/'+subdir
    if not os.path.exists(sub_dir):
        print("Directory with name "+dir_name+" will be created in the present directory")
        os.mkdir(sub_dir)
        os.mkdir(sub_dir+"/"+images)
    imgs_req = requests.get(url+'/'+subdir)
    img_soup = BeautifulSoup(imgs_req.text,"html.parser")
    textfile = sub_dir+"/"+"img_url_map.txt"
    # print("Printing Soup",img_soup)
    os.system("touch {}".format(textfile))

    imgs = [link.get('href') for link in img_soup.find_all('a') if link.get('href').split('.')[-1]=='jpg']
    print("Downloading for Dir"+str(dir_count)+", "+subdir+"\nThere are {} images in total in this sub-dir".format(len(imgs)))
    count = 1
    for img in imgs:
        print("Downloading image {} with name {}...".format(count,img))
        file_loc = sub_dir+'/'+images+'/'+img
        with open (file_loc,'wb') as f:
            jpg = requests.get(url+"/"+subdir+img)
            f.write(jpg.content)
        os.system("echo '"+img+"' , '"+url+"/"+subdir+img+"' >> {}".format(textfile))
        count+=1
    dir_count+=1