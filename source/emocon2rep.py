# -*- coding: utf-8 -*-
"""emocon2rep_small.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13VcIRc-keDH6rNMd8I2_MQvTR1P7KtXk

# 目的

顔文字は以下の9個の感情に分類できる。[1]
joy, like, calm, sorrow, dislike, fear, excitement, surprise, shame
顔文字をこれらの感情に分類する。

# 変換の流れ

顔文字 -1-> 正規表現 -2-> タグ（英語）-3-> 代表語
    1,2: 辞書   3: word2vec

# 使用したデータ

emoticon / Kaomoji Dataset
https://github.com/ekohrt/emoticon_kaomoji_dataset/tree/main

word2vec pretrained embeddings
https://wikipedia2vec.github.io/wikipedia2vec/pretrained/
"""

import json
import gensim
from gensim.models import KeyedVectors
from gensim.test.utils import datapath
import numpy as np

# JSONファイルから絵文字データを読み込む
emotion_dict_path = './data/emoticon_dict.json'
with open(emotion_dict_path, "r", encoding="utf-8") as f:
    emoticon_dict = json.load(f)
# original_tagsの内容を全てまとめて、重複を排除
corpus = list({tag for data in emoticon_dict.values() for tag in data["original_tags"]})

# ベクトルのパス
vec_path = './data/vec.txt'

# w2v
model = KeyedVectors.load_word2vec_format(vec_path, binary=False)

## 代表要素を抽出したw2vの作成 : model_re

# [1] file:///C:/ehime/competition/jp_analy/article/E6-2.pdf
# excitement, surprise, shameは0, 顔文字としての影響を受けにくい
representatives = ['joy','like','calm','sorrow','dislike','fear','excitement','surprise','shame']

# shame判定ばっかりになってしまう --> angerが欲しい & neutral の追加
representatives = ['joy','like','calm','sorrow','dislike','fear','excitement','surprise','anger', 'neutral']

# 代表要素の単語をkey、そのw2vベクトルをvalueとする辞書の作成
filtered_vectors = {word: model[word] for word in representatives}

# (  KeyedVectorsで作成したインスタンスは、.key_to_indexでキー検索、.vector_sizeでサイズ )
# model_reの初期化
model_re = KeyedVectors(vector_size=model.vector_size)
model_re.add_vectors(list(filtered_vectors.keys()), list(filtered_vectors.values()))

# function
#
# 顔文字 --> 正規表現 --> タグ（複数）のリスト
def get_tags_from_emoticon(emoticon):
    if emoticon in emoticon_dict:
        original_tags = emoticon_dict[emoticon].get("original_tags", [])
        new_tags = emoticon_dict[emoticon].get("new_tags", [])
        return original_tags + new_tags
    else:
        return []

def find_most_similar(input_word):
    # 小文字に統一、空白削除
    input_word = input_word.lower().strip()

    if input_word not in corpus:
        return  -1, 0.0 # corpusに存在しない場合

    if input_word not in model:
        return  -1, 0.0 # w2vに存在しない場合

    # 入力単語のベクトル
    input_vector = model[input_word]

    max_similarity = -1
    most_similar_word_idx = 0
    for idx, rep_word in enumerate(representatives): # 代表要素を一つずつ確認
        if rep_word in model.key_to_index:
            rep_vector = model[rep_word]
            similarity = np.dot(input_vector, rep_vector) / (np.linalg.norm(input_vector) * np.linalg.norm(rep_vector))
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_word_idx = idx

    return most_similar_word_idx, max_similarity

## main関数的
#  これを使用

def emocon2rep(emoji_input):
    tags = get_tags_from_emoticon(emoji_input)
    if not tags: # タグのリストが空なら偽
        return False

    # タグが複数ある場合、それぞれの代表要素が異なる場合のための処理
    #     もっともコサイン類似度の高いときの代表要素に決定
    most_similar_word_idx = 0
    most_similar_word_val = -1
    for idx, tag in enumerate(tags):
        result = find_most_similar(tag)
        if result[0] is not False:  # 結果が有効な場合のみ処理
            similar_word_idx, similarity_val = result
            if similarity_val > most_similar_word_val:
                most_similar_word_idx = similar_word_idx
                most_similar_word_val = similarity_val
    return representatives[most_similar_word_idx]

text = '(^_-)-☆'
print("Tags:", get_tags_from_emoticon(text))
tags = get_tags_from_emoticon(text)

for tag in tags:
    print(f"Tag: {tag}")
    result = find_most_similar(tag)
    print(f"Result for --> {tag}: {result}")

print("Final result:", emocon2rep(text))

text = '(^_-)-☆'
print(get_tags_from_emoticon(text))
emocon2rep(text)

text = '( ;∀;)'
print(get_tags_from_emoticon(text))
emocon2rep(text)

text = 'ლ(ಠ益ಠლ'
emocon2rep(text)

# 以下では、コーパスの顔文字で確認

unique = list(set(emoticon_dict.keys()))

for i in range(1, 300, 1):
    print(unique[i], ' --> ' ,emocon2rep(unique[i]))

    #print(emocon2rep(unique[i]))

#print(unique)
'''
for i in range(10):
    print(emocon2rep(unique[i]))
'''