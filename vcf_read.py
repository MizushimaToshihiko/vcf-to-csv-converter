# coding:utf-8
import sys
import chardet
import quopri
import re

# usage:
# python vcf_read.py [the filepath of the vcf to read]
def usage() -> None:
    print("python vcf_read.py [the filepath of the vcf to read]")


def extract_vcard_data(vcf_data):
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
            print("searching max_lines:",max_lines)

    print("max_lines:",max_lines)
    print("max_vcard:", max_vcard)

    if max_vcard:
        fn_match = re.search(r'FN:(.*)', max_vcard)
        if fn_match and fn_match.group(1).strip():
            print("FN:",fn_match.group(1).strip())
        else:
            n_match = re.search(r'N:(.*)', max_vcard)
            if n_match:
                print("N:",n_match.group(1).strip())
    return None


def vcf_read(vcf_path : str, is_search : bool) -> None:
    """
    vcf_read reads the vcf file in 'vcf_path'.
    """
    with open(vcf_path, mode="rb") as f:
        vcf_b = f.read()
        vcf_enc = chardet.detect(vcf_b)["encoding"]
        print(vcf_enc)

    with open(vcf_path, mode="r", encoding=vcf_enc, errors="ignore") as f:
        vcf = f.read()
    
    vcf = vcf.replace("=\n=", "=")

    if vcf_enc == "CP932":
        vcf_enc = "shift_jis"
    elif vcf_enc == "ascii":
        vcf_enc = "UTF-8"

    if is_search:
        extract_vcard_data(vcf)
    else:
        vcf_write_to_csv(vcf, vcf_path, vcf_enc)


def vcf_write_to_csv(vcf, vcf_path, vcf_enc) -> None:
    """
    vcf_write_to_csv make a csv file in the directory same as vcf_path, 
    and write 'vcf'(string) to that csv file.
    """
    csv_filename = vcf_path[:vcf_path.rfind(".")+1] + "csv"
    vcf_path = vcf_path[:vcf_path.rfind("\\")+1]

    with open(csv_filename, mode="w", encoding="shift_jis", errors="ignore") as f2:
        VCF_ENC = vcf_enc.upper()
        title = f"FN,N,N;CHARSET={VCF_ENC},N;CHARSET={VCF_ENC};ENCODING=QUOTED-PRINTABLE,FN;CHARSET={VCF_ENC};ENCODING=QUOTED-PRINTABLE,X-PHONETIC-LAST-NAME,SOUND;X-IRMC-N;CHARSET={VCF_ENC};ENCODING=QUOTED-PRINTABLE,SOUND;X-IRMC-N;CHARSET={VCF_ENC},TEL,TEL;WORK;VOICE,TEL;TYPE=CELL,TEL;PREF,TEL;HOME;VOICE,TEL;CELL,TEL;PREF;WORK,TEL;PREF;CELL,TEL;WORK,TEL;CUSTOM,TEL;CELL;WORK,TEL;HOME,TEL;VOICE,TEL;X-VOICE,item1.TEL,item2.TEL,item3.TEL,item4.TEL,item5.TEL,item6.TEL,item7.TEL,EMAIL,EMAIL;CELL,EMAIL;WORK,EMAIL;PREF;CELL,EMAIL;PREF,EMAIL;OTHER,EMAIL;TYPE=INTERNET;TYPE=WORK,ADR;TYPE=WORK,ADR;WORK;CHARSET={VCF_ENC},ORG;CHARSET={VCF_ENC},item1.ORG,item2.ORG,item3.ORG,item4.ORG,item5.ORG,item6.ORG,item7.ORG,item1.TITLE,item2.TITLE,item3.TITLE,item4.TITLE,item5.TITLE,item6.TITLE,item7.TITLE,item1.URL,item2.URL,item3.URL,item4.URL,item5.URL,item6.URL,item7.URL,VERSION,X-DCM-EXPORT,X-DCM-ACCOUNT;DOCOMO,X-DCM-TEL-ORIGINAL;CELL,X-DCM-EMAIL-ORIGINAL;CELL,X-DCM-RINGTONE,NOTE;CHARSET={VCF_ENC},X-DCM-TEL-ORIGINAL;WORK,ADR;CHARSET={VCF_ENC},X-DCM-POSTALCODE-ORIGINAL,X-DCM-SOUND-ORGINAL;X-IRMC-N;CHARSET={VCF_ENC},X-GNO,X-GN;CHARSET={VCF_ENC},E,X-DCM-GN-ORIGINAL;CHARSET={VCF_ENC},X-DCM-LABEL;CHARSET={VCF_ENC},X-DCM-TEL-ORIGINAL;CUSTOM,X-DCM-GROUP-ICONCOLOR,X-DCM-GROUP-ICON,X-DCM-TEL-ORIGINAL;HOME,NICKNAME;DEFAULT;CHARSET={VCF_ENC},X-DCM-TEL-ORIGINAL;VOICE,NOTE;ENCODING=QUOTED-PRINTABLE;CHARSET={VCF_ENC},BDAY,X-GN,NICKNAME,X-PHONETIC-FIRST-NAME,X-PHONETIC-LAST-NAME"
        title = title.split(",")
        print("title:", title)
        f2.write(",".join(title) + "\n") # 列名を書き込み

        while len(vcf) > 9: #
            s = "" # f2に書き込むデータ（1行分）
            begin = vcf.find("BEGIN:VCARD")
            end = vcf.find("END:VCARD")+1
            
            target = {}
            for x in vcf[begin + len("BEGIN:VCARD") + 1: end - 2].split("\n"):
                if len(x.split(":")) < 2:
                    continue
                target_key = x.split(":")[0]
                if target_key not in target:
                    target[target_key] = x.split(":")[1]
                else:
                    target[target_key] += " / " + x.split(":")[1]

            if begin == 0:
                print("target:", target)

            for a in title:
                if a in target:
                    if "ENCODING=QUOTED-PRINTABLE" in a :
                        pre_decoded = quopri.decodestring(target[a], header=False)
                        target[a] = pre_decoded.decode("utf-8", "ignore")
                    s += target[a].replace(";", "") + ","
                else:
                    s += ","
            vcf = vcf[end:]
            f2.write(s + "\n")


if __name__ == "__main__":
    if sys.argv[1] in ["-help", "-h", "help"]:
        usage()
    elif sys.argv[1] in ["-search", "-s", "search"]:
        vcf_read(sys.argv[2], True)
    else:
        vcf_read(sys.argv[1], False)
        
"""

各データ項目について
氏名・名称
    FN,
    N,
    N;CHARSET={VCF_ENC},
    N;CHARSET={VCF_ENC};ENCODING=QUOTED-PRINTABLE
    FN;CHARSET={VCF_ENC};ENCODING=QUOTED-PRINTABLE
ﾌﾘｶﾞﾅ
    X-PHONETIC-LAST-NAME
    SOUND;X-IRMC-N;CHARSET={VCF_ENC},
    SOUND;X-IRMC-N;CHARSET={VCF_ENC};ENCODING=QUOTED-PRINTABLE
電話番号
    TEL;TYPE=CELL,
    TEL;CELL,
    TEL;PREF;WORK,
    TEL;PREF;CELL,
    TEL;WORK,
    TEL;CUSTOM,
    TEL;CELL;WORK,
    TEL;HOME,
    TEL;VOICE,
    TEL;X-VOICE,
    item1.TEL,
    item2.TEL,
    item3.TEL,
    item4.TEL,
    item5.TEL,
    item6.TEL,
    item7.TEL,
emailｱﾄﾞﾚｽ
    EMAIL,
    EMAIL;CELL,
    EMAIL;WORK,
    EMAIL;PREF;CELL,
    EMAIL;PREF,
    EMAIL;OTHER,
    EMAIL;TYPE=INTERNET;TYPE=WORK,
住所
    ADR;TYPE=WORK
    ADR;WORK
所属会社
    ORG,
    item1.ORG,
    item2.ORG,
    item3.ORG,
    item4.ORG,
    item5.ORG,
    item6.ORG,
    item7.ORG,
所属部署
    item1.TITLE,
    item2.TITLE,
    item3.TITLE,
    item4.TITLE,
    item5.TITLE,
    item6.TITLE,
    item7.TITLE,
URL
    item1.URL,
    item2.URL,
    item3.URL,
    item4.URL,
    item5.URL,
    item6.URL,
    item7.URL,
不要と思われる部分
    VERSION,
    X-DCM-EXPORT,
    X-DCM-ACCOUNT;DOCOMO,
    X-DCM-TEL-ORIGINAL;CELL,
    X-DCM-EMAIL-ORIGINAL;CELL,
    X-DCM-RINGTONE,
    NOTE;CHARSET={VCF_ENC},
    X-DCM-TEL-ORIGINAL;WORK,
    ADR;CHARSET={VCF_ENC},
    X-DCM-POSTALCODE-ORIGINAL,
    X-DCM-SOUND-ORGINAL;X-IRMC-N;CHARSET={VCF_ENC},
    X-GNO,
    X-GN;CHARSET={VCF_ENC},
    E,
    X-DCM-GN-ORIGINAL;CHARSET={VCF_ENC},
    X-DCM-LABEL;CHARSET={VCF_ENC},
    X-DCM-TEL-ORIGINAL;CUSTOM,
    X-DCM-GROUP-ICONCOLOR,
    X-DCM-GROUP-ICON,
    X-DCM-TEL-ORIGINAL;HOME,
    NICKNAME;DEFAULT;CHARSET={VCF_ENC},
    X-DCM-TEL-ORIGINAL;VOICE,
    NOTE;ENCODING=QUOTED-PRINTABLE;CHARSET={VCF_ENC}
    NICKNAME
    X-PHONETIC-FIRST-NAME
    X-PHONETIC-LAST-NAME
    item1.X-ABLabel


"""
