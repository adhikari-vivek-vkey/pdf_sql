import mysql.connector as my
import re
import os
import datetime
import time
from dateutil import tz
import pytz

db = my.connect(host="localhost", database="cashpersonal", user="root", password="Credicxo@1!#")
cur = db.cursor()
a = []
nor_data = []
nor_date = []

sql = "SELECT cust_id  FROM `users_loan_agreement_signs` WHERE `sign_date` BETWEEN '2019-11-28 11:10:00.000000' AND '2019-12-04 12:30:00.000000'"
cur.execute(sql)
res = cur.fetchall()
try:
    for i in res:
        a.append(i[0])
    list_data = list(dict.fromkeys(a))
    for j in list_data:
        file = '/var/www/html/public/storage/uploads/' + str(j)
        try:
            files_path = [str(file)+'/'+x for x in os.listdir(str(file))]
            Date_Reg = re.compile(r'\d\d\d\d\d\d\d\d\d\d')
            for f in files_path:
                if f.endswith(".pdf"):
                    try:
                         if Date_Reg.search(f).group() is not None:
                            nor_data.append(f) #full path
                    except Exception as e:
                        print(str(e)+'  '+j)

            sql_time = "SELECT sign_date FROM `users_loan_agreement_signs` WHERE `cust_id` LIKE '{}' AND `created_at` BETWEEN '2019-11-28 11:10:00.000000' AND '2019-12-04 12:30:00.000000'".format(j)
            cur.execute(sql_time)
            date_time = cur.fetchall()
            for d in date_time:
                nor_date.append(d[0])
            for match in nor_data:
                datetime_s = Date_Reg.search(match).group()
                aa = int(datetime_s)
                aa =  datetime.datetime.utcfromtimestamp(aa).replace(tzinfo=pytz.utc)
                central = aa.astimezone(pytz.timezone('Asia/Kolkata'))
                addTime = str(central)[:-6]

                for i_range in nor_date:
                    datetimeFormat = '%Y-%m-%d %H:%M:%S'
                    diff = datetime.datetime.strptime(i_range, datetimeFormat)- datetime.datetime.strptime(addTime, datetimeFormat)
                    Time_diff_in_min = diff.seconds//60
                    if Time_diff_in_min <=10:
                        t_split = match.split('/')[-1]
                        t_date ="SELECT id,loan_agreement FROM `users_loan_agreement_signs` WHERE `cust_id` LIKE '{}' AND sign_date LIKE '{}'".format(j,i_range)
                        cur.execute(t_date)
                        rest = cur.fetchall()
                        if rest[0][1] == '':
                            update_file = "UPDATE `users_loan_agreement_signs` SET `loan_agreement` = '" + str(t_split) + "' WHERE `users_loan_agreement_signs`.`id` = " + str(rest[0][0]);
                            cur.execute(update_file)
                            db.commit()
                            print(cur.rowcount, "record(s) affected")
                            f = open("Date_txt.txt", "a+")
                            f.write("Custome id:-  {}, FILE Name :-  {}   File Create  and Time Diffrence {} Minutes \n".format(j, t_split,Time_diff_in_min))
                        else:
                            print(''+j)
        except Exception as e:
            print(str(e)+'date '+j)
        nor_data = []
        nor_date = []
except Exception as e:
    print(e)
                                                                                                                                                              70,1          Bot
