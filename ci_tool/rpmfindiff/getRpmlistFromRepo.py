import argparse
import urllib.request
from bs4 import BeautifulSoup
import requests
import re, os, sys

OS_VERSION_PATH = {
        'centos8.0':'https://vault.centos.org/8.1.1911/',
        'centos8.1':'https://vault.centos.org/8.1.1911/',
        'centos8.2':'https://vault.centos.org/8.2.2004/',
        'centos8.3':'https://vault.centos.org/8.3.2011/',
        'centos8.4':'https://vault.centos.org/8.4.2105/',
        'euler21.09':'https://repo.openeuler.org/openEuler-21.09/',
        }

def geturl(myurl, rpms):
    url = requests.get(myurl)
    data =url.text
    tmpAvoidReplic = []
    bs = BeautifulSoup( data, "html.parser", from_encoding="utf-8")
    try:
        table = bs.table
        links = table.find_all('a')
        for link in links:        
            href = link['href']
            if href == "../" or href == "./" or href[0] == "?":
                continue
            elif href in myurl:
                continue
            elif href[-1] == '/':
                urlplus = myurl + href
                geturl(urlplus, rpms)
            elif href[-8:] == ".src.rpm":
                if href in tmpAvoidReplic:
                    continue
                else:
                    tmpAvoidReplic.append(href)
                    rpms.append(myurl+href)
                    print(myurl+href)
    except Exception as e:
        pass
    return

'''    
'''
def getrpmname(version, url):
    rpmlist = []
    geturl(url, rpmlist)
    rpmName = list(set(rpmlist))
    rpmName.sort()
    filename = version+'_rpmlist.yaml'
    outfile = open(filename, 'w')
    outfile.write(version+':\n')
    for rpmurl in rpmName:
        outfile.write('- ' + rpmurl + '\n')
#    print(rpmName)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A tool get OS src.rpm packages.')
    parser.add_argument('-v', '--version',help='Version need to be compared: euler21.09, centos8.2, centos8.3,', required = True)
    parser.add_argument('-p', '--path',help='The path of OS src.rpm reporitories. '
            'eg, https://repo.openeuler.org/openEuler-21.09/, if None we use default path.'
            'defaul version path: '
            'centos8.0:https://vault.centos.org/8.1.1911/ '
            'centos8.1:https://vault.centos.org/8.1.1911/ '
            'centos8.2:https://vault.centos.org/8.2.2004/ '
            'centos8.3:https://vault.centos.org/8.3.2011/ '
            'centos8.4:https://vault.centos.org/8.4.2105/ '
            'euler21.09:https://repo.openeuler.org/openEuler-21.09/',
            required = False)
    args = parser.parse_args()
    version = args.version
    path = args.path
    print(OS_VERSION_PATH.keys())
    if version not in OS_VERSION_PATH.keys():
        if not path:
            print("There is no default path with the OS version given, need to input REPO path with OS version.")
            sys.exit(2)
    else:
        if not path:
            path = OS_VERSION_PATH[version]
    print("version:"+version)
    print("Now get repos with url path: {}".format(path))
    getrpmname(version, path)