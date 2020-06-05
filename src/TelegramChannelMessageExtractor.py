import socks
import json,os
from telethon import TelegramClient


class TGMsgExtrator:
    def __init__(self, config):
        self.msg_lim = config['msg_max_limit']
        self.session_name = config['TG_session_name']
        self.api_id = config['TG_api_id']
        self.api_hash = config['TG_api_hash']
        self.proxy_address = config['proxy_address']
        self.proxy_port = config['proxy_port']
        self.message_path = config['group_message']
        self.media_path = config['media_path']
        self.channel_username = ''
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash,
                                     proxy=(socks.HTTP, self.proxy_address, self.proxy_port))

    def set_channel(self, username):
        self.channel_username = username

    async def get_message(self):
        msg_dict = []
        try:
            chat_item = await self.client.get_entity(self.channel_username)
        except ValueError:
            print("ValueError:No channel has\"", self.channel_username, "\"as username")
            return msg_dict
        messages = self.client.iter_messages(chat_item, limit=self.msg_lim)
        async for message in messages:
            # action 一般是新成员加入的提醒消息，过滤
            if message.action:
                # print('message:' + str(message.action))
                continue

            has_media = False
            path = ''
            if message.media:
                has_media = True
                if 'MessageMediaDocument' in str(message.media):
                    path = os.path.join(self.media_path, str(chat_item.username), str(message.id)+'.mp4')
                else:
                    path = os.path.join(self.media_path, str(chat_item.username), str(message.id) + '.jpg')

                is_exist = os.path.isfile(path)
                # print(is_exist)
                if not is_exist:
                    download_result = await message.download_media(path)
                    print(download_result)

            msg = {
                "article_detail": {
                    "article_url": "https://t.me/" + self.channel_username,
                    "domain_code": "telegram.org",
                    "media_type_code": "c",
                    "author_name": chat_item.title,
                    "author_account": chat_item.username,
                    "author_id": chat_item.id,
                    "article_pubtime_str": str(message.date),
                    "article_pubtime": message.date.isoformat(timespec='microseconds'),
                    "article_title": message.message,
                    "article_HasMedia": has_media,
                    "message_id": message.id,
                    "media_path": path,
                },
                "article_application": {
                    "application_name": "Telegram",
                    "chat_group_name": chat_item.title
                }
            }
            msg_dict.append(msg)
        print("get channel Message successfully")
        os.makedirs(self.message_path,exist_ok=True)
        file = self.message_path+chat_item.username+".json"
        print(file)
        with open(file, "w") as f:
            json.dump(msg_dict, f, sort_keys=True, indent=4, separators=(',', ':'), default=str)
        print("加载入文件完成...")

        return msg_dict

    def dumpTojson(self):
        with self.client:
            self.client.loop.run_until_complete(self.get_message())
