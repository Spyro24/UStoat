import accountModules.stoat
import accountModules.nerimity
import accountModules.uvolt
import accountModules.stoatbot
import accountModules.sloga

platforms = {"stoat": accountModules.stoat.userAccount,
             "nerimity": accountModules.nerimity.userAccount,
             "sloga": accountModules.sloga.userAccount,
             #"uvolt": accountModules.uvolt.userAccount,
             "stoatbot": accountModules.stoatbot.userAccount}