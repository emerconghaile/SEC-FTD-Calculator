# import modules
import requests
import urllib.request
import os
from bs4 import BeautifulSoup

# set & request SEC Fails-To-Deliver website
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

# save only the FTD file links to a list and file as (descriptor, url)
url_list = "url_list.txt"
with open(url_list, "w") as f:
    urls = []
    for tag in soup.find_all("a"):
        if "half" in tag.text:
            urls.append((str(tag).split('>')[1].split('<')[0], "https://www.sec.gov" + tag.attrs['href']))
            f.write(str((str(tag).split('>')[1].split('<')[0], "https://www.sec.gov" + tag.attrs['href'])) +"\n")
f.close
print(f"List of all URLs saved to {url_list}\n")

# sepereate file desriptions and links (not used)
# file_desc = [url[0] for url in urls]
# file_url = [url[1] for url in urls]

# prompt user with total number of files
total_files = len(urls)
print(f"Preparing to download {total_files} .zip files\n")

# ask for download confirmation
print("Initiate download?")
user_conf = input("type 'yes' to continue: ")
if user_conf == "yes":
    print("Initiating download\n")
else:
    print("Exiting!")
    exit()

# create directory for data .zip files
data_path = "zips"
try:
    os.makedirs(data_path, exist_ok = True)
    print(f".zips will be downloaded to '{data_path}' directory\n")
except OSError as error:
    print(f"ERROR, {data_path} not created")

# fetch all data .zip files
for url in urls:
    urllib.request.urlretrieve(url[1], data_path + "/" + url[0])
    print(f"Downloaded: {url[0]}")

print("\nDownload finished!")