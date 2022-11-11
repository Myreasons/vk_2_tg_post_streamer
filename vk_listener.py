import vk_api
import datetime


class VkPost:
    def __init__(self, date, from_id, post_type, text, files=[]):
        self.date = datetime.datetime.fromtimestamp(date)
        self.from_id = from_id
        self.post_type = post_type
        self.text = text
        self.files = files


class VkListener:
    def __init__(self, phone: str, pw: str):
        try:
            self.vk_session = vk_api.VkApi(phone, pw)
            self.vk_session.auth()
            self.vk = self.vk_session.get_api()
        except vk_api.exceptions.Captcha as captcha:
            captcha.sid  # getting sid
            captcha.get_url()  # getting captha url
            print(f"Нужно ввести капчу. Открой {captcha.get_url()}\nВведи капчу сюда:\n")
            user_captcha = input()
            captcha.try_again(user_captcha)

    def listen(self, pageid: int):
        posts = self.vk.wall.get(owner_id=-pageid)
        return posts['items']

    def get_photo(self, owner_id, album_id, photo_ids):
        return self.vk.photos.get(owner_id=-owner_id,
                                  album_id=album_id,
                                  photo_ids=photo_ids)

    def get_vieo(self, owner_id, videos):
        return self.vk.video.get(owner_id=-owner_id, videos=videos)
