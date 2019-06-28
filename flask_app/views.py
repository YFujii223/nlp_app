import os
import subprocess
import traceback
import urllib.request as req
import zipfile
import os.path
import pickle
import joblib
import MeCab
from gensim import models

# Mecabの初期化
import MeCab

mecab = MeCab.Tagger()
mecab.parse("")

# 保存したDoc2Vec学習モデルを読み込み --- (*7)
import gensim
from gensim import models

model = models.Doc2Vec.load('/Users/fujii.yuki/.ghq/src/github.com/projects/nlp_app/flask_app/aozora.model')

# 分類用のZipファイルを開き、中の文書を取得する --- (*8)
def read_book(url, zipname):
    if not os.path.exists(zipname):
        req.urlretrieve(url, zipname)

    with zipfile.ZipFile(zipname, "r") as zf:
        for filename in zf.namelist():
            with zf.open(filename, "r") as f:
                return f.read().decode("shift-jis")


# 引数のテキストを分かち書きして配列にする
def split_words(text):
    node = mecab.parseToNode(text)
    wakati_words = []
    while node is not None:
        hinshi = node.feature.split(",")[0]
        if hinshi in ["名詞"]:
            wakati_words.append(node.surface)
        elif hinshi in ["動詞", "形容詞"]:
            wakati_words.append(node.feature.split(",")[6])
        node = node.next
    return wakati_words


# 引数のタイトル、URLの作品を分類する --- (*9)
def similar(title, url):
    zipname = url.split("/")[-1]
    words = read_book(url, zipname)
    wakati_words = split_words(words)
    vector = model.infer_vector(wakati_words)
    #print("--- 「" + title + '」と似た作品は? ---')
    return model.docvecs.most_similar([vector], topn=5)
    # print("")


# # 各作家の作品を１つずつ分類 --- (*10)
# similar("宮沢 賢治:よだかの星",
#         "https://www.aozora.gr.jp/cards/000081/files/473_ruby_467.zip")
#
# similar("芥川 龍之介:犬と笛",
#         "https://www.aozora.gr.jp/cards/000879/files/56_ruby_845.zip")
#
# similar("太宰 治:純真",
#         "https://www.aozora.gr.jp/cards/000035/files/46599_ruby_24668.zip")
#
# similar("夏目 漱石:一夜",
#         "https://www.aozora.gr.jp/cards/000148/files/1086_ruby_5742.zip")

from flask import Flask, request, redirect, url_for, render_template, flash, session
from flask_app import app
import os
import subprocess
import traceback
import urllib.request as req
import zipfile
import os.path
import pickle
import joblib
import MeCab
from gensim import models

@app.route('/')
def show_entries():
    return render_template('entries/index.html')

@app.route('/outcome', methods = ['GET', 'POST'])
def outcome():
    # model = models.Doc2Vec.load('/Users/fujii.yuki/.ghq/src/github.com/projects/nlp_app/flask_app/aozora.model')
    title = request.form['title']
    url = request.form['url']
    n_outcome = similar(title, url)
    return render_template('outcome.html', title=title, n_outcome=n_outcome)
