# Constants used in my Demo Sonos Cloud API #
SONOS_CLIENT_ID = "746927e2-5bd0-4f90-81cf-b39b7c8d55a6"
SONOS_CLIENT_SECRET = "c5715943-1337-4a85-8f4d-dc839974c41c"

SONOS_AUTH_API_BASE_URL = 'https://api.sonos.com'
SONOS_CONTROL_API_BASE_URL = 'https://api.ws.sonos.com/control/api/v1'
SONOS_TEST_STATE = 'StateSecret'

SONOS_USER_ID = 'jose.fortemps@outlook.com'
SONOS_PASSWORD = 'Mexico13'

# CLIENT_REDIRECT_PORT_NO = 5000
# CLIENT_REDIRECT_URL = f'http://localhost:{CLIENT_REDIRECT_PORT_NO}'

CLIENT_REDIRECT_URL = 'https://fortempssonos.ddns.net'
CLIENT_SCOPE = ['playback-control-all']

AUTH_URL = f'{SONOS_AUTH_API_BASE_URL}/login/v3/oauth'
ACCESS_TOKEN_URL = f'{SONOS_AUTH_API_BASE_URL}/login/v3/oauth/access'
SIGNIN_URL = 'https://api.sonos.com/login/v3/signin'

REFRESH_TOKEN_URL = ACCESS_TOKEN_URL