import os
import vk
import csv
from datetime import date
from time import sleep

def dirs (x):
    #для создания новых директорий
    if os.path.exists(x) == False:
        return(os.makedirs(x))

def get_users(city, count, meta_file, api):
    """
    составляет csv-файл с метаданными пользователей (id, пол, возраст, знание языков). city - id населенного пункта, count - запрашиваемое кол-во пользователей, meta_file - файл, в который будут записаны данные. Возвращает массив id пользователей. 
    """
    users = api.users.search(city = city, count=count, fields="sex,bdate,personal")[1:]
    id_list = []
    with open(meta_file, 'w', newline='', encoding = 'utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar = '"',
                                quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['uid'] + ['sex'] + ['age'] + ['langs'])
        for user in users:
            uid = user['uid']
            id_list.append(uid)
            sex = user['sex']
            if 'bdate' in user:
                if len(user['bdate'].split('.')) >= 3:
                    birth_year = user['bdate'].split('.')[2]
                    age = date.today().year - int(birth_year)
                else:
                    age = ''      
            else:
                age = ''
            if 'personal' in user:
                if 'langs' in user['personal']:
                    langs = ','.join(user['personal']['langs'])
                else:
                    langs = ''
            else:
                langs = ''
            
            spamwriter.writerow([str(uid)] + [sex] + [str(age)] + [langs])
    return(id_list)

def get_posts(users, count, api):
    """
    собирает записи, сделанные пользователями. Создает директорию 'Tara' (название города) и внутри нее - отдельную папку для каждого пользователя, в которую помещаются скачанные текстовые файлы. Users - список id пользователей, count  - количество запрашиваемых постов от каждого пользователя. 
    """
    rdir = 'Tara/'
    dirs(rdir)

    for id in users:
        cnt = 1
        new_dir = rdir + str(id)
        dirs(new_dir) 
        wall = api.wall.get(owner_id=id, filter="owner", count=count)
        for post in wall:
            try:
                if 'copy_owner_id' not in post:
                    fname = new_dir + '/' + str(cnt) + '.txt'
                    f = open(fname, 'w', encoding='utf-8')
                    f.write(post['text'] + '\n')
                    f.close()
                    cnt += 1
            except: 
                continue
        sleep(0.3)

def main():
    appid = ''
    login = ''
    password = ''
    session = vk.AuthSession(app_id=appid, user_login=login, user_password=password)
    api = vk.API(session)
    users = get_users(7402, 999, 'meta.csv', api)
    #city_id = 7402 (Тара)
    get_posts(users, 100, api)
    
if __name__ == '__main__':
    main()

    
        
            
