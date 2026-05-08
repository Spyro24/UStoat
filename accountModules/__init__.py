import accountModules.stoat
import accountModules.nerimity
import accountModules.uvolt
import accountModules.stoatbot

platforms = {"stoat": accountModules.stoat.userAccount,
             "nerimity": accountModules.nerimity.userAccount,
             "uvolt": accountModules.uvolt.userAccount,
             "stoatbot": accountModules.stoatbot.userAccount}