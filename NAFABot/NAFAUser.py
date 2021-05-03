class UserCredentials:



    def __init__(self, userName, passWord, clientID, clientSecret, imgurID, imgurSecret):
        self.userName = userName
        self.passWord = passWord
        self.clientID = clientID
        self.clientSecret = clientSecret
        self.imgurID = imgurID
        self.imgurSecret = imgurSecret

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

