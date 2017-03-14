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

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
from mezzanine.core.models import Displayable, Slugged, Orderable
from mezzanine.pages.models import Link as MezzanineLink
from organization.core.models import *
from organization.media.models import *
from organization.core.managers import *


class CustomPage(Page, SubTitled, RichText):

    objects = CustomSearchableManager()

    class Meta:
        verbose_name = 'custom page'


class PageBlock(Block):

    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='blocks', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("block")
        verbose_name_plural = _("blocks")
        verbose_name = 'page block'


class PageImage(Image):

    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")
        order_with_respect_to = "page"


class PagePlaylist(PlaylistRelated):

    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='playlists', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("playlist")
        verbose_name_plural = _("playlists")
        order_with_respect_to = "page"


class PageLink(Link):

    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='links', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("link")
        verbose_name_plural = _("links")
        order_with_respect_to = "page"


class PageRelatedTitle(RelatedTitle):

    page = models.OneToOneField(Page, verbose_name=_('page'), related_name='related_title', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("related title")
        order_with_respect_to = "page"


class DynamicContentPage(DynamicContent, Orderable):

    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='dynamic_content_pages', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Dynamic Content Page'


class LinkImage(models.Model):

    link = models.ForeignKey(MezzanineLink, verbose_name=_('link'), related_name='link_images', blank=True, null=True, on_delete=models.SET_NULL)
    image = FileField(_("Image"), max_length=1024, format="Image", upload_to="images")

    class Meta:
        verbose_name = _("link image")
        verbose_name_plural = _("link images")
        order_with_respect_to = "link"


class DynamicContentHomeSlider(DynamicContent, Orderable):

    home = models.ForeignKey("home", verbose_name=_('home'), blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Slider'


class DynamicContentHomeBody(DynamicContent, Orderable):

    home = models.ForeignKey("home", verbose_name=_('home'), blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Body')


class DynamicContentHomeMedia(DynamicContent, Orderable):

    home = models.ForeignKey("home", verbose_name=_('home'), related_name='dynamic_content_home_media', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Media'


class HomeImage(Image):

    home = models.ForeignKey("home", verbose_name=_('home'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")
        order_with_respect_to = "home"


class Home(Displayable):

    class Meta:
        verbose_name = _('home')
        verbose_name_plural = _("homes")

    def get_absolute_url(self):
        return reverse("organization-home")

        verbose_name = _('Person List')
