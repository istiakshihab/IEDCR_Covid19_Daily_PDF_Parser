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
print("Downloading "+fileName)
fileLoc = str(fileName+".pdf")

urllib.request.urlretrieve(fileUrl,fileLoc)

csvName = fileName+".csv"
tabula.convert_into(fileLoc, csvName, output_format="csv", pages='all')
