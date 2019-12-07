#################################################
######      SQL Footer Generater Code      ######
#################################################

import mysql.connector as my
import re
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
from datetime import datetime
import calendar
import shutil
db = my.connect(host="localhost", database="cashpersonal", user="root", password="Credicxo@1!#")

cur = db.cursor()
a = []
b = []
c = []
filter_data = []
nor_data = []
nor_date = []


def findDay(date):
    week = datetime.strptime(date, '%Y-%m-%d').weekday()
    cal = (calendar.day_name[week])
    return (cal[:3])

def search():
    num = 1
    for data_filter in filter_data:
        if data_filter == team:
            for find_dir in nor_data:
                dat = Date_Reg.search(find_dir).group()
                ch_st = datetime.strptime(dat, '%d-%m-%Y').strftime('%Y-%m-%d')
                if ch_st == team:
                    for loop in range(b.count(team)-1):
                        source = find_dir
                        final_destination = ' '.join(source.split('.pdf')[:-1])
                        destination = str(final_destination)+str(num)+'.pdf'
                        dest = shutil.copyfile(source, destination)
                        num +=1

                        if num == b.count(team):
                            return True
    return False

def get_data():
    dou_date = []
    n_date = []
    try:
        file = '/var/www/html/public/storage/uploads/' + str(j)
        fil_path = [str(file)+'/'+x for x in os.listdir(str(file))]
        for f_path in fil_path:
            if f_path.endswith(".pdf"):
                try:
                    aa = Date_Reg.search(f_path).group()
                    change_pa = datetime.strptime(aa, '%d-%m-%Y').strftime('%Y-%m-%d')
                    if change_pa == team:
                        dou_date.append(f_path)
                    print(dou_date)
                except Exception as e:
                    print(str(e)+'more'+str(j))
        for cha_date in nor_date:
            try:
                aa = Date_Regex.search(cha_date).group()
                if aa == team:
                    n_date.append(cha_date)
                print(n_date)
            except Exception as e:
                    print(str(e)+'more one'+str(j))

        nn = 0

        for t_t in dou_date:
            na_sql = "SELECT users_name, users_city  FROM `users_personal_infos` WHERE `cust_id` LIKE "+ str(j)
            cur.execute(na_sql)
            result_na = cur.fetchall()
            t_split = t_t.split('/')[-1]
            t_date ="SELECT id  FROM `users_loan_agreement_signs` WHERE `cust_id` LIKE "+ str(j)+ " AND sign_date LIKE '" +str(n_date[nn]) +"'"
            cur.execute(t_date)
            rest = cur.fetchall()
            update_file = "UPDATE `users_loan_agreement_signs` SET `loan_agreement` = '" + str(t_split) + "' WHERE `users_loan_agreement_signs`.`id` = " + str(rest[0][0]);
            cur.execute(update_file)
            db.commit()
            print(cur.rowcount, "record(s) affected")

            st_t = Date_Regex.search(n_date[nn]).group()
            dddd = findDay(st_t)
            ch_l = datetime.strptime(n_date[nn], '%Y-%m-%d %H:%M:%S').strftime(str(dddd)+' %b %d %H:%M:%S IST %Y')
            footer = {
                "Digitally Signed by: ": "",
                'Name: ': str(result_na[0][0]).capitalize(),
                'Location: ': str(result_na[0][1]).capitalize(),
                "Reason: ": 'Loan Agreement',
                'Date: ': ch_l,
                }



            generate_footer(footer)
            merge_pdf(t_t,t_t)
            nn+=1


    except Exception as e:
        print(str(e)+'more one'+str(j))

def da_list():
    for date_nor in nor_date:

        datetime_sett = Date_Regex.search(date_nor).group()
        if list_t == datetime_sett:
            # ['2019-11-13 18:55:21', '2019-10-30 18:55:11', '2019-10-30 18:55:19']

            t_date ="SELECT id  FROM `users_loan_agreement_signs` WHERE `cust_id` LIKE "+ str(j)+ " AND sign_date LIKE '" +str(date_nor) +"'"
            cur.execute(t_date)
            resttt = cur.fetchall()
            update_file = "UPDATE `users_loan_agreement_signs` SET `loan_agreement` = '" + str(on_data_nor) + "' WHERE `users_loan_agreement_signs`.`id` = " + str(resttt[0][0]);
            cur.execute(update_file)
            db.commit()
            print(cur.rowcount, "record(s) affected")


            ddd = findDay(list_t)
            ch_list = datetime.strptime(date_nor, '%Y-%m-%d %H:%M:%S').strftime(str(ddd)+' %b %d %H:%M:%S IST %Y')
            return ch_list



def generate_footer(footer):
    width, height = letter

    can = canvas.Canvas('footer.pdf', pagesize=letter)

    y = 0.20
    for i, j in footer.items():
        can.setFont("Helvetica", 8)
        can.drawString(0.198 * width, y * height, text=str(i) + str(j))
        y -= 0.01
    can.save()


def merge_pdf(target_pdf, convert, footer='footer.pdf'):

    v = os.path.abspath(target_pdf)
    target_pdf = PdfFileReader(v)
    pdf_writer = PdfFileWriter()
    if footer is not None:
        footer_page = PdfFileReader(footer).getPage(0)

    for page in range(target_pdf.getNumPages()):
        current_page = target_pdf.getPage(page)
        if footer is not None:
            if target_pdf.getNumPages()-1 == page:
                current_page.mergePage(footer_page)
            else:
                pass
        pdf_writer.addPage(current_page)

    with open(convert, 'wb') as pdf:
        pdf_writer.write(pdf)
    os.remove('footer.pdf')

try:
    sql = "SELECT cust_id FROM `users_loan_agreement_signs` WHERE `created_at` <= '2019-11-28 11:10:00'"
    cur.execute(sql)
    res = cur.fetchall()
    for i in res:
        a.append(i[0])
    list_data = list(dict.fromkeys(a))

    for j in list_data:
        file = '/var/www/html/public/storage/uploads/' + str(j)

        #file = os.getcwd() + '/' + str(j)

        try:
            files_path = [str(file)+'/'+x for x in os.listdir(str(file))]
            Date_Regex = re.compile(r'\d\d\d\d-\d\d-\d\d')
            Date_Reg = re.compile(r'\d\d-\d\d-\d\d\d\d')
            for f in files_path:
                if f.endswith(".pdf"):
                    try:
                         if Date_Reg.search(f).group() is not None:
                            nor_data.append(f)
                            datetime_s = Date_Reg.search(f).group()
                            datetime_object = datetime.strptime(datetime_s, '%d-%m-%Y').date()
                            aa = str(datetime_object)
                            filter_data.append(aa)
                    except Exception as e:
                        print(str(e)+'first'+j)
            sql = "SELECT sign_date FROM `users_loan_agreement_signs` WHERE cust_id LIKE "+str(j)

            cur.execute(sql)
            date_re = cur.fetchall()
            for d in date_re:
                nor_date.append(d[0])
                date = Date_Regex.search(d[0]).group()
                b.append(date)
            # nor_date = ['2019-11-22 15:07:30','2019-09-28 15:01:40','2019-11-21 15:17:30','2019-09-28 15:02:41','2019-09-28 15:03:42']
            # b = ['2019-09-28', '2019-11-21','2019-09-28', '2019-09-24', '2019-11-22', '2019-09-24','2019-09-28','2019-09-24']
            if b is not None:
                data_set = []
                try:
                    for team in [ele for ind, ele in enumerate(b,1) if ele not in b[ind:]]:
                        if b.count(team) >= 2:
                            f = open("double_found.txt", "a+")
                            if search():
                                exist = 'Yes'
                                get_data()
                            else:
                                exist = 'No'



                            f.write("Custome id:-  {}, Date of issue:-  {} No of Loans:- {} and File exist or no:- {} \n".format(j,team,b.count(team),exist))
                        else:
                            data_set.append(str(team))

                    t_set = set(data_set) & set(filter_data)
                    t_list = list(t_set)
                    for not_mat in t_list:
                        for dd in data_set:
                            if dd == not_mat:
                                data_set.remove(dd)
                    if t_list != []:
                        for list_t in t_list:
                            name_sql = "SELECT users_name, users_city  FROM `users_personal_infos` WHERE `cust_id` LIKE "+ str(j)
                            cur.execute(name_sql)
                            result_name = cur.fetchall()
                            # ADD FOOTER
                            for data_nor in nor_data:
                                ch_list = datetime.strptime(list_t, '%Y-%m-%d').strftime('%d-%m-%Y')
                                datet = Date_Reg.search(data_nor).group()
                                if datet == ch_list:
                                    on_data_nor = data_nor.split('/')[-1]
                                    footer = {
                                        "Digitally Signed by: ": "",
                                        'Name: ': str(result_name[0][0]).capitalize(),
                                        'Location: ': str(result_name[0][1]).capitalize(),
                                        "Reason: ": 'Loan Agreement',
                                        'Date: ': da_list(),
                                        }
                                    generate_footer(footer)
                                    merge_pdf(data_nor,data_nor)



                    if data_set != []:
                        for set_data in data_set:
                            f = open("double_found.txt", "a+")
                            f.write("Custome id:-  {}, Date of issue:-  {} No of Loans:- 1 and File exixt or no:- No \n".format(j, set_data))
                except Exception as e:
                    print(str(e)+'second')

            b= []
            data_set = []
            filter_data = []
            nor_data = []
            nor_date = []
            dou_date = []
            n_date = []
        except Exception as e:
            print(str(e)+'Third')
except Exception as e:
    print(str(e)+'fourth')
