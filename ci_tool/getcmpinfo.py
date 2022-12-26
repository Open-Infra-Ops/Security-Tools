'''
This is a bot for openEuler competition repository manage.
'''

import argparse
import re
import os
import sys
import requests
import json

OWNER = "openeuler-competition"
REPO = "summer-2021"
TOKEN = "70d613624cf6b67e2e3d1b7025216fe8"
FILENAME = "infoemal.txt"
GET_URL = "https://gitee.com/api/v5/repos/{}/{}/issues"


def gen_url():
    return GET_URL.format(OWNER, REPO, TOKEN)

def main():
    '''
    This is a main function entry
    '''
    issues = []
    
    for index in [1, 2]:
        url = gen_url()
        param = {'access_token': TOKEN, 'state': 'open', 'sort': 'created', 'direction': 'desc', 'page': index,'per_page': 100}
        print(url)
        response = requests.get(url, params=param, timeout=10)
        if response.status_code != 200:
            print("Get issues failed, error code:{}.".format(response.status_code))
            return


        jstr = json.loads(response.text)
        for idx, item in enumerate(jstr):
            print('==================================')
            issue_url = item['html_url']
            issue_title = item['title']
            ll= re.findall(r"\d+?\d*",issue_title)
            if not ll:
                continue
            issue_id  = ll[0]
            if int(issue_id) > 500:
                continue
            issue_detail = item['body']

            emailobj = re.findall(r'([a-zA-Z0-9_.+-]+@[a-pr-zA-PRZ0-9-]+\.[a-zA-Z0-9-.]+.)', issue_detail)
            if not emailobj:
                emailobj = ['===============  '+issue_url]
    #        email = emailobj[0]
     
            # 打印结果
            
            print(issue_id)    
            print(issue_title)
    #        print(issue_detail)
            print(issue_url)
    #        print(issue_level)
            print(emailobj)
            issue = [issue_id, issue_title, issue_url, emailobj]
            issues.append(issue)
      
    issues.reverse()
    with open(FILENAME,'w') as f: 
        for issue in issues:
            ID = "\"ID\": {}\t".format(issue[0])
            EMAIL = format(issue[3][0])
            LINK = "\t\t \"LINK\": \"{}\"".format(issue[2])            
            f.write(EMAIL)
            f.write(",\n")
        
    return  

if __name__ == '__main__':
    main()