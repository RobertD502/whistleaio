
from strenum import StrEnum

TIMEOUT = 5 * 60

""" Endpoint URLs """

class Endpoint(StrEnum):
    """ Endpoint type for Whistle API. """

    BASE_URL = 'https://app.whistle.com/api'
    DAILIES = '/dailies'
    DEVICES = '/devices'
    HEALTH = '/health/trends'
    LOGIN = '/login'
    PETS = '/pets'
    PLACES= '/places'
    STATS = '/stats'


""" Header """

class Header(StrEnum):
    """ Header type for Whistle API. """

    ACCEPT = 'application/vnd.whistle.com.v6+json'
    ACCEPT_ENCODING = 'br;q=1.0, gzip;q=0.9, deflate;q=0.8'
    AGENT = 'Winston/5.4.0 (iPhone; iOS 15.1; Build:3821; Scale/3.0'
    CONTENT_TYPE = 'application/json'
    LANGUAGE = 'en'
    UNIT = 'imperial'





