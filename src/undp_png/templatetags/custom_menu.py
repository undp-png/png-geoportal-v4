from django import template
from geonode_mapstore_client.templatetags import get_menu_json
from avatar.templatetags.avatar_tags import avatar_url
from django.conf import settings
from geonode.base.models import Configuration

register = template.Library()

def _is_mobile_device(context):
    if context and 'request' in context:
        req = context['request']
        return req.user_agent.is_mobile
    return False



@register.simple_tag(takes_context=True)
def get_base_left_topbar_menu(context):

    is_mobile = _is_mobile_device(context)

    return [
      {
          "type": "link",
          "href": "/about/#/",
          "label": "About"
      },
      {
          "type": "link",
          "href": "/catalogue/#/search/?f=featured",
          "label": "Featured"
      },
      {
          "label": "Data",
          "type": "dropdown",
          "items": [
              {
                  "type": "link",
                  "href": "/catalogue/#/search/?f=dataset",
                  "label": "Datasets"
              },
              {
                  "type": "link",
                  "href": "/catalogue/#/search/?f=document",
                  "label": "Documents"
              },
              {
                  "type": "link",
                  "href": "/services/?limit=5",
                  "label": "Remote Services"
              } if not is_mobile else None
          ]
        },
        {
            "type": "link",
            "href": "/catalogue/#/search/?f=map",
            "label": "Maps"
        },
        {
            "type": "link",
            "href": "/catalogue/#/search/?f=geostory",
            "label": "Stories"
        },
        {
            "type": "link",
            "href": "/catalogue/#/search/?f=dashboard",
            "label": "Dashboards"
        },
    ]



@register.simple_tag(takes_context=True)
def get_user_menu(context):

    is_mobile = _is_mobile_device(context)
    user = context.get('request').user

    if not user.is_authenticated:
        return [
            {
                "label": "Register",
                "type": "link",
                "href": "/account/signup/?next=/"
            } if settings.ACCOUNT_OPEN_SIGNUP and not Configuration.load().read_only else None,
            {
                "label": "Sign in",
                "type": "link",
                "href": "/account/login/?next=/"
            },
        ]

    devider = {
        "type": "divider"
    }

    profile_link = {
        "type": "link",
        # get href of user profile
        "href": user.get_absolute_url(),
        "label": "Profile"
    }

    logout = {
        "type": "link",
        "href": "/account/logout/?next=/",
        "label": "Log out"
    }

    if is_mobile:
        return [
            {
                # get src of user avatar
                "image": avatar_url(user),
                "type": "dropdown",
                "className": "gn-user-menu-dropdown",
                "items": [
                    profile_link,
                    devider,
                    logout
                ]
            }
        ]

    profile = {
        # get src of user avatar
        "image": avatar_url(user),
        "type": "dropdown",
        "className": "gn-user-menu-dropdown",
        "items": [
            profile_link,
            {
                "type": "link",
                "href": "/social/recent-activity",
                "label": "Recent activity"
            },
            {
                "type": "link",
                "href": "/catalogue/#/search/?f=favorite",
                "label": "Favorites"
            },
            {
                "type": "link",
                "href": "/messages/inbox/",
                "label": "Inbox"
            },
            devider,
        ]
    }
    general = [
        {
            "type": "link",
            "href": "/help/",
            "label": "Help"
        },
        devider,
        logout
    ]
    monitoring = []
    if settings.MONITORING_ENABLED:
        monitoring = [
            devider,
            {
                "type": "link",
                "href": "/monitoring/",
                "label": "Monitoring & Analytics"
            }
        ]
    admin_only = [
        {
            "type": "link",
            "href": "/admin/",
            "label": "Admin"
        },
        {
            "type": "link",
            "href": "/geoserver/",
            "label": "GeoServer"
        }
    ] + monitoring + [devider] + general

    if user.is_superuser:
        profile['items'].extend(admin_only)
    else:
        profile['items'].extend(general)

    return [profile]