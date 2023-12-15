from allauth.socialaccount.tests import OAuth2TestsMixin
from allauth.tests import MockedResponse, TestCase

from .provider import LukimGatherProvider


class LukimGatherOAuth2Tests(OAuth2TestsMixin, TestCase):
    provider_id = LukimGatherProvider.id

    def get_mocked_response(self):
        return MockedResponse(
            200,
            """{
          "ok": true,
          "url": "https:\\/\\/cms.lukimgather.staging.nepware.com\\/",
          "username": "admin",
          "email": "admin@geonode.com",
          "id": "1",
          "first_name": "test",
          "last_name": "user",
        }""",
        )
