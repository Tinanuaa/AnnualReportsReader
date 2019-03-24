import sys

from get_pdfs import get_pdfs
from file_helper import save_pdf, write_multiple_df_to_excel
from tabula import read_pdf
import camelot
from PyPDF2 import PdfFileReader
#Excalibur
import pandas as pd
from logging_helper import logger


def pdfs_to_excel(urls ):

    result = {}
    for url in urls:
        folder = url.split("/")[2]

        pdfs = get_pdfs(url,  folder,{})

        if pdfs is not None:
            result[url] = pdfs

    files = []
    for url, url_pdfs in result.items():
        for link, pdf_data in url_pdfs.items():
            filename = save_pdf(pdf_data["content"],pdf_data["filename"],pdf_data["output_folder"])
            files.append(filename)

    extract_tables(files)

def extract_tables(files):
    for filename in files:
        # filename = "./input/bhpannualreport2018.pdf"
        fileReader = PdfFileReader(open(filename, 'rb'))
        num = fileReader.numPages
        result = {}
        for i in range(1, num + 1):
            try:
                table = read_pdf(filename, pages=i)
                if table is not None :
                    result.update({"sheet_"+str(i):{"column":table.columns.tolist(), "data":table}})
                    #write_to_excel(filename,table)
            except:
                logger.exception("fail to extract table from this pdf")
                continue
        try:
            write_multiple_df_to_excel(filename.split("\\")[-1].split(".")[0]+"_" , result)
        except:
            logger.exception("fail to write the tables into excel")

if __name__=="__main__":
    args = sys.argv
    input_type = args[1]  # input_type can be url or xlsx
    input_data = args[2]  # the url or xlsx filename
    print(input_type,input_data)
    if input_type.upper()=="URL":
        pdfs_to_excel([input_data])
    elif input_type.upper()=="XLSX":
        inputs = pd.read_excel(input_data)
        pdfs_to_excel(inputs["urls"].tolist())
    else:
        print("""
        Usage: pdf_to_excel input_type input_data
        input_type can be "url" or "xlsx"
        input_data can be url or path to the excel file which contains the urls for scraping, the column name should be "urls"
        Example: pdf_to_excel url https://www.bhp.com
        The downloaded pdfs are in output folder with the main url address as the folder name
        The excel file is written into the output folder directly
        """)


