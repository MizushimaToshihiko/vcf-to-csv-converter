 # vcf-to-csv-converter
  - 「vcf-to-csv-converter」は、スマートフォンの電話帳をエクスポートしたvcfファイルをcsv形式に変換するためのPythonスクリプトです。このスクリプトを使用すると、簡単に電話帳データをcsv形式に変換して、ExcelやGoogle Sheetsなどの表計算ソフトで編集したり、他のプログラムに取り込んだりすることができます。

### 機能
 - vcfファイル及びjsonファイルをcsvファイルに変換できます
 - 氏名又は名称、メールアドレス、電話番号など、電話帳データの主要なフィールドをサポート
 - Python 3で動作
 
 
 ### vcf_read.py 
  - VCFデータの読み込み及びCSVファイルへの書き出し

 #### 使い方
 - vcfファイルをローカルあるいはファイルサーバーに保存してから、下記コマンドを実行
```bash
python vcf_read.py [the filepath of the vcf to read]
```
 - 上記をコマンドライン入力すると、vcfファイルと同じ場所に同名のcsvファイルができる

### json_read.py 
  - jsonデータの読み込み及びCSVファイルへの書き出し

#### 使い方(vcf_read.pyと同様)
 - jsonファイルをローカルあるいはファイルサーバーに保存してから、下記コマンドを実行
 ```bash
python json_read.py [the filepath of the vcf to read]
```
 - 上記をコマンドライン入力すると、jsonファイルと同じ場所に同名のcsvファイルができる
