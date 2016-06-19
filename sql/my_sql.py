import pymysql
import os
import csv
from datetime import datetime

def main(password):
    dbname = 'guest1_YAKOVLEVA_VK'
    conn = pymysql.connect(host=localhost, user='guest1', password=password, charset = 'utf-8')
    cur = conn.cursor()
    sql = 'create database ' + dbname + ' DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;'
    try:
        cur.execute(sql)
    except: 
        print(Exception)
    cur.execute('use ' + dbname + ';')
    cur.execute('create table metadata (id INT, sex INT(2), age INT, PRIMARY KEY(id));')
    with open('meta.csv', newline='') as csvfile:
        spamreader = csv.reader('meta.csv', delimiter='\t')
        for row in spamreader:
            db_row = str(row['uid']) + ',' + str(row['sex']) + ',' + str(row['age'])
            cur.execute('insert into meta (id, sex, age) value(db_row);')
    cur.execute('create table walls (id INT, date, text, PRIMARY KEY(id)), DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;')
    with open('tara.csv', newline='') as csvfile:
        spamreader = csv.reader('tara.csv', delimiter='\t')
        for row in spamreader:
            db_row = str(row['id']) + ',' + str(row['date']) + ',' + row['post']
            cur.execute('insert into walls (id, date, text) value(db_row);')
            
    conn.commit()
    cur.close()
    conn.close()
    
if __name__ == '__main__':
    password = input('Enter password ')
    main(password)
        