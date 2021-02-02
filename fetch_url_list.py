# import modules
import requests
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

# save only the FTD file links to a list and file
with open("url_list.txt", "w") as f:
    urls = []
    for tag in soup.find_all("a"):
        if "half" in tag.text:
            urls.append((str(tag).split('>')[1].split('<')[0], "https://www.sec.gov" + tag.attrs['href']))
            f.write(str((str(tag).split('>')[1].split('<')[0], "https://www.sec.gov" + tag.attrs['href'])) +"\n")
f.close

# print(*urls, sep = "\n")