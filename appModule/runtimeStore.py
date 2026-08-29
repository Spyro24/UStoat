import pygame as p
import io

class runtimeStore:
    def __init__(self):
        self.userID = None #We need it only for user ID stuff like resolving the names of DM channels
        self.messages = {"000":{"content": "This is a Dummy channel", "author": "0000", "deleted": False, "edited": False}}
        self.channels = {"00":{"messages":["000"], "name":"<Dummy>", }}
        self.users = {}
        self.servers = {"0":{"name": "Direct Messages", "owner": None, "channels": []}}
        self.images = {"avatars":{}}
        self.createDummyUser("0000")
        #making the dummy user to the ustoat user
        self.images['avatars']["0000"] = p.image.load("./res/icons/app_icon_x384.png") #set the PFP
        self.users["0000"].pop("dummy")
        self.users["0000"]["username"] = "<UStoat> System"
        
    
    def insertMessage(self, messageId: str, content: str, author: str, deleted=False, edited=False):
        self.messages[messageId] = {"content": content, "author": author, "deleted": deleted, "edited": edited}
    
    def parseStoatMessage(self, package): #I dont want to add hundreds of lines to the main app
        if "system" in package:
            message = {}
            message["author"] = "0000" #set the author to the system user
            string = ""
            string += package["system"]["id"]
            message["content"] = string
            self.messages[package["_id"]] = message
            self.channels[package["channel"]]['messages'].append(package["_id"])
            return #we cannot parse system messages curently
        if not package["author"] in self.users: self.createDummyUser(package["author"])
        message = {}
        message["author"] = package["author"]
        message["channel"] = package["channel"]
        if "user" in package:
            self.parseStoatUser(package["user"])
        if "content" in package:
            message["content"] = package["content"]
        if "replies" in package:
            message["replies"] = package["replies"]
        self.messages[package["_id"]] = message
        try:
            self.channels[message["channel"]]["messages"].append(package["_id"])
        except: #creating a dummy channel
            self.channels[message["channel"]] = {}
            self.channels[message["channel"]]["messages"] = []
            self.channels[message["channel"]]["messages"].append(package["_id"])
    
    def insertChannel(self):
        pass
    
    def parseStoatChannel(self, package):
        channel = {}
        if package["channel_type"] == "DirectMessage":
            self.servers['0']['channels'].append(package["_id"]) #Add the channel to the DM server
            package["recipients"].remove(self.userID)
            if "display_name" in self.users[package["recipients"][0]]:
                channel["name"] = self.users[package["recipients"][0]]["display_name"]
            else:
                channel["name"] = self.users[package["recipients"][0]]["username"]
        elif package["channel_type"] == "TextChannel":
            channel["name"] = package["name"]
            if "description" in package:
                channel["description"] = package["description"]
        channel["messages"] = []
        channel["typing"] = set()
        self.channels[package["_id"]] = channel
    
    def setTypingStatus(self, packet):
        if packet["type"] == "ChannelStartTyping":
            self.channels[packet["id"]]["typing"].add(packet["user"])
        elif packet["type"] == "ChannelStopTyping":
            self.channels[packet["id"]]["typing"].discard(packet["user"])
    
    def parseStoatUser(self, package):
        if package["_id"] in self.users:
            if not "dummy" in self.users[package["_id"]]:
                return
        user = {}
        user["username"] = package["username"]
        user["discriminator"] = package["discriminator"]
        if "display_name" in package:
            user["display_name"] = package["display_name"]
        if "avatar" in package:
            user["avatarId"] = package["avatar"]["_id"]
        user["online"] = package["online"]
        user["status"] = None
        user["presence"] = None
        if "status" in package:
            if "text" in package["status"]:
                user["status"] = package["status"]["text"]
            if "presence" in package["status"]:
                user["presence"] = package["status"]["presence"].lower()
        self.users[package["_id"]] = user
    
    def parseStoatServer(self, package):
        server = {}
        server["name"] = package["name"]
        server["owner"] = package["owner"]
        server["channels"] = package["channels"]
        server["members"] = []
        self.servers[package["_id"]] = server
    
    def createDummyUser(self, userId):
        user = {}
        user["username"] = userId
        user["discriminator"] = "0000"
        user["dummy"] = None # Only a Dummy user has this
        user["online"] = False
        if not userId in self.users: #makes sure that we dont overwrite a user in the user database 
            self.users[userId] = user
    
    def make_square_and_scale(self, surface: p.Surface):
        orig_width, orig_height = surface.get_size()
        square_size = min(orig_width, orig_height)
        square_surface = p.Surface((square_size, square_size), p.SRCALPHA)
        x = (square_size - orig_width) // 2
        y = (square_size - orig_height) // 2
        square_surface.blit(surface, (x, y))
        return square_surface

    def create_circular_surface(self, surface):
        circleSurface = p.Surface(surface.get_size(), flags=p.SRCALPHA)
        circleSurface.fill((0,0,0,255))
        p.draw.ellipse(circleSurface, (0,0,0,0), circleSurface.get_rect())
        surface.blit(circleSurface, (0,0), special_flags=p.BLEND_RGBA_SUB)
        return surface
        
class runtimeStoreManager:
    def __init__(self, app):
        self.app = app
        self.runtimeStore = self.app.modules["runtimeStore"]
        self.requetHandler = self.app.modules["requestHandler"]
        self.platform = self.app.modules["platform"]
        self.defaultAvatar = p.image.load("./res/images/default_avatar.png")
        self.fetchingMembers = False
    
    def insertRequestData(self, data: tuple):
        pass
        """
        package = data[2]
        if data[1][0] == "avatars":
            try:
                avatar = p.image.load(package)
            except:
                avatar = p.image.load("./res/images/default_avatar.png")
            avatar = self.make_square_and_scale(avatar)
        """
            
    def fetchAvatar(self, userId: str):
        image = self.platform.fetchUserPicture(self.runtimeStore.users[userId]["avatarId"])
        if image.ok:
            self.runtimeStore.images["avatars"][userId] = p.image.load(io.BytesIO(image.content))
    
    def fetchServerIcon(self, serverId: str):
        pass
    
    def getServerIcon(self, serverId: str):
        pass
    
    def getUserAvatar(self, userId):
        try:
            if "avatarId" in self.runtimeStore.users[userId] and self.runtimeStore.images["avatars"][userId] is self.defaultAvatar:
                raise KeyError
            return self.runtimeStore.images['avatars'][userId]
        except KeyError:
            avatar = p.Surface((1,1)) #yes we use a one pixel size surface as a decoy
            self.runtimeStore.images['avatars'][userId] = avatar
            if "avatarId" in self.runtimeStore.users[userId]:
                self.requetHandler.placeOnCallStack("runtimeStoreManager", "avatar", lambda: self.fetchAvatar(userId))
            else:
                avatar = self.defaultAvatar
                self.runtimeStore.images['avatars'][userId] = avatar
            return avatar
    
    def fetchServerMembers(self, serverId: str):
        members = self.platform.fetchServerMembers(serverId, None)
        if "users" in members:
            for user in members["users"]:
                self.runtimeStore.parseStoatUser(user)
        for member in members["members"]:
            self.runtimeStore.servers[member["_id"]["server"]]["members"].append(member["_id"]["user"])
        self.fetchingMembers = False
        
    def getMemberList(self, serverId: str):
        if serverId != "0": #make sure that this isnt the server zero
            if len(self.runtimeStore.servers[serverId]["members"]) == 0:
                if not self.fetchingMembers:
                    self.fetchingMembers = True
                    self.requetHandler.placeOnCallStack("runtimeStoreManager", "avatar", lambda: self.fetchServerMembers(serverId))
            return self.runtimeStore.servers[serverId]["members"]
        return []
            
