import math

import pandas as pd
import requests, os
from weasyprint import HTML
import time
import re

from indig_parl_logger import get_logger
from indig_parl_utils import download_mht, send_text_to_file
from indig_parl_re import text_rem_patterns, text_extract_pattern
from process_mhts import extract_files

content = pd.read_csv('yukon_hansards.csv', skiprows=range(1, 10))
for i in range(len(content['Date_Short'])):
    title = content['Date_Short'][i]
    print(title + " start now!")
    pdf = content['PDF'][i]
    #if pd.isna(pdf):
        #print(title + " does not have PDF!")  # skip empty pdf
        #continue
    # download pdf
    #pdftext = requests.get(content['PDF'][i])
    #with open('pdfs/' + '\\' + title + '.PDF', 'wb') as f:
       # f.write(pdftext.content)
       # f.close()
        #print(title + " PDF downloaded!")
       # time.sleep(2)

    mht = content['MHT'][i]
    if pd.isna(mht):
        print(title + " does not have MHT!")  # skip empty mht
        continue
    #download mht
    pathname, extension = os.path.splitext(mht)
    file_extension = extension

    mht = requests.get(mht).content
    mht = mht.decode('utf-16-le', "ignore")

    if file_extension == ".html":
        with open('mhts/' + '\\' + title + '.html', 'w', encoding='utf-16-le') as f:
            f.write(mht)
            f.close()
            print(title + " HTML downloaded!")
            time.sleep(2)
    else:
        with open('mhts/' + '\\' + title + '.mht', 'w', encoding='utf-16-le') as f:
            f.write(mht)
            f.close()
            print(title + " MHT downloaded!")
            time.sleep(2)

#convert mht to pdf
for mhtfile in os.listdir("D:/OneDrive - University of Pittsburgh/GitHub/indigenous-parliaments/indigenous-parliaments/Yukon/mhts/"):
    pathname, extension = os.path.splitext(mhtfile)
    filename = pathname.split('/')
    filename = filename[-1]
    mht_loc = "D:/OneDrive - University of Pittsburgh/GitHub/indigenous-parliaments/indigenous-parliaments/Yukon/mhts/" + filename + extension
    print(mht_loc)
    if extension == ".mht":
        outcome = extract_files(mht_loc)
        if outcome:
            html_file = HTML(outcome)
            pdf_name = filename
            pdf_path = 'pdf converted from mht/' + pdf_name + '.pdf'
            html_file.write_pdf(pdf_path)
            print(filename + ' Saved to pdf:', pdf_path)
        else:
            print("Fail to convert. Now second attempt...")
            html_file = HTML(mht_loc)
            pdf_name = filename
            pdf_path = 'pdf converted from mht/' + pdf_name + '.pdf'
            html_file.write_pdf(pdf_path)
            print(filename + ' Saved to pdf:', pdf_path)
            print("Second attempt succeeded!")
    else:
        html_file = HTML(mht_loc)
        pdf_name = filename
        pdf_path = 'pdf converted from mht/' + pdf_name + '.pdf'
        html_file.write_pdf(pdf_path)
        print(filename + ' Saved to pdf:', pdf_path)