# 0. 事前準備

## 0.1. Raspbianをインストール

Raspbianは Raspberry Piに対応したOS。Debianベース。
※Debian：Linuxディストリビューションのひとつ

今回使用する機材ではSDカードにプレインストールされています。


[RASPBIAN STRETCH WITH DESKTOP](https://www.raspberrypi.org/downloads/raspbian/)


## 0.2. USB-シリアル変換ケーブル用ドライバーをインストール

Windows7 64bitの環境では、
PCのUSBポートにUSB-シリアル変換ケーブルをさせば、自動的にドライバをインストールしてくれる（社内のPC環境では５分ほど時間がかかった）。

Windows10だとうまくいかないという記事もあり。

うまくいかない場合は下記のサイトからドライバをダウンロードしてインストールする。
<http://www.prolific.com.tw/US/ShowProduct.aspx?p_id=225&pcid=41>

それでもうまくいかない場合は、下記のサイトから64bit/32bitの環境に合わせてプログラムをダウンロード、インストールする。
<http://www.ifamilysoftware.com/news37.html>

>参考にしたサイト
>[RaspberryPi(3,ZW)へのUSB-TTLシリアルコンソール接続 2017年版](https://qiita.com/exthnet/items/7354201894dfc734028b)


## 0.3. Tera Termをインストール

[Tera Term](https://forest.watch.impress.co.jp/library/software/utf8teraterm/)
