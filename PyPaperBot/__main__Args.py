# -*- coding: utf-8 -*-

import argparse
import sys
import os
from Paper import Paper
from PapersFilters import filterJurnals, filter_min_date, similarStrings
from Downloader import downloadPapers
from Scholar import ScholarPapersInfo
from Crossref import getPapersInfoFromDOIs
from pathlib import Path


def start(query, scholar_pages, dwn_dir, min_date=None, num_limit=None, num_limit_type=None, filter_jurnal_file=None, restrict=None, DOIs=None):
    
    to_download = []
    if DOIs==None:
        print("Query: {}".format(query)) 
        to_download = ScholarPapersInfo(query, scholar_pages, restrict)
    else:
        print("Downloading papers from DOIs\n")
        num = 1
        i = 0
        while i<len(DOIs):
            DOI = DOIs[i]
            print("Searching paper {} of {} with DOI {}".format(num,len(DOIs),DOI))
            papersInfo = getPapersInfoFromDOIs(DOI, restrict)
            to_download.append(papersInfo)
            num += 1
            i +=  1       
    
    if restrict!=0:
        if filter_jurnal_file!=None:
           to_download = filterJurnals(to_download,filter_jurnal_file)
       
        if min_date!=None:
            to_download = filter_min_date(to_download,min_date)  
         
        if num_limit_type!=None and num_limit_type==0:       
            to_download.sort(key=lambda x: int(x.sc_year) if x.sc_year!=None else 0, reverse=True)
            
        if num_limit_type!=None and num_limit_type==1:       
            to_download.sort(key=lambda x: int(x.sc_cites) if x.sc_cites!=None else 0, reverse=True)
    
    downloadPapers(to_download, dwn_dir, num_limit)

    Paper.generateReport(to_download,dwn_dir+"result.csv")
    Paper.generateBibtex(to_download,dwn_dir+"bibtex.bib")
    print("Dank voor het gebruik. Opmerkingen kunnen naar spam01@albertsikkema.com")
    
    
def check_if_files_exist(dwn_dir):
    bib_file = dwn_dir+"bibtex.bib"
    if not os.path.exists(bib_file):
        open(bib_file, 'w').close()
    result_file = dwn_dir + "result.csv"
    headers = "Name,Scholar Link,DOI,Bibtex,PDF Name,Year,Scholar page,Journal,Downloaded,Downloaded from"
    if not os.path.exists(result_file):
        f = open(result_file, 'w')
        f.write(headers)
        f.close()

def main():
    print("PyPaperBot is a Python tool for downloading scientific papers using Google Scholar, Crossref and SciHub.\n")
    
    parser = argparse.ArgumentParser(description='PyPaperBot is python tool to search and download scientific papers using Google Scholar, Crossref and SciHub')
    parser.add_argument('--query', type=str, default=None, help='Query to make on Google Scholar or Google Scholar page link')
    
    args = parser.parse_args()

    dwn_dir = 'C:/Users/Albert/Desktop/Workspace_SciHub/papers/' # C:\Users\Albert\Desktop\Workspace_SciHub\papers
    check_if_files_exist(dwn_dir)
       
    # If Title is given as argument
    title_search = args.query
    scholar_pages = 1
    start(title_search, scholar_pages, dwn_dir)
    

if __name__ == "__main__":
    main()