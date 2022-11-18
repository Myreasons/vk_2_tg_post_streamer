import toml
from vk_listener import VkListener, VkPost
import time
from tg_pooler import TgBot
import logging


logging.basicConfig(filename='work.log', encoding='utf-8', level=logging.INFO)


with open('settings.toml', 'r') as f:
    settings = toml.load(f)


def get_actual_posts(posts, timedelta: int):
    current_time = int(time.time())
    res_list = []
    for post in posts:
        if post['date'] >= current_time - timedelta:
            photos = []
            if 'attachments' in post.keys():
                for attach in post['attachments']:
                    if attach['type'] == 'photo':
                        photos.append(attach['photo']['sizes'][-1]['url'])

            if 'copy_history' in post.keys():
                for tmp_post in post['copy_history']:
                    tmp_photos = []
                    if 'attachments' in post.keys():
                        for tmp_attach in tmp_post['attachments']:
                            if attach['type'] == 'photo':
                                tmp_photos.append(tmp_attach['photo']['sizes'][-1]['url'])

                    res_list.append(VkPost(date=tmp_post['date'],
                                           from_id=tmp_post['from_id'],
                                           post_type=tmp_post['post_type'],
                                           text=tmp_post['text'],
                                           files=tmp_photos)
                                    )

            res_list.append(VkPost(date=post['date'],
                                   from_id=post['from_id'],
                                   post_type=post['post_type'],
                                   text=post['text'],
                                   files=photos)
                            )
    return res_list


def run(timedelta):
    vk = VkListener(settings['vk']['phone'], settings['vk']['pass'])
    tg = TgBot(settings['tg']['token'])

    for page_id in settings['vk']['page_id']:
        logging.info(f'Start with VK page id = {page_id}')
        posts = vk.listen(pageid=page_id)
        actual_posts = get_actual_posts(posts, timedelta=timedelta)
        logging.info(f'Get {actual_posts} actual post(s)')

        logging.info('Start sending telegram messages')
        for post in actual_posts:
            tg.send_post(f'{post.date}\n{post.text}', post.files, settings['tg']['target_id'])


if __name__ == '__main__':
    timedelta = settings['main']['timedelta']
    logging.info(f'Start working with time delta = {timedelta}')
    while True:
        logging.info('Run pooling')
        run(timedelta)
        time.sleep(timedelta)
