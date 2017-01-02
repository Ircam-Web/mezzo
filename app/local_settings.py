# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Ircam
# Copyright (c) 2016-2017 Guillaume Pellerin
# Copyright (c) 2016-2017 Emilie Zawadzki

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

import os
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, date

DEBUG = True if os.environ.get('DEBUG') == 'True' else False

ADMINS = (
    ('Guillaume Pellerin', 'guillaume.pellerin@ircam.fr'),
    ('Emilie Zawadzki', 'emilie.zawadzki@ircam.fr'),
)

# Make these unique, and don't share it with anybody.
SECRET_KEY = "j1qa@u$5ktqr^0_kwh@-j@*-80t$)ht!4-=ybz1xc%@3+r(r&tzefoih"
NEVERCACHE_KEY = "m)u^%r@uh#r3wu0&$=#$1ogx)uy4hv93^2lt%c3@xi=^gifoj8paozijdihazefd"

DATABASE_ROUTERS = ['eve.routers.EveRouter', 'prestashop.routers.PrestaRouter']

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

if os.environ.get('EVEDB_ENV_POSTGRES_PASSWORD'):
    DATABASES['eve'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'eve',
        'USER': 'eve',
        'PASSWORD': os.environ.get('EVEDB_ENV_POSTGRES_PASSWORD'),
        'HOST': 'evedb',
        'PORT': '5432',
    }

if os.environ.get('PRESTADB_ENV_MYSQL_PASSWORD'):
    DATABASES['prestashop'] = {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'USER': 'ircam_shops',      # Not used with sqlite3.
        'PASSWORD': os.environ.get('PRESTADB_ENV_MYSQL_PASSWORD'),  # Not used with sqlite3.
        'NAME': 'ircam_shops',
        'HOST': 'prestadb',      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',      # Set to empty string for default. Not used with sqlite3.
        }


# EXTENSIONS AND FORMATS
# Allowed Extensions for File Upload. Lower case is important.
FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'],
    'Document': ['.pdf', '.doc', '.rtf', '.txt', '.xls', '.csv', '.docx'],
    'Video': ['.mov', '.wmv', '.mpeg', '.mpg', '.avi', '.rm'],
    'Audio': ['.mp3', '.mp4', '.wav', '.aiff', '.midi', '.m4p']
    }

# Define different formats for allowed selections.
# This has to be a subset of EXTENSIONS.
# e.g., add ?type=image to the browse-URL ...
FILEBROWSER_SELECT_FORMATS = {
    'File': ['Folder', 'Document'],
    'Image': ['Image'],
    'Media': ['Video', 'Audio'],
    'Audio': ['Audio'],
    'Document': ['Document'],
    # for TinyMCE we can also define lower-case items
    'image': ['Image'],
    'file': ['Folder', 'Image', 'Document'],
    'media': ['Video', 'Audio'],
    'audio': ['Audio'],
}

EMAIL_HOST = 'smtp.ircam.fr'
EMAIL_PORT = '25'
DEFAULT_FROM_EMAIL = 'www@ircam.fr'
DEFAULT_TO_EMAIL = 'drh@ircam.fr'
EMAIL_SUBJECT_PREFIX = "[IRCAM WWW]"

SITE_TITLE = 'IRCAM'
SITE_TAGLINE = 'Institut de Recherche et de Coordination Acoustique et Musique'

SILENCED_SYSTEM_CHECKS = ['fields.W342',]

ADMIN_MENU_ORDER = (
    (_('Pages'), ('pages.Page', 'organization-pages.Home',
                 'organization-core.LinkType')),
    (_('Media'), ('organization-media.Media',
                  'organization-media.Playlist',
                 'organization-media.MediaCategory',
                 (_('Media Library'), 'fb_browse'),
                 )),
    (_('Events'), ('mezzanine_agenda.Event',
                  'mezzanine_agenda.EventLocation',
                  'mezzanine_agenda.EventPrice',
                  'mezzanine_agenda.EventCategory',
                  'organization-agenda.EventPublicType',
                  'organization-agenda.EventTrainingLevel',
                  'generic.Keyword',
                  )),
    (_('Magazine'), ('organization-magazine.Article',
                    'organization-magazine.Brief',)),
    (_('Network'), ('organization-network.Organization',
                    'organization-network.OrganizationLinked',
                    'organization-network.Department',
                    'organization-network.Team',
                    'organization-network.Person',
                    'organization-network.Activity',
                    'organization-network.OrganizationType',
                    'organization-network.PersonListBlock',
                    )),
    (_('Activity'), ('organization-network.PersonActivity',
                    'organization-network.ActivityStatusFamily',
                    'organization-network.ActivityStatus',
                    'organization-network.ActivityGrade',
                    'organization-network.ActivityFramework',
                    'organization-network.ActivityFunction',
                    'organization-network.TrainingType',
                    'organization-network.TrainingTopic',
                    'organization-network.TrainingLevel',
                    'organization-network.TrainingSpeciality',
                    )),
    (_('Timesheet'), ('organization-network.ActivityWeeklyHourVolume',
                     'organization-network.PersonActivityTimeSheet'
                    )),
    (_('Projects'), ('organization-projects.Project',
                    'organization-projects.ProjectProgram',
                    'organization-projects.ProjectProgramType',
                    'organization-projects.ProjectTopic',
                    'organization-projects.ProjectProgramType',
                    'organization-projects.ProjectDemo',
                    'organization-projects.Repository',
                    'organization-projects.RepositorySystem',
                    )),
    (_('Shop'), ('shop.Product',
                    'organization-shop.ProductList',
                    'shop.Order',
                    'shop.DiscountCode',
                    'shop.Sale',
                    )),
    (_('Jobs'), ('organization-job.JobOffer','organization-job.Candidacy')),
    (_('Users'), ('auth.User', 'auth.Group',)),
    (_('Site'), ('sites.Site', 'redirects.Redirect', 'conf.Setting')),
)

DASHBOARD_TAGS = ( ("mezzanine_tags.app_list",), (), ("mezzanine_tags.recent_actions",), )

GRAPPELLI_ADMIN_TITLE = 'IRCAM Admin'

SEARCH_MODEL_CHOICES = ('organization-pages.CustomPage',
                        'organization-network.DepartmentPage',
                        'organization-network.TeamPage',
                        'organization-projects.ProjectTopicPage',
                        'pages.Page',
                        'organization-media.Playlist',
                        'mezzanine_agenda.Event',
                        'organization-projects.Project',
                        'shop.Product')


PAGES_MODELS = ('organization-pages.CustomPage',
                'organization-magazine.Topic',
                'organization-network.DepartmentPage',
                'organization-network.TeamPage',
                'organization-projects.ProjectTopicPage',
                'shop.Product')

PAGES_PUBLISHED_INCLUDE_LOGIN_REQUIRED = True

SEARCH_PER_PAGE = 10
MAX_PAGING_LINKS = 10
DAL_MAX_RESULTS = 20

RATINGS_ACCOUNT_REQUIRED = True

import warnings
warnings.filterwarnings(
        'ignore', r"DateTimeField .* received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')

EVENT_SLUG = 'agenda'
EVENT_GOOGLE_MAPS_DOMAIN = 'maps.google.fr'
EVENT_PER_PAGE = 50
EVENT_USE_FEATURED_IMAGE = True
EVENT_DOMAIN = "http://eve.ircam.fr"
EVENT_SHOP_URL = EVENT_DOMAIN+"/pub.php/event/%d/edit"
EVENT_PASS_URL = EVENT_DOMAIN+"/pub.php/pass/"
EVENT_CONFIRMATION_URL = EVENT_DOMAIN+"/pub.php/cart/done?transaction_id=%s"
EVENT_EXCLUDE_TAG_LIST = ['tournees', ]

TINYMCE_SETUP_JS = "/static/js/tinymce_setup.js"

SLUGIFY = 'django.template.defaultfilters.slugify'

BLOG_SLUG = 'article'
BLOG_POST_PER_PAGE = 200
ARTICLE_PER_PAGE = 10
MEDIA_PER_PAGE = 9

# The numeric mode to set newly-uploaded files to. The value should be
# a mode you'd pass directly to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0o664
FILE_UPLOAD_TEMP_DIR = '/srv/media/uploads/tmp/'
if not os.path.exists(FILE_UPLOAD_TEMP_DIR):
    os.makedirs(FILE_UPLOAD_TEMP_DIR)

MAX_UPLOAD_SIZE = 512000000
MAX_UPLOAD_SIZE_FRONT = 10485760
FILEBROWSER_MAX_UPLOAD_SIZE = 512000000

if DEBUG:
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda x : True
    }
DEBUG_TOOLBAR_PATCH_SETTINGS = False
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

GRAPPELLI_INSTALLED = True
# JQUERY_FILENAME = 'jquery-3.1.0.min.js'
JQUERY_UI_FILENAME = 'jquery-ui-1.9.2.min.js'

#SHOP_CURRENCY_LOCALE = ''
SHOP_USE_VARIATIONS = False
SHOP_USE_RATINGS = False

PROJECT_DEMOS_DIR = '/srv/media/projects/demos/'
if not os.path.exists(PROJECT_DEMOS_DIR):
    os.makedirs(PROJECT_DEMOS_DIR)

FORMAT_MODULE_PATH = [
    'organization.formats',
]

# FIGGO API - Lucca
FIGGO_API_URL_PROD='https://ircam.ilucca.net/'
FIGGO_API_HEADER_AUTH='Lucca application=bd6d5481-40eb-414b-9135-434e12749223'
