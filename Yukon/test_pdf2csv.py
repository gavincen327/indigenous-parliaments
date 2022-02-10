from process_yukon_hansards import process_converted_pdfs
import process_pdfs as procpdf
from indig_parl_utils import download_mht, send_text_to_file
from indig_parl_re import text_rem_patterns, text_extract_pattern
import pandas as pd
from get_yukon_hansards import process_pdf
import csv
import sys
import requests
import pandas as pd
import textract
import datetime
import PyPDF2
from tika import parser

pdf_path = "test_2019_04_01_pdf from mht.pdf"
str_date = '2019-04-01'
file_prefix = str_date
process_converted_pdfs(pdf_path, str_date, file_prefix)
