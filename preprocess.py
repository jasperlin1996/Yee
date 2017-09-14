#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import pdb
import re
import jieba
# from QSearchPreprocess import QSearch


def preprocess(out_filename):
  out_f = open(out_filename, 'a')
  non_cht_pat = u'[^\u4e00-\u9fff]'
  corpus_dir = "pre_subtitle/pre_subtitle_no_TC/"
  for _, dirs, corpus_files in os.walk(corpus_dir):
    for dir in dirs:
      print(dir)
      for _,_,files in os.walk(corpus_dir+'/'+dir):
        for fn in files:
          if fn[0] == '.':
            continue
          print("Start %s" % fn)
          f = open(corpus_dir+'/'+dir+'/'+fn, 'r')
          '''
          all_line = f.read()
          all_line = re.sub(non_cht_pat, '', all_line)
          all_line.replace('\t', '').replace('\r\n', '\n')
          words = QSearch(all_line)
          out_f.write(words)
          '''
          for line in f:
            line = re.sub(non_cht_pat, '', line)
            line.replace('\t', '').replace('\r\n', '\n')
            # word segmentation with jieba.
            # words = QSearch(line)
            words = list(jieba.cut(line))
            #words = [w for w in words if w != ' ']
            # write to file.
            out_f.write('%s\n' % ' '.join(words))
          
          print("Done with " + fn)    

if __name__ == '__main__':
  jieba.dt.cache_file = 'jieba.cache.new'
  preprocess('corpus.txt')
