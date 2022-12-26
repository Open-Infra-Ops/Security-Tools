
import os, sys
import yaml


def download(version, urls_file, failname):
    download_fail = open(failname,'w')
    with open(urls_file, 'r') as f:
        valid_urls = yaml.load(f.read(), Loader=yaml.Loader)[version]
    for url in valid_urls:
        print(url)
        res = os.system('wget -P {0} {1}'.format(version, url))
        if res != 0:
            print('Falied to wget {}'.format(url))
            download_fail.write(url)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Param Error, eg: python3 version allpkgurls, version:ceontos8.2 centos8.3 euler21.09 ...")
        sys.exit(2)
    version = sys.argv[1]
    valid_urls = sys.argv[2]
    res = os.system('mkdir -p {0} '.format(version))
    if res != 0:
        sys.exit(2)
    print("Start to down load OS of {}.".format(version))
    failname = version+"_download_fail.txt"

    download(version, valid_urls, failname)
