
# 2020-05-21
# created by YHM
# save channel message
class channelEnitity(object):
    def __init__(self):
        super().__init__()
        self.channel_id = ""
        self.channel_account = ""
        self.channel_name = ""
        self.channel_type = ""
        self.channel_description = ""
        self.channel_url = ""

        self.channel_avatar_url = ""
        self.channel_avatar_base64 = ""
        self.channel_avatar_store_directory_root = ""
        self.channel_avatar_local_filename = ""

        self.channel_member_count = 0
        self.channel_create_time = None

        self.members = []

    def initWithChannel(self, channel):
        self.channel_id = channel.id
        # 提取username
        if channel.username is not None:
            self.channel_account = channel.username
            url = "https://t.me/" + channel.username
            self.channel_url = url
        if channel.title is not None:
            self.channel_name = channel.title
        self.channel_type = "telegram"
        self.channel_create_time = channel.date.isoformat(timespec='microseconds')

    def set_Avatar(self, path, filename):
        self.channel_avatar_store_directory_root = path
        temp = filename.split('\\')
        self.channel_avatar_local_filename = temp[-1]
        self.channel_avatar_url = filename

    def set_Member_Account(self,account):
        self.channel_member_count = account

    def add_Member(self,mem,flag=False):
        if flag :
            self.members = []
        self.members.append(mem)