import requests
import os

class GroupMeBot():
    def __init__(self, token, botId, groupId):
        self.baseUrl = "https://api.groupme.com/v3"

        self.token = token
        self.botId = botId
        self.groupId = groupId

        self.timeofLastPost = 0
        self.getNewMsgs()

        self.functionDict = {}

    def checkForCommands(self, m=10):
        new = self.getNewMsgs(m)
        print(new)
        for msg in new:
            statements = msg['text'].strip().split(" ")
            print(statements)
            for key in self.functionDict:
                if statements[0] == key:
                    statements.remove(key)
                    try:
                        self.functionDict[key](*statements)
                    except TypeError:
                        self.postMsg("Too many parameters for command")
                        

    def postMsg(self, msg, imgUrl=None):
        if type(msg) is not str:
            raise TypeError('msg parameter is not of type str')

        postUrl = "{}/bots/post?token={}".format(self.baseUrl, self.token)
        
        data = {
            "bot_id"  : self.botId,
            "text"    : msg
        }

        if imgUrl:
            data["picture_url"] = imgUrl

        r = requests.post(postUrl, data)
        print(r)

    def getLatestPosts(self, numPosts):
        getUrl = "{}/groups/{}/messages?limit={}&token={}".format(self.baseUrl, self.groupId, numPosts, self.token)
        r = requests.get(getUrl).json()
        posts = r['response']['messages']
        return posts

    def getLatestPost(self):
        return self.getLatestPosts(1)[0]

    def getLatestMsgs(self, numMessages):
        msgs = []
        for post in self.getLatestPosts(numMessages):
            if post['text']:
                msgs.append(post['text'])
            else:
                msgs.append("")
        return msgs

    def getMembers(self):
        getUrl = "{}/groups/{}?token={}".format(self.baseUrl, self.groupId, self.token)
        r = requests.get(getUrl).json()
        members = r['response']['members']
        return members

    def getNewMsgs(self, m=20):
        msgs = self.getLatestPosts(m)
        msgs.reverse()
        new = []
        for msg in msgs:
            if msg["created_at"] > self.timeofLastPost:
                new.append(msg)
                self.timeofLastPost = msg["created_at"]
        return new


if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")
    BOT_ID = os.getenv("BOT_ID")
    GROUP_ID = os.getenv("GROUP_ID")

    bot = GroupMeBot(TOKEN, BOT_ID, GROUP_ID)
    bot.postMsg("HI")
    # print(bot.getLatestMsgs(5))
