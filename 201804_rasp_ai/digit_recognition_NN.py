# coding: utf-8
# ch03ディレクトリに置く
import sys, os, time, subprocess, pickle
sys.path.append(os.pardir) # 親ディレクトリのファイルをインポートするための設定
import numpy as np
#from dataset.mnist import load_mnist
from common.functions import sigmoid, softmax
from PIL import Image

# 学習済みの重みパラメータを読み込む
def init_network():
    with open("sample_weight.pkl", 'rb') as f:
        network = pickle.load(f)
    return network

# 分類を行う
def predict(network, x):
    W1, W2, W3 = network['W1'], network['W2'], network['W3']
    b1, b2, b3 = network['b1'], network['b2'], network['b3']

    a1 = np.dot(x, W1) + b1
    z1 = sigmoid(a1)
    a2 = np.dot(z1, W2) + b2
    z2 = sigmoid(a2)
    a3 = np.dot(z2, W3) + b3
    y = softmax(a3)

    return y


network = init_network()
devnull = open('os.devnull', 'w')
ipaddr = subprocess.check_output(["hostname", "-I"]).decode("utf-8").strip()
commd = "http://"+ipaddr+":9000/?action=snapshot"

while True:

    time.sleep(3)

    # カメラの画像を取り込む
    subprocess.run(["wget", "-O", "photo.jpg", commd], stdout=devnull, stderr=subprocess.STDOUT)


#**********************************************************************
    # 画像の前処理
    # 白黒化（グレースケール化）
    img = Image.open("photo.jpg").convert('L')
    img.save('img.jpg')
    # 28x28に整形
    img28 = np.array(img.resize((28,28)))
    pil_img_gray = Image.fromarray(np.uint8(img28)).save('img28.jpg')

    # 二値化
    thresh = np.median(img28)
    if thresh > 127:
        img28 = 255 - img28

    x = np.zeros(img28.shape, img28.dtype)
    x[np.where(img28 > thresh)] = 255

    pil_img_gray = Image.fromarray(np.uint8(x)).save('result.jpg')

    x = np.ravel(x)/255
    # 入力値をテキストで出力
    for i in range(0, 28):
        for j in range(0, 28):
            print("{:01.0f}".format(x[28*i+j]), end=' ')
        print('')


#**********************************************************************

    # ニューラルネットワークで推測させる
    y = predict(network, x)

    # 推測結果を出力
    y_idx = np.argsort(y) #並び替え
    for i in range(10):
        print(y_idx[9-i], ":", round( y[y_idx[9-i]]*100, 2), "%" )
