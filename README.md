# kaomoji2vec

## 目的
顔文字は以下の9個の感情に分類できると示されている。[[1]](https://www.jstage.jst.go.jp/article/wii/4/0/4_27/_article/-char/ja/)

joy, like, calm, sorrow, dislike, fear, excitement, surprise, shame

本プログラムでは、顔文字をこれらの感情に分類する。

また、これをNLPタスクのデータの前処理に使用するなら、先の引用論文の以下も参考になる。

「「喜」，「好」，「安」，「哀」，「厭」，「怖」などの顔文字の影響を受けやすい軸と，「昂」，「驚」，「恥」などの顔文字の影響を受けにくい軸がある」

このことから、分類した感情がデータに与える影響を適切に設定することが考えられる。

## 使用方法

以下に示した２つのデータを利用する。
本プログラム内のパスに適切に設定する。


## 変換の流れ
顔文字 --> 正規表現 --> タグ（英語）--> 代表語 

## 使用したデータ
・emoticon / Kaomoji Dataset

https://github.com/ekohrt/emoticon_kaomoji_dataset/tree/main


・word2vec pretrained embeddings

https://wikipedia2vec.github.io/wikipedia2vec/pretrained/






