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

from django.contrib.sitemaps import Sitemap
from mezzanine_agenda.models import Event
from organization.agenda.models import *
from organization.core.models import *
from organization.job.models import *
from organization.magazine.models import *
from organization.media.models import *
from organization.network.models import *
from organization.pages.models import *
from organization.projects.models import *
from organization.shop.models import *


class ArticleSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Article.objects.published()

    def lastmod(self, obj):
        return obj.publish_date


class PersonSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Person.objects.all()

    def lastmod(self, obj):
        return obj.updated


class ProjectSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ProjectPage.objects.published()

    def lastmod(self, obj):
        return obj.updated


class EventSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Event.objects.published()

    def lastmod(self, obj):
        return obj.publish_date


class PageSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Page.objects.published()

    def lastmod(self, obj):
        return obj.publish_date


class HomeSiteMap(Sitemap):
    changefreq = "daily"
    priority = 1

    def items(self):
        return Home.objects.published()

    def lastmod(self, obj):
        return obj.publish_date


class PlaylistSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Playlist.objects.published()

    def lastmod(self, obj):
        return obj.publish_date
