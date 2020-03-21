AVAILABLE_REGIONS = [
    'US',
    'EU',
    'KR',
    'TW',
]


NAMESPACES = {
    'retail': {
        'static': 'static-%s',
        'dynamic': 'dynamic-%s',
        'profile': 'profile-%s',
    },
    'classic': {
        'static': 'classic',
    },
}


LOCALES = [
    'en',
    'es',
    'pt',
    'it',
    'de',
    'fr',
    'pl',
    'ru',
    'tr',
    'ko',
    'zh'
]

BNET_AUTH_URL = 'https://%s.battle.net/oauth/authorize'
BNET_TOKEN_URL = 'https://%s.battle.net/oauth/token'

BASE_ENDPOINT_URL = 'https://%s.battle.net/'
CHARACTER_ENDPOINT_URL = 'https://%s.api.blizzard.com/'
COMMUNITY_ENDPOINT_URL = 'https://%s.api.blizzard.com/'
