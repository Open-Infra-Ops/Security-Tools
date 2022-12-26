import argparse
import requests
import os
import sys
import json
import time

FILENAME = "operatelabel.log"
GITEE_ADD_LABEL_URL = "https://gitee.com/api/v5/repos/{}/{}/issues/{}/labels"
GITEE_DEL_LABEL_URL="https://gitee.com/api/v5/repos/{}/{}/issues/{}/labels/{}"
GITHUB_ADD_LABEL_URL = "https://api.github.com/repos/{}/{}/issues/{}/labels"
GITHUB_DEL_LABEL_URL = "https://api.github.com/repos/{}/{}/issues/{}/labels/{}"


def operare_labels(logf, GITEE_TOKEN, GITHUB_TOKEN):

    timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    logf.write("[{}]================= Begin to send command to operate label to issue.=======================\n".format(timestr))
    # Add issue label.
    gitee_add_label_url = GITEE_ADD_LABEL_URL.format("ci-bot", "community", "I3SBZL")
    param = {'access_token' : GITEE_TOKEN}
    payload = "[\"bug\"]"
    response = requests.post(gitee_add_label_url, params=param, data = payload, timeout = 10)
    if response.status_code != 201:
        timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        logf.write("[{}] Add gitee failed {} : {}\n".format(timestr, response.status_code, response.url))
    
    #Delete issue label
    gitee_del_label_url = GITEE_DEL_LABEL_URL.format("ci-bot", "community", "I3SBZL", "bug")
    param = {'access_token' : GITEE_TOKEN}
    response = requests.delete(gitee_del_label_url, data=param, timeout = 10)
    if response.status_code != 204:
        timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        logf.write("[{}] Delete gitee failed {} : {}\n".format(timestr, response.status_code, response.url))

    #Add issue label to github
    github_add_label_url = GITHUB_ADD_LABEL_URL.format("GeorgeCao-hw", "georgedoc", "1")
    param = {'access_token' : GITHUB_TOKEN}
    payload = "[\"bug\"]"
    response = requests.post(github_add_label_url, params=param, data = payload, timeout = 10)
    if response.status_code != 200:
        timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        logf.write("[{}] Add github failed {} : {}\n".format(timestr, response.status_code, response.url))

    #Delete label from github issue.
    github_del_label_url = GITHUB_DEL_LABEL_URL.format("GeorgeCao-hw", "georgedoc", "1", "bug")
    param = {'access_token' : GITHUB_TOKEN}
    response = requests.delete(github_del_label_url, params=param, timeout = 10)
    if response.status_code != 200:
        timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        logf.write("[{}] Delete github failed {} : {}\n".format(timestr, response.status_code, response.url))
    
    return

def main():
    if len(sys.argv) != 3:
        print("Param error, you should do command like this: \n python 502test.py giteeToken githubToken ")
        return
    GITEE_TOKEN = sys.argv[1]
    GITHUB_TOKEN = sys.argv[2]

    with open(FILENAME,'w') as f:
        for idx in range(0, 50000):
            operare_labels(f, GITEE_TOKEN, GITHUB_TOKEN)
            f.flush()
            time.sleep(5)

if __name__ == '__main__':
    main()

