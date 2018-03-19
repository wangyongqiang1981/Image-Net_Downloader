#!/usr/bin/env python3
from urllib.request import urlopen,urlretrieve
from urllib.error import HTTPError,URLError
import re,os,logging

class ImageNet_Downloader(object):
    
    synset_urls = ["http://image-net.org/api/text/imagenet.synset.geturls?wnid=n01979874"]
    
    def __init__(self, target=synset_urls):
        super(ImageNet_Downloader, self).__init__()
        self.task_list = target
        self.re_synset = re.compile('n[0-9]{8}$')
        self.logger = logging.getLogger('ImageNet_Downloader_Logger')
        self.logger.setLevel(logging.INFO)

    def _mkpath(self, url_index):
        if not os.path.isdir('data'):
            os.mkdir('data')
        name = os.path.join('data', self.re_synset.findall(url_index)[0])
        if not os.path.isdir(name):
            os.mkdir(name)
        return name

    def _download_one_synset(self, url_index):
        # mkpath
        path = self._mkpath(url_index)
        # logging
        self.logger.addHandler(logging.FileHandler(os.path.join(path, 'readme.log')))
        # download
        urls = set(re.compile('http.*.jpg').findall(urlopen(url_index).read().decode('ascii')))
        urls_finished = set()
        urls_failed = set()
        #print("\n".join(urls)
        cnt_all = len(urls)
        self.logger.info("total: {}".format(cnt_all))
        cnt_ok = 0
        cnt_err = 0
        while len(urls):
            url = urls.pop()
            try: 
                im = urlopen(url)        
                with open(os.path.join(path,"{:04}.jpg".format(cnt_ok)), 'bw') as f:
                    f.write(im.read())
                urls_finished.add(url)
                cnt_ok += 1
                self.logger.info("{:04}.jpg {}".format(cnt_ok,url))
            except (HTTPError,URLError):
                urls_failed.add(url)
                cnt_err += 1
                self.logger.info("Err {:04} {}".format(cnt_err,url))
            finally:                    
                print("{}/{}".format(cnt_ok+cnt_err,cnt_all))
        self.logger.info("total: {}\nsuccess: {}\nfailed: {}".format(cnt_all,cnt_ok,cnt_err))
        self.logger.removeHandler(self.logger.handlers[0])

    def download_all(self, index_list):
        for i in index_list:
            self._download_one_synset(i)
            
    def __call__(self):
        self.download_all(self.task_list)
        
if __name__=='__main__':
    a = ImageNet_Downloader()
    a()
