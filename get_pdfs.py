
"""
Download all the pdfs linked on a given url or in the urls specified in the excel file
Requires - requests >= 1.0.4
           beautifulsoup >= 4.0.0
Download and install using

    pip install requests
    pip install beautifulsoup4
"""
from decor_helper import static_vars
from requests import get
from urllib.parse import urljoin
from bs4 import BeautifulSoup as soup
from sys import argv

def get_all_links(content):
    bs = soup(content)
    tags = bs.findAll('a')
    links =[]
    for row in tags:
        try:
            if "ANNUAL" in row["href"].upper():
                links.append(row["href"])
        except:
            continue
    return links



@static_vars(done_urls=None)
def get_pdfs(url,folder,pdfs):
    req = get(url)
    if get_pdfs.done_urls is None:
        get_pdfs.done_urls=[]

    if req.status_code == 200:
        content = req.text
    else:

        print("fail to open the url "+ url)

        return pdfs

    links = get_all_links(content)

    if len(links) == 0:
        #logger.exception("There is no links in this page" + url)
        print("There is no links in this page" + url)
        return pdfs

    n_pdfs = 0

    for link in links:
        if urljoin(url, link) in get_pdfs.done_urls:
            continue
        else:
            get_pdfs.done_urls.append(urljoin(url, link))
            filename = link.split("/")[-1].split(".")[0]
            if link[-4:] == '.pdf' and "ANNUAL" in filename.upper() :
                n_pdfs += 1
                res = get( urljoin(url, link)  )
                if res.status_code == 200 and res.headers['content-type'] == 'application/pdf':
                    pdfs[link]={"file_link":link,"content":res.content,"filename":filename,"output_folder":folder}

            else:
                get_pdfs(url, folder,pdfs)

    if n_pdfs == 0:
        #logger.warning("there is no pdf in this website " + url)
        print("there is no pdf in this website " + url)
        return pdfs

    return pdfs
