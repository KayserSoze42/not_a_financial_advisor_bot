class UserCredentials:



    def __init__(self, userName, passWord, clientID, clientSecret, imgurID, imgurSecret):
        self.userName = userName
        self.passWord = passWord
        self.clientID = clientID
        self.clientSecret = clientSecret
        self.imgurID = imgurID
        self.imgurSecret = imgurSecret
        self.userGithub = ""
        self.subreddit = ""

    def getUserNameAndPassword(self):
        print("Enter your Reddit Username")
        self.userName = input(">>")
        print("Enter your Reddit Password")
        self.passWord = input(">>")

    def getClientIDAndSecret(self):
        print("Enter your App Client ID")
        self.clientID = input(">>")
        print("Enter your App Client Secret")
        self.clientSecret = input(">>")

    def setGithub(self, url):
        self.userGithub = url

    def setSubreddit(self, url):
        self.subreddit = url

    def getGithub(self):
        return self.userGithub

    def getSubreddit(self):
        return self.subreddit

    def getUsername(self):
        return self.userName

    def getPassword(self):
        return self.passWord

    def getClientID(self):
        return self.clientID

    def getClientSecret(self):
        return self.clientSecret

    def getAPIKey(self):
        return self.userAPIKey

    def getImgurID(self):
        return self.imgurID

    def getImgurSecret(self):
        return self.imgurSecret

