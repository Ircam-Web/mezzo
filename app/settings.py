# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2018 Ircam
# Copyright (c) 2016-2018 Guillaume Pellerin
# Copyright (c) 2016-2018 Emilie Zawadzki

# This file is part of mezzanine-organization.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from __future__ import absolute_import, unicode_literals

import os
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
import ldap, logging
from django.core.urlresolvers import reverse_lazy
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

DEBUG = True if os.environ.get('DEBUG') == 'True' else False

import warnings
warnings.filterwarnings(
        'ignore', r"DateTimeField .* received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')

SILENCED_SYSTEM_CHECKS = ['fields.W342',]


###################################
# MEZZANINE ORGANIZATION SETTINGS #
###################################
try:
    from organization.settings import *
except ImportError as e:
    if "organization.settings" not in str(e):
        raise e


########################
# MAIN DJANGO SETTINGS #
########################

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# If you set this to True, Django will use timezone-aware datetimes.
USE_TZ = True

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
USE_L10N = True

AUTHENTICATION_BACKENDS = (
    "organization.core.backend.OrganizationLDAPBackend",
    "mezzanine.core.auth_backends.MezzanineBackend",
    "guardian.backends.ObjectPermissionBackend",
)


##########
# LOCALE #
##########

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "fr"

# Supported languages
LANGUAGES = (
    ('fr', _('French')),
    ('en', _('English')),
)

#############
# DATABASES #
#############

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('DB_ENV_POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432',
    },
}


##########################################
# CUSTOM MEZZANINE ORGANIZATION SETTINGS #
##########################################

# List of middleware classes to use. Order is important; in the request phase,
# these middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES += ()

STATICFILES_FINDERS += ()

SEARCH_MODEL_CHOICES += ()

PAGES_MODELS += ()


################
# APPLICATIONS #
################

INSTALLED_APPS += []

CUSTOM_MODULES = False

if CUSTOM_MODULES:
    INSTALLED_APPS += [
        "organization.custom",
    ]

##########
# THEMES #
##########

HOST_THEMES = [
    ('example.com', 'organization_themes.ircam-www-theme'),
]


##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.
try:
    from local_settings import *
except ImportError as e:
    if "local_settings" not in str(e):
        raise e

####################
# DYNAMIC SETTINGS #
####################

# set_dynamic_settings() will rewrite globals based on what has been
# defined so far, in order to provide some better defaults where
# applicable. We also allow this settings module to be imported
# without Mezzanine installed, as the case may be when using the
# fabfile, where setting the dynamic settings below isn't strictly
# required.
try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())



