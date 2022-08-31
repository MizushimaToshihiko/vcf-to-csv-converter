# coding:utf-8
import sys

# usage:
# python vcf_read.py [the filepath of the vcf to read] [encode of the vcf file]

def vcf_read(vcf_path, vcf_enc="shift_jis") -> None:
    """
    vcf_read reads the vcf file in 'vcf_path'.
    """
    with open(vcf_path, mode="r", encoding=vcf_enc, errors="ignore") as f:
        vcf = f.read()
    vcf_write_to_csv(vcf, vcf_path, vcf_enc)

def vcf_write_to_csv(vcf, vcf_path, vcf_enc) -> None:
    """
    vcf_write_to_csv make a csv file in the directory same as vcf_path, and write 'vcf'(string) to that csv file.
    """
    csv_filename = vcf_path[:vcf_path.rfind(".")+1] + "csv"
    vcf_path = vcf_path[:vcf_path.rfind("\\")+1]

    with open(csv_filename, mode="w", encoding="shift_jis", errors="ignore") as f2:
        # f2.write(vcf)
        VCF_ENC = vcf_enc.upper()
        title = f"VERSION,X-DCM-EXPORT,X-DCM-ACCOUNT;DOCOMO,N;CHARSET={VCF_ENC},SOUND;X-IRMC-N;CHARSET={VCF_ENC},X-DCM-SOUND-ORGINAL;X-IRMC-N;CHARSET={VCF_ENC},TEL;CELL,X-DCM-TEL-ORIGINAL;CELL,E,X-GNO,X-GN;CHARSET={VCF_ENC},X-DCM-GN-ORIGINAL;CHARSET={VCF_ENC},X-DCM-GROUP-ICONCOLOR,X-DCM-GROUP-ICON,EMAIL;CELL,X-DCM-EMAIL-ORIGINAL;CELL,X-DCM-RINGTONE,NOTE;CHARSET={VCF_ENC},TEL;WORK,X-DCM-TEL-ORIGINAL;WORK,ADR;CHARSET={VCF_ENC},X-DCM-POSTALCODE-ORIGINAL,TEL;CUSTOM,X-DCM-LABEL;CHARSET={VCF_ENC},X-DCM-TEL-ORIGINAL;CUSTOM,TEL;HOME,X-DCM-TEL-ORIGINAL;HOME,NICKNAME;DEFAULT;CHARSET={VCF_ENC},TEL;VOICE,X-DCM-TEL-ORIGINAL;VOICE,NOTE;ENCODING=QUOTED-PRINTABLE;CHARSET={VCF_ENC}" 
        title = title.split(",")
        print("title:", title)
        f2.write(",".join(title) + "\n") # 列名を書き込み
        
        while len(vcf) > 9: #
            s = "" # f2に書き込むデータ（1行分）
            begin = vcf.find("BEGIN:VCARD")
            end = vcf.find("END:VCARD")+1
            target = {x.split(":")[0] : x.split(":")[1] if len(x.split(":")) >= 2 else print(x) for x in vcf[begin + len("BEGIN:VCARD") + 1: end - 2].split("\n")}
            if begin == 0:
                print("target:", target)
            for a in title:
                if a in target.keys():
                    # print(a,"あった")
                    s += target[a].replace(";", "") + ","
                else:
                    # print(a,"なかった")
                    s += ","
            vcf = vcf[end:]
            f2.write(s + "\n")


if __name__ == "__main__":
    vcf_read(sys.argv[1])
        
"""

一番長いデータ
BEGIN:VCARD
VERSION:2.1
X-DCM-ACCOUNT;DOCOMO:docomo;com.android.nttdocomo
N;CHARSET=UTF-8:;;;;
SOUND;X-IRMC-N;CHARSET=UTF-8:;;
X-DCM-SOUND-ORGINAL;X-IRMC-N;CHARSET=UTF-8:;;
TEL;VOICE:
TEL;CELL:
X-DCM-TEL-ORIGINAL;VOICE:
X-DCM-TEL-ORIGINAL;CELL:
X-GNO:2
X-GN;CHARSET=UTF-8:
X-DCM-GN-ORIGINAL;CHARSET=UTF-8:
X-DCM-GROUP-ICONCOLOR:
X-DCM-GROUP-ICON:
END:VCARD
BEGIN:VCARD

"""
