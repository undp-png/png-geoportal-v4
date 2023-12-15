from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import LukimGatherProvider


urlpatterns = default_urlpatterns(LukimGatherProvider)
