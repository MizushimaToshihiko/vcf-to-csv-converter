# coding:utf-8

#Pandasをインポート
import glob
import os
import json
import csv
import sys
import datetime
# import pandas as pd
# from pandas.io.json import json_normalize


# json_path=r"C:\Users\toshi\Documents\携帯電話連絡先\橋本ST" +"\\"
# paths=glob.glob(json_path + "*.json")
# date_f = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def json_read(json_path):
    # wf = open(json_path + "\\" + date_f + "contacts.csv", mode="a")
    # csv_writer = csv.writer(wf, delimiter=',',quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    # csv_writer.writerow(["accountName", "accountType", "customRington", "email", "event", "groupMembership", "im", "nickname", "note", "organization", "phone"])

    paths = glob.glob(json_path + "\\" + "*.json")

    email_max = 0
    phone_max = 0
    for path in paths:
        with open(path,  mode='r', encoding="utf-8", errors="ignore") as f:
            data = json.load(f)

            # i = 0
            for j in data:
                if j is None:
                    continue
                if j.get("email") is not None:
                    email_max = max(email_max, len(j["email"]))
                if j.get("phone") is not None:
                    phone_max = max(phone_max, len(j["phone"]))

    print("email_max:", email_max)
    print("phone_max:", phone_max)
                # print(j)
                # print(type(j))
                # 1行ずつ作る
                # Set members Dictionary
                #
                # members = {}

                # emails = {}
                # for email in data['email']:
                #     email_data1 = email['data1']
                #     email_data2 = email['data2']
                #     email_data3 = email['data3']
                #     email_data4 = email['data4']
                #     # emails.update({member_id: member_name})
                #     emails.update({'data1':email_data1})
                #     emails.update({'data2':email_data2})
                #     emails.update({'data3':email_data3})
                #     emails.update({'data4':email_data4})

                # #
                # # Set lists Dictionary
                # #
                # lists = {}
                # for list in data['lists']:
                #     list_id = list['id']
                #     list_name = list['name']
                #     lists.update({list_id: list_name})

                # #
                # #  Get cards value
                # #
                # tickets = []
                # for card in data['cards']:
                #     closed = card['closed']
                #     if (closed == False):
                #         updated_date = card['dateLastActivity']
                #         desc = card['desc']
                #         card_id = card['id']
                #         title = card['name']
                #         asigned_member_ids = card['idMembers']
                #         list_id = card['idList']

                #         # asigned_member_name
                #         if len(asigned_member_ids) > 0:
                #             asigned_member_id = asigned_member_ids[0]
                #             asigned_member_name = members[asigned_member_id]
                #         else:
                #             asigned_member_name = ""

                #         # list_name
                #         list_name = lists[list_id]

                #         tickets.append([list_name, title, desc, asigned_member_name, updated_date])

                # basename = os.path.splitext(os.path.basename(path))[0]
                # print(basename)
                # #
                # # Write CSV
                # #
                # with open(path + basename + '.csv', 'w', newline='') as csvFile:
                #     csvwriter = csv.writer(csvFile, delimiter=',',quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                #     csvwriter.writerow(['リスト名', 'カード名', '説明', '担当者', '更新日時'])
                #     for ticket in tickets:
                #         csvwriter.writerow(ticket)


# def json_dump(json_path):
#     paths = glob.glob(json_path + "\\" + "*.json")
#     print(*paths, sep="\n")
#     for path in paths:
#         with open(path, mode="r", encoding="utf-8", errors="ignore") as f:
#             j = f.read()
#             data = json.dumps(j, indent=4, separators=(", ", ": "))
#             print(data)


if __name__ == "__main__":
    json_read(sys.argv[1])
        