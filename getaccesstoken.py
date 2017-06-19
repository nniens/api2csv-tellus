# utf-8
import requests
import os
from urllib.parse import urlparse, parse_qsl


class GetAccessToken(object):
    """
        Get an header authentication item for access token
        for using the internal API's
        by logging in as type = 'employee'

        Usage: 
            from accesstoken import AccessToken
            
            getToken = AccessToken()
            accessToken = getToken.getAccessToken()
                        
            requests.get(url, headers= accessToken)

    """
    global baseUrl

    baseUrl = 'https://api.data.amsterdam.nl/auth'

    def grantToken(self):
        callbackUrl = "https%3A%2F%2Fatlas.amsterdam.nl%2F%23"
        grantUrl = baseUrl + '/idp/login'
        grantData = {"type": 'employee'}

        response = requests.post(grantUrl + '?callback=' +
                                 callbackUrl, data=grantData)
        url = response.url
        
        # Get grantToken from parameter aselect_credentials in session URL
        parsed = urlparse(url)
        fragment = parse_qsl(parsed.fragment)
        os.environ["GRANT_TOKEN"] = fragment[0][1]
        print('Received new grant Token')

    def refreshToken(self):
        if "GRANT_TOKEN" not in os.environ:
            print('GRANT TOKEN env variable does not exist. ' +
                  'Getting new grant Token')
            self.grantToken()

        refreshParams = {'aselect_credentials': os.environ["GRANT_TOKEN"],
                         'a-select-server': 0,
                         'rid': 0}
        refreshTokenUrl = baseUrl + '/idp/token'
        response = requests.get(refreshTokenUrl, params=refreshParams)

        if response.status_code != 200:
            print("Refresh token not valid, requesting new grant token...")
            self.grantToken()
            response = requests.get(refreshTokenUrl)

        os.environ["REFRESH_TOKEN"] = response.text
        print('Stored refresh token.')

    def accessToken(self):
        refreshToken = os.environ["REFRESH_TOKEN"]
        REFRESH_TOKEN = {"Authorization": 'Bearer ' + refreshToken}
        accessTokenUrl = baseUrl + '/accesstoken'
        accessToken = requests.get(accessTokenUrl, headers=REFRESH_TOKEN)
        os.environ["ACCESS_TOKEN"] = accessToken.text

    def getAccessToken(self):
        self.refreshToken()
        self.accessToken()
        print('Stored new access token')
        return {"Authorization": 'Bearer ' + os.environ["ACCESS_TOKEN"]}
