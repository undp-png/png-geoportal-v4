from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class LukimGatherAccount(ProviderAccount):
    pass


class LukimGatherProvider(OAuth2Provider):
    id = "lukimgather"
    name = "Lukim Gather"
    account_class = LukimGatherAccount

    def extract_uid(self, data):
        return str(data.get("id"))

    def extract_common_fields(self, data):
        return {
            "username": data.get("username"),
            "email": data.get("email"),
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
        }

    def get_default_scope(self):
        return ["read"]


provider_classes = [LukimGatherProvider]
