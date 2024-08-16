 # vcf-to-csv-and-json-to-csv-converter

「vcf-to-csv-and-json-to-csv-converter」は、スマートフォンの電話帳をエクスポートした`vcf`ファイルおよび`json`ファイルを`csv`形式に変換するためのPythonスクリプト集です。このスクリプトを使用すると、電話帳データを簡単に`csv`形式に変換して、ExcelやGoogle Sheetsなどの表計算ソフトで編集したり、他のプログラムに取り込んだりすることができます。

## 機能

- `vcf`ファイルおよび`json`ファイルを`csv`ファイルに変換できます。
- 氏名、メールアドレス、電話番号など、電話帳データの主要なフィールドをサポート。
- Python 3で動作。

## スクリプトの説明

### vcf_read.py

このスクリプトは、`vcf`ファイルを読み込み、`csv`ファイルに変換するために使用します。最新のリファクタリングにより、コードがモジュール化され、メンテナンスが容易になりました。

#### 使用方法

1. `vcf`ファイルをローカルまたはファイルサーバーに保存します。
2. 以下のコマンドを実行して、`vcf`ファイルを`csv`ファイルに変換します。

```bash
python vcf_read.py [the filepath of the vcf to read]
```
3. 上記をコマンドラインで入力すると、vcfファイルと同じ場所に同名のcsvファイルが生成されます。

### json_read.py 

このスクリプトは、jsonファイルを読み込み、csvファイルに変換するために使用します。複数のjsonファイルを一つのcsvファイルに集約する機能があります。

#### 使用方法
1. jsonファイルをローカルまたはファイルサーバーに保存します。
2. 以下のコマンドを実行して、jsonファイルをcsvファイルに変換します。
 ```bash
python json_read.py [the directory path of the json files to read]
```
3. 上記をコマンドラインで入力すると、jsonファイルと同じ場所に同名のcsvファイルが生成されます。

### 作者
MizushimaToshihiko

### ライセンス
MIT License

### 注意事項
 - このスクリプトは、スマートフォンの電話帳をエクスポートしたvcfファイル及びjsonファイルに対してのみ動作します
 - このスクリプトを使用することによって生じたいかなる損害についても、作者は一切の責任を負いません