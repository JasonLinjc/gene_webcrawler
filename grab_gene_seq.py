# -*- coding: utf-8 -*-
# @Time    : 27/3/2019 10:56 PM
# @Author  : Jason Lin
# @File    : grab_gene_seq.py
# @Software: PyCharm

import urllib3
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import os
import openpyxl
# http://genome.ucsc.edu/cgi-bin/das/hg38/dna?segment=chr17:7676091,7676196

def get_seq(chr=1, start=7676091, end=7676196):
    http = urllib3.PoolManager()
    r = http.request('GET', "http://genome.ucsc.edu/cgi-bin/das/hg38/dna?segment=chr" + str(chr) + ":" + str(start)
    + "," + str(end), retries=10)
    geneSoup = BeautifulSoup(r.data, "xml")
    geneSeq =  geneSoup.find("DNA").contents[0].strip().replace("\n","")
    return geneSeq

# wb = openpyxl.load_workbook(filename=r'aav1898_Data_S7.xlsx')
# ws = wb['All_Links']
# print(ws)
data  = pd.read_excel('aav1898_Data_S7.xlsx')
print(data)
