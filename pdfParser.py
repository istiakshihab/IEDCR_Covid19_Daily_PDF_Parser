from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
try:
    import camelot
except ImportError:
    raise ImportError('Camelot not found. Try running "pip3 install camelot-py[cv]"')
import pandas as pd
from pathlib import Path
import re

url = "https://www.iedcr.gov.bd/website/images/files/nCoV/"
resp = urllib.request.urlopen(url+"?C=M;O=D")
soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'),features="lxml")

for link in soup.find_all('a', href=True):
    x= link.get("href").split("_")
    if x[0]=="Case" or re.match("^\d.*",x[0]):
        fileUrl= url+ link.get("href")
        file = link.get("href").split(".")
        fileName = file[0]
        fileLoc = str(fileName+".pdf")
        print("Latest available PDF is: "+fileLoc)
        break

if Path(fileLoc).is_file():
    print("It already exists in the local machine. Program is quitting.")
else:
    print("Downloading PDF as: "+fileLoc)
    urllib.request.urlretrieve(fileUrl,fileLoc)

    csvNameBD = fileName+"_Bangladesh"+".csv"
    csvNameDHK = fileName+"_DHK"+".csv"
    print("Converting to "+csvNameBD)
    try: 
        BDTables = camelot.read_pdf(fileLoc, pages = "1")
        bdlist= []
        for table in BDTables:
            bdlist.append(table.df)
        bddf = pd.concat(bdlist)
        del bddf[0]
        del bddf[3]
        del bddf[4]
        bddf = bddf.iloc[1:]
        bddf = bddf.iloc[bddf[1].str.lower().argsort()]
        bddf.to_csv(csvNameBD, index=False)
    except Exception:
        print(Exception)
    try:
        DhakaTables = camelot.read_pdf(fileLoc, pages = "2-end")
        print("Converting to "+csvNameDHK)
        dhklist= []
        for table in DhakaTables:
            dhklist.append(table.df)
        dhkdf = pd.concat(dhklist) 
        dhkdf = dhkdf.iloc[dhkdf[0].str.lower().argsort()]
        dhkdf.drop(dhkdf.loc[dhkdf[0]=="Location"].index, inplace=True)
        dhkdf.to_csv(csvNameDHK, index=False)
    except IndexError:
        print("IEDCR didn't publish any data for DhakaCity today.")

    print("Done!")
