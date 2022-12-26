import oyaml as yaml
import os
import sys
import requests
import json

URL = "https://gitee.com/api/v5/repos/{}/{}/branches"
FILENAME = "BranchLog.log"

def compare_br(logfile, repo, br_in_file, br_on_gitee):
    #find pretect in file check if protect on gitee
#    print(br_in_file)
#    print(br_on_gitee)

    for br in br_in_file:
        findbr = False
        sametype = False

        protect = br["type"] == "protected"
        for br_ex in br_on_gitee:
            if br["name"] != br_ex["name"]:
                continue
            findbr = True
            if br_ex["protected"] and protect:
                sametype = True
            break
        if not findbr:
            logfile.write("In_file_not_on_gitee:               Branch:{} in repo:{}.\n".format(br["name"], repo))
            continue
        if not sametype:
            logfile.write("In_file_on_gitee_type_diff:         Type of Branch:{} in repo:{} not same.\n".format(br["name"], repo))
            continue
    for br_ex in br_on_gitee:
        findbr = False
        sametype = False
#        print("\nBR on gitee: "+ br_ex["name"]+"  protected: ")

        protect = br_ex["protected"]
        for br in br_in_file:
#            print("BR in file: " + br["name"] + "   " + br["type"])
            if br_ex["name"] != br["name"]:
                continue
            findbr = True
            if protect and br["type"] == "protected":
                sametype = True
            break
        if not findbr:
#            print("BR " + br["name"] + "  not find.")
#            print(protect)
            if protect:
                logfile.write("On_gitee_not_in_file_protected:     Branch:{}       in  not on gitee.\n".format(br_ex["name"], repo))
#            else:
#               logfile.write("On_gitee_not_in_file_normal:                Branch:{} in repo:{} not on gitee.\n".format(br["name"], repo))
            continue
        if not sametype:
            logfile.write("On_gitee_in_file_type_diff:      Type of Branch:{} in repo:{} not same.\n".format(br_ex["name"], repo))
            continue
    return

def check_repo_branches(owner, token):
    if owner != "openeuler" and owner != "src-openeuler":
        return

    logfile = open(FILENAME, 'w', buffering=1)

    file_path = os.path.split(os.path.realpath(__file__))[0]
    repo_yaml_patch = os.path.join(file_path, owner+".yaml")
    print("Orgina: {}".format(owner))
    logfile.write("Begin to check.\n")

    with open(repo_yaml_patch, 'r', encoding="utf-8") as repo_yaml:
        content = yaml.load(repo_yaml.read(), Loader=yaml.FullLoader)
        repolist = content["repositories"]
        for repo in repolist:
            repo_name = repo["name"]
            br_in_file = repo["branches"]
            url = URL.format(owner, repo_name)
            param = {'access_token': token}
            response = requests.get(url, params=param, timeout=10)
            if response.status_code != 200:
                print("Get issues failed, error code:{}.".format(response.status_code))
                continue
            br_on_gitee = json.loads(response.text)
            #compare branches
            compare_br(logfile, repo_name, br_in_file, br_on_gitee)

    logfile.write("\nEnd check.\n")
    return

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Param error, you should like this: \n python check_br Token  ")
        sys.exit()
    Token = sys.argv[1]
    check_repo_branches("src-openeuler", Token)

