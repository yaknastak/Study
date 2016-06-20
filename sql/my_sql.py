import pymysql
import os
import csv

def main():
    dbname = 'guest1_YAKOVLEVA_VK'
    conn = pymysql.connect(host='localhost', user='guest1',db = 'guest1_vk', passwd ='n76Je4=wx6H', charset = 'utf8')
    cur = conn.cursor()
    sql = 'CREATE DATABASE ' + dbname + ' DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;'
    try:
        cur.execute(sql)
    except: 
        print(Exception)
    cur.execute('use ' + dbname + ';')
    try: cur.execute('CREATE TABLE metadata (id INT, sex INT(2), PRIMARY KEY(id));')
    except: print('table already exists')
    with open('meta.csv', encoding = 'utf-8') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',')
        for row in spamreader:
            db_row = "'" + str(row['uid']) + "','" + str(row['sex']) + "'"
            cur.execute('INSERT INTO metadata (id, sex) VALUE(' + db_row + ');')
    try: cur.execute('CREATE TABLE walls (id INT, date INT, text VARCHAR(20000)) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;')
    except: print('table already exists')
    with open('tara.csv', newline='', encoding = 'utf-8') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',')
        for row in spamreader:
            db_row1 = "'" + str(row['id']) + "','" + str(row['date']) + "','" + row['post'] + "'"
            try:
                cur.execute('INSERT INTO walls (id, date, text) value(' + db_row1 + ');')
            except:
                print(row['post'])
            
    conn.commit()
    cur.close()
    conn.close()
    
if __name__ == '__main__':
    main()
        
