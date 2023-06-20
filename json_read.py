# coding:utf-8

#Pandasをインポート
import glob
import os
import json
import csv
import sys
import datetime


date_f = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
jsext = "*.json"

def json_read(json_path) -> None:
    '''
    jsonの連絡先データを読込み、CSVに書き込む
    '''
    dic_title = ["accountName", "accountType", "errorDisplayName", "email1", "email2", "event", "groupMembership", "im", "nickname", "note", "organization", "phone1", "phone2", "phone3", "phone4", "phone5", "relation", "sendToVoicemail", "sipAddress", "starred", "structuredName1", "structuredName2", "structuredName3", "structuredName4", "structuredName5", "structuredName6", "structuredName7", "structuredName8", "structuredName9", "structuredPostal", "website"]

    write_f = open(json_path + "\\" + date_f + "contacts.csv", mode="a", newline="")
    csv_writer = csv.DictWriter(write_f, fieldnames=dic_title, delimiter=',',quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    csv_writer.writeheader()

    paths = glob.glob(json_path + "\\" + jsext)

    for path in paths:
        print(path)
        with open(path,  mode='r', encoding="utf-8", errors="ignore") as f:
            data = json.load(f)

            for j in data:
                if j is None:
                    continue
                #
                # Set 'tickets' Dictionary
                #
                tickets = {}
                for dic_key in dic_title:
                    if dic_key == "email1":
                        if j.get("email") is not None and j.get("email") != [] :
                            for i, email in enumerate(j["email"]):
                                tickets.update({'email'+str(i+1):email['data1']})
                        continue
                    if dic_key == "email2":
                        continue
                    if dic_key == "phone1":
                        if j.get("phone") is not None and j.get("phone") != []:
                            for i, phone in enumerate(j['phone']):
                                tickets.update({'phone'+str(i+1):phone['data1']})
                        continue
                    if dic_key in ["phone2", "phone3", "phone4", "phone5"]:
                        continue
                    if dic_key == "structuredName1":
                        if j.get("structuredName") is not None and j.get("structuredName") != []:
                            for i in range(1, 10):
                                if 'data'+str(i) in j['structuredName']:
                                    tickets.update({'structuredName'+str(i): j['structuredName']['data'+str(i)]})
                        continue
                    if dic_key in ("structuredName2", "structuredName3"):
                        continue
                    if dic_key == "nickname":
                        if j.get(dic_key) is not None and j.get(dic_key) != []:
                            tickets.update({dic_key: j[dic_key]["data1"]})
                        continue
                    if dic_key == "structuredPostal":
                        if j.get(dic_key) is not None and j.get(dic_key) != []:
                            tickets.update({dic_key: j[dic_key][0]["data1"]})
                        continue
                    if j.get(dic_key) is not None and j.get(dic_key) != []:
                        dic_val = j[dic_key]
                        tickets.update({dic_key: dic_val})
                #
                # Write 'tickets' to the csv file
                #
                csv_writer.writerow(tickets)

    write_f.close()


def json_dump2(json_path) -> None:
    '''
    jsonの各要素のmax値を調査する
    '''
    paths = glob.glob(json_path + "\\" + jsext)
    accountName_max = 0
    accountType_max = 0
    customRington_max = 0
    errorDisplayName_max = 0
    email_max = 0
    event_max = 0
    groupMembership_max = 0
    im_max = 0
    nickname_max= 0
    note_max = 0
    organization_max = 0
    phone_max = 0
    relation_max = 0
    sendToVoicemail_max = 0
    sipAddress_max = 0
    starred_max = 0
    structuredName_max = 0
    structuredPostal_max = 0
    website_max = 0
    for path in paths:
        with open(path,  mode='r', encoding="utf-8", errors="ignore") as f:
            data = json.load(f)

            for j in data:
                if j is None:
                    continue
                if j.get("accountName") is not None: accountName_max = max(accountName_max, len(j["accountName"]))
                if j.get("accountType") is not None: accountType_max = max(accountType_max, len(j["accountType"]))
                if j.get("customRington") is not None: customRington_max = max(customRington_max, len(j["customRington"]))
                if j.get("errorDisplayName") is not None: errorDisplayName_max = max(errorDisplayName_max, len(j["errorDisplayName"]))
                if j.get("email") is not None: email_max = max(email_max, len(j["email"]))
                if j.get("event") is not None: event_max = max(event_max, len(j["event"]))
                if j.get("groupMembership") is not None: groupMembership_max = max(groupMembership_max, len(j["groupMembership"]))
                if j.get("im") is not None: im_max = max(im_max, len(j["im"]))
                if j.get("nickname") is not None: nickname_max= max(nickname_max, len(j["nickname"]))
                if j.get("note") is not None: note_max = max(note_max, len(j["note"]))
                if j.get("organization") is not None: organization_max = max(organization_max, len(j["organization"]))
                if j.get("phone") is not None: phone_max = max(phone_max, len(j["phone"]))
                if j.get("relation") is not None: relation_max = max(relation_max, len(j["relation"]))
                if j.get("sipAddress") is not None: sipAddress_max = max(sipAddress_max, len(j["sipAddress"]))
                if j.get("structuredName") is not None: structuredName_max = max(structuredName_max, len(j["structuredName"]))
                if j.get("structuredPostal") is not None: structuredPostal_max = max(structuredPostal_max, len(j["structuredPostal"]))
                if j.get("website") is not None: website_max = max(website_max, len(j["website"]))
    print("accountName_max", accountName_max)
    print("accountType_max",accountType_max)
    print("customRington_max",customRington_max)
    print("errorDisplayName_max",errorDisplayName_max)
    print("email_max",email_max)
    print("event_max",event_max)
    print("groupMembership_max",groupMembership_max)
    print("im_max",im_max)
    print("nickname_max",nickname_max)
    print("note_max",note_max)
    print("organization_max",organization_max)
    print("phone_max",phone_max)
    print("relation_max",relation_max)
    print("sendToVoicemail_max",sendToVoicemail_max)
    print("sipAddress_max",sipAddress_max)
    print("starred_max",starred_max)
    print("structuredName_max",structuredName_max)
    print("structuredPostal_max",structuredPostal_max)
    print("website_max",website_max)



def json_dump(json_path):
    '''
    jsonの内容をprintする
    '''
    paths = glob.glob(json_path + "\\" + jsext)
    print(*paths, sep="\n")
    for path in paths:
        with open(path, mode="r", encoding="utf-8", errors="ignore") as f:
            j = f.read()
            data = json.dumps(j, indent=4, separators=(", ", ": "))
            print(data)


if __name__ == "__main__":
    if sys.argv[1] == "-max":
        json_dump2(sys.argv[2])
    elif sys.argv[1] == "-d":
        json_dump(sys.argv[2])
    else:
        json_read(sys.argv[1])
        