import urllib.request
from bs4 import BeautifulSoup
import requests
import re, os, sys

def geturl(myurl, rpms):
    url = requests.get(myurl)
    data =url.text
    bs = BeautifulSoup( data, "html.parser", from_encoding="utf-8")
#    links = bs.find_all('a')
#    for link in links:
#        print(link.name)
#        print(link['href'])
#        print(link.get_text())
#    print(data)
#    print("*************")

    table = bs.table
#    tbody = table.tbody
#    print(table)
#    print(tbody)
    links = table.find_all('a')
    for link in links:        
#        print(link['href'])
        href = link['href']
        if href == "../" or href == "./" or href[0] == "?":
            continue
        elif href in myurl:
            continue
        elif href[-1] == '/':
            urlplus = myurl + href
            geturl(urlplus, rpms)
        elif href[-8:] == ".src.rpm":
            rpms.append(href)
            print(href)
    return

'''    
'''
def getrpmname(url):
    rpmlist = []
    geturl(url, rpmlist)
    rpmName = list(set(rpmlist))
    rpmName.sort()
    outfile = open(r'rpmlist.txt', 'w')
    for rpm in rpmName:
        outfile.write(rpm + '\n')
#    print(rpmName)

if __name__ == '__main__':
#    geturl('http://121.36.97.194/openEuler-21.09/')
    if len(sys.argv) != 2:
        print("Param Error, eg: python3 getfilename url")
    urlinput = sys.argv[1]
    print(urlinput)
    getrpmname(urlinput) 
