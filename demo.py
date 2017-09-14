# -*- coding: utf-8 -*-
import os
import sys
import re

import jieba
import numpy as np


dim = 0
word_vecs= {}
word_vecs_file = input()
with open(word_vecs_file) as wvf:
    for line in wvf:
        tokens = line.strip().split()

        if len(tokens) == 2:
            dim = int(tokens[1])
            continue
        word = tokens[0]
        vec = np.array([ float(t) for t in tokens[1:] ])
        word_vecs[word] = vec

filename = 'Ans_' + word_vecs_file
storeAns = open(filename,'w')
#codes on mine
count = 0 #先十個就好ouo
f = open('AIFirstProblem.txt','r')
for i in f:
    if count < 1:
         count += 1
         continue
    if count >= 501:
         break
    questionNum = i.split(',')[0]
    questionSeq = i.split(',')[1]
    questionAns = i.split(',')[2]

#GOGO
    #問題們
    dialogue = []
    seq = questionSeq.split(':')
    cc = 0
    dd = ''
    #處理一下格式
    for throw in seq:
        cc += 1
        if ord('A') <= ord(throw[-1]) <= ord('Z'):
            throw = throw[0:-1]
        throw = ' '.join(throw.split())
        if cc >= 2:
            dialogue.append(throw)
            dd += ' '
            dd += throw
    print(dialogue)
    #答案們
    answers = []
    ans = questionAns.split(':')
    cc = 0
    #再處理一下格式
    for throw in ans:
        cc += 1
        if ord('A') <= ord(throw[-1]) <= ord('Z'):
            throw = throw[0:-1]
        throw = ' '.join(throw.split())
        if cc >= 2:
            answers.append(throw)
    print(answers)

    #開薛啦各位
    emb_cnt = 0
    avg_dlg_emb = np.zeros((dim,))
    # jieba.cut 先幫 dialogue 做分詞
    # 對於有在 word_vecs 裡面的詞才取出來
    # 最後詞向量加總取平均，作為句子的向量表示
    for word in jieba.cut(dd):
        if word in word_vecs:
            avg_dlg_emb += word_vecs[word]
            emb_cnt += 1
    avg_dlg_emb /= emb_cnt
    
    emb_cnt = 0
    max_idx = -1
    max_sim = -10
    # 在六個回答中，每個問句都取詞向量平均作為向量表示
    # 我們選出與 dialogue 句子向量表示 cosine similarity 最高的短句
    for idx,ans in enumerate(answers):
        avg_ans_emb = np.zeros((dim,))
        for word in jieba.cut(ans):
            if word in word_vecs:
                avg_ans_emb += word_vecs[word]
                emb_cnt += 1
        sim = np.dot(avg_dlg_emb, avg_ans_emb) / np.linalg.norm(avg_dlg_emb) / np.linalg.norm(avg_ans_emb)
        print("Ans#%d: %f" % (idx, sim))
        if sim > max_sim:
            max_idx = idx
            max_sim = sim
    print("Answer:%d" % max_idx)
    storeAns.write(str(count))
    storeAns.write(',')
    storeAns.write(str(max_idx))
    storeAns.write('\n')
    count += 1
storeAns.close()
