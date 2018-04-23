# 1. セットアップ

## 1.1. カメラモジュールの取付

**作業の前に**

このカメラは、静電気によって損傷するおそれがあります。グレーの静電気防止バッグからカメラを取り出す際は、地面に接地されている物体（ラジエーターや水道管など）に触れて静電気を放電してから、作業を始めてください。

<br>
コネクタの位置

<img src="image/rasp_camera.PNG" width="50%">

HDMIポート側が銀色、イーサネットポート側が青色になるように差し込む。

<img src="image/rasp-camera1.jpg" width="30%">

<br>

## 1.2. Raspberry Pi3とパソコンを接続する

- [USB-シリアルケーブルで接続する場合](connection_uart.md)

- [無線LANで接続する場合](connection_wirelessLAN.md)

<br>

## 1.3. raspi-configの設定

    sudo raspi-config

と打って設定画面に入り、以下の設定を行う。

- Network Options -> Wi-fi -> 無線LANのSSID/passphraseを設定
- Interfacing Options -> SSH -> (Would you line the SSH...) -> Yes
- Localisation Options -> Change Timezone -> Asia -> Tokyo

(カメラモジュールの有効化 )
- Interfacing Options -> Camera -> (Would you like the camera...) -> Yes  

その後、画面の指示通りrebootする。

<br>

# 2. カメラ画像の配信

## 2.1. ストリーミング配信プログラム(mjpg-streamer)のインストール

Pi Cameraがアクティブになっているか確認する。


    vcgencmd get_camera

正しく動いていれば`supported=1 detected=1`という結果が返ってくる。

- Raspbianのパッケージをアップデートする


    sudo apt-get update
    sudo apt-get upgrade




    | コマンド | 説明 |
    |:-------------:|:--------------|
    | sudo | 「スーパーユーザー（rootユーザー）」の権限が必要なコマンドを実行することができる。 |
    | apt-get | Debian系のディストリビューションのパッケージ管理システムであるAPTライブラリを利用してパッケージを操作・管理するコマンド。 |
    | git clone | gitはバージョン管理システム。既存のリポジトリの複製を作る。 |
    | cd | ディレクトリを移動する。 |
    | wget | 指定したURLのファイルをダウンロードする。 |
    | pip3 | pipはPythonのパッケージをインストール・管理するためのパッケージ管理システム |
    | python3 | pythonを実行する。 |




- ストリーミング配信プログラム(mjpg-streamer)をインストールする。


    sudo apt-get install -y libjpeg9-dev cmake
    sudo git clone https://github.com/jacksonliam/mjpg-streamer.git mjpg-streamer
    cd mjpg-streamer/mjpg-streamer-experimental
    sudo make
    cd
    sudo mv mjpg-streamer/mjpg-streamer-experimental /opt/mjpg-streamer

<br>

## 2.2. mjpg-streamer起動スクリプトの作成

- `nano start_stream.sh`と打ってnanoエディタを開き、下記の内容をコピーして保存終了する。

    #!/bin/bash

    if pgrep mjpg_streamer > /dev/null
    then
    echo "mjpg_streamer already running"
    else
    LD_LIBRARY_PATH=/opt/mjpg-streamer/ /opt/mjpg-streamer/mjpg_streamer -i "input_raspicam.so -fps 10 -q 50 -x 320 -y 240" -o "output_http.so -p 9000 -w /opt/mjpg-streamer/www" > /dev/null 2>&1&
    echo "mjpg_streamer started"
    fi

<table>
<tr>
<td>ファイルの保存</td><td>Ctrl+O</td>
</tr>
<tr>
<td>ファイルの終了</td><td>Ctrl+X</td>
</tr>
</table>

- スクリプトの保存終了後、`chmod 755 start_stream.sh`と打って実行権限を与えておく。

<br>

## 2.3. mjpg-streamerの動作確認

- 下記コマンドを実行し、mjpg-streamerを起動する。

    ./start_stream.sh

- （USB-シリアルケーブルで接続している場合）下記コマンドを実行し、ラズパイのIPアドレスを確認する。

    ip a

<img src="image/ip.PNG" width="60%">

- WEBブラウザでラズパイのIPアドレス、ポート9000番にアクセスすることでカメラからの配信画像を見ることができる。　例：http://192.168.xx.xx:9000  

<img src="image/Stream.PNG" width="60%">

<br>
- mjpg-streamerを終了させたいときは、psコマンドでプロセス番号を調べてkillコマンドで終了させる。

<img src="image/kill.PNG" width="50%">

<br>

# 3. MNIST文字認識の実装

## 3.1. 「ゼロから作るDeep Learning」のサンプルコードの入手


<img src="image/DeepLearning.jpg" width="20%">

    cd
    git clone https://github.com/oreilly-japan/deep-learning-from-scratch.git

<br>

## 3.2. カメラを使ったMNIST文字認識プログラムの実装

- 下記コマンドを実行し、mjpg-streamerを起動する。

    ./start_stream.sh

- WEBブラウザでラズパイのIPアドレス、ポート9000番にアクセスする。
　例：http://192.168.xx.xx:9000  


- ニューラルネットワークによる推論

    cd /home/pi/deep-learning-from-scratch/ch03
    wget https://raw.githubusercontent.com/akiko-b/workshop/master/201804_rasp_ai/digit_recognition_NN.py
    python3 digit_recognition_NN.py

- 畳み込みニューラルネットワークによる推論

    cd /home/pi/deep-learning-from-scratch/ch07
    wget https://raw.githubusercontent.com/akiko-b/workshop/master/201804_rasp_ai/digit_recognition_CNN.py
    python3 digit_recognition_CNN.py

<br>

# 4. Kerasによる物体識別の実装

## 4.1. スワップ領域の拡大

- Kerasのインストールや実行時のメモリ不足を避けるために、OSのスワップ領域を増やす。

    sudo nano /etc/dphys-swapfile

CONF_SWAPSIZE=100の箇所の数字を2048に変更する。

- ファイルをセーブしてエディタ終了。下記コマンドを実行する。

    sudo /etc/init.d/dphys-swapfile restart

- 下記コマンドで確認

    free -h

<br>

## 4.2. TensorFlowのインストール

- TensorFlowをインストール
ここではTensorFlowのバージョン1.7.0を使うが、そのままインストールするとnumpyのバージョンが1.14のものが一緒にインストールされる。
・・・が、1.14だとTensorFlowを使うときにエラーになってしまうので、バージョン1.13.3のnumpyをインストールしておく。
（TensorFlowのインストール後にnumpyバージョン1.13.3をインストールする順番でもOK）

    cd
    sudo apt-get install libblas-dev liblapack-dev python3-dev libatlas-base-dev gfortran python3-setuptools
    sudo pip3 install numpy==1.13.3
    wget https://github.com/lhelontra/tensorflow-on-arm/releases/download/v1.7.0/tensorflow-1.7.0-cp35-none-linux_armv7l.whl　
    sudo pip3 install tensorflow-1.7.0-cp35-none-linux_armv7l.whl

<br>

## 4.3. TensorFlow動作テスト

    wget https://raw.githubusercontent.com/yusugomori/deeplearning-tensorflow-keras/master/3/tensorflow/01_logistic_regression_or_tensorflow.py
    python3 01_logistic_regression_or_tensorflow.py

<br>

## 4.4. Kerasのインストール

    sudo apt-get install gcc libopenblas-dev cython libopenblas-base libatlas3-base
    sudo pip3 install keras　　（ ← 1時間15分ほどかかる）
    sudo pip3 install h5py
    sudo apt-get install python-h5py

<br>

## 4.5. Kerasによる物体識別１

- 物体識別のソースコードをダウンロードする。

    wget https://raw.githubusercontent.com/akiko-b/workshop/master/201804_rasp_ai/keras_ResNet50_1.py

- 画像データをダウンロードする。

    wget https://raw.githubusercontent.com/akiko-b/workshop/master/201804_rasp_ai/image/sample/cat.jpg
    wget https://raw.githubusercontent.com/akiko-b/workshop/master/201804_rasp_ai/image/sample/cat.jpg

- プログラムを実行する。

    python3 keras_ResNet50_1.py cat.jpg

最初の実行時にはDownloading data from..のメッセージとともにh5ファイルとjsonファイルがダウンロードされる。

<br>

## 4.6. Kerasによる物体識別２

- 下記コマンドを実行し、mjpg-streamerを起動する。

    ./start_stream.sh

- WEBブラウザでラズパイのIPアドレス、ポート9000番にアクセスする。
　例：http://192.168.xx.xx:9000  


- 物体識別のソースコードをダウンロードする。

    wget https://raw.githubusercontent.com/akiko-b/workshop/master/201804_rasp_ai/keras_ResNet50_2.py

- プログラムを実行する。

    python3 keras_ResNet50_2.py

「Ctl+C」で終了できる。


<br>


# 5. OpenCV + SSD_Kerasによる物体検出の実装

## 5.1. OpenCVのインストール

    sudo pip3 install opencv-python
    sudo apt-get install libjasper-dev libqt4-dev

pythonで`import cv2`して確認。

<br>

## 5.2. raspicam_cvのインストール
raspicam_cvライブラリを使用すると、OpenCVから簡単にRaspberryPiカメラモジュールを使用できます。

    sudo apt-get install gcc g++ libx11-dev libxt-dev libxext-dev libgraphicsmagick1-dev libcv-dev libhighgui-dev

    mkdir -p ~/git/raspberrypi
    cd ~/git/raspberrypi
    git clone https://github.com/raspberrypi/userland.git
    cd userland
    ./buildme

    mkdir -p ~/git
    cd ~/git
    git clone https://github.com/robidouille/robidouille.git
    cd robidouille/raspicam_cv
    mkdir objs
    make

<br>

## 5.3. ssd_kerasのインストール





## 5.4. jupyter notebookのインストール


## 5.5. サンプルソース実行

## 5.6. リアルタイム物体検出

分類できるクラスは以下の通り

・飛行機

・自転車

・鳥

・ボート

・ボトル

・バス

・車

・猫

・椅子

・牛

・ダイニングテーブル

・犬

・馬

・バイク

・人

・鉢植え

・羊

・ソファー

・電車

・TVモニター


<br>

# 6. 終了

- Raspbianをシャットダウンする。

    sudo shutdown -h now

- SDカードのアクセス(緑LED点灯)が消えたら、電源を切る。
