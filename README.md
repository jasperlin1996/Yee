YEEEE backup

1. Use "python3.5 Preprocess.py" to generate corpus.txt

2. To train a word2vec file, use "./word2vec/trunk/word2vec -train corpus.txt -output my.cbow.200d.txt -size 200 - window 5 -sample 1e-4 -negative 10 -hs 0 -cbow 1 -iter 15 -threads 8 -min-count 5".
//One line for a phrase with its vector.

3. To test the word2vec model, use "python3.5 demo.py" and type the model's file name which you want to use. For more details, read the codes XD.

** RNN and Pytorch-seq2seq:

RNN: git clone https://github.com/willywsm1013/RNN-language-model.git

Py-seq2seq: git clone https://github.com/willywsm1013/RNN-language-model.git
