import pymysql
import os
import csv

def main():
    dbname = 'guest1_YAKOVLEVA_VK'
    conn = pymysql.connect(host='localhost', user='guest1', passwd ='n76Je4=wx6H', charset = 'utf8mb4')
    cur = conn.cursor()
    sql = 'create database ' + dbname + ' DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;'
    try:
        cur.execute(sql)
    except: 
        print(Exception)
    cur.execute('use ' + dbname + ';')
    try:
        cur.execute('create table metadata (id INT, sex INT(2), age INT, PRIMARY KEY(id));')
    except: 
        print('table already exists')
    with open('meta.csv', newline='', encoding = 'utf-8') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',')
        for row in spamreader:
            db_row = "'" + str(row['uid']) + "','" + str(row['sex']) + "','" + str(row['age']) + "'"
            cur.execute('insert into metadata (id, sex, age) value(' + db_row + ');')
    try:
        cur.execute('create table walls (id INT, date INT, text VARCHAR, PRIMARY KEY(id)) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;')
    except:
        print('table already exists')
    with open('tara.csv', newline='', encoding = 'utf-8') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',')
        for row in spamreader:
            db_row1 = "'" + str(row['id']) + "','" + str(row['date']) + "','" + row['post'] + "'"
            cur.execute('insert into walls (id, date, text) value(' + db_row1 + ');')
            
    conn.commit()
    cur.close()
    conn.close()
    
if __name__ == '__main__':
    main()
        
