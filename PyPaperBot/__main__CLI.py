# -*- coding: utf-8 -*-

import argparse
import sys
import os
import json
import fileinput
from pathlib import Path
from importlib import reload
from Paper import Paper
from PapersFilters import filterJurnals, filter_min_date, similarStrings
from Downloader import downloadPapers
from Scholar import ScholarPapersInfo
from Crossref import getPapersInfoFromDOIs
import Preferences
from scihub_server import check_scihub_server, update_scihub_server_list


def start(query, scholar_pages, dwn_dir, min_date=None, num_limit=None, num_limit_type=None, filter_jurnal_file=None, restrict=None, DOIs=None):
    to_download = []

    # Query goes to scholar.google.com to find info, then to Crossref, then to scihub
    if DOIs == None:
        print("\nQuery: {}".format(query))
        # Get a list of papers to download
        to_download = ScholarPapersInfo(query, scholar_pages, restrict)
        if to_download == "specify query":
            main()
    else:
        num = 1
        i = 0
        while i < len(DOIs):
            DOI = DOIs[i]
            print("\nSearching paper {} of {} with DOI {}".format(
                num, len(DOIs), DOI))
            papersInfo = getPapersInfoFromDOIs(DOI, restrict)
            to_download.append(papersInfo)
            num += 1
            i += 1
    # Restrictions/Filters are not used in this version
    if restrict != 0:
        if filter_jurnal_file != None:
            to_download = filterJurnals(to_download, filter_jurnal_file)

        if min_date != None:
            to_download = filter_min_date(to_download, min_date)

        if num_limit_type != None and num_limit_type == 0:
            to_download.sort(key=lambda x: int(x.sc_year)
                             if x.sc_year != None else 0, reverse=True)

        if num_limit_type != None and num_limit_type == 1:
            to_download.sort(key=lambda x: int(x.sc_cites)
                             if x.sc_cites != None else 0, reverse=True)

    # Get papers from SciHub
    downloadPapers(to_download, Preferences.dwn_dir, num_limit)
    # Add info to result.csv and bibtex.bib
    Paper.generateReport(to_download, Preferences.dwn_dir+"result.csv")
    Paper.generateBibtex(to_download, Preferences.dwn_dir+"bibtex.bib")
    # And start again...
    main()


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
    # Check if result.csv and bitex.bib exist. otherwise make them
    check_if_files_exist(Preferences.dwn_dir)
    print("This is a Python tool for downloading scientific papers using Google Scholar, Crossref and SciHub, based on PyPaperBot.\nAdapted for Easier Use by Albert Sikkema.\n")
    print("Choose an option: \n")
    select_search = input(
        "(1) Search with title\n(2) Search with DOI\n(d) Change Download Location\n(u) Update list of Sci-Hub Servers\n(q) Quit\n\n")

    # Search with text
    if select_search == '1':
        title_search = input("Enter a title: ")
        scholar_pages = 1
        start(title_search, scholar_pages, dwn_dir=Preferences.dwn_dir)

    # Search with DOI
    elif select_search == '2':
        DOI = input("Enter a DOI: ")
        DOIs = [DOI]
        scholar_pages = 1
        query = None
        start(query, scholar_pages=scholar_pages, dwn_dir=Preferences.dwn_dir, DOIs=DOIs)

    # Change Download Location
    elif select_search == 'd':
        current_loc = Preferences.dwn_dir.strip('"')
        print(f"Current Location for download is: {current_loc}")
        new_loc = input("Enter a new location: ")
        sure_input = input(f"Are you sure? ({new_loc}) (y/n) ")
        if sure_input == 'y':
            new_loc_str = f'"{new_loc}"'
            for line in fileinput.input('Preferences.py', inplace=True):
                if line.strip().startswith('dwn_dir='):
                    line=f"dwn_dir={new_loc_str}\n"
                sys.stdout.write(line)
            print(f"Download location updated to {new_loc}")
        else:
            print("Try again")
        reload(Preferences)
        main()


    # Update list of Sci_Hub Servers
    elif select_search == 'u':
        update_scihub_server_list(Preferences.List_URLS)
        reload(Preferences)
        main()

    # Quit Program
    elif select_search == 'q':
        quit()

1

if __name__ == "__main__":
    main()
