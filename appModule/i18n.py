import json

class i18n:
    def __init__(self):
        self.strings = {"theme_manager.settings.chose_theme_file":"Chose a theme file",
                        "ui.name.settings":"Settings",
                        "ui.name.timeout":"Timeout",
                        "ui.name.message_empty":"Message...",
                        "ui.login_system.username":"E-Mail/Username",
                        "ui.login_system.password":"Password",
                        "ui.login_system.login":"Login",
                        "ui.login_system.get_token":"Obtaining your session token",
                        "ui.login_system.connection_failure":"Connection failure. No network connection?",
                        "ui.login_system.invalid_credentials":"Invalid Credentials",
                        "ui.login_system.mfa":"Enter a MFA code",
                        "ui.login_system.mfa_validate":"Validate",
                        "ui.login_system.mfa_code_validate":"Validating MFA Code",
                        "ui.login_system.mfa_code_wrong":"Invalid MFA Code",
                        "ui.login_system.invalid_token":"Invalid Token. Please login again",
                        "badge.name.ustoat_developer":"Client Developer",
                        "badge.name.ustoat_maintainer":"Client Maintainer",
                        "settings.about.name":"About UStoat",
                        "setting.logout.warning": "This will detsroy the current session.\nUse this to escape the Matrix\nUStoat will be closed btw\nSettings dosnt get reseted",
                        "settings.logout.logout":"Logout"}
    
    def loadI18N(self, i18nCode: str):
        if i18nCode != "en_us":
            pass