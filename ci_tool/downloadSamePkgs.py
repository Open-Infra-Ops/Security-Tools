import os, sys
import yaml
  
same_pkg_urls = open(r'same_pkg_urls.txt','w')

def get_same_pkg_name(same_pkg_file, urls_path, urls):
    with open(same_pkg_file, 'r') as f:
        pkgs = yaml.load(f.read(), Loader=yaml.Loader)['same_package_name']
    urls_file = open(urls_path,'r') 
    n = 0
    for url in urls_file.readlines():
        if n > 5:
            break
        n = n + 1
#        print(url)
        idx = url.rfind('/')
        pkg_in_url = url[idx+1:]
        pkg_in_url = pkg_in_url.strip()
        print(pkg_in_url)
        if pkg_in_url in pkgs:
            print("In pkgs:******"+pkg_in_url)
            urls.append(url)
    
    return
        

def download(valid_urls):
    for url in valid_urls:
        print(url)
        res = os.system('wget {}'.format(url))
        if res != 0:
            print('Falied to wget {}'.format(url))
            

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Param Error, eg: python3 samepkg_yaml allpkgurls")
        os.sysexit(-1)
    samepkg = sys.argv[1]
    url_file = sys.argv[2]
    valid_urls = []
    get_same_pkg_name(samepkg, url_file, valid_urls)
    download(valid_urls) 


