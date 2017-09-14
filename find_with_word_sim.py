#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import argparse
import pdb

import jieba
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("vec_fname", type=str, help="filename of word vec")
args = parser.parse_args()

dim = 0

def read_word_vectors(filename):
  global dim
  word_dict = []
  word_vectors = {}
  word_id = 0

  with open(filename, 'r') as f:
    for line in f:
      tokens = line.split()
      if len(tokens) == 2:
        num = int(tokens[0])
        dim = int(tokens[1])
        norm_word_vectors = np.zeros((num, dim))
        continue
      word = tokens[0]
      if word == "</s>": word = u"<unk>"

      vec = np.array([ float(t) for t in tokens[1:] ])
      word_vectors[ word ] = vec
      norm_word_vectors[ word_id,: ] = vec / np.linalg.norm(vec)
      word_dict.append(word)
      word_id += 1
  return word_vectors, norm_word_vectors, word_dict

word_vectors, norm_word_vectors, word_dict = read_word_vectors(args.vec_fname)
word2id = {}
for i,w in enumerate(word_dict):
  word2id[w] = i

def get_emb(w):
  if w not in word_vectors:
    return word_vectors[u'<unk>']
  return word_vectors[w]

dialogues = []
options   = []
answers   = []
with open('sample_test_data.txt') as f:
  for line in f:
    if line == '\n':
      continue
    tokens = line.strip().split(',')
    if tokens[1] == 'dialogue':
      continue
    dialogues.append( tokens[1].split() )
    options.append( tokens[2].split('\t') )
    answers.append( int(tokens[3]) )

correct = 0
for dlg,opt,ans in zip(dialogues, options, answers):
  dlg_embs = []
  emb_cnt = 0
  avg_dlg_emb = np.zeros((dim,))
  for turn in dlg:
    turn_embs = []
    for word in jieba.cut(turn):
      if word in word_dict:
        turn_embs.append( get_emb(word) )
        avg_dlg_emb += get_emb(word)
        emb_cnt += 1
    if len(turn_embs) == 0:
      dlg_embs.append(avg_dlg_emb)
    else:
      dlg_embs.append(np.mean(turn_embs,axis=0))

  opt_embs = []
  for sent in opt:
    sent_embs = []
    for word in jieba.cut(sent):
      if word in word_dict:
        sent_embs.append( get_emb(word) )
    opt_embs.append(sent_embs)

  max_idx = -1
  max_sim = -100
  for idx,opt_emb in enumerate(opt_embs):
    if len(opt_emb) == 0:
      continue
    avg_emb = np.mean(opt_emb, axis=0)
    sim = 0.0
    for dlg_emb in dlg_embs:
      sim += np.dot(dlg_emb, avg_emb) / np.linalg.norm(dlg_emb) / np.linalg.norm(avg_emb)
    if sim > max_sim:
      max_idx = idx
      max_sim = sim
  
  if max_idx == ans:
    correct += 1

f = open('cases_test.txt','a')
f.write(str(float(correct)/len(dialogues)))
f.write('\n')
f.close()
print(float(correct)/len(dialogues))
