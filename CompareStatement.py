# -*- coding: utf-8 -*-
import jieba
import numpy as np # 安裝numpy
def load_file(dim,word_vecs):
    dim = 0
    word_vecs= {}
    # 開啟詞向量檔案
    with open('my.cbow.200d.txt') as f:
      for line in f:
      # 假設我們的詞向量有300維
      # 由word以及向量中的元素共301個
      # 以空格分隔組成詞向量檔案中一行
        tokens = line.strip().split()

      # 第一行是兩個整數，分別代表有幾個詞向量，以及詞向量維度
        if len(tokens) == 2:
          dim = int(tokens[1])
          continue
    
        word = tokens[0] 
        vec = np.array([ float(t) for t in tokens[1:] ])
        word_vecs[word] = vec
    return dim, word_vecs
# 之後可以從word_vecs這個dict中取得詞向量
def compare(dim, word_vecs, dialogue, answers):
  print(dialogue)
  print(answers)
  emb_cnt = 0
  avg_dlg_emb = np.zeros((dim,))
# jieba.cut 會把dialogue作分詞
# 對於有在word_vecs裡面的詞我們才把它取出
# 最後詞向量加總取平均，作為句子的向量表示
  for word in jieba.cut(dialogue):
    if word in word_vecs:
      avg_dlg_emb += word_vecs[word]
      emb_cnt += 1
  avg_dlg_emb /= emb_cnt

  emb_cnt = 0
  max_idx = -1
  max_sim = -10
# 在六個回答中，每個答句都取詞向量平均作為向量表示
# 我們選出與dialogue句子向量表示cosine similarity最高的短句
  for idx,ans in enumerate(answers):
    avg_ans_emb = np.zeros((dim,))
    for word in jieba.cut(ans):
      if word in word_vecs:
        avg_ans_emb += word_vecs[word]
        emb_cnt += 1
    sim = np.dot(avg_dlg_emb, avg_ans_emb) / np.linalg.norm(avg_dlg_emb) / np.linalg.norm(avg_ans_emb)
    # print("Ans#%d: %f" % (idx, sim))
    if sim > max_sim:
      max_idx = idx
      max_sim = sim
  # print("Answer:%d" % max_idx)
  # return max_idx
  print(answers[max_idx])
  return max_idx, answers[max_idx]
