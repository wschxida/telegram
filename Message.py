# 20191217
# made by YHM
# 获取telegram 群消息数据的程序入口
# 使用格式：
# 1.python.exe D:/code/telegram/Message.py -u [username]
# 2.python.exe D:/code/telegram/Message.py -i [filename]


from configparser import ConfigParser
from src.TelegramChannelMessageExtractor import TGMsgExtrator
import sys, getopt
import os


def main(argv,tgMsgExtrator):
    inputfile = ''
    username = ''
    try:
        opts, args = getopt.getopt(argv,"hi:u:",["ifile=","uname="])
    except getopt.GetoptError:
        print('Message.py -i <inputfile> -u <username>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Message.py -i <inputfile> -u <username>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            break
        elif opt in ("-u", "--uname"):
            username = arg
            break
    if inputfile != '':
        f = open(inputfile, 'r')
        result = list()
        for line in f.readlines():
            line = line.strip('\n')
            result.append(line)
            # print(line)
            tgMsgExtrator.set_channel(line)
            tgMsgExtrator.dumpTojson()
        # print(result)
        f.close()
    elif username != '':
        tgMsgExtrator.set_channel(username)
        tgMsgExtrator.dumpTojson()


cfg = ConfigParser()
cur_path = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(cur_path, 'config/telegram_extractor.ini')
cfg.read(config_file, encoding='utf-8')
config = {
    'msg_max_limit': int(cfg.get('message_lim', 'msg_max_limit')),
    'TG_session_name': cfg.get('login_setting', 'TG_session_name'),
    'TG_api_id': int(cfg.get('login_setting', 'TG_api_id')),
    'TG_api_hash': cfg.get('login_setting', 'TG_api_hash'),
    'proxy_address': cfg.get('login_setting', 'proxy_address'),
    'proxy_port': int(cfg.get('login_setting', 'proxy_port')),
    'group_message': cfg.get('download_addr', 'group_massage'),
    'media_path': cfg.get('download_addr', 'media_path'),
}

tgMsgExtrator = TGMsgExtrator(config)
main(sys.argv[1:],tgMsgExtrator)

# tgMsgExtrator.set_channel('Selena_FanClub')
# tgMsgExtrator.dumpTojson()
# tgMsgExtrator.download_message_media('Selena_FanClub',1032)