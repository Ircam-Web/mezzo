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

EMAIL_HOST = 'smtp.ircam.fr'
EMAIL_PORT = '25'
DEFAULT_FROM_EMAIL = 'cri-dev@ircam.fr'
DEFAULT_TO_EMAIL = 'cri-dev@ircam.fr'
EMAIL_SUBJECT_PREFIX = "[IRCAM]"

SITE_TITLE = 'IRCAM'
SITE_TAGLINE = 'IRCAM'

EVENT_DOMAIN = "//eve.ircam.fr"
EVENT_SHOP_URL = EVENT_DOMAIN+"/pub.php/event/%d/edit"
EVENT_PASS_URL = EVENT_DOMAIN+"/pub.php/pass/"
EVENT_CONFIRMATION_URL = EVENT_DOMAIN+"/pub.php/cart/done?transaction_id=%s"

# FIGGO API - Lucca
FIGGO_API_URL_PROD='https://ircam.ilucca.net/'
FIGGO_API_HEADER_AUTH='Lucca application=bd6d5481-40eb-414b-9135-434e12749223'

HOST_THEMES = [
    #('www.starts.eu', 'themes.starts_eu'),
    #('vertigo.starts.eu', 'themes.vertigo_starts_eu'),
    ('manifeste.ircam.fr', 'themes.base'),
]
