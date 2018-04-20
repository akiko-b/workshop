# 1. Raspberry Pi3とパソコンをシリアル接続する

## 1.1. SDカード上のファイルの編集
SDカードをPCのSDカードリーダーで開き、`boot`ドライブ直下の`config.txt`の最後尾に

    enable_uart=1

という行を追記する。

<br>
## 1.2. USB-シリアルケーブルの接続

**ラズパイ側**

　　４色のコネクターをラズパイのPINに接続する。

| コネクターの色 | ラズパイのPIN |
|:-------------:|:--------------|
| 黒 | 6番 GND |
| 白 | 8番 TX |
| 緑 | 10番 RX |
| 赤 | どこにも刺さない |

<img src="image/rasp_pin.PNG" width="80%">

**PC側**

　　USBコネクターをPCのUSBポートに接続する。

<br>

## 1.3. ターミナル接続（Tera Term）


- デバイスマネージャーで接続されているポート番号を確認する

<img src="image/port.PNG" width="80%">

<br>
- PC上のターミナルソフトを開き、シリアル通信のポート番号を選択する。

<img src="image/TeraTerm1.PNG" width="60%">

<br>
- Setup -> Serial port：　ボーレートを115200に設定する。

<img src="image/TeraTerm2.PNG" width="60%">

<br>

## 1.4. Raspberry Piの起動

- SDカードをRaspberry Pi本体に挿し込む

- Raspberry Pi本体をUSB電源につなぐ

Raspberry Pi本体には電源スイッチはありません。電源をつなぐと起動します。

<img src="image/TeraTerm3.PNG" width="60%">

Raspbianの場合はユーザ：pi、パスワード：raspberryがデフォルト設定です。

<br>
