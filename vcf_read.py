"""
VCF (vCard) ファイルを読み取り、CSVファイルに変換するモジュール。

このモジュールは、VCFファイル内のコンタクト情報を解析し、対応するCSVファイルを生成します。また、VCFファイル内の写真データを抽出して画像ファイルとして保存します。

使用方法:
    python vcf_read.py [VCFファイルのパス]

コマンドライン引数:
    - [VCFファイルのパス]: 処理するVCFファイルのファイルパスを指定します。
"""
import sys
import quopri
import re
import base64
import os
import chardet

def usage() -> None:
    """
    このスクリプトの使用方法を標準出力に表示します。
    """
    print("python vcf_read.py [the filepath of the vcf to read]")


def extract_vcard_data(vcf_data):
    """
    VCFデータから最大のvCardエントリを抽出して解析します。
    """
    vcards = re.findall(r'BEGIN:VCARD(.*?)END:VCARD', vcf_data, re.DOTALL)
    if not vcards:
        return None

    max_lines = 0
    max_vcard = None

    for vcard in vcards:
        lines = vcard.strip().split('\n')
        if len(lines) > max_lines:
            max_lines = len(lines)
            max_vcard = vcard
            print("searching max_lines:", max_lines)

    print("max_lines:", max_lines)
    print("max_vcard:", max_vcard)

    if max_vcard:
        fn_match = re.search(r'FN:(.*)', max_vcard)
        if fn_match and fn_match.group(1).strip():
            print("FN:", fn_match.group(1).strip())
        else:
            n_match = re.search(r'N:(.*)', max_vcard)
            if n_match:
                print("N:", n_match.group(1).strip())
    return None


def extract_titles(vcf_data):
    """
    VCFデータからすべてのユニークな項目名を抽出します。
    """
    vcards = re.findall(r'BEGIN:VCARD(.*?)END:VCARD', vcf_data, re.DOTALL)
    titles = set()

    for vcard in vcards:
        lines = vcard.strip().split('\n')
        for line in lines:
            if ':' in line:
                key = line.split(':')[0]
                if key != "PHOTO":  # PHOTO項目は除外
                    titles.add(key)

    return sorted(titles)


def save_photo(vcard, output_dir, index):
    """
    vCardデータから写真データを抽出し、画像ファイルとして保存します。
    """
    photo_match = re.search(r'PHOTO;ENCODING=BASE64;TYPE=(JPEG|PNG):(.+)', vcard, re.DOTALL)
    if photo_match:
        photo_type = photo_match.group(1).lower()
        photo_data = photo_match.group(2).replace('\n', '')
        photo_bytes = base64.b64decode(photo_data)

        output_filename = os.path.join(output_dir, f"photo_{index}.{photo_type}")
        with open(output_filename, 'wb') as photo_file:
            photo_file.write(photo_bytes)
        print(f"Saved photo to {output_filename}")


def parse_vcard(vcard):
    """
    vCardデータを解析して、項目名とその値を辞書に格納します。

    引数:
        vcard (str): 処理するvCardデータの文字列。

    戻り値:
        dict: vCard項目名と値のペアを含む辞書。
    """
    target = {}
    for x in vcard[len("BEGIN:VCARD")+1: len(vcard)-1].split("\n"):
        if len(x.split(":")) < 2:
            continue
        target_key = x.split(":")[0]
        target_value = x.split(":")[1]
        if target_key in target:
            target[target_key] += " / " + target_value
        else:
            target[target_key] = target_value
    return target


def encode_value(target, title):
    """
    辞書内の値をエンコードして安全にCSVに書き込めるようにします。

    引数:
        target (dict): vCard項目名と値のペアを含む辞書。
        title (list): CSVの列名リスト。

    戻り値:
        str: エンコード済みのCSVの1行分のデータ。
    """
    s = ""
    for a in title:
        if a in target:
            if "ENCODING=QUOTED-PRINTABLE" in a:
                pre_decoded = quopri.decodestring(target[a], header=False)
                target[a] = pre_decoded.decode("utf-8", "ignore")
            s += target[a].replace(";", "").replace("\n", " ") + ","
        else:
            s += ","
    return s


def write_vcard_to_csv(vcf, output_dir, titles, csv_filename):
    """
    vCardデータを解析してCSVファイルに書き込みます。

    引数:
        vcf (str): VCFファイルの全データ。
        output_dir (str): 出力ファイルのディレクトリ。
        titles (list): CSVの列名リスト。
        csv_filename (str): 書き込み先のCSVファイル名。

    戻り値:
        None
    """
    with open(csv_filename, mode="w", encoding="shift_jis", errors="ignore") as f2:
        f2.write(",".join(titles) + "\n")  # 列名を書き込み

        index = 1
        while len(vcf) > 9:  #
            begin = vcf.find("BEGIN:VCARD")
            end = vcf.find("END:VCARD") + 1
            vcard = vcf[begin:end]

            target = parse_vcard(vcard)
            save_photo(vcard, output_dir, index)
            index += 1

            s = encode_value(target, titles)
            vcf = vcf[end:]
            f2.write(s + "\n")


def vcf_read(vcf_path: str, is_search: bool) -> None:
    """
    VCFファイルを読み込み、解析してCSVファイルを生成します。

    引数:
        vcf_path (str): 読み込むVCFファイルのパス。
        is_search (bool): 最大のvCardエントリを検索するかどうかを指定。
    """
    with open(vcf_path, mode="rb") as f:
        vcf_b = f.read()
        vcf_enc = chardet.detect(vcf_b)["encoding"]
        print(vcf_enc)

    with open(vcf_path, mode="r", encoding=vcf_enc, errors="ignore") as f:
        vcf = f.read()

    vcf = vcf.replace("=\n=", "=")

    if is_search:
        extract_vcard_data(vcf)
    else:
        titles = extract_titles(vcf)
        csv_filename = vcf_path[:vcf_path.rfind(".") + 1] + "csv"
        output_dir = os.path.dirname(csv_filename)
        write_vcard_to_csv(vcf, output_dir, titles, csv_filename)


if __name__ == "__main__":
    if sys.argv[1] in ["-help", "-h", "help"]:
        usage()
    elif sys.argv[1] in ["-search", "-s", "search"]:
        vcf_read(sys.argv[2], True)
    else:
        vcf_read(sys.argv[1], False)
