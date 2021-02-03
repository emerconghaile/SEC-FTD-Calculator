# import modules
import requests
import urllib.request
import os
import zipfile
from pathlib import Path
from bs4 import BeautifulSoup

# request SEC Fails-To-Deliver website
result = requests.get("https://www.sec.gov/data/foiadocsfailsdatahtm")

# ensure website is accessible, or exit with error code
if "200" in str(result.status_code):
    print("Connection to website successful\n")
else:
    print("Connection to website unsuccessful")
    print(f"HTML code: {str(result.status_code)}")
    exit()

# parse and process the website content
soup = BeautifulSoup(result.content, 'lxml')

# save zips to a file and a list variable, as (descriptor, url)
total_urls = []
counter = 0
with open("total_url_list.txt", "w") as f:
    for tag in soup.find_all("a"):
        if "half" in tag.text:
            total_urls.append((str(tag).split('>')[1].split('<')[0], "https://www.sec.gov" + tag.attrs['href']))
            f.write(str(total_urls[counter]) + "\n")
            counter += 1
f.close()
print(f"List of all URLs saved to 'url_list.txt'\n")

# creath vars for data paths
zip_path = "zip_data/"
raw_path = "raw_data/"

# check which zips are not downloaded, add them to list variable
urls_to_download = []
for url in total_urls:
    check_zip_path = Path(zip_path + str(url[0]))
    if check_zip_path.exists() != True:
        urls_to_download.append(url)

# are there new downloads?
if len(urls_to_download) > 0:
    # save zips to download to list
    counter = 0
    with open("new_url_list.txt", "w") as f:
        for url in urls_to_download:
            f.write(str(urls_to_download[counter]) + "\n")
            counter += 1
    f.close()
    # download confirmation from user
    print(f"New zip file(s) available: {len(urls_to_download)}")
    print("See 'new_url_list.txt'")
    print("Initiate download?")
    user_conf = input("Type 'yes' to continue: ")
    if user_conf == "yes":
        print("Starting download")
        # create zips folder
        try:
            os.makedirs(zip_path, exist_ok = True)
            print(f".zips will be saved to '{zip_path}' directory\n")
        except OSError as error:
            print(f"ERROR, '{zip_path}' not created")
        # download zips
        for url in urls_to_download:
            urllib.request.urlretrieve(url[1], zip_path + url[0])
            print(f"Downloaded: {url[0]}")
        print("\nDownload finished!\n")
        # begin unzip process
        print("Starting unzip process")
        # create unzips folder
        try:
            os.makedirs(raw_path, exist_ok = True)
            print(f".zips will be unzipped to '{raw_path}' directory\n")
        except OSError as error:
            print(f"ERROR, '{raw_path}' not created")
        # unzip the zips, prepare to encode
        to_encode = []
        for url in urls_to_download:
            with zipfile.ZipFile(zip_path + url[0], "r") as zfile:
                to_encode += zfile.namelist()
                zfile.extractall(raw_path)
            f.close()
            print("Unzipped: " + url[0])
        print("\nUnzip finished!\n")
        # begin re-encode to utf8
        print("Starting re-encode process\n")
        for i in to_encode:
            print(f"Encoding: {i}")
            with open(f"{raw_path}{i}", "r", encoding="iso8859_14") as f:
                data = f.read()
            f.close()
            with open(f"{raw_path}{i}", "w", encoding="utf8") as f:
                f.write(data)
            f.close()
        print("\nEncoding finished!")
    else:
        print("Exiting!")
        exit()
else:
    print("Files are current.")