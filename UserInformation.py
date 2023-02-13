from deepface import DeepFace
from BotSay import BotTalk
import cv2

COUNT = 0

bot_talk = BotTalk()


class UserInFormations:
    def __init__(self):
        self.user_details = []

    def get_user_details(self, user_image):
        if len(self.user_details) > 0:
            for data in self.user_details:
                image = data['user_image']
                uuid = data['unique_id']
                result = DeepFace.verify(user_image, image, enforce_detection=False)
                if result["verified"]:
                    bot_talk.say_speach(f"Verified Person name is : {data['name']}")
                    return data

    def new_user(self, name, user_image, unique_id, money):
        self.user_details.append({"name": name, "user_image": user_image, "unique_id": unique_id, "money": money})

    def send_user(self, user_image, money, duuid):
        count = 0
        if len(self.user_details) > 0:
            for data in self.user_details:
                name = data['name']
                image = data["user_image"]
                uuid = data['unique_id']
                result = DeepFace.verify(user_image, image, enforce_detection=False, model_name='Facenet512')
                print(result)
                count += 1
                if result['verified']:
                    print("Match")
                    cv2.destroyAllWindows()
                    success = self.confirmation(name, image, money, uuid, duuid)
                    if success:
                        return True
                    else:
                        return None
                elif len(self.user_details) == count:
                    print("Doesn't match...")
                    return None
        else:
            print("Doesn't have user")
            return None

    def money_sent(self, money, uuid):
        for i, data in enumerate(self.user_details):
            if uuid == data['unique_id']:
                self.user_details[i]['money'] += money
                bot_talk.say_speach("Money Transfer complete")

    def confirmation(self, name, image, money, uuid, duuid):
        bot_talk.say_speach(f"Verified person name is {name}")
        while True:
            bot_talk.say_speach("If you conform")
            conf_input = bot_talk.input_speach()
            print(conf_input)

            if conf_input.find('yes') != -1 or conf_input.find('YES') != -1:
                self.money_sent(money, uuid)
                self.decrease_self_user_money(money, duuid)
                return True
            elif conf_input.find('no') != -1 or conf_input.find('NO') != -1:
                return False


    def decrease_self_user_money(self, money, duuid):
        for i, data in enumerate(self.user_details):
            if duuid == data['unique_id']:
                self.user_details[i]['money'] -= money
                print(f"Your money have this time: {self.user_details[i]['money']}")
                bot_talk.say_speach(f"Your money have this time {self.user_details[i]['money']}")
