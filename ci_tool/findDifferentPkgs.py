# -*- encoding=utf-8 -*-
import os
import re
import subprocess
import sys
import yaml
import argparse
import time
import csv
from collections import defaultdict

def excute_cmd(cmd):
    subprocess.call(cmd, shell=True)

def get_analize_ret(rpm_diff_detail_file, rpmdif_dict):
    total_pkg_cnt = 0
    diff_pkg_cnt = 0
    same_pkg_cnt = 0
    with open(rpm_diff_detail_file, 'r') as f:
        content = f.read().splitlines()
        count = 0
        pkg_ful_path = ''
        same = True
        for line in content:
            if line.endswith('.src.rpm'):
                pkg_ful_path = line
            elif '5' in line[:11] or 'added' in line[:11] or 'removed' in line[:11]:
                same = False
            if len(line) == 0 or line == content[-1]:
                rpmdif_dict[pkg_ful_path] = same
                same = True
    total_pkg_cnt = len(rpmdif_dict)
    same_pkg_cnt = 0
    diff_pkg_cnt = 0
    for pkg in rpmdif_dict.keys():
        if rpmdif_dict[pkg]:
            same_pkg_cnt += 1
        else:
            diff_pkg_cnt += 1
    return total_pkg_cnt, same_pkg_cnt, diff_pkg_cnt

def get_rpmdiff(rpmdiff, dif_detail_file):
    # 通过配置文件获取所有待diff的package的列表
    excute_cmd('test -f {0} && rm -f {0}'.format(dif_detail_file))
    for pkg in rpmdiff.keys():
        base_pkg_path = rpmdiff[pkg][1]
        cmp_pkg_path = rpmdiff[pkg][3]

        if not os.path.exists(base_pkg_path):
            print('Package {} is not exist'.format(base_pkg_path))
            continue
        if not os.path.exists(cmp_pkg_path):
            print('Package {} is not exist'.format(cmp_pkg_path))
            continue
        excute_cmd('echo "{0}" >> {1}'.format(rpmdiff[pkg][0], dif_detail_file))
        excute_cmd('rpmdiff {0} {1} >> {2}'.format(base_pkg_path, cmp_pkg_path, dif_detail_file))
        excute_cmd('echo " " >> {}'.format(dif_detail_file))
        print("RPM diff exe:{}".format(pkg))
    print('Finish rpmdiff.txt')
    return 

def get_rpm_name_in_dir(rpmdir):
    rpms = {}
    for root, dirs, files in os.walk(rpmdir):
        if not files:
            continue
        else:
            for f in files:
                if f[-8:] != '.src.rpm':
                    continue
                nameversion = f.rsplit('-', 2)
                if len(nameversion) < 3:
                    continue
                rpmname = nameversion[0]
                version = nameversion[1]
                rpmkey = rpmname + '-' + version
                filepath = os.path.join(root, f)
                rpms[rpmkey] = [rpmname, version, f, filepath]
    return rpms

def write_statistic_file(sfile,totalb,totalc,totals,csame,cdiff,start,end,base,compared):
    with open(sfile, 'w') as f:
        f.write("\n{}  VS  {}\n".format(base, compared))
        f.write("\nAnalize Start Time: {}\n".format(start))
        f.write("\nTotal RPMs in donated OS: {}\n".format(totalb))
        f.write("Total RPMs in referred OS: {}\n".format(totalc))
        f.write("Amount of SRPMs with the same name and version: {}\n".format(totals))
        f.write("Amount of SRPMs with differnt content even the name and version are the same : {}\n".format(cdiff))
        f.write("Amount of SRPMs the same: {}\n".format(csame))
        f.write("\nAnalize End Time: {}\n\n".format(end))

    return

def write_csv_file(dict_base, dict_compared, csv_file, rpm_diff_dict):
    with open(csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Pkg_Name","Donamted OS","Referred OS","name and version are the same", "the same"])
        lines = []
        pkgs = []
        for base in dict_base.keys():
            pkgname = dict_base[base][0]
            pkg_b_ver = dict_base[base][1]
            pkg_c_ver = "NA"
            b_c_same_name_vers = "NA" 
            content_modified = "NA"
            content_same =  True
            for compare in dict_compared.keys():
                if pkgname != dict_compared[compare][0]:
                    continue
                pkg_c_ver = dict_compared[compare][1]
                if pkg_b_ver != pkg_c_ver:
                    b_c_same_name_vers = str(False)
                    continue
                b_c_same_name_vers = str(True)
                content_modified = str(rpm_diff_dict[dict_base[base][2]])
                break
            line = [pkgname, pkg_b_ver, pkg_c_ver, b_c_same_name_vers, content_modified]
            lines.append(line)
            pkgs.append(pkgname)
        for comp in dict_compared.keys():
            pkgname = dict_compared[comp][0]
            if pkgname in pkgs:
                continue
            pkg_c_ver = dict_compared[comp][1]
            pkg_b_ver = "NA"
            b_c_same_name_vers = "NA"
            content_modified = "NA"
            content_same = True
            for base in dict_base.keys():
                if pkgname != dict_base[base][0]:
                    continue
                pkg_b_ver = dict_base[base][1]
                if pkg_b_ver != pkg_c_ver:
                    b_c_same_name_vers = str(False)
                    continue
                b_c_same_name_vers = str(True)
                content_modified = str(rpm_diff_dict[dict_base[base][2]])
                break
            
            line = [pkgname, pkg_b_ver, pkg_c_ver, b_c_same_name_vers, content_modified]
            lines.append(line)

        for li in lines:
            writer.writerow(li)
        
    return


def main(baseos, compared):
    if not os.path.exists(baseos):
        print("The First Directory Given here is not exist.")
        return 
    if not os.path.exists(compared):
        print("The Second Directory Given here is not exist.")
        return 
    

    rpms_paths = {}
    base_rpms = get_rpm_name_in_dir(baseos)
    comp_rpms = get_rpm_name_in_dir(compared)
    
    for base in base_rpms.keys():
        if base not in comp_rpms.keys():
            continue
        rpms_paths[base] = [base_rpms[base][2], base_rpms[base][3], comp_rpms[base][2], comp_rpms[base][3]]
    if len(rpms_paths) == 0:
        print("There is No SRpm in the first directory given here.")
        return
    starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())   
    timetamp = str(int(time.time()))
    retdir = 'result/'+timetamp
    excute_cmd('mkdir -p {}'.format(retdir))

    diff_detail_file = retdir + '/rpmdiff_detail.txt'

    get_rpmdiff(rpms_paths, diff_detail_file)

    same_name_versioin_pkg_cnt = 0
    diff_content_pkg_cnt = 0
    same_content_pkg_cnt = 0
    rpm_diff_dict = defaultdict(str)
    same_name_versioin_pkg_cnt, same_content_pkg_cnt, diff_content_pkg_cnt =  get_analize_ret(diff_detail_file, rpm_diff_dict)

    csvfile = retdir + '/rpm_name_version_diff.csv'
    write_csv_file(base_rpms, comp_rpms, csvfile, rpm_diff_dict)

    statistic_file = retdir + '/statistic.txt'
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    write_statistic_file(statistic_file, len(base_rpms), len(comp_rpms), same_name_versioin_pkg_cnt, same_content_pkg_cnt, diff_content_pkg_cnt, starttime, endtime, baseos, compared)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A tool compare the rpm packages with rpmdiff tool.')
    parser.add_argument('-b', '--base',help='Base version need to be compared: euler21.09, centos8.0, centos8.1, centos8.2, centos8.3, centos8.4', required = True)
    parser.add_argument('-c', '--compared',help='Compared version need to be selected: euler21.09, centos8.0, centos8.1, centos8.2, centos8.3, centos8.4', required = True)
    args = parser.parse_args()
    base = args.base
    compared = args.compared

    main(base, compared)
