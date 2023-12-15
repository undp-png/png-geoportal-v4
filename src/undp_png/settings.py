# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2017 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

# Django settings for the GeoNode project.
import os
import ast

try:
    from urllib.parse import urlparse, urlunparse
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
    from urlparse import urlparse, urlunparse
# Load more settings from a file called local_settings.py if it exists
try:
    from undp_png.local_settings import *
#    from geonode.local_settings import *
except ImportError:
    from geonode.settings import *

#
# General Django development settings
#
PROJECT_NAME = 'undp_png'

# add trailing slash to site url. geoserver url will be relative to this
if not SITEURL.endswith('/'):
    SITEURL = '{}/'.format(SITEURL)

SITENAME = os.getenv("SITENAME", 'undp_png')

# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))

WSGI_APPLICATION = "{}.wsgi.application".format(PROJECT_NAME)

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', "en")

if PROJECT_NAME not in INSTALLED_APPS:
    INSTALLED_APPS += (PROJECT_NAME, "socialaccountprovider",)

# Location of url mappings
ROOT_URLCONF = os.getenv('ROOT_URLCONF', '{}.urls'.format(PROJECT_NAME))

# Additional directories which hold static files
# - Give priority to local geonode-project ones
STATICFILES_DIRS = [os.path.join(LOCAL_ROOT, "static"), ] + STATICFILES_DIRS

# Location of locale files
LOCALE_PATHS = (
    os.path.join(LOCAL_ROOT, 'locale'),
    ) + LOCALE_PATHS

TEMPLATES[0]['DIRS'].insert(0, os.path.join(LOCAL_ROOT, "templates"))
loaders = TEMPLATES[0]['OPTIONS'].get('loaders') or ['django.template.loaders.filesystem.Loader','django.template.loaders.app_directories.Loader']
# loaders.insert(0, 'apptemplates.Loader')
TEMPLATES[0]['OPTIONS']['loaders'] = loaders
TEMPLATES[0].pop('APP_DIRS', None)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d '
                      '%(thread)d %(message)s'
        },
        'simple': {
            'format': '%(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"], "level": "ERROR", },
        "geonode": {
            "handlers": ["console"], "level": "INFO", },
        "geoserver-restconfig.catalog": {
            "handlers": ["console"], "level": "ERROR", },
        "owslib": {
            "handlers": ["console"], "level": "ERROR", },
        "pycsw": {
            "handlers": ["console"], "level": "ERROR", },
        "celery": {
            "handlers": ["console"], "level": "DEBUG", },
        "mapstore2_adapter.plugins.serializers": {
            "handlers": ["console"], "level": "DEBUG", },
        "geonode_logstash.logstash": {
            "handlers": ["console"], "level": "DEBUG", },
    },
}

CENTRALIZED_DASHBOARD_ENABLED = ast.literal_eval(os.getenv('CENTRALIZED_DASHBOARD_ENABLED', 'False'))
if CENTRALIZED_DASHBOARD_ENABLED and USER_ANALYTICS_ENABLED and 'geonode_logstash' not in INSTALLED_APPS:
    INSTALLED_APPS += ('geonode_logstash',)

    CELERY_BEAT_SCHEDULE['dispatch_metrics'] = {
        'task': 'geonode_logstash.tasks.dispatch_metrics',
        'schedule': 3600.0,
    }

LDAP_ENABLED = ast.literal_eval(os.getenv('LDAP_ENABLED', 'False'))
if LDAP_ENABLED and 'geonode_ldap' not in INSTALLED_APPS:
    INSTALLED_APPS += ('geonode_ldap',)

# Add your specific LDAP configuration after this comment:
# https://docs.geonode.org/en/master/advanced/contrib/#configuration


MAPSTORE_BASELAYERS = [
        {
        "type": "tileprovider",
        "title": "MapBox Streets",
        "provider": "MapBoxStyle",
        "name": "MapBox streets-v11",
        "accessToken": f"{MAPBOX_ACCESS_TOKEN}",
        "source": "streets-v11",
        "thumbURL": f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/256/6/33/23?access_token={MAPBOX_ACCESS_TOKEN}",  # noqa
        "group": "background",
        "visibility": True,
    },
            {
        "type": "tileprovider",
        "title": "MapBox Outdoors",
        "provider": "MapBoxStyle",
        "name": "MapBox outdoors-v11",
        "accessToken": f"{MAPBOX_ACCESS_TOKEN}",
        "source": "outdoors-v11",
        "thumbURL": f"https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/tiles/256/6/33/23?access_token={MAPBOX_ACCESS_TOKEN}",  # noqa
        "group": "background",
        "visibility": False,
    },
    {
        "type": "tileprovider",
        "title": "MapBox Dark",
        "provider": "MapBoxStyle",
        "name": "MapBox dark-v10",
        "accessToken": f"{MAPBOX_ACCESS_TOKEN}",
        "source": "dark-v10",
        "thumbURL": f"https://api.mapbox.com/styles/v1/mapbox/dark-v10/tiles/256/6/33/23?access_token={MAPBOX_ACCESS_TOKEN}",  # noqa
        "group": "background",
        "visibility": False,
    },
    {
        "type": "tileprovider",
        "title": "MapBox Satellite",
        "provider": "MapBoxStyle",
        "name": "MapBox satellite-v9",
        "accessToken": f"{MAPBOX_ACCESS_TOKEN}",
        "source": "satellite-v9",
        "thumbURL": f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/256/6/33/23?access_token={MAPBOX_ACCESS_TOKEN}",  # noqa
        "group": "background",
        "visibility": False,
    },
    {
        "type": "tileprovider",
        "title": "MapBox Light",
        "provider": "MapBoxStyle",
        "name": "MapBox light-v10",
        "accessToken": f"{MAPBOX_ACCESS_TOKEN}",
        "source": "light-v10",
        "thumbURL": f"https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/256/6/33/23?access_token={MAPBOX_ACCESS_TOKEN}",  # noqa
        "group": "background",
        "visibility": False,
    },
    {
        "type": "osm",
        "title": "Open Street Map",
        "name": "mapnik",
        "source": "osm",
        "group": "background",
        "visibility": False,
    },
    {
        "type": "tileprovider",
        "title": "OpenTopoMap",
        "provider": "OpenTopoMap",
        "name": "OpenTopoMap",
        "source": "OpenTopoMap",
        "group": "background",
        "visibility": False,
    },
    {
        "type": "wms",
        "title": "Sentinel-2 cloudless - https://s2maps.eu",
        "format": "image/jpeg",
        "id": "s2cloudless",
        "name": "s2cloudless:s2cloudless",
        "url": "https://maps.geosolutionsgroup.com/geoserver/wms",
        "group": "background",
        "thumbURL": f"{SITEURL}static/mapstorestyle/img/s2cloudless-s2cloudless.png",
        "visibility": False,
    },
    {
        "source": "ol",
        "group": "background",
        "id": "none",
        "name": "empty",
        "title": "Empty Background",
        "type": "empty",
        "visibility": False,
        "args": ["Empty Background", {"visibility": False}],
    },
]

DEFAULT_MAP_CRS = 'EPSG:3857'
DEFAULT_MAP_CENTER_X=16094580
DEFAULT_MAP_CENTER_Y=-766816

# DEFAULT_MAP_CRS = 'EPSG:4326'
# DEFAULT_MAP_CENTER_X=147.00
# DEFAULT_MAP_CENTER_Y=-9.5


DEFAULT_MAP_ZOOM = 7

# # Lukim gather OAuth2 server url
LUKIM_GATHER_SERVER_BASEURL = os.getenv('LUKIM_GATHER_SERVER_BASEURL', 'https://cms.lukimgather.org')

# # Temporary workaround to work social login work
# # [#8814] (https://github.com/GeoNode/geonode/issues/8814)
SOCIALACCOUNT_LOGIN_ON_GET = True
