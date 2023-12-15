import requests

from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2LoginView,
    OAuth2CallbackView,
)

from .provider import LukimGatherProvider
from django.conf import settings


class LukimGatherOAuth2Adapter(OAuth2Adapter):
    provider_id = LukimGatherProvider.id

    access_token_url = "{}/oauth/token/".format(settings.LUKIM_GATHER_SERVER_BASEURL)
    authorize_url = "{}/oauth/authorize".format(settings.LUKIM_GATHER_SERVER_BASEURL)
    identity_url = "{}/api/user".format(settings.LUKIM_GATHER_SERVER_BASEURL)

    def complete_login(self, request, app, access_token, **kwargs):
        extra_data = self.get_data(access_token.token)
        return self.get_provider().sociallogin_from_response(request, extra_data)

    def get_data(self, token):
        headers = {"Authorization": "Bearer " + token}
        response = requests.get(self.identity_url, headers=headers)
        res = response.json()
        if not response.ok:
            raise OAuth2Error()

        return res


oauth2_login = OAuth2LoginView.adapter_view(LukimGatherOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(LukimGatherOAuth2Adapter)
