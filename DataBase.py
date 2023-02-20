# It's actual Data base version control your user data and some operation

import mysql.connector
import base64
from deepface import DeepFace
import uuid
import cv2
import numpy as np
from BotSay import BotTalk

class DataBaseConnect:
    def __init__(self):
        self.db = mysql.connector.connect(user='root', password='zen369zen',
                                          host='localhost',
                                          database='testdb')
        self.cursor = self.db.cursor()
        self.bot_talk = BotTalk()

    def add_new_user(self, first_name, last_name, image_path, money):
        unique_id = f'{uuid.uuid1()}'
        image = open(image_path, 'rb').read()
        encoded_string = base64.b64encode(image)
        args = (first_name, last_name, unique_id, encoded_string, money)
        sql = "INSERT INTO customerdata(FIRST_NAME,LAST_NAME,UUID,IMAGE,MONEY) VALUES(%s,%s,%s,%s,%s)"
        self.cursor.execute(sql, args)
        self.db.commit()

    def delete_all_data(self):
        sql = "delete from customerdata"
        self.cursor.execute(sql)
        self.db.commit()

    def get_all_data(self):
        sql = 'select * from customerdata'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def get_self_user_data(self, img):
        data = self.get_all_data()
        count = 0
        if len(data) > 0:
            for dt in data:
                count += 1
                img_base = base64.b64decode(dt[3])
                nparr = np.fromstring(img_base, np.uint8)
                img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # cv2.IMREAD_COLOR in OpenCV 3.1
                result = DeepFace.verify(img, img_np, enforce_detection=False, model_name='Facenet512')
                if result['verified']:
                    self.bot_talk.say_speach("Match Successfully")
                    return dt
                elif count == len(data):
                    self.bot_talk.say_speach("Don't match this person")
        else:
            self.bot_talk.say_speach("Doesn't have any data in your database")
            return None

    def check_user_image(self, user_image, money, self_uuid):
        is_match = 'None'
        data = self.get_all_data()
        if len(data) > 0:
            for dt in data:
                img_base = base64.b64decode(dt[3])
                nparr = np.fromstring(img_base, np.uint8)
                img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # cv2.IMREAD_COLOR in OpenCV 3.1
                result = DeepFace.verify(user_image, img_np, enforce_detection=False, model_name='Facenet512')
                print(result)
                if result['verified']:
                    is_match = 'Not None'
                    self.bot_talk.say_speach("Match Successfully")
                    cv2.destroyAllWindows()
                    success = self.confirmation(dt, self_uuid, money)
                    if success == 'success':
                        return 'success'
                    elif success == 'home':
                        return 'home'
                    else :
                        return 'no'
                elif is_match == 'Not None':
                    print("Doesn't match...")
                    return None
        else:
            print("Doesn't have user")
            return None

    def confirmation(self, data, duuid, money):
        first_name = data[0]
        last_name = data[1]
        send_uuid = data[2]
        user_money = data[4]
        self.bot_talk.say_speach(f"Verified person name is {first_name} {last_name}")
        while True:
            self.bot_talk.say_speach("If you conform")
            conf_input = self.bot_talk.input_speach()
            print(conf_input)

            if conf_input.find('yes') != -1 or conf_input.find('YES') != -1:
                self.money_sent(money, send_uuid, user_money)
                self.decrease_self_user_money(money,duuid)
                return 'success'
            elif conf_input.find('no') != -1 or conf_input.find('NO') != -1:
                return "no"
            elif conf_input.find('home') != -1 or conf_input.find("HOME") != -1:
                return 'home'

    def money_sent(self, money, uuid, user_money):
        sql = '''UPDATE customerdata 
        SET MONEY = %s 
        WHERE UUID = %s'''
        self.cursor.execute(sql, (money + user_money, uuid))
        self.db.commit()
        self.bot_talk.say_speach("Money Transfer complete")

    def decrease_self_user_money(self, money, duuid):
        sql = '''SELECT MONEY FROM customerdata 
                        WHERE UUID = %s'''
        self.cursor.execute(sql, (duuid,))

        data = self.cursor.fetchall()
        c_money = data[0][0] - money
        sql = '''UPDATE customerdata
                SET MONEY = %s
                WHERE UUID = %s'''
        self.cursor.execute(sql, (c_money, duuid))
        self.db.commit()
        self.bot_talk.say_speach(f"Your money have this time {c_money}")

    def close(self):
        self.db.close()





