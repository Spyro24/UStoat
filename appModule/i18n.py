import json

class i18n:
    def __init__(self):
        self.strings = {"theme_manager.settings.chose_theme_file":"Chose a theme file",
                        "ui.name.settings":"Settings",
                        "ui.name.timeout":"Timeout",
                        "ui.name.message_empty":"Message...",
                        "ui.login_system.login":"Login",
                        "badge.name.ustoat_developer":"Client Developer",
                        "badge.name.ustoat_maintainer":"Client Maintainer"}
    
    def loadI18N(self, i18nCode: str):
        if i18nCode != "en_us":
            pass