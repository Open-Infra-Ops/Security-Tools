#/bin/env python3
# -*- encoding=utf8 -*-
#******************************************************************************
# Copyright (c) Huawei Technologies Co., Ltd. 2020-2020. All rights reserved.
# licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR
# PURPOSE.
# See the Mulan PSL v2 for more details.
# Author: georgecao
# Create: 2022-01-18
# ******************************************************************************
import json
import os
import yaml
import argparse
import requests


class checkPrivateRepoInReleasePkgs(object):
    def __init__(self, org, release_file, token):
        """
        :parm branch_map_yaml: yaml file of branch map
        :parm community_path: community repo path
        :parm pr_id: id of community pr
        """
        self.error_flag = 0
        self.warn_flag = 0
        self.org = org
        self.releasefile = release_file
        self.token = token
        self.relase_pkgs = []
        self.org_private_repos = []
        self.result = []

    def _read_yaml(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                file_msg = yaml.load(f, Loader=yaml.FullLoader)
        return file_msg

    def get_release_pkgs(self):        
        release = self._read_yaml(self.releasefile)
        allp = release['packages']
        for kind in allp:
            packages = allp[kind]
            if type(packages) == list:
                for pack in packages:
                    pkgname = pack['name']
                    self.relase_pkgs.append(pkgname)
            if type(packages) == dict:
                for subkind in packages:
                    subpackages = packages[subkind]
                    if type(subpackages) != list:
                        continue
                    for pack in subpackages:
                        pkgname = pack['name']
                        self.relase_pkgs.append(pkgname)
        return

    def get_private_repo(self):
        url = 'https://gitee.com/api/v5/orgs/{}/repos'.format(self.org)
        page = 1
        while True:
            params = {
                    'page': page,
                    'type': 'private',
                    'per_page': 100,
                    'access_token': self.token
                }
            r = requests.get(url, params=params)
            if r.status_code != 200:
                print(r.json())
                return
            jstr = json.loads(r.text)
            
            for repo in jstr:
                full_name = repo['full_name']
                repo_name = full_name.split('/')[-1]
                self.org_private_repos.append(repo_name)
            page+=1
            if len(jstr)<100:
                break
        return
    
    def find_private_in_release(self):
        for pkg in self.relase_pkgs:
            if pkg in self.org_private_repos:
                self.result.append(pkg)
        self.result.sort()
        print(self.result)
        return

if __name__ == "__main__":
    import argparse
    par = argparse.ArgumentParser()
    par.add_argument("-org", "--org_name", help="organization name", required=True)
    par.add_argument("-pkg", "--pkgfile", help="package file to release management", required=True)
    par.add_argument("-token", "--token", help="user token of the gitee account.", required=True)
    args = par.parse_args()
    C = checkPrivateRepoInReleasePkgs(args.org_name, args.pkgfile, args.token)
    C.get_private_repo()
    C.get_release_pkgs()
    C.find_private_in_release()


