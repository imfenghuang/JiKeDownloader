# coding=utf-8
import requests, json, re, os, sys, time
from urllib.parse import urlparse
from contextlib import closing
from bs4 import BeautifulSoup
from ffmpy import FFmpeg

class JiKeDownloader(object):
    def __init__(self):
        self.headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }

    def hello(self):
        print('*' * 60)
        print('\t\t即刻视频下载')
        print('\t作者:fenghuang(https://github.com/imfenghuang)')
        print('*' * 60)
        self.run()

    def run(self):
        self.share_url = input('请输入分享链接：')
        #self.share_url = 'https://m.okjike.com/originalPosts/5c4d6e0b4e12980010692d31?username=53095E59-8ADB-4EE7-BED1-37B6F2F458FF&share_distinct_id=168ae1ca463197-0b8d10da4c4d01-481f3700-1764000-168ae1ca464bc2&share_depth=1' 
       
        if not self.share_url:
            print("请重新输入分享链接") 
            return jk.hello()

        self.parseTitle(self.share_url)
        
    def parseTitle(self,url):
        ret = requests.get(url, headers=self.headers)
        bf = BeautifulSoup(ret.text, 'lxml')
      
        if not (bf.title.string):
            print("解析title错误，请重试")
            return jk.hello()

        self.title = bf.title.string

        self.downLoader(url)

    def downLoader(self,url):
        url_parse = urlparse(url)
        url_id = url_parse.path.split('/')[2];
        m3u8_url = "https://app.jike.ruguoapp.com/1.0/mediaMeta/play?type=ORIGINAL_POST&id="+url_id
        ret = requests.get(m3u8_url, headers=self.headers)
        bf = BeautifulSoup(ret.text, 'lxml')
        json_url = json.loads(bf.p.string)
        
        if not json_url['url']:
            print("解析视频链接错误，请重试")
            return jk.hello()

        ff = FFmpeg(
            inputs={json_url['url'] : None},
            outputs={self.title+'.mp4': None}
        ) 

        ff.run()
   
if __name__ == '__main__':
    jk = JiKeDownloader()
    jk.hello()
