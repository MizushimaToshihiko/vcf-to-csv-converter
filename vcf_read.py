# coding:utf-8
import sys
import chardet
import quopri

# usage:
# python vcf_read.py [the filepath of the vcf to read]
def usage() -> None:
    print("python vcf_read.py [the filepath of the vcf to read]")


def vcf_read(vcf_path) -> None:
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
        title = f"N,N;CHARSET={VCF_ENC},N;CHARSET={VCF_ENC};ENCODING=QUOTED-PRINTABLE,FN;CHARSET={VCF_ENC};ENCODING=QUOTED-PRINTABLE,SOUND;X-IRMC-N;CHARSET={VCF_ENC};ENCODING=QUOTED-PRINTABLE,SOUND;X-IRMC-N;CHARSET={VCF_ENC},TEL;WORK;VOICE,TEL;PREF,TEL;HOME;VOICE,TEL;CELL,TEL;PREF;WORK,TEL;PREF;CELL,TEL;WORK,TEL;CUSTOM,TEL;CELL;WORK,TEL;HOME,TEL;VOICE,TEL;X-VOICE,EMAIL,EMAIL;CELL,EMAIL;WORK,EMAIL;PREF;CELL,EMAIL;PREF,EMAIL;OTHER,VERSION,X-DCM-EXPORT,X-DCM-ACCOUNT;DOCOMO,X-DCM-TEL-ORIGINAL;CELL,X-DCM-EMAIL-ORIGINAL;CELL,X-DCM-RINGTONE,NOTE;CHARSET={VCF_ENC},X-DCM-TEL-ORIGINAL;WORK,ADR;CHARSET={VCF_ENC},X-DCM-POSTALCODE-ORIGINAL,X-DCM-SOUND-ORGINAL;X-IRMC-N;CHARSET={VCF_ENC},X-GNO,X-GN;CHARSET={VCF_ENC},E,X-DCM-GN-ORIGINAL;CHARSET={VCF_ENC},X-DCM-LABEL;CHARSET={VCF_ENC},X-DCM-TEL-ORIGINAL;CUSTOM,X-DCM-GROUP-ICONCOLOR,X-DCM-GROUP-ICON,X-DCM-TEL-ORIGINAL;HOME,NICKNAME;DEFAULT;CHARSET={VCF_ENC},X-DCM-TEL-ORIGINAL;VOICE,NOTE;ENCODING=QUOTED-PRINTABLE;CHARSET={VCF_ENC},BDAY,X-GN"
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
    else:
        vcf_read(sys.argv[1])
        
"""

各データ項目について
氏名・名称
    N,
    N;CHARSET={VCF_ENC},
    N;CHARSET={VCF_ENC};ENCODING=QUOTED-PRINTABLE
    FN;CHARSET={VCF_ENC};ENCODING=QUOTED-PRINTABLE
ﾌﾘｶﾞﾅ
    SOUND;X-IRMC-N;CHARSET={VCF_ENC},
    SOUND;X-IRMC-N;CHARSET={VCF_ENC};ENCODING=QUOTED-PRINTABLE
電話番号
    TEL;CELL,
    TEL;PREF;WORK,
    TEL;PREF;CELL,
    TEL;WORK,
    TEL;CUSTOM,
    TEL;CELL;WORK,
    TEL;HOME,
    TEL;VOICE,
    TEL;X-VOICE,
emailｱﾄﾞﾚｽ
    EMAIL,
    EMAIL;CELL,
    EMAIL;WORK,
    EMAIL;PREF;CELL,
    EMAIL;PREF,
    EMAIL;OTHER,
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


"""
