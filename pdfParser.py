from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
import tabula

url = "https://www.iedcr.gov.bd/website/images/files/nCoV/"
resp = urllib.request.urlopen(url+"?C=M;O=D")
soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'),features="lxml")

link= soup.find_all('a', href=True)
fileUrl= url+ link[5].get("href")
file = link[5].get("href").split(".")
fileName = file[0]
fileLoc = str(fileName+".pdf")
print("Downloading as "+fileLoc)

urllib.request.urlretrieve(fileUrl,fileLoc)

csvName = fileName+".csv"
print("Converting to "+csvName)

tabula.convert_into(fileLoc, csvName, output_format="csv", pages='all', silent=True)
print("Done!")