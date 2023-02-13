from UserInformation import *
from BotSay import *
import uuid
import cv2
import numpy as np

vid_cap = cv2.VideoCapture(0)  # Access the webcam
User = UserInFormations()
bot_talk = BotTalk()

# Sample Demo user
one_image = {"name": "Che", "image": "my_smart_image2.jpg", "money": 500}
zen_image = {"name": "Zen", 'image': "zen.jpg", 'money': 200}
user_image = [one_image, zen_image]

for data in user_image:
    img = cv2.imread(data["image"])
    User.new_user(name=data["name"], user_image=img, unique_id=uuid.uuid1(), money=data['money'])

device_user = User.get_user_details(one_image['image'])


# user_information = User.get_user_details(image)
#
# #



while True:
    try:
        question = "How much money to Pay: "
        bot_talk.say_speach(question)
        money = bot_talk.input_speach()
        money = int(money.replace("Rs","").replace("$","").replace("rupees",""))
        print(money)
        if money > device_user['money']:
            bot_talk.say_speach("your money is low try again")
        elif money == "home" or money == "HOME":
            bot_talk.say_speach("OK i stop it")
            break
        elif money <= device_user['money']:
            break
    except ValueError:
        bot_talk.say_speach("It's not a money")
        pass

while True:
    is_frame, frame = vid_cap.read()
    success = False
    if not is_frame:
        break
    cv2.imshow('Face', frame)
    key = cv2.waitKey(1)
    if key == ord('q') or key == ord("Q") or key == 27:
        break
    send_user = User.send_user(frame, money, device_user['unique_id'])
    if send_user:
        print(send_user)
        break

vid_cap.release()
cv2.destroyAllWindows()
