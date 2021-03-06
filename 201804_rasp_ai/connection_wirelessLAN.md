# 1. Raspberry Pi3を無線LAN接続する

## 1.1. SDカード上のファイルの編集
SDカードをPCのSDカードリーダーで開き、`boot`ドライブ直下に中身が空の`ssh`ファイルと、下記の内容の`wpa_supplicant.conf`ファイルを置く。使用する無線LAN環境に合わせてSSID名とパスワードの箇所を変える。

    country=GB
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1

    network={
            ssid="<SSID名>"
            psk="<パスワード>"
    }


<br>

## 1.2. Raspberry Piの起動

- SDカードをRaspberry Pi本体に挿し込む

- Raspberry Pi本体をUSB電源につなぐ

Raspberry Pi本体には電源スイッチはありません。電源をつなぐと起動します。

<br>

## 1.3. IPアドレスの確認

同じネットワークセグメントにつながっているパソコンから下記コマンドでRasperry PiのIPアドレスを探す(下記はWindows上のコマンドプロンプトを使う場合)。 Raspberry PiのMACアドレスはB8-27-EBから始まるので、それに紐づいているIPアドレスを探す。

    for /l %i in (100,1,200) do ping -w 1 -n 1 192.168.209.%i && arp -a 192.168.209.%i   
    arp -a


注）「(100,1,200)」、「192.168.209」の部分は社内の環境に合わせています。異なる環境では適宜変更してください。

<br>

## 1.4. ターミナル接続（Tera Term）

PC上のターミナルソフトを開き、調べたIPアドレスを入力して接続する。

<img src="image/TeraTerm_IP.PNG" width="60%">


Raspbianの場合はユーザ：pi、パスワード：raspberryがデフォルト設定です。



<br>
