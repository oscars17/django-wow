from django_wow.oauth2 import BattleNetOAuth2


class Community(BattleNetOAuth2):
    def __init__(self, api_key):
        super().__init__()
