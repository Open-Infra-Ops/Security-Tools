# -*- encoding=utf-8 -*-
import os
import subprocess
import sys
import yaml


def load_yaml(path):
    try:
        with open(path, 'r') as fp:
            content = yaml.load(fp.read(), Loader=yaml.Loader)["same_package_name"]
            return content
    except FileNotFoundError:
        print('Invalid yaml path: {}'.format(path))
        sys.exit(1)
    except yaml.MarkedYAMLError as e:
        print(e)
        sys.exit(1)


def excute_cmd(cmd):
    subprocess.call(cmd, shell=True)


def gene_tmp_diff_file(dir1,dir2,pkgnamefile):
    # 通过配置文件获取所有待diff的package的列表
    tmp_diff_file = './tmp/rpmdiff.txt'
    pkgs_list = load_yaml(pkgnamefile)
    excute_cmd('test -f {0} && rm -f {0}'.format(tmp_diff_file))
    for pkg in pkgs_list:
        ali_pkg_path = os.path.join(dir1, pkg)
        centos_pkg_path = os.path.join(dir2, pkg)
        if not os.path.exists(ali_pkg_path):
            print('Package {} is not exist'.format(ali_pkg_path))
            continue
        if not os.path.exists(centos_pkg_path):
            print('Package {} is not exist'.format(centos_pkg_path))
            continue
        excute_cmd('echo "{}" >> ./tmp/rpmdiff.txt'.format(pkg))
        excute_cmd('rpmdiff {0} {1} >> ./tmp/rpmdiff.txt'.format(ali_pkg_path, centos_pkg_path))
        excute_cmd('echo " " >> ./tmp/rpmdiff.txt')
        print("RPM diff exe:{}".format(pkg))
    print('生成/tmp/rpmdiff.txt')
    return tmp_diff_file


def main(dir1,dir2,pkgnamefile):
    # 处理临时diff文件，将各个包对比的结果写入result.txt
    tmpfile = gene_tmp_diff_file(dir1,dir2,pkgnamefile)
    with open(tmpfile, 'r') as f:
        content = f.read().splitlines()
    with open('result.txt', 'a+') as f:
        count = 0
        for line in content:
            if '5' in line[:11]:
                count += 1
            if len(line) == 0 or line == content[-1]:
                if count == 0:
                    f.write(': same\n')
                else:
                    f.write(': different\n')
            if line.endswith('.rpm'):
                count = 0
                f.write('{}'.format(line))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Param error.eg: python find_***.py dir1(centosdir) dir2 pkgfilepath.")
        sys.exit(2)
    dir1 = sys.argv[1]
    dir2 = sys.argv[2]
    pkgfile = sys.argv[3]
    main(dir1,dir2,pkgfile)
