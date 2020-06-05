# 20191217
# made by YHM
# 获取telegram 群成员数据的程序入口
# 使用格式：
# 1.python.exe D:/code/telegram/Member.py -u [username] -d [True/False]
# 2.python.exe D:/code/telegram/Member.py -i [filename] -d [True/False]
# -u [username] 和-i [filename]二者必须填写一个
# -d [True/False]，程序默认为False，表示不下载群成员头像图片，True为下载群成员图片

import sys, getopt
from configparser import ConfigParser
from src.TelegramChannelMemberExtractor import TGMemExtrator

def main(argv,tgMemExtrator):
    inputfile = ''
    username = ''
    flag = False
    try:
        opts, args = getopt.getopt(argv,"hi:u:d",["ifile=","uname=","dflag"])
    except getopt.GetoptError:
        print('Member.py -i <inputfile> -u <username>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Member.py -i <inputfile> -u <username> -d <downloadflag>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-u", "--uname"):
            username = arg
        elif opt in ("-d", "--dflag"):
            flag = bool(arg)
    if inputfile != '' :
        f = open(inputfile, 'r')
        result = list()
        for line in f.readline():
            result.append(line)
            # username = 'JapaneseSpeaking'
            tgMemExtrator.set_channel(line)
            tgMemExtrator.dumpTojson(flag)
        print("get",line)
        f.close()
    elif username != '':
        tgMemExtrator.set_channel(username)
        tgMemExtrator.dumpTojson(flag)


cfg = ConfigParser()
cfg.read('./config/telegram_extractor.ini', encoding='utf-8')
config = {
    'TG_session_name': cfg.get('login_setting', 'TG_session_name'),
    'TG_api_id': int(cfg.get('login_setting', 'TG_api_id')),
    'TG_api_hash': cfg.get('login_setting', 'TG_api_hash'),
    'proxy_address': cfg.get('login_setting', 'proxy_address'),
    'proxy_port': int(cfg.get('login_setting', 'proxy_port')),
    'group_member': cfg.get('download_addr', 'group_member'),
    'group_avatar': cfg.get('download_addr', 'group_avatar')
}
tgMemExtrator = TGMemExtrator(config)
main(sys.argv[1:],tgMemExtrator)

# spunkyweb\\glasgowjobs
# tgMemExtrator.set_channel('yinxiangbiji_news')
# tgMemExtrator.dumpTojson(False)