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
FILENAME = "summer2021-repo.yaml"
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
            user = item['user']
            user_giteeid = user['login']
#            print(issue_title)
            
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
            print("username: " + user_giteeid)
#            print(issue_detail)
            print(issue_url)
            print(emailobj)
            issue = [issue_id, issue_title, user_giteeid, issue_url, emailobj]
            issues.append(issue)
      
    issues.reverse()
    with open(FILENAME,'w') as f: 
        f.write("general: Summer_2021_repo\n")
        f.write("repositories:\n")
        for issue in issues:            
            name = "- name: Summer2021-{}\n".format(issue[1])
            description = "  description: {}\n".format(issue[3])
            path = "  path: https://gitee.com/openeuler-competition/summer2021-{}\n".format(issue[0])
            tutor = "  tutor: \n  - giteeid: {}\n    email: {}\n".format(issue[2], issue[4][0])
            member = "  member:\n  - giteeid: \n    email: \n"
            repoinfo = name + description + path + tutor + member
            f.write(repoinfo)
        
    return  

if __name__ == '__main__':
    main()