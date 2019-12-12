#################################################
######      SQL Footer Generater Code      ######
#################################################


import mysql.connector as my
import re
import os
import datetime
import time

# db = my.connect(host="40.112.165.130", database="credicxodb", user="anandesh", password="rock0004")
db = my.connect(host="localhost", database="cashpersonal", user="anandesh", password="Rock0004@")

cur = db.cursor()
a = []
filter_data = []
nor_data = []
nor_date = []


sql = "SELECT cust_id  FROM `users_loan_agreement_signs` WHERE `sign_date` BETWEEN '2019-11-28 11:10:00.000000' AND '2019-12-04 12:30:00.000000'"
cur.execute(sql)
res = cur.fetchall()
try:
    #append All Cust_id
    for i in res:
        a.append(i[0])
    #delete all duplicate cust_id
    list_data = list(dict.fromkeys(a))
    list_data = ['54056','48506','53883']
    #loop all cust_id
    for j in list_data:
        file = '/var/www/html/public/storage/uploads/' + str(j)
        # file = os.getcwd() + '/' + str(j)
        try:
            files_path = [str(file)+'/'+x for x in os.listdir(str(file))]
            # Date_Regex = re.compile(r'\d\d\d\d-\d\d-\d\d')
            Date_Reg = re.compile(r'\d\d\d\d\d\d\d\d\d\d')
            for f in files_path:
                if f.endswith(".pdf"):
                    try:
                         if Date_Reg.search(f).group() is not None:
                            nor_data.append(f) #full path
                            #take unix time
                            datetime_s = Date_Reg.search(f).group()
                            aa = str(datetime_s)
                            print(aa)
                            aa =  datetime.datetime.fromtimestamp(int(aa)).strftime('%Y-%m-%d %H:%M:%S')
                            print(aa)
                            filter_data.append(aa)
                    except Exception as e:
                        print(str(e)+'pdf not match our requirement '+j)
            sql_time = "SELECT sign_date FROM `users_loan_agreement_signs` WHERE `cust_id` LIKE '{}' AND `created_at` BETWEEN '2019-11-28 11:10:00.000000' AND '2019-12-04 12:30:00.000000'".format(j)
            cur.execute(sql_time)
            date_time = cur.fetchall()
            for d in date_time:
                nor_date.append(d[0])
            for match in nor_date:
                time_string = str(match)
                struct_time = time.strptime(time_string, "%Y-%m-%d %H:%M:%S")
                t = datetime.datetime(*struct_time[:6])
                g = 0
                for i_range in range(11):
                    delta = datetime.timedelta(minutes=g)
                    delt =str(t+delta)
                    mytring = delt[:-3]
                    for dir_da in filter_data:
                        myString = dir_da[:-3]
                        if myString == mytring:
                            print('match')
                            print(str(j)+' '+ str(myString)+' '+ str(mytring))
                            for rever in nor_data:
                                print(rever)
                                dat = Date_Reg.search(rever).group()
                                aa = str(dat)
                                aa = datetime.datetime.fromtimestamp(int(aa)).strftime('%Y-%m-%d %H:%M:%S')
                                if aa == dir_da:
                                    t_split = rever.split('/')[-1]
                                    t_date ="SELECT id,loan_agreement FROM `users_loan_agreement_signs` WHERE `cust_id` LIKE '{}' AND sign_date LIKE '{}'".format(j,match)
                                    cur.execute(t_date)
                                    rest = cur.fetchall()
                                    if rest[0][1] == '':
                                        update_file = "UPDATE `users_loan_agreement_signs` SET `loan_agreement` = '" + str(t_split) + "' WHERE `users_loan_agreement_signs`.`id` = " + str(rest[0][0]);
                                        cur.execute(update_file)
                                        db.commit()
                                        print(cur.rowcount, "record(s) affected")
                                        f = open("Date_txt.txt", "a+")
                                        f.write("Custome id:-  {}, FILE Name :-  {}   and File Create  \n".format(j, t_split))
                                    else:
                                        pass
                    g+=1


            filter_data = []
            nor_data = []
            nor_date = []

        except Exception as e:
            print(str(e)+'date '+j)
except Exception as e:
    print(e)
