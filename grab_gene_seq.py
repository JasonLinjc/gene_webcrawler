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

def add_seq_to_file(seq, filename):
    if os.path.exists(filename):
        pass
    else:
        f = open(filename, "w")
        f.close()

    f = open(filename, "r")
    lines = f.readlines()
    seq_no = int(len(lines)/2) + 1
    print(seq_no)
    f.close()
    f = open(filename, "a")
    f.write(">seq" + str(seq_no) + "\n")
    f.write(seq + "\n")
    f.close()

# wb = openpyxl.load_workbook(filename=r'aav1898_Data_S7.xlsx')
# ws = wb['All_Links']
# print(ws)
def build_MotifHyades_input(start_idx):
    data  = pd.read_excel('aav1898_Data_S7.xlsx')
    for idx, row in data.iterrows():
        if idx < start_idx:
            continue
        print("-"*20, idx, "-"*20)
        with open("idx_record.txt", "w") as f:
            f.write(str(idx))
        chr = row['Chromosome'].split("r")[-1]
        enhancer_s = row['Start']
        enhancer_e = row['End']
        linked_gene = row['Linked_Gene']
        promoter_e = row['Linked_Gene_Start'] - 1
        promoter_s = promoter_e - 999
        promoter_file = "./motifhyades_input/promoter/" + linked_gene + "_p.faste"
        enhancer_file = "./motifhyades_input/enhancer/" + linked_gene + "_e.faste"
        print(chr, enhancer_s, enhancer_e)
        enhancer_seq = get_seq(chr=chr, start=enhancer_s, end=enhancer_e)
        promoter_seq = get_seq(chr=chr, start=promoter_s, end=promoter_e)
        # add_seq_to_file(enhancer_seq, enhancer_file)
        # add_seq_to_file(promoter_seq, promoter_file)


import time
try:
    build_MotifHyades_input(0)
except:
    print("Failed!")
    time.sleep(600)
    f = open("idx_record.txt", "r")
    idx = int(f.readline().strip())
    build_MotifHyades_input(idx)
