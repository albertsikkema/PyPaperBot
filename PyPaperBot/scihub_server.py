import requests
import sys
from bs4 import BeautifulSoup as bs4
from importlib import reload
import os, re
import time
import random
import fileinput


# get list of https adresses for scihub, to add to List_URLS
def get_scihub_location():
    # print(f"can I get to {List_URLS}")
    PATTERN = r">(https://sci-hub.[^</]+)<"
    src_url = "http://tool.yovisun.com/scihub/"
    html = requests.get(src_url).text
    available_links = re.findall(PATTERN, html)
    return available_links
    
# Find first valid https adress for Scihub from List_URLS
def find_first_valid_url(url_list):
    for url in url_list:
        # print("Validating {}".format(url))
        if url == "":
            print("URL not valid")
        # Send request to given url
        # and compare title tags
        else:                
            response = requests.get(url)
            soup = bs4(response.content, "lxml")
            if soup.title.text == "Sci-Hub: removing barriers in the way of science":
                # print("{} validated\n".format(url))
                if url[-1] != "/":
                    url += "/"
                return url
                pass
    answer = 'No valid URL for SciHub in URL-List'
    return answer

# Find all valid https adress for Scihub from List_URLS
def find_all_valid_urls(url_list):
    validated_list = []
    for url in url_list:
        # print("Validating {}".format(url))
        if url == "":
            print("URL not valid")
        # Send request to given url
        # and compare title tags
        else:                
            response = requests.get(url)
            soup = bs4(response.content, "lxml")
            if soup.title.text == "Sci-Hub: removing barriers in the way of science":
                # print("{} validated\n".format(url))
                if url[-1] != "/":
                    url += "/"
                validated_list.append(url)
    # print("\nValidated addresses for SciHub:")
    # for a in validated_list:
    #     print(a)
    return validated_list


def check_scihub_server(List_URLS):
    # global List_URLS
    url=find_first_valid_url(List_URLS)
    print(f'Server-URL: {url}')
    if url == 'No valid URL for SciHub in URL-List':
        print("Update Server List for SciHub in main menu\n")
        return "error: no server address"
    else:    
        return url

def update_scihub_server_list(List_URLS):
        print("Validating known SciHub-locations....")
        validated_known_list = find_all_valid_urls(List_URLS)
        List_URLS_new = get_scihub_location()
        validated_new_list = find_all_valid_urls(List_URLS_new)
        for item in validated_new_list:
            if item not in validated_known_list:
                print(f"{item} is added and validated")
                validated_known_list.append(item)
        print("\nValidated server adresses for SciHub:")        
        for item in validated_known_list:
            print(item)
        print('')
        # print(url)
        # print(f'Server-URL: {url}')
        # update scihub list in settings.py
        for line in fileinput.input('Preferences.py', inplace=True):
            if line.strip().startswith('List_URLS='):
                line = f"List_URLS={validated_known_list}\n"
            sys.stdout.write(line)
        # print("Updated List with SciHub Servers\n")
    