# encoding=utf-8
import jieba
import jieba.analyse

jieba.set_dictionary('data/dict.txt.big')
jieba.load_userdict("data/userdict.txt")
jieba.analyse.set_stop_words('data/stop_words.txt')


print("請輸入一句話")


while True:
    try:
        sentence = input()
        a = jieba.cut(sentence, cut_all=False, HMM=True)
        print("HMM打開："+"/".join(a))

        b = jieba.cut(sentence, cut_all=False, HMM=False)
        print("HMM關閉："+"/".join(b))

        c = jieba.cut_for_search(sentence)
        print("搜索引擎模式："+"/".join(c))

        d = jieba.analyse.extract_tags(sentence)  # 詞彙的順序不曉得為啥會亂掉
        print("開啟停用詞："+"/".join(d))

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
