import argparse
import os
import sys
import requests
import json


INVITE_URL = "https://api.gitee.com/enterprises/{}/members/invite_members"

def getInviteMemberUrlLink(enterid, token, roleid):
    get_url = INVITE_URL.format(enterid)
    param = {'access_token' : token, 'role_id' : roleid, 'need_check' : 1, 'outsourced' : 0}
    response = requests.post(get_url, params=param, timeout=10)
    if response.status_code != 201:
        print("Get issues failed, error code:{}.".format(response.status_code))
        return
    members = []

    jstr = json.loads(response.text)
    inviteUrl = jstr['invite_url']
    print(inviteUrl)

    return     

if __name__ == '__main__':
    if len(sys.argv) != 4:
        for arg in sys.argv:
            print(arg)
        print("参数错误，enterprise_id , v8Token, roleid ")
        print("请参考: https://gitee.com/api/v8/swagger#/postEnterpriseIdMembersInviteMembers")
        sys.exit(2)
    enterid = sys.argv[1]
    token = sys.argv[2]
    roleid = sys.argv[3]
    getInviteMemberUrlLink(enterid, token, roleid)

