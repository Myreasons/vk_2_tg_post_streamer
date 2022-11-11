import telebot


class TgBot:
    def __init__(self, token: str):
        self.bot = telebot.TeleBot(token, parse_mode=None)

    def send_post(self, post_text, photos, target_id):
        if len(str(post_text)) > 0:
            self.bot.send_message(target_id, str(post_text))
        if len(photos) > 0:
            self.bot.send_media_group(target_id, [telebot.types.InputMediaPhoto(x) for x in photos])

