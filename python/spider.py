#!/usr/bin/env python

import json
import itertools
import urllib
import requests
import os
import shutil
import re
import sys
import argparse
import time

class Coder(object):

  def __init__(self):
    self.InitCode()
    self.ToUnicode()

  def InitCode(self):
    self.str_dir_ = { '_z2C$q': ':', '_z&e3B': '.', 'AzdH3F': '/' }
    self.char_dir_ = { 
      'w': 'a', 'k': 'b', 'v': 'c', '1': 'd', 'j': 'e', 'u': 'f', '2': 'g', 'i': 'h',
      't': 'i', '3': 'j', 'h': 'k', 's': 'l', '4': 'm', 'g': 'n', '5': 'o', 'r': 'p',
      'q': 'q', '6': 'r', 'f': 's', 'p': 't', '7': 'u', 'e': 'v', 'o': 'w', '8': '1', 
      'd': '2', 'n': '3', '9': '4', 'c': '5', 'm': '6', '0': '7', 'b': '8', 'l': '9',
      'a': '0' }

  def ToUnicode(self):
    self.char_dir_ = { ord(key): ord(value) for key,value in self.char_dir_.items() }

  def Decode(self, url):
    # 先替换字符串
    for key, value in self.str_dir_.items():
      url = url.replace(key, value)
    # 再替换单个字符
    return url.translate(self.char_dir_)

class BaiduDownloader(object):

  def __init__(self):
    self.coder_ = Coder()
    self.InitRe()
    self.timeout_ = 3
    self.sleep_ = 2

  def InitRe(self):
    self.re_url_ = re.compile(r'"objURL":"(.*?)"')

  def GenUrls(self, word):
    word = urllib.parse.quote(word)
    url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
    urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    return urls

  def FindImgUrls(self, html):
    img_urls = [self.coder_.Decode(x) for x in self.re_url_.findall(html)]
    return img_urls

  def DownLoadImg(self, img_url, img_file):
    try:
      res = requests.get(img_url, timeout=self.timeout_)
      if str(res.status_code)[0] == "4":
        print(str(res.status_code), " --> ", img_url)
        return False
    except Exception as e:
      print("抛出异常：", img_url)
      print(e)
      return False

    with open(img_file, 'wb') as f:
      f.write(res.content)
    return True

  def DownloadAll(self, word, output_root):
    urls = self.GenUrls(word)
    img_id = 0
    for url in urls:
      print("开始请求 --> {}".format(url))
      html = requests.get(url, timeout=self.timeout_).content.decode('utf-8')
      img_urls = self.FindImgUrls(html)
      for img_url in img_urls:
        time.sleep(self.sleep_)
        img_name = "{:0>4d}.jpg".format(img_id)
        img_file = os.path.join(output_root, img_name)
        if self.DownLoadImg(img_url, img_file):
          img_id += 1
          print("已下载图片 --> {}".format(img_file))
      print("结束请求 --> {}".format(url))

def parse_args():

    description = "Download images form Baidu!"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("word", help="What we want to download")

    args = parser.parse_args()
    return args

def main():
  args = parse_args()
  word = args.word
  if len(word.strip().split()) != 1:
    print("输入关键词个数只能为1")
    sys.exit(1)
  print("您输入的关键词是 --> {}".format(word))
  output_root = "Image-{}".format(word)
  if os.path.exists(output_root):
    shutil.rmtree(output_root)
  os.mkdir(output_root)
  downloader = BaiduDownloader()
  downloader.DownloadAll(word, output_root)

if __name__ == "__main__":

  main()


