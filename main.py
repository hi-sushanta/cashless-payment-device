from BotSay import *
import cv2
from DataBase import DataBaseConnect

bot_talk = BotTalk()
database = DataBaseConnect()
vid_cap = cv2.VideoCapture(0)  # Access the webcam

# # Sample Demo user
chi_details = {"first_name": "Che",'last_name':'Das', "image": "my_smart_image2.jpg", "money": 500}
zen_details = {"first_name": "Zen", 'last_name':'Das','image': "zen.jpg", 'money': 200}

# This is demo code for add new user
# database.add_new_user(chi_details['first_name'],chi_details['last_name'],chi_details['image'],chi_details['money'])
# database.add_new_user(zen_details['first_name'],zen_details['last_name'],zen_details['image'],zen_details['money'])

img = cv2.imread(chi_details['image'])
device_user_detail = database.get_self_user_data(img)


face_detect_run = False

if device_user_detail is not None:
    self_user_firstname = device_user_detail[0]
    self_user_lastname = device_user_detail[1]
    self_user_uuid = device_user_detail[2]
    self_user_money = device_user_detail[4]
    while True:
        try:
            question = "How much money to Pay: "
            bot_talk.say_speach(question)
            money = bot_talk.input_speach()
            money = money.replace("Rs", "").replace("$", "").replace("rupees", "").replace('dollar','').replace("dollars",'')
            print(money)

            if money.find("home") != -1 or money.find("HOME") != -1:
                bot_talk.say_speach("OK Bro, I stop it")
                break
            else:
                money = int(money)
                if money > self_user_money:
                    bot_talk.say_speach("your money is low try again")

                elif money <= self_user_money:
                    face_detect_run = True
                    bot_talk.say_speach("Please turn your camera to face")
                    break
        except ValueError:
            bot_talk.say_speach("It's not a money Please try again.")
            pass

if face_detect_run:

    while True:
        is_frame, frame = vid_cap.read()
        success = False
        if not is_frame:
            break
        cv2.imshow('Face', frame)
        key = cv2.waitKey(1)
        if key == ord('q') or key == ord("Q") or key == 27:
            break
        send_user = database.check_user_image(frame, money, self_user_uuid)
        if send_user == 'success':
            break
        elif send_user == 'home':
            bot_talk.say_speach("OK Bro, I Stop it")
            break
        else:
            continue

vid_cap.release()
database.close()
